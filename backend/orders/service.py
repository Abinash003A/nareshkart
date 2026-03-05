"""
orders/service.py
Business logic for placing orders.
Handles both direct buy and cart checkout flows.
"""
from orders.models import get_cart_items, get_product_price, create_order, clear_cart

def place_order(user_id, location, source, product_id=None, qty=1):
    items = []

    if source == "direct":
        if not product_id:
            return False, "product_id required for direct order", {}
        product = get_product_price(product_id)
        if not product:
            return False, "Product not found", {}
        total = product["price"] * int(qty)
        items = [(product_id, int(qty), product["price"])]

    else:
        rows = get_cart_items(user_id)
        if not rows:
            return False, "Cart is empty", {}
        total = sum(r["qty"] * r["price"] for r in rows)
        items = [(r["product_id"], r["qty"], r["price"]) for r in rows]

    order_id = create_order(user_id, total, location, items)

    if source != "direct":
        clear_cart(user_id)

    return True, "Order placed successfully", {"order_id": order_id, "total": float(total)}
