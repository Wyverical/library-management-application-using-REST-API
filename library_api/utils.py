# library_api/utils.py
from flask_jwt_extended import get_jwt_identity
from .models import User

def is_admin():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    return user is not None and user.role.lower() == "admin"
