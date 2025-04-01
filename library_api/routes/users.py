# library_api/routes/users.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from library_api.models import User
from library_api import db
from library_api.utils import is_admin
from passlib.hash import bcrypt

users_bp = Blueprint("users", __name__)

@users_bp.route("", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")
        
        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists"}), 400

        new_user = User(username, password, role)
        # Print the hash for debugging (remove in production)
        print(f"Created user hash for '{username}': {new_user.password}")
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": f"User '{username}' created successfully"}), 201
    except Exception as e:
        print("Error creating user:", e)
        return jsonify({"msg": "Internal server error"}), 500

