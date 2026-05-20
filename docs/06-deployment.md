# 06 · Deployment

Expands §9 of `OPENSPEC.md`.

## Reference deployment

| URL                                          | Path                                       |
|----------------------------------------------|--------------------------------------------|
| https://syfo.secondlife.today/                | `/srv/syfo/` on HK box `129.226.144.118`   |
| https://syfo.secondlife.today/zh/             | `/srv/syfo/zh/` on the same box            |

Server: Caddy with automatic Let's Encrypt issuance + HTTP→HTTPS redirect.

## Caddy configuration

```caddy
syfo.secondlife.today {
    encode gzip zstd

    root * /srv/syfo
    file_server

    @jsx path *.jsx
    header @jsx Content-Type "text/javascript; charset=utf-8"

    header {
        X-Content-Type-Options nosniff
        X-Frame-Options SAMEORIGIN
        Referrer-Policy strict-origin-when-cross-origin
    }
}
```

Lives at `/etc/caddy/Caddyfile.d/97-syfo.caddyfile`. Reload with `systemctl reload caddy` after edits.

### Why the `.jsx` MIME header is required

`.jsx` is not a recognized MIME extension. Without the explicit `Content-Type: text/javascript`, Caddy sends `application/octet-stream` or `text/plain`. Strict browsers (Chrome with strict-MIME on) will then refuse to execute the script even though Babel doesn't care about the MIME for its own parsing.

The header maps **only `.jsx` files**, not all responses, so it doesn't interfere with HTML/CSS/PNG MIME detection.

## DNS

`syfo.secondlife.today` is an A-record (or CNAME) pointing to `129.226.144.118`. The TLS cert auto-issues on first request via Let's Encrypt ACME-HTTP-01.

## Refreshing the prototype on the server

```bash
# from the design repo, after pulling latest:
rsync -avz --checksum prototype/en/  root@129.226.144.118:/srv/syfo/
rsync -avz --checksum prototype/zh/  root@129.226.144.118:/srv/syfo/zh/

# the deploy box keeps a copy of index.html as the spaced original too
ssh root@129.226.144.118 'cp "/srv/syfo/Syfo Prototype.html" /srv/syfo/index.html'
ssh root@129.226.144.118 'cp "/srv/syfo/zh/Syfo Prototype.html" /srv/syfo/zh/index.html'

# Caddy serves static files atomically — no reload needed for content changes.
```

When the Caddyfile itself changes (new subdomain, new route, header tweak):

```bash
ssh root@129.226.144.118 'caddy validate --config /etc/caddy/Caddyfile && systemctl reload caddy'
```

## Local development

```bash
# English
cd prototype/en && python3 -m http.server 8080

# Chinese
cd prototype/zh && python3 -m http.server 8081
```

Or any static server. No build step. Browser refresh picks up changes.

## Adding a new language variant

1. `cp -r prototype/en prototype/<lang>`.
2. Edit `<html lang="…">`, `<title>`.
3. Append `:lang(<lang>)` rules in `colors_and_type.css` for fonts + line-heights.
4. Translate JSX strings.
5. Update both language toggles (EN + ZH currently; add the new option).
6. Deploy under `/srv/syfo/<lang>/` — Caddy serves automatically (no config change for path-based variants).

## Cache strategy

- Caddy sends default `ETag` + `Last-Modified` for static files.
- No content fingerprinting yet; the file path is the cache key.
- **Production path**: when porting to a CDN, add `Cache-Control: public, max-age=31536000, immutable` for hashed assets and `Cache-Control: no-cache` for `index.html`.

## Custom domain alternative

To switch from path-based (`/zh/`) to subdomain (`syfo-zh.secondlife.today`):

1. Add `syfo-zh.secondlife.today` A-record.
2. Duplicate the Caddyfile block with `root * /srv/syfo/zh`.
3. Reload Caddy.

Path-based is preferred for now because it preserves shared link sharing (`/zh/path` ↔ `/path` are obvious siblings).

## Cloudflare / CDN

None currently — direct origin. If introducing CDN:
- Bypass cache for `*.html` (small files, frequent updates).
- Cache `*.jsx`, `*.css`, `*.svg`, `*.png` at edge with long TTL.
- Strip the inline `<script>` lang-positioner from CDN-cached HTML only if it doesn't depend on the same hostname.

## Health checks

The site has no `/healthz` route. To probe liveness from a monitor:

```bash
curl -sI https://syfo.secondlife.today/ | head -1
# expect: HTTP/2 200
```

## Backup / disaster recovery

The repo IS the deployment artifact. To restore from scratch:

1. Spin up a server with Caddy.
2. Clone `syfo-design`.
3. `rsync prototype/en/ → /srv/syfo/` and `prototype/zh/ → /srv/syfo/zh/`.
4. Copy `97-syfo.caddyfile` from `docs/06-deployment.md` (this file) into `/etc/caddy/Caddyfile.d/`.
5. `systemctl restart caddy`.

Zero state to migrate; the prototype is fully static.
