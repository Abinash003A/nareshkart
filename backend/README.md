## NareshKart

### Backend Setup (EC2)

1. Clone repo into /opt/nareshkart
2. Create venv:
   python3 -m venv venv
3. Install deps:
   venv/bin/pip install -r backend/requirements.txt
4. Create DB using backend/schema.sql
5. Create AWS Secret for DB credentials
6. Configure Redis endpoint
7. Copy backend/nareshkart.service to /etc/systemd/system
8. systemctl daemon-reload
9. systemctl start nareshkart

### Health Check (ALB)
/health

### Buy Flow
- Buy Now → creates order
- Cart Buy → creates order
- Payment dummy
- Orders visible in history
