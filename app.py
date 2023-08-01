"""
Chatbot Flask Application

This script implements a web application using Flask to provide stress relief suggestions 
and cognitive distortions challenges. Users can log in, record their stress levels, 
and receive personalized stress relief suggestions. 
They can also submit their thoughts to identify cognitive distortions and get reframing suggestions.

The application uses a SQLite database to store user information and stress level records.

"""
import datetime
import random
from datetime import datetime, timezone
from flask import Flask, flash, redirect, render_template, request, url_for, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_session import Session
from helpers import get_personalized_suggestions, cognitive_distortions, daily_tips, challenges

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Define the StressLevel model
class StressLevel(db.Model):
    __tablename__ = 'stress_levels'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stress_level = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.now(timezone.utc))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    thoughts = db.relationship('Thought', backref='user', lazy='dynamic')
    distortion_counts = db.relationship(
        'DistortionCount', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

class CopingStrategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"CopingStrategy(id={self.id}, name='{self.name}', description='{self.description}')"

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thought = db.Column(db.String(200), nullable=False)
    distortion = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class DistortionCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    distortion_type = db.Column(db.String(50))
    count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User {self.user_id}'s count for {self.distortion_type} is {self.count}"

# Create tables
with app.app_context():
    db.create_all()

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get("confirmation")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

        flash("A user with that username already exists.")

    return render_template('register.html')

# Handle the main route
@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    thought = None
    result = None
    daily_tip = get_daily_tip()
    random_challenge = get_random_challenge()

    if request.method == 'POST':
        # Get thought from form
        thought = request.form.get('thought')
        # Get the user's ID from the current_user object
        user_id = current_user.get_id()
        # Identify cognitive distortion
        distortion = identify_distortion(user_id, thought)
        if distortion:
            result = {
                'distortion': distortion,
                'explanation': cognitive_distortions[distortion]["explanation"],
                'reframe': cognitive_distortions[distortion]["reframe"]
            }
        else:
            result = None

    return render_template('index.html', result=result, thought=thought, daily_tip=daily_tip,
                           random_challenge=random_challenge)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Ensure username was submitted
        if not username:
            return render_template("apology.html", message="must provide username")

        # Ensure password was submitted
        if not password:
            return render_template("apology.html", message="must provide password")

        user = User.query.filter_by(username=username).first()

        # Ensure username exists and password is correct
        if not user or not user.check_password(password):
            return render_template("apology.html", message="invalid username and/or password")

        login_user(user)

        # Redirect user to home page
        return redirect(url_for('index'))
    
    # User reached route via GET
    else:
        return render_template("login.html")


# logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Stress level handler route implementation
@app.route("/stress_level", methods=['GET', 'POST'])
def stress_level_handler():
    if request.method == 'POST':
        submitted_stress_level = request.form.get('stress_level')
        if submitted_stress_level:
            stress_entry = int(submitted_stress_level)
            if 1 <= stress_entry <= 10:
                suggestion = get_personalized_suggestions(stress_entry)
                flash('Your stress level has been recorded. ' +
                      suggestion, 'success')
            else:
                flash("Please enter a stress level between 1 and 10.", 'error')

    return render_template('stress_level.html')

# Function to get the tip of the day
def get_daily_tip():
    day_of_year = datetime.now().timetuple().tm_yday
    random.seed(day_of_year)
    return random.choice(daily_tips)

# For tracking progress
user_progress = {}

def increment_distortion_count(user_id, distortion_type):
    distortion_count = DistortionCount.query.filter_by(user_id=user_id, distortion_type=distortion_type).first()
    if distortion_count:
        distortion_count.count += 1
    else:
        distortion_count = DistortionCount(user_id=user_id, distortion_type=distortion_type, count=1)
        db.session.add(distortion_count)
    db.session.commit()

def identify_distortion(user_id, thought):
    with current_app.app_context():
        # Logic for identifying distortion
        distortion_type = None 
        
       # Overgeneralization
        if "always" in thought or "never" in thought:
            increment_distortion_count(user_id, "overgeneralization")
            distortion_type = "overgeneralization"

        # Black and White Thinking
        elif "all or nothing" in thought or "either or" in thought:
            increment_distortion_count(user_id, "black_and_white")
            distortion_type = "black_and_white"

        # Filtering
        elif "only the bad" in thought or "ignoring the good" in thought:
            increment_distortion_count(user_id, "filtering")
            distortion_type = "filtering"

        # Catastrophizing
        elif "worst-case scenario" in thought or "it's the end" in thought:
            increment_distortion_count(user_id, "catastrophizing")
            distortion_type = "catastrophizing"

        # Personalization
        elif "my fault" in thought or "because of me" in thought:
            increment_distortion_count(user_id, "personalization")
            distortion_type = "personalization"

        # Mind Reading
        elif "they think" in thought or "he must think" in thought:
            increment_distortion_count(user_id, "mind_reading")
            distortion_type = "mind_reading"

        # Emotional Reasoning
        elif "I feel it, so it must be true" in thought:
            increment_distortion_count(user_id, "emotional_reasoning")
            distortion_type = "emotional_reasoning"

        # Should Statements
        elif "I should" in thought or "they should" in thought:
            increment_distortion_count(user_id, "should_statements")
            distortion_type = "should_statements"

        # Labeling
        elif "I am a" in thought and ("loser" in thought or "failure" in thought):
            increment_distortion_count(user_id, "labeling")
            distortion_type = "labeling"

        # Fallacy of Change
        elif "they must change" in thought or "if only they" in thought:
            increment_distortion_count(user_id, "fallacy_of_change")
            distortion_type = "fallacy_of_change"

        return distortion_type
    
# Example usage:
@app.route("/identify_distortion", methods=["POST"])
@login_required
def identify_distortion_route():
    thought = request.form["thought"]
    user_id = current_user.get_id()
    identified_distortion = identify_distortion(user_id, thought)

    if identified_distortion:
        return jsonify({
            "message": f"The thought exhibits {identified_distortion} cognitive distortion."
        })
    else:
        return jsonify({
            "message": "No cognitive distortion identified."
        })

# Visualize the User's cognitive distortion history
@app.route('/distortion_history')
@login_required
def distortion_history():
    distortion_counts = DistortionCount.query.filter_by(user_id=current_user.id).all()
    distortions = [distortion.distortion_type for distortion in distortion_counts]
    counts = [distortion.count for distortion in distortion_counts]
    return render_template('distortion_history.html', distortions=distortions, counts=counts, zip=zip)

# Function to get a random challenge
def get_random_challenge():
    """This function returns a random challenge from the 'challenges' list."""
    return random.choice(challenges)

# Handle the get_challenge route
@app.route("/get_challenge", methods=['GET'])
@login_required
def get_challenge():
    return get_random_challenge()

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
