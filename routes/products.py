from flask import Blueprint, request, jsonify
from models import Product
from extensions import db

products_bp = Blueprint("products", __name__)

# GET ALL PRODUCTS
@products_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category,
            "description": p.description,
            "image": p.image
        } for p in products
    ])

# ADD PRODUCT
@products_bp.route("/products", methods=["POST"])
def add_product():
    data = request.json

    product = Product(
        name=data["name"],
        price=data["price"],
        category=data.get("category"),
        description=data.get("description"),
        image=data.get("image")
    )

    db.session.add(product)
    db.session.commit()

    return {"message": "Product added"}
