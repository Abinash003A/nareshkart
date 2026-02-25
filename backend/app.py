"""
app.py
------
Main Flask application entry point for NareshKart backend.

Responsibilities:
- Create Flask app
- Register all blueprints
- Health check endpoint for ALB
- Run app (systemd / gunicorn compatible)
"""

from flask import Flask, jsonify

# ---- Blueprints ----
from auth.routes import auth_bp
from orders.routes import orders_bp
from products.routes import products_bp
from cart.routes import cart_bp
from wishlist.routes import wishlist_bp
from users.routes import users_bp


def create_app():
    app = Flask(__name__)

    # -------------------------------
    # Register API Blueprints
    # -------------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)

    # -------------------------------
    # ALB / Load Balancer Health Check
    # -------------------------------
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app


# Create app instance
app = create_app()

# -------------------------------------------------
# Used only if running directly (NOT systemd)
# systemd / gunicorn will ignore this block
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
