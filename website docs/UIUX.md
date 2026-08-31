# UIUX.md

> **Responsiveness is a core requirement, not an afterthought.** Every page below must be tested and confirmed usable at all three breakpoints before being considered done.

Breakpoints used throughout:
- **Mobile:** < 768px
- **Tablet:** 768px – 1024px
- **Desktop/Laptop:** > 1024px

---

## 1. Home Page

| Breakpoint | Layout Notes |
|---|---|
| Mobile (<768px) | Hamburger menu (top-right) replaces full nav; hero banner stacks full-width; featured items shown as a horizontally-scrollable row or single-column stack; category shortcuts as 2-column tap-friendly tiles (min. 44px tap targets). |
| Tablet (768–1024px) | Nav may show a condensed horizontal menu or hamburger (either is acceptable — be consistent); featured items grid: 2–3 columns; category tiles: 3 columns. |
| Desktop (>1024px) | Full horizontal nav bar with "Shop" dropdown listing all categories on hover/click; featured items grid: 3–4 columns; category tiles: 4–6 columns. |

## 2. Shop / Category Listing Page

| Breakpoint | Layout Notes |
|---|---|
| Mobile (<768px) | Hamburger nav; item grid: **1 column** (or 2 narrow columns if item cards are compact); each card shows primary image, name, price, stock badge; filter/sort controls (if added later) collapse into a "Filter" button opening a bottom sheet or modal. |
| Tablet (768–1024px) | Item grid: **2–3 columns**; category sidebar (if present) can show as a collapsible top bar instead of a left sidebar to save width. |
| Desktop (>1024px) | Item grid: **3–4 columns**; optional persistent left sidebar for category navigation; hover states on cards (subtle elevation/zoom) acceptable since desktop has a mouse. |

## 3. Item Detail Page

| Breakpoint | Layout Notes |
|---|---|
| Mobile (<768px) | Image gallery **on top**, full-width, swipeable carousel (touch swipe required, not just arrow buttons) with dot indicators; thumbnails below main image as a horizontally scrollable strip; product info (name, price, stock badge, "Call Now"/"WhatsApp" buttons) stacks directly below gallery; description/specs (material, dimensions, warranty, delivery) in an accordion or simple stacked sections to avoid excessive scrolling. |
| Tablet (768–1024px) | Gallery and info can either stack (like mobile) or move to a **2-column layout** (gallery left ~55%, info right ~45%) — 2-column is preferred if width allows without cramping. Thumbnails as a vertical or horizontal strip next to/under main image. |
| Desktop (>1024px) | **2-column layout**: gallery (with clickable thumbnails, larger main image, zoom-on-hover optional) on the left (~50–60% width), sticky product info panel (price, stock, color/variant selector, call/WhatsApp buttons, warranty/delivery badges) on the right. Description and full specs shown below the fold in a clean tabbed or sectioned layout. |

**Image gallery behavior (all breakpoints):**
- Primary image (`is_primary=True`) loads first.
- Touch swipe on mobile/tablet; arrow buttons + thumbnail click on desktop.
- Lazy-load non-visible images to keep mobile load times low.
- Alt text (`ItemImage.alt_text`) used on every image for accessibility/SEO.

## 4. About Page

| Breakpoint | Layout Notes |
|---|---|
| Mobile (<768px) | Single-column stacked text and any imagery; hamburger nav. |
| Tablet (768–1024px) | Optional 2-column layout (text left, image right) if content supports it; otherwise single column. |
| Desktop (>1024px) | 2-column layout common: story/text on one side, store photo(s) on the other; full nav bar. |

## 5. Contact Page

| Breakpoint | Layout Notes |
|---|---|
| Mobile (<768px) | Stacked vertically: contact form → phone/WhatsApp click-to-call/chat buttons → address & opening hours → embedded map (full-width, fixed height ~250–300px so it doesn't dominate the page). Form fields full-width, large tap-friendly inputs and submit button. |
| Tablet (768–1024px) | 2-column optional: form on one side, address/hours/map on the other, if width comfortably fits both without cramped form fields. |
| Desktop (>1024px) | 2-column layout: contact form + click-to-call/WhatsApp buttons on left, embedded map + address + opening hours table on right (map height ~350–400px). |

## 6. Global Navigation Behavior

| Breakpoint | Nav Behavior |
|---|---|
| Mobile (<768px) | Hamburger icon opens a full-screen or slide-in menu; "Shop" expands as an accordion listing all categories; large tap targets (min. 44x44px per accessibility guidance). |
| Tablet (768–1024px) | Either condensed horizontal nav or hamburger — decide based on how many categories exist; prioritize no horizontal overflow/cramming. |
| Desktop (>1024px) | Full horizontal nav with a "Shop" dropdown (hover or click) listing all categories; sticky header on scroll is recommended for easy access to Home/Shop/About/Contact. |

## 7. Cross-Cutting Trust Elements

Trust badges ("5 Year Warranty," "Free Delivery & Installation") should appear:
- On the homepage (as a small badge row/strip).
- On every item detail page near the price/CTA area.
- Must remain legible and not wrap awkwardly at any breakpoint — test badge row wrapping specifically on narrow mobile widths (~360px).
