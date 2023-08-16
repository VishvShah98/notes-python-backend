from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
import jwt
from config import SECRET_KEY

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    # Check if the username is already taken
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists. Please choose a different username.'}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate a JWT token without an expiry time
    payload = {'username': username}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jsonify({'access_token': access_token}), 200
