# AI_Instructions.md

Instructions for the AI coding agent (e.g. Claude Code) building the Manglam Furniture website. Read this file first, then reference the other 9 documents as needed during implementation.

## 1. Document Map

| Need to know... | Read |
|---|---|
| What the product does and doesn't do | `PRD.md` |
| Full feature list (MVP vs Future) | `Features.md` |
| App structure, folder layout, request flow | `Architecture.md` |
| Models, fields, relationships | `Database.md` |
| View/URL structure (and future REST option) | `API.md` |
| Exact libraries/frameworks to use | `TechStack.md` |
| Page-by-page responsive layout specs | `UIUX.md` |
| Auth, permissions, validation, hardening | `Security.md` |
| Environment setup, hosting, deploy steps | `Deployment.md` |

## 2. Hard Rules — Do NOT Do These

- **No payment gateway, cart, checkout, or order model of any kind.** This is a catalog-only site.
- **No customer login, registration, or account system.** Customers browse anonymously — full stop.
- **No product reviews/ratings** unless explicitly requested in a future phase.
- Do not invent features not listed as MVP in `Features.md` without confirming first.
- Do not hardcode admin credentials, secret keys, or API keys anywhere in source code — use environment variables per `Deployment.md`.

## 3. Coding Conventions

- Follow standard Django project conventions: apps organized by domain (`core`, `catalog`, `shop_info`) per `Architecture.md` — do not put unrelated models/views in the same app.
- Use Django's ORM and built-in admin wherever possible instead of custom-built equivalents (e.g., don't hand-roll auth, don't hand-roll the admin panel).
- Use `ModelForm`s for any user-facing form (contact form) to get built-in validation and CSRF protection for free.
- Use slugs (not raw IDs) in customer-facing URLs, matching `Database.md` and `API.md`.
- Keep settings split by environment (`dev.py` / `production.py`) as described in `Architecture.md` — never commit `DEBUG = True` or a real `SECRET_KEY` to source control.
- Match model fields, types, and relationships exactly as specified in `Database.md` unless a deviation is clearly justified and noted.

## 4. Responsiveness Requirement — Non-Negotiable

Every page must be built and **tested at all three breakpoints** before being considered complete:

- **Mobile:** < 768px
- **Tablet:** 768px – 1024px
- **Desktop/Laptop:** > 1024px

Specific layout requirements per page (nav behavior, grid columns, image gallery behavior) are defined in `UIUX.md` — follow them precisely, especially:
- Hamburger/collapsible nav on mobile and (typically) tablet.
- Touch-friendly, swipeable image gallery on the item detail page — not just clickable arrows.
- Grid column counts must adjust per breakpoint as specified (not a fixed column count across all screen sizes).

Do not mark any page "done" without confirming it renders correctly and remains usable (no overflow, no unreadable text, no broken tap targets) at all three breakpoints.

## 5. File/Folder Boundaries

- Do not create new top-level Django apps beyond what's defined in `Architecture.md` (`core`, `catalog`, `shop_info`, optionally `accounts`/`api` if explicitly scoped later) without checking in first.
- Keep customer-facing templates under each app's own `templates/<app_name>/` directory as shown in the folder structure in `Architecture.md`.
- Static assets (CSS/JS/images) go under `static/`; user-uploaded media goes under the configured media storage backend — never mix the two.
- Do not modify `Database.md`'s defined schema without updating that document to match — the docs and the code must stay in sync.

## 6. Security Baseline

Follow `Security.md` in full, especially:
- CSRF tokens on every form.
- Admin-only access to all write operations (categories, items, images, shop info).
- Server-side validation on the contact form and image uploads.
- `DEBUG = False`, HTTPS enforced, secrets via environment variables in production.

## 7. When Unsure

- If a requirement conflicts between documents, `PRD.md` and `Features.md` take precedence for scope questions; `Database.md` takes precedence for schema questions.
- If a package/library version isn't specified, verify the latest stable version at implementation time rather than assuming one.
- If a feature isn't listed as MVP anywhere, treat it as out of scope until confirmed.
