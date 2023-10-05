from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import timedelta
from functools import wraps
import os
from flask import Flask
from authlib.integrations.flask_client import OAuth
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guess'

# Get the base directory of the project
base_dir = Path(__file__).resolve().parent

# Set the database file path
db_path = base_dir / 'aurora.db'

# Set the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))

@jwt.user_identity_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            public_id=str(uuid.uuid4()),
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=generate_password_hash(request.form.get("password"))
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user and check_password_hash(user.password, request.form.get("password")):
            access_token = create_access_token(identity=user.public_id, expires_delta=timedelta(minutes=30))
            return make_response(jsonify({'token': access_token}), 201)
    return render_template("login.html")

@app.route("/logout")
@jwt_required
def logout():
    return redirect(url_for("home"))

@app.route("/")
@jwt_required
def home():
    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(public_id=current_user_identity).first()
    return render_template("home.html", current_user=current_user)

# OAuth Section
app.config['SERVER_NAME'] = 'localhost:5000'
oauth = OAuth(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google/')
def google():
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    # Access user profile information
    email = user['email']
    name = user['name']
    picture = user['picture']
    # You can use the profile information as needed
    # For example, you can store it in the database or use it to customize the user's experience
    print("Google User", user)
    return redirect('/')

@app.route('/twitter/')
def twitter():
    TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET')
    oauth.register(
        name='twitter',
        client_id=TWITTER_CLIENT_ID,
        client_secret=TWITTER_CLIENT_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        request_token_params=None,
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None,
        api_base_url='https://api.twitter.com/1.1/',
    )
    redirect_uri = url_for('twitter_auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)

@app.route('/twitter/auth/')
def twitter_auth():
    token = oauth.twitter.authorize_access_tokenwith_oauthlib_redirect()
    user= oauth.twitter.get('account/verify_credentials.json').json()
    # Access user profile information
    email = user['email']
    name = user['name']
    picture = user['profile_image_url']
    # You can use the profile information as needed
    # For example, you can store it in the database or use it to customize the user's experience
    print("Twitter User", user)
    return redirect('/')
def init_db():
    with current_app.app_context():
        db.create_all()
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)