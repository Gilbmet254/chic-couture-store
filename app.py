from flask import Flask, request, jsonify
from flask_cors import CORS
from extensions import db
from models import Customer
import os

# CREATE APP
app = Flask(__name__)
CORS(app)

# DATABASE CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# INIT DATABASE
db.init_app(app)

# IMPORT BLUEPRINTS
from routes.products import products_bp
from routes.admin import admin_bp

# REGISTER BLUEPRINTS
app.register_blueprint(products_bp)
app.register_blueprint(admin_bp)

# HOME ROUTE
@app.route("/")
def home():
    return {"message": "API running"}

# SIGNUP
@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    email = data.get("email")

    existing = Customer.query.filter_by(email=email).first()

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

# LOGIN
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

# ADMIN CUSTOMERS
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

# CREATE TABLES
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
