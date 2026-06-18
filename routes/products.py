from flask import Blueprint, jsonify, request
from extensions import db
from models import Product

products_bp = Blueprint("products_bp", __name__)

# GET ALL PRODUCTS
@products_bp.route("/admin/products", methods=["GET"])
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
        }
        for p in products
    ])

# CREATE PRODUCT
@products_bp.route("/admin/products", methods=["POST"])
def create_product():
    data = request.json

    new_product = Product(
        name=data["name"],
        price=data["price"],
        category=data.get("category"),
        description=data.get("description"),
        image=data.get("image")
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created"}), 201


# DELETE PRODUCT
@products_bp.route("/admin/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"})


# UPDATE PRODUCT
@products_bp.route("/admin/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Not found"}), 404

    data = request.json

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.category = data.get("category", product.category)
    product.description = data.get("description", product.description)
    product.image = data.get("image", product.image)

    db.session.commit()

    return jsonify({"message": "Product updated"})
