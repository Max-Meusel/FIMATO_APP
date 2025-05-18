from flask import Blueprint

bp = Blueprint('user_ui', __name__)

from app.user_ui import routes 