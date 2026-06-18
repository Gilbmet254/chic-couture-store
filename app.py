from flask import Flask
from flask_cors import CORS
from extensions import db
from routes.admin import admin_bp
app.register_blueprint(admin_bp)
import os

app = Flask(__name__)
CORS(app)

# config
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# IMPORT ROUTES (AFTER app is created)
from routes.products import products_bp
app.register_blueprint(products_bp)

@app.route("/")
def home():
    return {"message": "API running"}

with app.app_context():
    db.create_all()
