from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import uuid

def generate_id(prefix=""):
    return f"{prefix}{uuid.uuid4().hex[:12]}"

class RoleEnum(enum.Enum):
    STUDENT = "student"
    ALUMNI = "alumni"
    MENTOR = "mentor"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True, default=lambda: generate_id("usr_"))
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.STUDENT)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    portfolios = db.relationship("Portfolio", backref="owner", lazy="dynamic")
    feedbacks = db.relationship("Feedback", backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Portfolio(db.Model):
    __tablename__ = "portfolios"
    id = db.Column(db.String, primary_key=True, default=lambda: generate_id("pf_"))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    theme = db.Column(db.String(80), default="minimal")
    owner_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)

    work_items = db.relationship("WorkItem", backref="portfolio", lazy="dynamic", cascade="all, delete-orphan")
    feedbacks = db.relationship("Feedback", backref="portfolio", lazy="dynamic", cascade="all, delete-orphan")

class WorkItem(db.Model):
    __tablename__ = "work_items"
    id = db.Column(db.String, primary_key=True, default=lambda: generate_id("wi_"))
    portfolio_id = db.Column(db.String, db.ForeignKey("portfolios.id"), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    media_url = db.Column(db.String(1024))  # S3 or local path
    media_type = db.Column(db.String(30))   # image | video | pdf | other
    order = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(255))
    materials = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.String, primary_key=True, default=lambda: generate_id("fb_"))
    portfolio_id = db.Column(db.String, db.ForeignKey("portfolios.id"), nullable=False)
    author_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    strong_points = db.Column(db.Text)
    areas_to_improve = db.Column(db.Text)
    market_suggestions = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create any additional reference tables like Theme, Badges, etc., as needed.
