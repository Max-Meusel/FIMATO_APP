from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class SecurityQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_type = db.Column(db.String(10), nullable=False)  # 'standard' oder 'custom'
    question_text = db.Column(db.String(200), nullable=False)
    answer_hash = db.Column(db.String(200), nullable=False)
    
    def set_answer(self, answer):
        self.answer_hash = generate_password_hash(answer)
    
    def check_answer(self, answer):
        return check_password_hash(self.answer_hash, answer) 