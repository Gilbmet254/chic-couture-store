from flask import Flask, jsonify, request
import sqlite3
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def db():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn

# GET PRODUCTS
@app.route("/products")
def products():
    with open("json/products.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/test")
def test():
    return {"status": "working"}

@app.route("/")
def home():
    return "Chic Couture API is running..."

# SIGNUP
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = db()
    conn.execute(
        "INSERT INTO customers (name,email,password) VALUES (?,?,?)",
        (data["name"], data["email"], data["password"])
    )
    conn.commit()
    return {"message": "User created"}

# CREATE ORDER
@app.route("/order", methods=["POST"])
def order():
    data = request.json
    conn = db()
    conn.execute(
        "INSERT INTO orders (customer_id,total,status) VALUES (?,?,?)",
        (data["customer_id"], data["total"], "Pending")
    )
    conn.commit()
    return {"message": "Order placed"}

if __name__ == "__main__":
    app.run(debug=True)
