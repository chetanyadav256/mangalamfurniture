# PRD.md

## 1. Problem Statement
Manglam Furniture is a physical furniture store (sofas, beds, dining tables, chairs, wardrobes, etc.) with no current online presence. Customers cannot browse the catalog, check prices, or see product details before visiting the store or calling. The business needs a **catalog-only website** — no e-commerce transaction capability — that lets customers discover products online and then contact the store (call/WhatsApp/contact form) to inquire or visit in person.

## 2. Target Users

| Role | Description | Access |
|---|---|---|
| Admin/Owner | Store owner or staff managing the catalog | Logs into admin panel; full CRUD on items, categories, images, shop info |
| Customer | General public browsing the site | No login/account; view-only access to catalog and shop info |

## 3. Goals

- Give customers an always-available, mobile-friendly digital catalog of the store's furniture.
- Let the admin update items, prices, stock status, and images without developer help.
- Drive store visits and phone/WhatsApp inquiries — not online sales.
- Present trust signals (warranty, delivery/installation) to support in-store conversion.
- Be genuinely usable on phones, tablets, and desktops (majority of local shoppers browse on mobile).

## 4. User Stories

### Admin
- As an admin, I can log in securely to an admin panel so only I can manage the catalog.
- As an admin, I can create, edit, and delete furniture categories (e.g., Sofa, Bed).
- As an admin, I can create, edit, and delete individual furniture items within a category.
- As an admin, I can upload multiple images per item and reorder/remove them.
- As an admin, I can set an item's price, material, dimensions, color/variant options, warranty info, delivery info, and stock status (in stock / out of stock).
- As an admin, I can update shop info (address, map, phone, WhatsApp number, opening hours).
- As an admin, I can view messages submitted through the customer contact form.
- As an admin, I can mark an item as featured/active or hide it from the public site without deleting it.

### Customer
- As a customer, I can browse all furniture categories from a shop menu.
- As a customer, I can view a listing page for a category (e.g., all Sofas) with images, name, and price.
- As a customer, I can open an item's own detail page to see all images, full description, material, dimensions, color/variant options, stock status, warranty, and delivery info.
- As a customer, I can view the store's address (with embedded map), phone number, and opening hours.
- As a customer, I can call, WhatsApp, or submit a contact form to inquire — without creating an account.
- As a customer, I get a good experience whether I'm on a phone, tablet, or laptop.

## 5. Out of Scope (Explicit)

- **No payment gateway, cart, or checkout of any kind.**
- **No customer accounts, registration, or login.** All browsing is anonymous.
- **No product reviews or ratings** unless added in a later phase.
- No order management, invoicing, or inventory transactions (stock is a simple in-stock/out-of-stock flag, not quantity tracking).
- No multi-vendor or multi-store support.
- No live chat widget (contact is via phone/WhatsApp link/contact form only).

## 6. Success Criteria (MVP)

- Admin can fully manage catalog (categories, items, images, shop info) without developer intervention.
- Customer can browse every category and item detail page on mobile, tablet, and desktop without layout issues.
- Contact form submissions are reliably received/stored and viewable by admin.
- Page load and navigation feel fast on a mid-range mobile device.
