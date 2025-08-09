from datetime import datetime
from extensions import db
import uuid

def gen_id(prefix="wi_"):
    return prefix + uuid.uuid4().hex[:12]

class WorkItem(db.Model):
    __tablename__ = "work_items"
    id = db.Column(db.String, primary_key=True, default=gen_id)
    portfolio_id = db.Column(db.String, db.ForeignKey("portfolios.id"), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    media_url = db.Column(db.String(1024))
    media_type = db.Column(db.String(30))
    order = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(255))
    materials = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
