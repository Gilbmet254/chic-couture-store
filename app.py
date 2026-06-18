from flask import Flask, jsonify, request
import sqlite3
import json
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# =========================
# APP INIT (MUST BE FIRST)
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# DATABASE CONFIG (SAFE: works locally + Render)
# =========================
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL (Render)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    # fallback (local dev)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "json", "products.json")

# =========================
# SQLITE CONNECTION (keep for now)
# =========================
def get_db():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return {"message": "Chic Couture API is running..."}

@app.route("/test")
def test():
    return {"status": "working"}

# -------------------------
# PRODUCTS (still JSON for now)
# -------------------------
@app.route("/products")
def products():
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
    return jsonify(data)

# -------------------------
# SIGNUP
# -------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO customers (name,email,password) VALUES (?,?,?)",
        (data["name"], data["email"], data["password"])
    )
    conn.commit()
    return {"message": "User created"}

# -------------------------
# ORDER
# -------------------------
@app.route("/order", methods=["POST"])
def order():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO orders (customer_id,total,status) VALUES (?,?,?)",
        (data["customer_id"], data["total"], "Pending")
    )
    conn.commit()
    return {"message": "Order placed"}

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
