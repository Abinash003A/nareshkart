"""
app.py — NareshKart Flask entry point
"""
from flask import Flask, jsonify
from auth.routes import auth_bp
from orders.routes import orders_bp
from products.routes import products_bp
from cart.routes import cart_bp
from wishlist.routes import wishlist_bp
from users.routes import users_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
