# Reference Notes

This portfolio was designed from first principles after reviewing three established open-source portfolio approaches. No source code, copy, artwork, or distinctive layout was copied.

## 1. `bchiang7/v4`

Useful pattern: a strong visual hierarchy, restrained color system, focused project storytelling, and a clear static-production workflow.

Applied here:

- high-contrast hero with one memorable accent
- selected work presented as outcomes rather than a repository dump
- explicit design tokens and responsive typography

Not adopted:

- Gatsby and its dependency/build footprint
- the original site's layout, artwork, text, or component code

## 2. `RyanFitzgerald/devportfolio`

Useful pattern: content that is easy to update, optional sections, and a clear separation between personal information and presentation.

Applied here:

- predictable sections for identity, projects, approach, about, and contact
- project descriptions written from repository evidence
- maintainers can edit content without learning a framework

Not adopted:

- Astro, Tailwind, or TypeScript because this repository did not need a build step

## 3. `codewithsadee/vcard-personal-portfolio`

Useful pattern: mobile-first behavior and a complete personal site implemented with plain HTML, CSS, and JavaScript.

Applied here:

- responsive layouts that collapse cleanly on narrow screens
- minimal JavaScript for progressive enhancement only
- static assets suitable for direct GitHub Pages hosting

Not adopted:

- the original vCard layout, images, icons, styling, or source code

## Resulting architecture

The final implementation uses:

- semantic HTML for durable content and SEO
- a single CSS file with theme tokens and responsive rules
- a small JavaScript file for theme persistence, header state, and the current year
- no package manager, runtime framework, external font, analytics script, or client-side API dependency
- a standard-library Python check for repeatable CI validation
