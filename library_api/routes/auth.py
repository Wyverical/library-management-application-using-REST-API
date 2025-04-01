# library_api/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from library_api.models import User
from library_api import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
