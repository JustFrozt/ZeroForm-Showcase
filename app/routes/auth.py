from flask import Blueprint, request, jsonify
from ..models import User
from ..extensions import db, bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user.
    ---
    parameters:
      - in: body
        name: body
        schema:
          id: UserRegister
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The user's username.
            password:
              type: string
              description: The user's password.
    responses:
      201:
        description: User created successfully.
        schema:
          properties:
            message:
              type: string
      400:
        description: Username already exists.
        schema:
          properties:
            message:
              type: string
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"message": "Username is required."}), 400
    if not password:
        return jsonify({"message": "Password is required."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user and returns a JWT.
    ---
    parameters:
      - in: body
        name: body
        schema:
          id: UserLogin
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The user's username.
            password:
              type: string
              description: The user's password.
    responses:
      200:
        description: Authentication successful, returns access token.
        schema:
          properties:
            access_token:
              type: string
      401:
        description: Bad username or password.
        schema:
          properties:
            message:
              type: string
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Bad username or password."}), 401