# Database.md

## 1. Entity Overview

| Entity | Purpose |
|---|---|
| `Category` | Furniture category (Sofa, Bed, Dining Table, etc.) |
| `Item` | Individual furniture product |
| `ItemImage` | One of multiple images belonging to an Item |
| `ShopInfo` | Singleton record with store contact/address/hours |
| `ContactMessage` | Customer inquiries submitted via contact form |
| `User` (Django built-in `auth.User`) | Admin login only — no customer-facing usage |

## 2. Category

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | |
| `name` | CharField(100) | e.g. "Sofa" |
| `slug` | SlugField(100), unique | auto-generated from name, used in URLs |
| `description` | TextField, blank | optional category intro text |
| `image` | ImageField, blank/null | category thumbnail for shop menu |
| `is_active` | BooleanField, default=True | hide category without deleting |
| `display_order` | PositiveIntegerField, default=0 | controls menu/listing order |
| `created_at` | DateTimeField, auto_now_add | |
| `updated_at` | DateTimeField, auto_now | |

## 3. Item

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | |
| `category` | ForeignKey(Category, on_delete=PROTECT) | prevents accidental cascade delete of items |
| `name` | CharField(150) | |
| `slug` | SlugField(180), unique | used in item detail URL |
| `price` | DecimalField(10,2) | store in a single currency (INR assumed) |
| `discount` | DecimalField(10,2), default=0, blank | flat discount amount in INR; cannot be negative |
| `description` | TextField | full item description |
| `material` | CharField(150), blank | e.g. "Sheesham Wood, Velvet Upholstery" |
| `dimensions` | CharField(100), blank | e.g. "72in L x 34in W x 30in H" — free text is simplest for MVP |
| `color_variants` | CharField(255), blank | comma-separated for MVP (e.g. "Grey, Beige, Maroon"); can normalize into its own table in Future phase |
| `stock_status` | CharField, choices=["in_stock","out_of_stock"], default="in_stock" | |
| `warranty_info` | CharField(255), blank | e.g. "5 Year Warranty on Frame" |
| `delivery_info` | CharField(255), blank | e.g. "Free Delivery & Installation within city" |
| `is_featured` | BooleanField, default=False | shown on homepage |
| `is_active` | BooleanField, default=True | soft-hide from public site |
| `created_at` | DateTimeField, auto_now_add | |
| `updated_at` | DateTimeField, auto_now | |

## 4. ItemImage

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | |
| `item` | ForeignKey(Item, on_delete=CASCADE, related_name="images") | |
| `image` | ImageField | required |
| `alt_text` | CharField(150), blank | for accessibility/SEO |
| `is_primary` | BooleanField, default=False | used as the card thumbnail on listing pages |
| `display_order` | PositiveIntegerField, default=0 | controls gallery order |

> One `Item` has **many** `ItemImage` (1:N). Enforce in admin/view logic that exactly one image per item is marked `is_primary`.

## 5. ShopInfo (Singleton)

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | expect only one row; enforce via admin UX or a `singleton` pattern |
| `store_name` | CharField(150) | |
| `address` | TextField | |
| `map_embed_url` | URLField | Google Maps embed link |
| `phone_number` | CharField(20) | |
| `whatsapp_number` | CharField(20) | |
| `email` | EmailField, blank | |
| `opening_hours` | TextField or JSONField | per-day hours; JSONField recommended if using PostgreSQL |
| `about_text` | TextField, blank | content for About page |
| `updated_at` | DateTimeField, auto_now | |

## 6. ContactMessage

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | |
| `name` | CharField(100) | |
| `phone_or_email` | CharField(150) | single contact field for MVP simplicity |
| `message` | TextField | |
| `submitted_at` | DateTimeField, auto_now_add | |
| `is_read` | BooleanField, default=False | admin triage flag |

## 7. Relationships (ERD in Text)

```
Category (1) ──< (N) Item
Item     (1) ──< (N) ItemImage
ShopInfo  — standalone singleton, no FK relationships
ContactMessage — standalone, no FK relationships (not linked to Item/Category)
User (Django auth) — used only for admin login, not linked to any customer-facing table
```

## 8. Indexing Notes

- Add a database index on `Item.category_id` (Django adds this automatically for ForeignKey).
- Add a unique index on `Category.slug` and `Item.slug` (via `unique=True`).
- Consider a composite index on `(category_id, is_active)` if category listing queries grow slow with catalog size — not needed at MVP scale.

## 9. Database Choice

PostgreSQL is recommended for production (see justification in `TechStack.md`); SQLite is acceptable for local development only.
