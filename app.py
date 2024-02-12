"""
Module: app.py
"""
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from db import db
from resources.item import blp as ItemBlueprint
from resources.account import blp as AccountBlueprint
from resources.sale_item import blp as SaleItemBlueprint
from resources.store import blp as StoreBlueprint

def create_app(db_url=None):
    """
    Create App
    """
    app = Flask(__name__)
    app.config["API_TITLE"] = "Accounts REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "Rocio"
    JWTManager(app)

    # For testing when deployed need to close it for safety
    CORS(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(AccountBlueprint)
    api.register_blueprint(SaleItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
