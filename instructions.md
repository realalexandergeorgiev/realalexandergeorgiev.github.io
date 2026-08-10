# BSidesFrankfurt Site - Setup & Editing Guide

This site is built with [Hugo](https://gohugo.io/), a static-site generator. Output is plain HTML/CSS - no runtime, no database, no framework. Everything is edited through Markdown and YAML files.

---

## 1. Install prerequisites

### Hugo (extended)

macOS:

```sh
brew install hugo
```

Linux (Debian/Ubuntu):

```sh
sudo snap install hugo
# or download the deb from https://github.com/gohugoio/hugo/releases
```

Windows:

```sh
choco install hugo-extended
# or scoop install hugo-extended
```

Verify:

```sh
hugo version
# expected: hugo v0.160.1+extended+withdeploy ...
```

Make sure it says **extended** - we use SCSS-like features and resource fingerprinting.

### Git

Standard Git install (`brew install git`, `apt install git`, etc.) - needed only for pulling/pushing the repo.

---

## 2. Clone and run locally

```sh
git clone git@github.com:realalexandergeorgiev/realalexandergeorgiev.github.io.git
cd realalexandergeorgiev.github.io
hugo server
```

Open [http://localhost:1313](http://localhost:1313). Hugo watches the files and live-reloads on save - keep it running while editing.

Useful flags:

| Flag | Purpose |
|------|---------|
| `hugo server -D` | Also show content marked `draft: true` |
| `hugo server --bind 0.0.0.0` | Let other devices on your LAN reach the preview (e.g. phone testing) |
| `hugo server --disableFastRender` | Full rebuild on every change (slower, but catches more bugs) |

---

## 3. Project layout

```
hugo-site/
├── hugo.toml                  # Site config (title, menus, baseURL)
├── content/                   # All editable content (Markdown)
│   ├── _index.md              # Landing page
│   └── updates/               # Updates: posts + announcements (one .md file per item)
├── data/                      # Structured data (YAML)
│   ├── event.yaml             # Dates, location, social links
│   ├── sponsors.yaml          # Sponsor tiers + logos + URLs
│   ├── speakers.yaml          # Speaker profiles
│   └── about.yaml             # "What is BSides" cards
├── layouts/                   # HTML templates
│   ├── _default/baseof.html   # Root template - everything inherits this
│   ├── index.html             # Homepage layout
│   ├── updates/               # Updates list + single templates
│   └── partials/              # Reusable components (nav, footer, sponsors…)
├── assets/css/main.css        # Centralized design system
├── static/                    # Copied as-is to site root
│   ├── images/                # All images (sponsors, gallery, logo)
│   ├── favicon-*.png          # Favicons (multi-size)
│   ├── favicon.ico            # Legacy favicon
│   └── js/site.js             # Small amount of vanilla JS (nav toggle, carousels)
└── public/                    # Generated output (ignored in git; built by `hugo`)
```

---

## 4. Writing updates (posts & announcements)

Updates are the single news stream of the site - both longer community posts and short official announcements. They appear on the landing page (latest 3) and on `/updates/`.

### Create a new update

```sh
hugo new content updates/my-post-title.md
```

Or create the file manually at `content/updates/my-post-title.md`. The slug (URL) is the filename without `.md`.

### Frontmatter template

Every update starts with a YAML block between `---` fences:

```yaml
---
title: "Your post title"
date: 2026-05-01
author: "Your name"            # optional, shown next to the date
summary: "One-sentence description. Appears on the updates index and in the homepage feed."
tags: ["cfp", "community", "workshops"]
draft: false
---

Post body in **Markdown** goes here.

## Headings work

Use normal Markdown: [links](https://example.com), **bold**, *italics*,
`inline code`, lists, blockquotes, images.

> Blockquotes are styled with a green left border.

Code blocks too:

```sh
echo "hello"
```
```

For short announcement-style items you can use a single tag instead:

```yaml
---
title: "Ticket sales extended to 15 August"
date: 2026-06-15
tag: "Tickets"
summary: "We've extended early-bird pricing by two weeks due to popular demand."
draft: false
---
```

The `tag` is the short label shown before the date on the homepage (e.g. "Tickets · 15 Jun 2026").

### Rules

- `draft: true` hides the post unless you run `hugo server -D`.
- `date` controls ordering - newest first on the updates index and homepage strip.
- `summary` is used in previews; if omitted, Hugo auto-extracts the first paragraph.
- `tags` (list) or a single `tag` render as pill badges on the single-post page.
- Images: drop them in `static/images/blog/` and reference as `/images/blog/my-image.png`.
- Old `/blog/...` and `/announcements/...` URLs redirect to `/updates/...` via `aliases:` in the frontmatter of the moved posts.

---

## 5. Editing speakers

Speakers live in **one YAML file**: `data/speakers.yaml`.

### Add a speaker

```yaml
- name: "Dr. Example Person"
  photo: "/images/speakers/example-person.jpg"   # optional - leave "" for auto-initials
  role: "Principal Researcher, ACME Corp"
  bio: "Short bio, 1–2 sentences. Shown truncated to 3 lines on cards."
  linkedin: "https://www.linkedin.com/in/example/"
  talk: "Title of their talk"
```

### Notes

- `photo` - put the image in `static/images/speakers/` and reference as `/images/speakers/filename.jpg`. Square images (e.g. 400×400) work best; they're displayed in a 120px circle.
- If `photo` is empty (`""`), the card shows a gradient circle with the speaker's initials - useful for placeholders before photos arrive.
- `linkedin` is optional; the "LinkedIn" button disappears if empty.
- Order in the YAML file = order in the carousel.

---

## 6. Editing sponsors

Sponsors live in `data/sponsors.yaml` with three tiers: **gold**, **silver**, **partners**.

### Add a sponsor

```yaml
gold:
  - name: "Acme Security"
    logo: "/images/sponsors/acme-logo.svg"
    url: "https://acmesecurity.example/"

silver:
  - name: "…"
    logo: "…"
    url: "…"

partners:
  - name: "BSidesSomewhere"
    logo: "/images/sponsors/bsides-somewhere.png"
    url: "https://bsidessomewhere.example/"
```

### Notes

- Logo files go in `static/images/sponsors/`.
- **Prefer SVG** (scales perfectly, tiny file size). PNG with transparent background also works.
- Logos are automatically greyscale-dimmed and colored on hover - don't pre-stylise them.
- Tier order on the page: **Gold → Silver → Partners**.

---

## 7. Editing event info (dates, location, social)

`data/event.yaml` controls the event-wide details:

```yaml
name: BSidesFrankfurt
year: 2026
dates:
  conference: 2026-09-10
  workshops: 2026-09-11
  display: "10–11 September 2026"     # Human-friendly version shown in hero
location:
  name: Goethe University Frankfurt
  address: "Theodor-W.-Adorno-Platz 1, 60323 Frankfurt am Main"
  mapUrl: "https://www.uni-frankfurt.de/..."
social:
  twitter: "https://x.com/BSidesFRA"
  instagram: "https://instagram.com/BSidesFRA"
  mastodon: "https://infosec.exchange/@bsidesfra"
  linkedin: "https://www.linkedin.com/company/bsides-frankfurt/"
  email: "info@bsidesfrankfurt.org"
```

Editing this file updates every page.

---

## 8. Editing the navigation menu

`hugo.toml` under the `[menu]` block:

```toml
[[menu.main]]
  name = "Schedule"
  url = "/schedule/"
  weight = 20     # Lower = further left
```

Nested items (like the Archive dropdown) use `identifier` + `parent`:

```toml
[[menu.main]]
  name = "Archive"
  identifier = "archive"
  weight = 80

[[menu.main]]
  parent = "archive"
  name = "2024"
  url = "https://2024.bsidesfrankfurt.org"
```

The `menu.cta` block is a separate list used for the orange "Tickets" / "CFP" buttons on the right.

---

## 9. Editing styles

All design tokens (colors, fonts, spacing, shadows) are in `assets/css/main.css` at the top:

```css
:root {
  --color-primary: #9acd32;
  --color-secondary: #eb3812;
  --font-heading: 'Poppins', sans-serif;
  --font-body: 'Open Sans', sans-serif;
  ...
}
```

Change a token, every component updates. Don't edit individual component colors - change the token.

---

## 10. Building for production

```sh
hugo
```

Output goes to `public/`. That's what you'd deploy (but for GitHub Pages, the workflow below builds it automatically).

To preview the production build locally:

```sh
hugo && cd public && python3 -m http.server 8000
# open http://localhost:8000
```

---

## 11. Deployment (GitHub Pages)

The site auto-deploys on push to `main` via GitHub Actions. The workflow is at `.github/workflows/hugo.yml` (add if missing - see the Hugo docs for [GitHub Pages setup](https://gohugo.io/hosting-and-deployment/hosting-on-github/)).

**Quick setup:**

1. In repo **Settings → Pages**, set **Source** to *GitHub Actions*.
2. Push to `main` - the action builds with `hugo --minify` and publishes `public/`.

**Custom domain (`bsidesfrankfurt.org`):**

- Add a `CNAME` file in `static/` with `bsidesfrankfurt.org` as its only line. Hugo copies this to the site root.
- Configure DNS to point at GitHub Pages (A records to `185.199.108–111.153` or CNAME to `<user>.github.io`).

**Subdomain strategy for past years (`2024.bsidesfrankfurt.org`, etc.)** - each year gets its own repo on GitHub Pages with its own `CNAME`. Not covered by this Hugo site; see the old repo's `/2024/` folder for the archive you're splitting off.

---

## 12. Common tasks - quick reference

| Task | File(s) to edit |
|------|-----------------|
| Add an update (post or announcement) | `content/updates/new-post.md` |
| Add/edit a speaker | `data/speakers.yaml` |
| Add/edit a sponsor | `data/sponsors.yaml` + logo in `static/images/sponsors/` |
| Update event dates/venue | `data/event.yaml` |
| Change nav links | `hugo.toml` `[menu]` block |
| Change color palette | `assets/css/main.css` top (`:root` block) |
| Replace favicon | files in `static/` starting with `favicon-` |
| Change hero copy | `layouts/index.html` |

---

## 13. Troubleshooting

**Hugo says `No matching layout found`.**
Check that the frontmatter `layout:` field (if set) matches a file in `layouts/`. Hugo's lookup rules: [https://gohugo.io/templates/lookup-order/](https://gohugo.io/templates/lookup-order/).

**Favicon not showing in Chrome.**
Chrome caches favicons aggressively. Try an incognito window first to verify. If it works there, your tab is just cached - close all tabs for the site and reopen.

**Image not loading.**
Paths starting with `/` are relative to `static/`. Don't use `static/` in the URL itself - `static/images/foo.png` on disk is `/images/foo.png` in HTML.

**Changes not appearing locally.**
Hugo's watcher occasionally misses deep file changes. Stop (`Ctrl+C`) and restart `hugo server`. The `--disableFastRender` flag helps if edits don't reflect fully.

**`hugo version` shows non-extended.**
Reinstall with the extended variant (`brew install hugo` installs extended by default on macOS; on other platforms the binary name may be `hugo_extended`).

---

## 14. Where to get help

- Hugo docs: [https://gohugo.io/documentation/](https://gohugo.io/documentation/)
- Markdown reference: [https://commonmark.org/help/](https://commonmark.org/help/)
- This repo's issues: GitHub issues tab
- Team contact: `info@bsidesfrankfurt.org`
