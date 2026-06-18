from flask import Flask
from flask_cors import CORS
from extensions import db
import os

# 1. CREATE APP FIRST
app = Flask(__name__)
CORS(app)

# 2. CONFIGURE APP
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 3. INIT DB
db.init_app(app)

# 4. IMPORT ROUTES (AFTER app exists)
from routes.products import products_bp
from routes.admin import admin_bp

# 5. REGISTER BLUEPRINTS
app.register_blueprint(products_bp)
app.register_blueprint(admin_bp)

# 6. ROUTES
@app.route("/")
def home():
    return {"message": "API running"}

# 7. CREATE TABLES
with app.app_context():
    db.create_all()
