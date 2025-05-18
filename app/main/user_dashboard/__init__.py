from flask import Blueprint

bp = Blueprint('user_dashboard', __name__)

from app.user_dashboard import routes 