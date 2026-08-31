# Deployment.md

## 1. Hosting Recommendation

**Render or Railway** (PaaS) is recommended over a raw VPS for this project because:
- Both offer managed PostgreSQL provisioning, automatic HTTPS/SSL, and simple git-push deploys — appropriate for a small business site without dedicated devops support.
- A raw VPS (e.g., DigitalOcean, Linode) is a valid alternative if the team wants more control or lower long-term cost, but it requires manually managing Nginx/Gunicorn, SSL certificates (e.g., Let's Encrypt/Certbot), firewall rules, and OS patching — more operational overhead.

> Whichever platform is chosen, confirm current pricing/free-tier limits directly on the provider's site at implementation time, as these change frequently.

## 2. Environment Variables

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key — generate a new one for production, never reuse dev key |
| `DEBUG` | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated production domain(s) |
| `DATABASE_URL` | PostgreSQL connection string (most PaaS providers inject this automatically) |
| `CLOUD_STORAGE_*` (e.g. `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, or Cloudinary equivalent) | Credentials for media file storage backend |
| `EMAIL_HOST` / `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | If contact form sends admin email notifications |
| `SECURE_SSL_REDIRECT` | `True` in production |

Use `python-decouple` or `django-environ` to load these from a `.env` file locally and from the host's environment variable settings in production (see `TechStack.md`).

## 3. Static & Media File Handling

- **Static files** (CSS/JS/site images): run `python manage.py collectstatic` as part of the deploy build step; serve via **WhiteNoise** (verify latest version) for simplicity on PaaS, or via the host's CDN/static file serving if provided.
- **Media files** (admin-uploaded item images): **do not rely on local disk storage in production** — most PaaS platforms have ephemeral filesystems, meaning uploaded images can be lost on redeploy/restart. Use `django-storages` with a cloud backend (AWS S3, Cloudinary, or Backblaze B2) as established in `TechStack.md`.
- Confirm `MEDIA_URL` and `MEDIA_ROOT` (or the storage backend's equivalent settings) are correctly configured before the admin uploads real product images.

## 4. Database Setup

1. Provision a PostgreSQL instance via the hosting platform (Render/Railway both offer managed Postgres add-ons).
2. Set `DATABASE_URL` environment variable (use `dj-database-url`, verify latest version, to parse it into Django's `DATABASES` setting).
3. Run migrations on deploy: `python manage.py migrate`.
4. Create the initial admin superuser: `python manage.py createsuperuser` (run once, manually, via platform shell access — do not hardcode admin credentials anywhere).
5. Seed initial `ShopInfo` singleton row (address, hours, contact info) via the admin panel after first deploy.

## 5. Deployment Steps (Summary)

1. Push code to a git repository (GitHub recommended for Render/Railway integration).
2. Connect the repository to the chosen PaaS platform.
3. Set all environment variables listed above in the platform's dashboard.
4. Configure the build command: install dependencies (`pip install -r requirements.txt`), run `collectstatic`, run `migrate`.
5. Configure the start command: run Gunicorn (`gunicorn manglam_furniture.wsgi:application`) — verify latest Gunicorn version.
6. Point the custom domain (if any) to the platform and confirm HTTPS/SSL is issued automatically.
7. Smoke-test all pages (home, category listing, item detail, about, contact) on mobile, tablet, and desktop after deploy.

## 6. Backup Strategy

- Enable the hosting platform's automated PostgreSQL backups if available (most managed Postgres add-ons offer daily backups with a retention window — confirm specifics with the chosen provider).
- Periodically export a manual `pg_dump` backup before major catalog changes or migrations, stored securely off-platform (e.g., in cloud storage separate from the app's media bucket).
- Media files stored in cloud object storage (S3/Cloudinary/B2) typically have their own durability guarantees, but confirm the provider's redundancy/backup policy.
- Document a basic restore procedure (restore `pg_dump` to a fresh Postgres instance) so recovery isn't improvised during an incident.

## 7. Post-Deployment Checklist

- [ ] `DEBUG = False` confirmed in production.
- [ ] HTTPS enforced and working.
- [ ] Admin login tested in production.
- [ ] Image uploads tested end-to-end (upload → visible on live item detail page).
- [ ] Contact form submission tested end-to-end.
- [ ] Site tested on real mobile device, tablet (or emulator), and desktop browser.
- [ ] Database backup confirmed active/scheduled.
