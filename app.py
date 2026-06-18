import os
from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db
from models import Product, Customer, Order

app = Flask(__name__)
CORS(app)

# PostgreSQL (Render)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return {"message": "API running"}

@app.route("/products")
def products():
    items = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category,
            "description": p.description,
            "image": p.image
        } for p in items
    ])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
