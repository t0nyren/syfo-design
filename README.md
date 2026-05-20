# syfo-design

Syfo — interactive prototype + design system for a Slock-style collaborative workspace where humans and AI agents share channels, DMs, tasks, files, audit log, and a "Computers" runtime topology view.

This repository contains:

- 🧱 **The Syfo design system** — tokens, components, layouts, voice, accessibility, deployment.
- 🖼 **The mock website** — an interactive prototype rendering the design across **desktop + iPhone** shells and **two languages** (English / 中文 with CJK-tuned typography).
- 📘 **OpenSpec** — `OPENSPEC.md`, the canonical reference for coding agents who need to extend or reimplement the design system.

## Live deployment

| Variant     | URL                                          |
|-------------|----------------------------------------------|
| English     | https://syfo.secondlife.today/               |
| 中文         | https://syfo.secondlife.today/zh/            |

Both versions ship the desktop and mobile shells in the same page; use the top-right `[Desktop \| Mobile]` toggle to switch. Use the adjacent `[中文 \| EN]` toggle to switch languages.

## Repo layout

```
syfo-design/
├── README.md                  # this file
├── OPENSPEC.md                # ★ canonical design-system spec (start here)
├── LICENSE                    # MIT
├── prototype/                 # the deployable mock site
│   ├── en/                    # English variant (Inter-first)
│   └── zh/                    # Chinese variant (PingFang-first, CJK typography)
├── source/                    # untouched Claude Design bundle (chats + originals)
└── docs/                      # extended notes per topic
```

## Quick start

```bash
# 1. Serve the English prototype locally
cd prototype/en && python3 -m http.server 8080
# open http://localhost:8080/

# 2. Or the Chinese one
cd prototype/zh && python3 -m http.server 8081
```

No build step. The prototype uses React 18 + Babel standalone in-browser. Production reimplementations should compile JSX and pre-build, but the design system itself (tokens + CSS) is framework-agnostic.

## For AI coding agents

**Read `OPENSPEC.md` end-to-end before writing code.** It defines:

- Every design token (colors, typography, spacing, shadows, radii, motion).
- Every component (props, behavior, accessibility roles).
- Layout patterns for both desktop and mobile shells.
- Internationalization rules — especially the CJK typography deltas for the Chinese variant.
- Voice and tone guidelines.
- The deployment + Caddy config that the prototype lives behind.
- Extension guide for adding components, views, tokens, or new language variants.

When in doubt, **trust the code in `prototype/en/`** as the runtime contract, and the OpenSpec as the narrative contract.

## License

MIT — see [LICENSE](./LICENSE).
