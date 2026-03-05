# NareshKart — IT Learning Store

E-commerce platform for IT books, study materials, cloud/DevOps resources and tech gadgets.

---

## Architecture
```
Internet → Public ALB → Frontend EC2 (Nginx) → Private ALB → Backend ASG → RDS + Redis
```

---

## Backend Deployment

- Clone the repo and switch to backend
```bash
git clone https://github.com/<your-username>/nareshkart.git /opt/nareshkart
cd /opt/nareshkart/backend
```

- Install dependencies
```bash
sudo yum update -y
sudo yum install python3 python3-pip git -y
```

- Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

- Install requirements
```bash
pip install -r requirements.txt
```

---

## Initialize RDS Database

```bash
mysql -h <rds-endpoint> -u admin -p<password> < schema.sql

# Example
mysql -h nareshkart.cuk1or8kdbv9.ap-south-1.rds.amazonaws.com -u admin -pCloud123 < schema.sql
```

---

## AWS Secrets Manager — Store RDS Credentials

```bash
aws secretsmanager create-secret \
  --name nareshkart/db \
  --secret-string '{"host":"<RDS_ENDPOINT>","username":"admin","password":"<PASSWORD>","dbname":"nareshkart"}'
```

---

## Configure Environment Variables

Open `backend/core/config.py` and update these defaults:

```python
AWS_REGION       = os.getenv("AWS_REGION", "ap-south-1")          # your region
DB_SECRET_NAME   = os.getenv("DB_SECRET_NAME", "nareshkart/db")   # your secret name
REDIS_HOST       = os.getenv("REDIS_HOST", "127.0.0.1")           # ElastiCache endpoint
SES_SENDER_EMAIL = os.getenv("SES_SENDER_EMAIL", "you@gmail.com") # your verified SES email
```

> Verify your sender email in AWS Console → SES → Verified Identities before deploying.

---

## Create systemd Service

```bash
sudo vi /etc/systemd/system/nareshkart.service
```

Paste below — change `User` to your Linux username (run `whoami` to check):

```ini
[Unit]
Description=NareshKart Flask Backend
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/opt/nareshkart/backend
Environment="PATH=/opt/nareshkart/venv/bin"
Environment="JWT_SECRET=<run: openssl rand -hex 32>"
Environment="AWS_REGION=ap-south-1"
Environment="DB_SECRET_NAME=nareshkart/db"
Environment="REDIS_HOST=<elasticache-endpoint>"
Environment="REDIS_PORT=6379"
Environment="SES_SENDER_EMAIL=you@gmail.com"
ExecStart=/opt/nareshkart/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

- Start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable nareshkart
sudo systemctl start nareshkart
sudo systemctl status nareshkart
```

- Verify backend is running
```bash
curl http://127.0.0.1:8000/health
# Expected: {"status": "ok"}
```

---

## Create AMI → Launch Template → ASG

1. AWS Console → EC2 → select instance → Actions → Image → **Create Image**
   - Name: `nareshkart-backend-v1`

2. Create **Launch Template**
   - AMI: `nareshkart-backend-v1`
   - Instance type: `t3.small`
   - Security Group: `sg-backend`
   - IAM Profile: role with `secretsmanager:GetSecretValue` + `ses:SendEmail` + `AmazonSSMManagedInstanceCore`

3. Create **Target Group**
   - Name: `tg-backend`
   - Port: `8000`
   - Health check path: `/health`

4. Create **Private ALB** (internal)
   - Subnets: private subnets
   - Security Group: `sg-private-alb`
   - Listener: port `80` → forward to `tg-backend`

5. Create **ASG**
   - Launch Template: `nareshkart-backend-lt`
   - Min / Desired / Max: `1 / 2 / 4`
   - Scaling policy: CPU at 60%

---

## Frontend Deployment

- Clone repo
```bash
git clone https://github.com/<your-username>/nareshkart.git /opt/nareshkart
cd /opt/nareshkart/frontend
```

- Install Nginx
```bash
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

- Check `const API="/api"` is present in every HTML file's script section — **do not change this**, it is required for reverse proxy
```javascript
const API = "/api";  // mandatory for reverse proxy — do not change
```

- Copy frontend files to Nginx root
```bash
sudo cp -r /opt/nareshkart/frontend/* /usr/share/nginx/html/
```

---

## Reverse Proxy Setup

```bash
sudo vi /etc/nginx/conf.d/nareshkart.conf
```

Paste below and replace `<PRIVATE_ALB_DNS>` with your actual Private ALB DNS:

```nginx
server {
    listen 80;
    server_name _;

    # Reverse proxy — forward /api/* to Private ALB → Backend ASG
    location ^~ /api/ {
        proxy_pass         http://<PRIVATE_ALB_DNS>;
        proxy_http_version 1.1;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }

    # Serve static frontend files
    root  /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

> Private ALB DNS example:
> `internal-nareshkart-pvt-alb-xxxx.ap-south-1.elb.amazonaws.com`

- Test and reload Nginx
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## Create Frontend Target Group → Public ALB

1. Create **Target Group**
   - Name: `tg-frontend`
   - Port: `80`
   - Health check path: `/`
   - Register frontend EC2

2. Create **Public ALB** (internet-facing)
   - Subnets: public subnets
   - Security Group: `sg-public-alb`
   - Listener: port `80` → forward to `tg-frontend`

---

## Security Groups

| Security Group | Inbound |
|----------------|---------|
| `sg-public-alb` | 80, 443 from `0.0.0.0/0` |
| `sg-frontend` | 80 from `sg-public-alb` |
| `sg-private-alb` | 80 from `sg-frontend` |
| `sg-backend` | 8000 from `sg-private-alb` |
| `sg-rds` | 3306 from `sg-backend` |
| `sg-redis` | 6379 from `sg-backend` |

---

## Verify Everything

```bash
# Health check
curl http://<PUBLIC_ALB_DNS>/health

# Test API through reverse proxy
curl -X POST http://<PUBLIC_ALB_DNS>/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```
