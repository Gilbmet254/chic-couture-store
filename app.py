from flask import Flask, request, jsonify
from models import Customer
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

@app.route("/")
def home():
    return {"message": "API running"}

@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    email = data.get("email")

    existing = Customer.query.filter_by(
        email=email
    ).first()

    if existing:
        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 400

    customer = Customer(
        name=data.get("name"),
        email=email,
        password=data.get("password")
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registration successful"
    })

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    customer = Customer.query.filter_by(
        email=data.get("email"),
        password=data.get("password")
    ).first()

    if not customer:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful",
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email
        }
    })

@app.route("/admin/customers")
def customers():

    customers = Customer.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.email
        }
        for c in customers
    ])
