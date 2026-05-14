# Cloudflare Pages Deployment

Four separate CF Pages projects. Each corresponds to one domain.

## Packages ready for upload

| Package | Size | Files | Target domain |
|---------|------|-------|---------------|
| `bsidesfrankfurt-main.zip` | 57 MB | 187 | `bsidesfrankfurt.org` (main redesigned site) |
| `bsidesfrankfurt-2025.zip` | 313 MB | 276 | `2025.bsidesfrankfurt.org` |
| `bsidesfrankfurt-2024.zip` | 42 MB | 68 | `2024.bsidesfrankfurt.org` |
| `bsidesfrankfurt-2023.zip` | 51 MB | 75 | `2023.bsidesfrankfurt.org` |

All include `CNAME` and `_headers` files so CF Pages applies security headers automatically.

## Upload each package

For each zip:

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → Workers & Pages → **Create** → **Pages** → **Upload assets**
2. Project name: `bsidesfrankfurt-main` (or `-2023`, `-2024`, `-2025`)
3. Drag the corresponding `.zip`
4. Click **Deploy** — you'll get a `*.pages.dev` preview URL
5. Under the project's **Custom domains** tab, add the real domain (`bsidesfrankfurt.org`, `2025.bsidesfrankfurt.org`, etc.)

## DNS setup (Cloudflare-managed)

In your Cloudflare DNS zone for `bsidesfrankfurt.org`:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | `@` (root) | `bsidesfrankfurt-main.pages.dev` | Proxied |
| CNAME | `2025` | `bsidesfrankfurt-2025.pages.dev` | Proxied |
| CNAME | `2024` | `bsidesfrankfurt-2024.pages.dev` | Proxied |
| CNAME | `2023` | `bsidesfrankfurt-2023.pages.dev` | Proxied |

Cloudflare Pages handles HTTPS certificates automatically (~1 minute per domain).

## Notes

- **Oversized file removed from 2025**: `Versus Killnet - Frankfurt.pptx` (34 MB) exceeded the CF Pages 25 MB-per-file limit. It's saved at `/Users/chris/Code/test-project/OVERSIZED-removed-from-2025.pptx`. If you want it back on the 2025 archive, host it externally (GitHub release, S3, Google Drive) and update the link in `2025/workshop/workshop.html`.
- **Archive cross-links rewritten**: the original 2023/2024/2025 folders referenced each other via `../2024/index.html` etc. These have been rewritten to absolute subdomain URLs (`https://2024.bsidesfrankfurt.org`) so the archive dropdown works on subdomains.
- **Security headers** applied via `_headers` in each package (CSP on main, standard baseline on archives).
- **No per-subdomain dev-server preview** — archive previews are `*.pages.dev` directly. Once DNS is pointed, the subdomains serve the archive sites.
