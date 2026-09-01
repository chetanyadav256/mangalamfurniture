# EC2 Deployment Guide

This project is configured to run on an AWS EC2 instance using Gunicorn, PM2, and Nginx.

## One-time server setup

1. Launch an Ubuntu EC2 instance.
2. Connect to the instance:
   ```bash
   ssh ubuntu@<EC2_HOST>
   ```
3. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip git nginx curl
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install -y nodejs
   sudo npm install -g pm2
   ```
4. Clone the project repository:
   ```bash
   cd /home/ubuntu
   git clone <REPO_URL> chetanshop
   cd chetanshop
   ```
5. Create the Python virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
6. Create environment variables:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Fill in the values for:
   - SECRET_KEY
   - DEBUG
   - ALLOWED_HOSTS
   - DATABASE_URL
   - SECURE_SSL_REDIRECT
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_STORAGE_BUCKET_NAME
   - AWS_S3_REGION_NAME
7. Run Django setup once:
   ```bash
   source .venv/bin/activate
   python manage.py collectstatic --noinput
   python manage.py migrate --noinput
   ```
8. Start the app with PM2:
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   ```
9. Configure Nginx:
   ```bash
   sudo cp deploy/nginx.conf /etc/nginx/conf.d/chetanshop.conf
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```
10. Ensure the domain or EC2 public IP points to the server and update `ALLOWED_HOSTS` accordingly.

## Optional HTTPS

For production, install SSL with Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

## GitHub Actions deployment

The workflow in `.github/workflows/deploy.yml` deploys automatically on pushes to `main` using GitHub Secrets:
- `EC2_HOST`
- `EC2_USERNAME`
- `EC2_SSH_KEY`
