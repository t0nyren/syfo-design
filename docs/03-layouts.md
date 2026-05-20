# 03 · Layouts — deep reference

Expands §5 of `OPENSPEC.md`.

## Desktop shell

The desktop layout is a three-column grid with two fixed columns (Rail, Sidebar) and one flexible content column.

```
.syfo-app {
  display: grid;
  grid-template-columns: var(--rail-w) var(--sidebar-w) 1fr;
  height: 100vh;
}
```

The Rail is decoration-heavy with icons; the Sidebar is text-heavy with channel/DM names; the content column holds the active view. The view itself controls its own internal layout (e.g., ChannelView is also a sub-grid for chat + composer).

## Mobile shell

```
.syfo-mobile-stage > .syfo-iphone > .syfo-iphone-content > MobileApp
```

The "stage" is a centered display area on top of `--bg-sunken` with a subtle accent halo. The "iphone" is a 390×800 frame with notch + home indicator. The MobileApp inside is responsible for its own header + tab bar.

## Topbars

Desktop view topbars are `--topbar-h` tall (56px). They contain title + subtitle + secondary actions on the right. Tab strips, when present, sit immediately below the topbar in the view body.

## Reading max-width

The accent semantic class `.syfo-content` constrains content to `--content-max` (980px) and centers it. Use this for prose-heavy views (Settings sections, Audit log) but NOT for chat (chat wants the full available width).

## Overlays

```
.syfo-scrim {
  position: fixed;
  inset: 0;
  background: rgba(17, 19, 26, 0.30);
  z-index: 40;
}
```

The mode-toggle and lang-toggle live at z-index 50, ABOVE the scrim so they remain accessible during overlay states.

## Sticky positioning

The composer in ChatPane is sticky to the bottom of the chat scroll container, not the viewport. This keeps it inside the chat area when the sidebar is scrolled separately.

## Responsive notes

Current prototype is **desktop-only at 1440 viewport**. Mobile is a SECOND product surface (in the iPhone frame), not a responsive collapse of desktop. When building responsively:

1. Decide at what breakpoint to switch from desktop → mobile shell entirely (suggest 768px).
2. Below that breakpoint, render `MobileApp` outside the iPhone frame (full bleed).
3. Above that breakpoint, render the desktop grid.

Do **not** try to make a single layout fluidly span the entire range; the design system is intentionally two-shelled.

## Z-index ladder

| Layer                   | z-index | Examples                              |
|-------------------------|---------|---------------------------------------|
| Content                 | 0-10    | Default                               |
| Sticky chrome           | 20      | Composer, channel topbar              |
| Scrim                   | 40      | Overlay backdrops                     |
| Overlay panel           | 45      | SearchOverlay, WorkspaceSwitcher      |
| Floating controls       | 50      | `.syfo-mode-toggle`, `.syfo-lang-toggle` |

Don't introduce ad-hoc z-indices above 50 without amending this table.

## Keyboard navigation map

- Sidebar: arrow keys move focus through channels and DMs; Enter activates.
- Channel composer: Enter sends, Shift-Enter inserts newline.
- Search overlay: arrow keys move through results; Enter navigates; Esc dismisses.
- Workspace switcher: arrow keys + Enter; Esc dismisses.
