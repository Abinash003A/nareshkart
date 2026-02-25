-- NareshKart Database Schema

CREATE DATABASE IF NOT EXISTS nareshkart;
USE nareshkart;

CREATE TABLE IF NOT EXISTS users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(200) NOT NULL,
    category   VARCHAR(100),
    price      DECIMAL(10,2) NOT NULL,
    emoji      VARCHAR(10),
    hot        TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cart (
    user_id    INT NOT NULL,
    product_id INT NOT NULL,
    qty        INT NOT NULL DEFAULT 1,
    PRIMARY KEY (user_id, product_id),
    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS wishlist (
    user_id    INT NOT NULL,
    product_id INT NOT NULL,
    PRIMARY KEY (user_id, product_id),
    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT,
    total_amount DECIMAL(10,2) NOT NULL,
    location     VARCHAR(255),
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT,
    qty        INT NOT NULL,
    price      DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES orders(id)   ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Sample products
INSERT INTO products (name, category, price, emoji, hot) VALUES
('AWS Solutions Architect Guide',  'Books',     799,  '📘', 1),
('Docker & Kubernetes Handbook',   'Books',     699,  '📗', 1),
('Python for DevOps',              'Books',     599,  '📙', 0),
('Linux Command Reference',        'Materials', 299,  '📄', 0),
('Raspberry Pi 4 (4GB)',           'Gadgets',   4500, '🖥️', 1),
('USB-C Hub 7-in-1',               'Gadgets',   1299, '🔌', 0),
('Cloud Architecture Flashcards',  'Materials', 399,  '🃏', 1),
('Terraform Deep Dive',            'Books',     749,  '📕', 0);
