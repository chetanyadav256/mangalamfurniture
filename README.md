# Manglam Furniture

Server-rendered Django catalog for Manglam Furniture. Customers can browse categories and furniture details, then contact the store by phone, WhatsApp, or the contact form. There is no customer account, cart, checkout, payment, order, review, or rating system.

## Local setup

```powershell
py -m pip install -r requirements.txt
Copy-Item .env.example .env
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Open `http://127.0.0.1:8000/`. The admin is at `/admin/`. Uploaded media is local in development.

## Production

The target host is Render. `render.yaml` defines a Python web service, managed PostgreSQL database, `collectstatic`, migrations, and Gunicorn. Set the `SECRET_KEY`, `ALLOWED_HOSTS`, and cloud storage credentials in Render's environment settings; do not commit real values. Production uses `DEBUG=False`, HTTPS redirect, secure session/CSRF cookies, HSTS, and WhiteNoise for static files. Admin-uploaded media requires the configured S3-compatible bucket.

After the first deploy, run `python manage.py createsuperuser` from the Render shell and create the singleton ShopInfo record in the admin.

Live URL: Not deployed. GitHub CLI is not installed in the current environment, and no GitHub or Render credentials were provided.

## Verified checkpoints

- Initial project scaffold
- Data models and migrations
- Customized admin panel
- Responsive public views and templates
- Contact form and security hardening
- Static and media configuration