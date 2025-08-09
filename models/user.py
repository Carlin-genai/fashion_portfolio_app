from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

def gen_id(prefix="usr_"):
    return prefix + uuid.uuid4().hex[:12]

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True, default=gen_id)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    portfolios = db.relationship("Portfolio", backref="owner", lazy="dynamic")
    feedbacks = db.relationship("Feedback", backref="author", lazy="dynamic")

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)
