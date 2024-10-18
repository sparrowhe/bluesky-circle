from flask import Blueprint

# Create a Blueprint for avatar-related routes
avatar_bp = Blueprint('avatar', __name__)

from avatar import routes