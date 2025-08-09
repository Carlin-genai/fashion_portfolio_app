import os
from flask import Flask, jsonify
from config import Config
from extensions import db, jwt, migrate, cors, limiter
from routes.auth import auth_bp
from routes.portfolio import portfolio_bp
from routes.work_item import work_item_bp
from routes.feedback import feedback_bp
from routes.ai_analysis import ai_bp
from routes.export import export_bp

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    limiter.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(portfolio_bp, url_prefix="/portfolios")
    app.register_blueprint(work_item_bp, url_prefix="/portfolios")
    app.register_blueprint(feedback_bp, url_prefix="/feedback")
    app.register_blueprint(ai_bp, url_prefix="/ai")
    app.register_blueprint(export_bp, url_prefix="/export")

    @app.route("/")
    def index():
        return jsonify({"msg": "Fashion Portfolio API running"})

    return app

# expose `app` for gunicorn
app = create_app()

if __name__ == "__main__":
    # local dev
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
