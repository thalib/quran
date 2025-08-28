---
description: "Hugo template coding standards for fastdep ecommerce site"
applyTo: "**/*.html,**/*.css,**/*.js"
---

# Hugo Template Coding Standards

These standards define maintainable, performant, and SEO-optimized Hugo templates for the ecommerce site. They are concise, Hugo-native, and focused on speed, accessibility, and conversion.

## Formatting & Structure

- Use **2-space indentation**.
- Use **semantic HTML5 landmarks** (`<main>`, `<section>`, `<article>`, `<nav>`, `<header>`, `<footer>`).
- Organize layouts by type: **base, section, page, taxonomy, term, partials**.
- Keep reusable code in:

  - `layouts/_partials/` → UI components
  - `layouts/_shortcodes/` → reusable content blocks

- Each partial must include a **header comment** with params and example usage, for commenting use as below.
  ```
  {{/*
  Partial:
  Purpose:
  Params:
  Usage:
  Dependencies:
  Rules:
  Exception:
  */}}
  ```
- to return value from partial use `return [VALUE]`
- 
- Follow **DRY principles**: refactor repeated UI into partials/shortcodes.
- Use **Bootstrap 5.3 utilities** only for layout/spacing; keep core design **tokenized** via CSS variables.

## Hugo Idioms

- Prefer `.Site`, `.Page`, `.Params`, `.Resources`; avoid legacy Go template syntax.
- Use **Page Bundles** so product content and images live together.
- Use Hugo’s pipelines:

  - `.Resources.GetMatch` + `.Resize`/`.Fit`/`.Format` for responsive images
  - `resources.Get` + `resources.Minify` + `resources.Fingerprint` for CSS/JS (cache-busting)

- Document all **custom partials and shortcodes** with comments.

## Design System & UI

- **Mobile-first layout**: base styles for small screens; add `min-width` breakpoints.
- **Responsive typography**: use `clamp()` + CSS variables.
- **Component-driven**: document UI states (default, hover, focus, active, disabled, loading, error).
- **Light theme only** with WCAG AA/AAA contrast.

- **Component class and inline-style policy**: Use ONLY Bootstrap 5.3 utilities and existing classes from `assets/css/main.css` for all styling. Custom classes and inline styles are strictly prohibited. This enforces consistency, maintainability, and prevents style bloat.

  - ✅ **Allowed**: Bootstrap 5.3 utilities (`d-flex`, `text-center`, `btn`, `container-fluid`, etc.)
  - ✅ **Allowed**: Existing classes already defined in `assets/css/main.css`
  - ❌ **Prohibited**: Creating new custom classes in templates or partials
  - ❌ **Prohibited**: Any inline styles (`style=""` attributes)
  - ❌ **Prohibited**: Adding new CSS classes anywhere except `assets/css/main.css` (and only when explicitly instructed by user)

- **Aspect ratios and advanced styling**: For complex styling needs (aspect ratios, transforms, animations), use existing CSS classes from `assets/css/main.css` or request user to add new utilities there. Bootstrap's aspect ratio utilities (`ratio`, `ratio-1x1`, `ratio-16x9`) should be preferred when available.

## Anti-patterns / Don'ts

- **CSS Policy**: Follow the strict component class and inline-style policy outlined above.
- NEVER create or modify files under `static`. The `static` directory contains generated or published artifacts and must be treated as an output/deployment area, not a source location for development.
- Create source JavaScript files only under `assets/js` (use `.js` files there). Do not add or edit JS files in `static`.
- Create source CSS files only under `assets/css` (use `.css` files there). Do not add or edit CSS files in `static`.
- Use Hugo Pipes (for example `resources.Get`, `resources.Minify`, `resources.Fingerprint`) to process assets from `assets` and reference the processed, fingerprinted outputs in templates.
- When in doubt, prefer adding assets under `assets` or in page bundles inside `content/` instead of modifying `static`.
- Don't rely on JavaScript to render essential content or navigation. Ensure core content and navigation work without JS.
- Don't include large, render-blocking third-party scripts synchronously on the page (analytics, tag managers, A/B tools). Load them async/defer or via Consent Manager.
- Don't ship unoptimized images. Avoid full-size images in markup; prefer Hugo image processing (`.Resize`, `.Fit`, `.Format`) and provide srcset/sizes and next-gen formats.
- Don't duplicate business logic in templates. Keep templates declarative; move complex logic to shortcodes, partials, or data files.
- Don't hardcode environment secrets, API keys, or credentials in templates or content files.
- Don't use <table> for layout or non-tabular content.
- Don't create accessibility regressions: avoid missing alt attributes, non-focusable interactive elements, or removing keyboard access.
- Don't rely on non-standard browser features without feature detection/fallbacks (e.g., avoid experimental APIs without graceful degradation).
- Don't bloat pages with multiple large CSS frameworks — stick to Bootstrap utilities and minimal, scoped CSS.

