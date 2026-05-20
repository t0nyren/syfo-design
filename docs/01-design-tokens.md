# 01 · Design Tokens — deep reference

Tokens are defined in `prototype/<lang>/syfo/colors_and_type.css`. This document expands on §3 of `OPENSPEC.md`.

## Where they live

All tokens are CSS custom properties on `:root`. Components reference them with `var(--name)`. There is no JS token export yet — when porting to other tech stacks (Tailwind config, design-tokens.json, Swift assets), generate the export from the CSS file as the source of truth.

## Token categories

### Color — surfaces (warm paper palette)

The system uses a warm off-white "paper" base. Hierarchy is conveyed by tone shifts within a narrow range, not by hard color jumps.

| Token            | Hex       | OKLCH (approx.) | Use                                          |
|------------------|-----------|-----------------|----------------------------------------------|
| `--bg-paper`     | `#F7F3EA` | L 95 C 0.02 H 80 | App background                              |
| `--bg-surface`   | `#FCFAF4` | L 98 C 0.01 H 80 | Cards, panels                                |
| `--bg-sunken`    | `#EFEADE` | L 92 C 0.02 H 80 | Sidebar, hover wells, code blocks            |
| `--bg-sunken-2`  | `#E8E2D2` | L 89 C 0.03 H 80 | Nested sunken                                |

Designers may freely tint these by 1-2% L without changing tokens (use `color-mix(in oklch, var(--bg-surface), var(--accent) 4%)` patterns for context tints).

### Color — accent (burnt sienna / printer's ink)

A single accent family. Avoid introducing additional accent families without explicit design approval.

### Color — status

Status colors are intentionally low-chroma to coexist with paper. Use the `*-soft` pair for fills (chip backgrounds, banner backgrounds), and the base token for text/border/icon.

### Typography — scale

Modular scale at ratio 1.125, baseline 16px. Body baseline is 14px (one step below 16px) to keep dense product chrome readable on desktop.

CJK variants bump line-heights by ~10%; see `04-i18n-cjk.md`.

### Spacing — 4px base

All spacing variables are multiples of 4. When eyeballing a layout, snap to the nearest space token before adding a literal. Avoid `padding: 10px` etc.

### Radii

`xs` 4 / `sm` 6 / `md` 8 / `lg` 12 / `xl` 16 — and the special `999px` pill for chips and toggle buttons.

### Shadows

Three-tier elevation:
- `--shadow-1`: barely-there (chips, table rows on hover)
- `--shadow-2`: cards, popovers
- `--shadow-3`: overlays, dialogs

Avoid stacking `--shadow-3` on a surface that's already on `--shadow-2`; pick the highest.

### Motion

Two easings + three durations. Use `--dur-fast` for state-only transitions (hover/active), `--dur-base` for visual property changes (collapse/expand), `--dur-slow` rarely (entrance/exit of overlays).

## Adding a new token

1. Decide which group it belongs to (don't invent groups).
2. Use the existing naming convention (`--<group>-<role>` or `--<group>-<step>`).
3. Add to `:root` in `colors_and_type.css`.
4. Document in §3 of `OPENSPEC.md`.
5. Update both `en/` and `zh/` variants in lockstep.

## Anti-patterns

- ❌ Hardcoded hex / px values inside component CSS.
- ❌ Adding a new accent color without removing the old one.
- ❌ Forking tokens between EN and ZH (only typography line-heights and the font stacks may diverge).
- ❌ Renaming a token without grepping all references.
