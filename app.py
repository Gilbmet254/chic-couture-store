from flask import Flask, jsonify, request
import sqlite3
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
    conn = db()
    rows = conn.execute("SELECT * FROM products").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/test")
def test():
    return {"status": "working"}

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
