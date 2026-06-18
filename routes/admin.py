from flask import Blueprint, request, jsonify
from models import Product, Order, Customer
from extensions import db

admin_bp = Blueprint("admin", __name__)

# PRODUCTS DELETE
@admin_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return {"message": "Product deleted"}

# UPDATE ORDER STATUS
@admin_bp.route("/orders/<int:id>", methods=["PATCH"])
def update_order(id):
    data = request.json
    order = Order.query.get_or_404(id)

    order.status = data.get("status", order.status)
    db.session.commit()

    return {"message": "Order updated"}

# GET ORDERS
@admin_bp.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {
            "id": o.id,
            "customer_id": o.customer_id,
            "total": o.total,
            "status": o.status
        } for o in orders
    ])

# GET CUSTOMERS
@admin_bp.route("/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.email
        } for c in customers
    ])
