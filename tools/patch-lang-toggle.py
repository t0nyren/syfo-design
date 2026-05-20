#!/usr/bin/env python3
"""Fix overlap + height mismatch in language toggle:
- Switch <a> to <button> (matches mode-toggle browser default rendering exactly)
- Use the same .syfo-mode-toggle pill class for identical height + styling
- Place ON THE SAME ROW to the LEFT of mode toggle, computed dynamically via JS to avoid width assumptions

Strategy: replace the existing standalone lang-toggle pill with one that uses
the same DOM structure / classes as mode-toggle, then position it dynamically.
"""
from pathlib import Path

# New CSS: dedicated container styled identically to mode toggle; positioned at left of it.
NEW_LANG_CSS = """
    /* Language toggle (right-side, sibling of mode toggle; matches mode-toggle pill) */
    .syfo-lang-toggle {
      position: fixed; top: 14px; right: 16px; z-index: 50;
      display: inline-flex; align-items: center; gap: 0;
      background: var(--bg-surface); border: 1px solid var(--border-2);
      border-radius: 999px; padding: 3px;
      font-family: var(--font-sans); font-size: 12px;
      line-height: 16px;
      box-shadow: var(--shadow-1);
      transform: translateX(0);
    }
    .syfo-lang-toggle button {
      border: 0; background: transparent; color: var(--fg-2);
      padding: 5px 12px; border-radius: 999px; cursor: pointer;
      font-weight: 500;
      font-family: inherit; font-size: inherit; line-height: inherit;
      display: inline-flex; align-items: center; gap: 6px;
      transition: background var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out);
    }
    .syfo-lang-toggle button.is-active { background: var(--fg-1); color: var(--fg-inverse); }
"""

# JS to position the lang toggle right next to mode toggle (avoid overlap).
LANG_POSITION_JS = """
  <script>
    // Position language toggle to the left of mode toggle (avoid overlap).
    (function () {
      function reposition() {
        var mode = document.querySelector('.syfo-mode-toggle');
        var lang = document.querySelector('.syfo-lang-toggle');
        if (!mode || !lang) return;
        var modeRect = mode.getBoundingClientRect();
        // mode pill's right edge is at viewportWidth - 16 (since right: 16px on mode).
        // Place lang pill so its right edge = mode's left edge - 8px gap.
        var vw = window.innerWidth || document.documentElement.clientWidth;
        var newRight = vw - (modeRect.left - 8);
        lang.style.right = newRight + 'px';
      }
      // Run after React mounts and on resize / font load.
      function init() {
        reposition();
        // Re-run after a short tick in case React mounted async.
        setTimeout(reposition, 50);
        setTimeout(reposition, 250);
        setTimeout(reposition, 1000);
        if (document.fonts && document.fonts.ready) document.fonts.ready.then(reposition);
      }
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
      } else {
        init();
      }
      window.addEventListener('resize', reposition);
    })();
  </script>
"""

# Inline HTML for each version. Two-button segmented control; non-active links elsewhere.
EN_TOGGLE_HTML = '''  <div class="syfo-lang-toggle" role="tablist" aria-label="Language">
    <button role="tab" aria-selected="false" onclick="window.location.href='/zh/'" title="切换到中文版">中文</button>
    <button role="tab" aria-selected="true" class="is-active" disabled>EN</button>
  </div>
'''

ZH_TOGGLE_HTML = '''  <div class="syfo-lang-toggle" role="tablist" aria-label="Language">
    <button role="tab" aria-selected="true" class="is-active" disabled>中文</button>
    <button role="tab" aria-selected="false" onclick="window.location.href='/'" title="Switch to English">EN</button>
  </div>
'''

OLD_LANG_CSS_FRAGMENT_START = "    /* Language toggle (top-right, left of mode toggle) */"
OLD_LANG_CSS_FRAGMENT_END_MARKER = "    .syfo-lang-toggle a:hover { background: var(--bg-sunken); color: var(--fg-1); }\n"

def patch_html(path: Path, new_toggle_html: str) -> None:
    txt = path.read_text(encoding="utf-8")

    # 1. Remove the old lang-toggle CSS block (between marker comment and the :hover rule)
    if OLD_LANG_CSS_FRAGMENT_START in txt and OLD_LANG_CSS_FRAGMENT_END_MARKER in txt:
        s = txt.index(OLD_LANG_CSS_FRAGMENT_START)
        e = txt.index(OLD_LANG_CSS_FRAGMENT_END_MARKER) + len(OLD_LANG_CSS_FRAGMENT_END_MARKER)
        # Strip preceding blank line too
        txt = txt[:s].rstrip() + "\n" + txt[e:].lstrip("\n")

    # 2. Remove the old lang-toggle DIV (start to its </div> close).
    if '<div class="syfo-lang-toggle"' in txt:
        s = txt.index('<div class="syfo-lang-toggle"')
        # Find its matching </div> — first one after start (no nesting in our HTML).
        end_marker = "</div>\n"
        e = txt.index(end_marker, s) + len(end_marker)
        txt = txt[:s] + txt[e:]

    # 3. Insert new CSS right before </style>
    style_close = txt.index("</style>")
    txt = txt[:style_close] + NEW_LANG_CSS + txt[style_close:]

    # 4. Insert new toggle HTML right before <div id="root">
    root_marker = '<div id="root"></div>'
    txt = txt.replace(root_marker, new_toggle_html + root_marker, 1)

    # 5. Insert positioning JS right before </body>
    if "<!-- lang-position-init -->" not in txt:
        body_close = txt.index("</body>")
        txt = txt[:body_close] + "<!-- lang-position-init -->" + LANG_POSITION_JS + txt[body_close:]

    path.write_text(txt, encoding="utf-8")
    print(f"  [ok] patched {path}")

print("=== Patching EN ===")
en_root = Path("/tmp/syfo-v2/syfo-mock/project")
patch_html(en_root / "Syfo Prototype.html", EN_TOGGLE_HTML)
# Refresh index.html
(en_root / "index.html").write_text(
    (en_root / "Syfo Prototype.html").read_text(encoding="utf-8"),
    encoding="utf-8",
)
print("  [ok] EN index.html re-synced")

print("=== Patching ZH ===")
zh_root = Path("/tmp/syfo-zh")
patch_html(zh_root / "Syfo Prototype.html", ZH_TOGGLE_HTML)
(zh_root / "index.html").write_text(
    (zh_root / "Syfo Prototype.html").read_text(encoding="utf-8"),
    encoding="utf-8",
)
print("  [ok] ZH index.html re-synced")
