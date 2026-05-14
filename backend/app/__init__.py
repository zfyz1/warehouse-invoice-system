from webbrowser import register

from flask import Flask
from flask_cors import CORS

from app.routes.customer import customer_bp
from app.routes.user import user_bp
from app.routes.produt import product_bp
from app.routes.test import test_bp
def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(test_bp, url_prefix="/api/test")

    app.register_blueprint(user_bp,url_prefix="/api/user")
    app.register_blueprint(product_bp,url_prefix="/api/product")

    app.register_blueprint(customer_bp, url_prefix="/api/customer")
    return app