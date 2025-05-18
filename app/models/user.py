from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    accept_terms = db.Column(db.Boolean, nullable=False, default=False)
    accept_privacy = db.Column(db.Boolean, nullable=False, default=False)
    newsletter_subscription = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationship zu SecurityQuestion
    security_question = db.relationship('SecurityQuestion', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 