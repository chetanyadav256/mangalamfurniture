# Security.md

## 1. Admin Authentication

- Use Django's built-in session-based authentication (`django.contrib.auth`) for the admin login only.
- Enforce a strong password policy via Django's built-in `AUTH_PASSWORD_VALIDATORS`.
- Admin login should go through Django's default `/admin/login/` (or a custom-styled equivalent using `LoginView`) — do not build custom auth logic.
- Set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` in production (requires HTTPS).
- Consider a reasonably short `SESSION_COOKIE_AGE` for admin sessions and enable Django's session expiry on browser close if the admin uses shared/public computers.
- No customer authentication exists at all — do not add login/registration views for customers under any circumstance (explicit product constraint).

## 2. Permissions

| Action | Who Can Do It |
|---|---|
| View catalog, item details, shop info | Anyone (public, unauthenticated) |
| Submit contact form | Anyone (public, unauthenticated) |
| Add/edit/delete Category, Item, ItemImage | Admin only (`is_staff=True` / `is_superuser=True`) |
| Edit ShopInfo | Admin only |
| View/manage ContactMessage submissions | Admin only |

- Use Django's `@staff_member_required` decorator (or `LoginRequiredMixin` + `UserPassesTestMixin`) to protect any custom admin views outside the default Django admin.
- If using only the default Django Admin, permissions are enforced automatically by `is_staff`/`is_superuser` and model-level permissions — no extra code needed, but confirm `ModelAdmin` classes don't accidentally expose write access to non-staff.

## 3. CSRF Protection

- Django's CSRF middleware is enabled by default — **do not disable it**.
- Every form (contact form, admin forms) must include `{% csrf_token %}` in the template.
- If any AJAX calls are added later (e.g., for a dynamic contact form), include the CSRF token in the request headers per Django's documented pattern.

## 4. Input Validation — Contact Form

- Use a Django `ModelForm` for `ContactMessage` so field-level validation (max length, required fields) is enforced server-side automatically.
- Validate `phone_or_email` format at the form level (basic regex or Django's `EmailValidator` if split into separate fields later).
- Enforce a reasonable `max_length` on the `message` field (e.g., 2000 characters) to prevent abuse.
- Add basic spam protection: honeypot field or a simple rate limit (e.g., `django-ratelimit`, verify latest version) on the contact POST endpoint to reduce automated spam submissions. A CAPTCHA (e.g., Google reCAPTCHA) is a reasonable addition if spam becomes a real problem post-launch.
- Never render user-submitted contact message content unescaped anywhere (Django templates auto-escape by default — do not use `|safe` on user input).

## 5. Image Upload Validation

- Restrict `ImageField` uploads to standard image MIME types (JPEG, PNG, WebP) at the form/admin level.
- Set a reasonable max file size (e.g., 5–10MB) and validate it in the `ModelForm`/`ModelAdmin` clean method — Django does not enforce file size limits by default.
- Rely on Pillow (used internally by `ImageField`) to validate that uploaded files are genuinely valid images, not disguised executables.
- Since only admins upload images (no public upload surface), the attack surface here is limited — but validation should still be enforced as defense-in-depth in case an admin account is compromised.
- Store uploaded images outside of any directly-executable path; if using cloud object storage (recommended, see `TechStack.md`), this is handled by the storage provider by default.

## 6. General Hardening Checklist

- [ ] `DEBUG = False` in production settings.
- [ ] `SECRET_KEY` loaded from environment variable, never committed to source control.
- [ ] `ALLOWED_HOSTS` set explicitly to the production domain(s).
- [ ] Force HTTPS: `SECURE_SSL_REDIRECT = True`, `SECURE_HSTS_SECONDS` set appropriately.
- [ ] `X-Frame-Options`, `SECURE_CONTENT_TYPE_NOSNIFF`, and Django's other default security middleware left enabled.
- [ ] Database credentials loaded from environment variables, not hardcoded.
- [ ] Regular `pip`/dependency updates to patch known vulnerabilities (verify latest versions periodically, don't pin indefinitely).
- [ ] Admin panel URL can optionally be changed from `/admin/` to reduce automated bot probing (minor obscurity measure, not a substitute for strong auth).
- [ ] Rate-limit or monitor login attempts on the admin login page (Django doesn't do this by default — consider `django-axes` or similar, verify latest version, if brute-force attempts are a concern).
- [ ] Backups of the database are taken regularly (see `Deployment.md`).
- [ ] No payment or sensitive financial data is ever collected or stored — reduces overall risk surface significantly by design.
