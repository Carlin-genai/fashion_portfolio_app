from datetime import datetime
from extensions import db
import uuid

def gen_id(prefix="pf_"):
    return prefix + uuid.uuid4().hex[:12]

class Portfolio(db.Model):
    __tablename__ = "portfolios"
    id = db.Column(db.String, primary_key=True, default=gen_id)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    theme = db.Column(db.String(80), default="minimal")
    owner_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    work_items = db.relationship("WorkItem", backref="portfolio", lazy="dynamic", cascade="all, delete-orphan")
    feedbacks = db.relationship("Feedback", backref="portfolio", lazy="dynamic", cascade="all, delete-orphan")
