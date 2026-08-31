# Architecture.md

## 1. High-Level Overview

Manglam Furniture is a **server-rendered Django monolith** (Django templates, not a separate SPA frontend). This is appropriate because:
- The site is read-only/catalog-style for customers — no complex client-side state.
- SEO matters (customers should find items via Google search) — server-rendered HTML is simpler to get right than a JS SPA.
- Admin needs are covered by Django's built-in admin (customized), avoiding a separate admin app.

There is one Django project with multiple focused apps, a PostgreSQL database, and media files (item images) served via a storage backend (local disk in dev, cloud object storage recommended in production — see `TechStack.md` and `Deployment.md`).

## 2. Django App Structure

| App | Responsibility |
|---|---|
| `core` | Shared base templates, homepage view, static assets, common utilities/mixins |
| `catalog` | Category, Item, ItemImage models; category listing & item detail views/URLs |
| `shop_info` | ShopInfo model (address, hours, contact numbers), About/Contact pages, ContactMessage model & form handling |
| `accounts` (or Django's built-in `auth`) | Admin authentication only — no customer-facing account features |

Optional future app: `api` — if a REST layer is added later for a mobile app (see `API.md`).

## 3. Request Flow (Text Diagram)

**Customer browsing a category:**
```
Browser (GET /shop/sofa/)
   -> Django URL router (catalog/urls.py)
   -> CategoryListView (catalog/views.py)
   -> Query: Item.objects.filter(category__slug='sofa', is_active=True)
   -> Render: catalog/category_list.html (extends core/base.html)
   -> Response: HTML with responsive grid of item cards
```

**Customer viewing an item:**
```
Browser (GET /shop/sofa/3-seater-recliner/)
   -> ItemDetailView (catalog/views.py)
   -> Query: Item.objects.get(slug=..., is_active=True) + prefetch ItemImages
   -> Render: catalog/item_detail.html
   -> Response: HTML with image gallery, price, specs, stock badge
```

**Admin editing an item:**
```
Browser (admin login) -> Django auth middleware checks session
   -> Django Admin (or custom admin view) for Item model
   -> Form submission -> validation -> DB write
   -> Redirect to admin item list with success message
```

**Customer submitting contact form:**
```
Browser (POST /contact/)
   -> ContactFormView (shop_info/views.py)
   -> Django Form validation (CSRF token checked automatically)
   -> ContactMessage.objects.create(...)
   -> (Optional) email notification to admin
   -> Redirect with success message
```

## 4. Folder Structure

```
manglam_furniture/
├── manage.py
├── requirements.txt
├── .env.example
├── manglam_furniture/          # project package
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── templates/core/
│   │   ├── base.html
│   │   └── home.html
│   ├── static/core/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── views.py
│   └── urls.py
├── catalog/
│   ├── models.py               # Category, Item, ItemImage
│   ├── views.py
│   ├── urls.py
│   ├── admin.py                # custom ModelAdmin config
│   ├── forms.py
│   └── templates/catalog/
│       ├── category_list.html
│       └── item_detail.html
├── shop_info/
│   ├── models.py                # ShopInfo, ContactMessage
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── templates/shop_info/
│       ├── about.html
│       └── contact.html
├── static/                      # collected static (production)
├── media/                       # uploaded images (dev only; use object storage in prod)
└── templates/
    └── 404.html, 500.html
```

## 5. Key Architectural Decisions

- **Monolith over SPA/API-first**: simpler to build, deploy, and hand off; matches the catalog-only scope.
- **Slugs, not IDs, in URLs**: `/shop/sofa/3-seater-recliner/` is SEO-friendly and human-readable.
- **Soft-hide (`is_active`) instead of hard delete on Item**: preserves data integrity if an item is temporarily out of catalog.
- **Settings split by environment** (`dev.py` / `production.py`): keeps secrets and debug flags environment-specific — standard Django practice.
