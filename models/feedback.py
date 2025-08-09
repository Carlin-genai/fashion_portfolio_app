from datetime import datetime
from extensions import db
import uuid

def gen_id(prefix="fb_"):
    return prefix + uuid.uuid4().hex[:12]

class Feedback(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.String, primary_key=True, default=gen_id)
    portfolio_id = db.Column(db.String, db.ForeignKey("portfolios.id"), nullable=False)
    author_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    strong_points = db.Column(db.Text)
    areas_to_improve = db.Column(db.Text)
    market_suggestions = db.Column(db.Text)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

