# pakentrepreneur.me

The source for Abdul Basit's personal portfolio, published from `abdulbasit742.github.io` and served through the custom domain `pakentrepreneur.me`.

## What is included

- responsive, framework-free portfolio
- semantic landmarks and keyboard-friendly navigation
- dark and light themes with saved preference
- featured project summaries grounded in each project's README
- canonical metadata, structured data, sitemap, robots file, favicon, and custom 404 page
- dependency-free repository checks in CI

## Local preview

No install step is required.

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

Do not open `index.html` directly from the filesystem because root-relative asset paths are designed for the deployed domain.

## Verification

Run the same check used in CI:

```bash
python tests/check_site.py
```

The check validates required files, important metadata, internal file references, custom-domain consistency, and common accidental secret patterns.

## Content updates

- edit page copy and project cards in `index.html`
- edit visual tokens and responsive rules in `styles.css`
- keep interaction code small and dependency-free in `script.js`
- preserve the single hostname in `CNAME`, canonical metadata, `robots.txt`, and `sitemap.xml`

## Deployment

GitHub Pages can publish this user site directly from the repository's default branch. The committed `CNAME` keeps the configured custom domain attached to the Pages build.

See [`docs/reference-notes.md`](docs/reference-notes.md) for the portfolio patterns reviewed before implementation.