## Performance & Loading UX

- Targets: Lighthouse scores ≥ 90; LCP < 2.5s, CLS < 0.1.
- Minimize render-blocking: Defer/async nonessential JS
- Fonts: preload key fonts, `font-display: swap`, prefer system/variable fonts.
- Optimize assets with Hugo Pipes; serve fingerprinted files via CDN.
- Use `loading="eager"` for above-the-fold images and visuals. DO NOT use lazy loading for above-the-fold content.
- Use native `loading="lazy"` for images and iframes in below-the-fold content. Treat lazy loading as an opt-in, not a default—apply it only where it improves performance without harming UX.
- For images, always set explicit `width` and `height` attributes to prevent layout shifts. If not specified, ask the user.
- Ask user whether an image is above or below the fold for clarification when determining loading strategy.

Hugo Pipes example (build, minify, fingerprint CSS)

```html
{{/* in layouts/_partials/head.html */}} {{ $styles := resources.Get
"css/main.css" | resources.Minify | resources.Fingerprint }}
<link
  rel="stylesheet"
  href="{{ $styles.Permalink }}"
  integrity="{{ $styles.Data.Integrity }}"
/>
```

## Images & Media

- Generate **multiple sizes & next-gen formats (WebP/AVIF)** with Hugo image processing.
- Use `layouts/_partials/gen/webpConverter.html` for WebP conversion with fallbacks.
- Provide `srcset`/`sizes` for product and content images.
- to get product image use `layouts/_partials/gen/productImage.html`
- Use **LQIP/dominant color placeholders** for perceived speed.
- Enforce **image size budgets**; serve from CDN with caching headers.

```html
{{ $mainImg := "path/to/image.png" }} {{ $mainAlt := .Title }} {{ $mainWebp :=
partial "gen/webpConverter" (dict "CallerName" "product/image.html" "ImageSrc"
$mainImg "WebpParam" "1024x1024 webp q85") }} {{ $mainJpg := partial
"gen/webpConverter" (dict "CallerName" "product/image.html" "ImageSrc" $mainImg
"WebpParam" "1024x1024 jpg q85") }}

<div class="mb-3 rounded-3">
  <picture>
    <source srcset="{{ $mainWebp }}" type="image/webp" />
    <source srcset="{{ $mainJpg }}" type="image/jpeg" />
    <img
      id="mainProductImage"
      src="{{ $mainJpg }}"
      alt="{{ $mainAlt }}"
      width="1024"
      height="1024"
      class="img-fluid rounded shadow-sm"
      loading="lazy"
      aria-label="Product main image"
      tabindex="0"
      data-magnify-src="{{ $mainJpg }}"
    />
  </picture>
</div>
```

## Accessibility

- Semantic HTML, `alt` attributes, ARIA roles where needed.
- Ensure **keyboard navigation**, visible focus outlines, skip-to-content links.
- Respect `prefers-reduced-motion`.
- Document ARIA patterns for custom widgets (modals, menus, carousels).

## Progressive Enhancement

- Core navigation & content must work **without JavaScript**.
- Add interactivity unobtrusively.
- PWA (optional): document service worker + offline fallbacks, avoid stale data.

## SEO & Social

- Add **JSON-LD structured data** (Product, Offer, BreadcrumbList, AggregateRating).
- Always emit Schema.org LD+JSON as a flat, templated JSON-LD block in your templates — never build the object with Hugo dict/slice/map helpers and jsonify (or similar) to serialize structured data.
- Ensure **canonical tags, Open Graph, Twitter Card metadata**.
- Server-render product price, availability, trust signals in markup.
