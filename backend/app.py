"""
Main Flask application entry point
"""

from flask import Flask
from auth.routes import auth_bp
from users.routes import users_bp
from products.routes import products_bp
from orders.routes import orders_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
