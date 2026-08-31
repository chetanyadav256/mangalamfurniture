# API.md

## 1. Approach

The MVP uses **Django templates with server-rendered views** — there is no REST API for the website itself. This section documents the internal view/URL structure. A REST layer is documented separately below as a **Future** option, in case a mobile app is added later.

## 2. Internal View/URL Structure (MVP)

| URL Pattern | View | Template | Purpose |
|---|---|---|---|
| `/` | `HomeView` | `core/home.html` | Featured items, category shortcuts |
| `/shop/` | `CategoryIndexView` | `catalog/category_index.html` | List of all categories |
| `/shop/<category_slug>/` | `CategoryListView` | `catalog/category_list.html` | Items within a category |
| `/shop/<category_slug>/<item_slug>/` | `ItemDetailView` | `catalog/item_detail.html` | Full item details, gallery |
| `/about/` | `AboutView` | `shop_info/about.html` | About page + shop info |
| `/contact/` | `ContactView` (GET + POST) | `shop_info/contact.html` | Contact form, map, hours |
| `/admin/` | Django Admin (customized) | Django default | Admin catalog & shop info management |

### View Notes
- `CategoryListView` and `ItemDetailView` filter on `is_active=True` — customers never see hidden/draft items.
- `ItemDetailView` should `prefetch_related("images")` ordered by `display_order` to avoid N+1 queries.
- `ContactView` renders the form on GET and validates + saves a `ContactMessage` on POST, then redirects (POST/redirect/GET pattern) to avoid duplicate submissions on refresh.
- All views are function-based or class-based per team convention — no strong preference, but be consistent (see `AI_Instructions.md`).

## 3. Future: REST API Layer (If a Mobile App Is Added)

If needed later, recommend **Django REST Framework** (verify latest version at implementation time) added as a separate `api` app, reusing the same models.

### Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/categories/` | List active categories | Public |
| GET | `/api/categories/<slug>/` | Category detail | Public |
| GET | `/api/categories/<slug>/items/` | Items in a category | Public |
| GET | `/api/items/<slug>/` | Item detail with images | Public |
| GET | `/api/shop-info/` | Shop contact/address/hours | Public |
| POST | `/api/contact/` | Submit a contact message | Public (rate-limited) |
| POST | `/api/admin/items/` | Create item | Admin (token/session auth) |
| PATCH | `/api/admin/items/<id>/` | Update item | Admin |
| DELETE | `/api/admin/items/<id>/` | Delete item | Admin |

### Sample: `GET /api/items/3-seater-recliner/`

```json
{
  "id": 42,
  "name": "3 Seater Recliner Sofa",
  "slug": "3-seater-recliner",
  "category": "sofa",
  "price": "34999.00",
  "description": "Premium recliner sofa with...",
  "material": "Sheesham Wood, Velvet Upholstery",
  "dimensions": "72in L x 34in W x 30in H",
  "color_variants": ["Grey", "Beige", "Maroon"],
  "stock_status": "in_stock",
  "warranty_info": "5 Year Warranty on Frame",
  "delivery_info": "Free Delivery & Installation within city",
  "images": [
    {"url": "/media/items/recliner-1.jpg", "is_primary": true},
    {"url": "/media/items/recliner-2.jpg", "is_primary": false}
  ]
}
```

### Sample: `POST /api/contact/` request

```json
{
  "name": "Rohan Sharma",
  "phone_or_email": "9876543210",
  "message": "Is the 3 seater recliner available in Maroon?"
}
```

### Sample response

```json
{
  "status": "success",
  "message": "Your message has been received. We'll contact you shortly."
}
```

> **Note:** This REST layer is explicitly out of scope for MVP. Do not build it unless requested — it is documented here only so a future AI agent or developer has a clear reference if a mobile app phase is approved.
