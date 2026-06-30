# Syfo Tutorial — 《Syfo 使用教程》

A complete, screenshot-driven Syfo onboarding guide in **Chinese and English**, covering
every feature across 14 chapters, built from real operations in a live org (mini-pinecorn).
Output as a static website **and** a print-ready PDF, styled with the Syfo design system
(warm paper + burnt sienna).

Deployed (hidden page) via the official pipeline at **syfo.ai/guide** (EN: `/guide/en`). Source mirror: syfo-guide.secondlife.today.

## Layout
- Deployable copy lives under `site/guide/` (served at syfo.ai/guide). This `src/` builds it:
  - `index.html` (中文), `en/index.html` (English), with an EN ↔ 中文 toggle
  - `assets/tokens.css`, `shots/`, `en/shots/`
  - `Syfo-使用教程.pdf`, `Syfo-Tutorial-EN.pdf`
- `src/` — sources to regenerate everything:
  - `build.py` → `site/` (中文 web) + `site/print.html`; chapters are inline Chinese content
  - `build_en.py` → `site-en/` (English web) + print; English chapters
  - `_base.css` / `_web.css` / `_print.css` / `_print_en.css` — shared styling
  - `shots/` (中文 UI screenshots), `shots-en/` (English UI + Google-Translated content)
  - `tooling/` — Playwright capture scripts used to (re)take the screenshots

## Build
```
cd src
python3 build.py        # -> site/index.html, site/print.html  (中文)
python3 build_en.py     # -> site-en/index.html, site-en/print.html  (English)
weasyprint site/print.html    Syfo-使用教程.pdf
weasyprint site-en/print.html Syfo-Tutorial-EN.pdf
```

## Notes
- Screenshots are real. The English set was captured with the Syfo UI switched to English;
  residual in-app Chinese (real third-party messages) was rendered to English via Google Translate.
- In-text emphasis in `build.py` uses full-width 「」 quotes to avoid clashing with Python string delimiters.
- The hands-on chapter was run live: a demo channel + a Syfo Cloud agent + a real task/deliverable.
