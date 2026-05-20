# Syfo Design System — OpenSpec

> **Audience:** AI coding agents implementing features against the Syfo design system. Read this end-to-end before writing code; it is the single source of truth for tokens, components, layouts, internationalization, and deployment.
>
> **Status:** v1.0 — derived from Claude Design bundle `c8kEtt5Cb2wIDlvYqM6vVQ` (English desktop+mobile) + `6c4vFeWZygedfhEU-Bak-w` (mobile refinements) + the Chinese localization patch (CJK typography + 77-string UI translation) applied 2026-05-20.

---

## 1. What Syfo Is

Syfo is the interactive prototype of a Slock-style collaborative workspace — humans + AI agents in shared channels, DMs, tasks, files, audit log, and a "Computers" view that surfaces the daemon/runtime topology. The prototype demonstrates **both desktop and mobile shells** in a single page, and ships in **two language variants** (`en/` and `zh/`).

Implementation tech:
- React 18 + Babel standalone, all JSX served as `text/babel` scripts and transpiled in-browser.
- CSS custom properties for tokens (`syfo/colors_and_type.css`) + component CSS in `syfo/app.css`.
- No build step — every file is plain text, deployable behind any static file server (Caddy is reference).

This is **NOT production code**. Treat it as a fixture that fully and precisely describes the visual + interaction system. When implementing for a real codebase, recreate the look pixel-perfectly in whatever stack the target requires; do not lift the prototype's in-browser-Babel approach into production.

---

## 2. Repository Layout

```
syfo-design/
├── README.md                  # public-facing overview
├── OPENSPEC.md                # ← this file: canonical spec for coding agents
├── LICENSE                    # MIT
├── prototype/                 # deployable mock site (mirror of syfo.secondlife.today)
│   ├── en/                    # English root (Inter-first typography, lang="en")
│   │   ├── index.html         # entry; identical to Syfo Prototype.html
│   │   ├── Syfo Prototype.html
│   │   ├── syfo/              # design system assets + components
│   │   └── uploads/           # screenshots + reference imagery
│   └── zh/                    # Chinese root (CJK-first typography, lang="zh-Hans")
│       └── …                  # same shape; CSS + JSX strings localized
├── source/                    # untouched Claude Design bundle (chats + originals)
│   ├── README.md              # the "coding agents: read this first" file
│   ├── chats/                 # design conversation transcripts
│   └── project/               # original Syfo Mock files
└── docs/                      # extended notes (each topic deep-linked from below)
    ├── 01-design-tokens.md
    ├── 02-components.md
    ├── 03-layouts.md
    ├── 04-i18n-cjk.md
    ├── 05-voice-tone.md
    └── 06-deployment.md
```

Mental model: `prototype/` is the **runnable artifact**. `source/` is the **authored reference**. `docs/` is the **deep dive per topic**. This `OPENSPEC.md` is the **index + contract**.

---

## 3. Design Tokens (canonical)

All tokens live in `prototype/<lang>/syfo/colors_and_type.css` as CSS custom properties on `:root`. When implementing in non-CSS stacks (Tailwind, design-token JSON, Swift, etc.) reuse the names so they remain semantically traceable.

### 3.1 Color — surfaces

| Token            | Value     | Use                                          |
|------------------|-----------|----------------------------------------------|
| `--bg-paper`     | `#F7F3EA` | App background; warm off-white "paper"       |
| `--bg-surface`   | `#FCFAF4` | Cards, panels, composer                      |
| `--bg-sunken`    | `#EFEADE` | Sidebar, hover wells, code blocks            |
| `--bg-sunken-2`  | `#E8E2D2` | Nested sunken surfaces                       |

### 3.2 Color — foreground

| Token           | Value     | Use                          |
|-----------------|-----------|------------------------------|
| `--fg-1`        | `#1A1612` | Primary text (graphite)      |
| `--fg-2`        | `#65605A` | Secondary text               |
| `--fg-3`        | `#9A938A` | Tertiary / placeholder       |
| `--fg-inverse`  | `#FCFAF4` | On dark / on accent          |

### 3.3 Color — borders

| Token             | Value     | Use                                       |
|-------------------|-----------|-------------------------------------------|
| `--border-1`      | `#E4DECF` | Default divider                           |
| `--border-2`      | `#D4CCB8` | Stronger divider, input border            |
| `--border-strong` | `#1A1612` | Rare; focus/selection outlines            |

### 3.4 Color — accent (burnt sienna / printer's ink)

| Token             | Value     | Use                                       |
|-------------------|-----------|-------------------------------------------|
| `--accent`        | `#D4501E` | Primary action                            |
| `--accent-hover`  | `#B8421A` |                                           |
| `--accent-press`  | `#9A3814` |                                           |
| `--accent-soft`   | `#F4DCC8` | Selected row, accent chip fill            |
| `--accent-strong` | `#9A3814` | Dark variant for contrast                 |

### 3.5 Color — status

| Token            | Value     | Pair token       |
|------------------|-----------|------------------|
| `--success`      | `#7A7A4D` | `--success-soft` `#EFEDDE` |
| `--warning`      | `#B86E32` | `--warning-soft` `#F1E2CE` |
| `--danger`       | `#A8392A` | `--danger-soft`  `#F0D8D3` |
| `--info`         | `#7A746A` | `--info-soft`    `#EBE6DC` |

### 3.6 Typography — families

| Token         | Stack (English-first)                                                         |
|---------------|-------------------------------------------------------------------------------|
| `--font-sans` | `'Inter', 'Noto Sans SC', 'Source Han Sans SC', system-ui, -apple-system, 'Segoe UI', sans-serif` |
| `--font-serif`| `'Noto Serif SC', 'Source Han Serif SC', Georgia, 'Times New Roman', serif`   |
| `--font-mono` | `'IBM Plex Mono', 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace`|

**In the `zh/` variant** the sans stack is reordered CJK-first; see §6 i18n.

### 3.7 Typography — scale (modular ratio 1.125, baseline 16)

| Role        | Size  | Line-height (en) | Line-height (zh) |
|-------------|-------|------------------|------------------|
| display     | 40px  | 48px             | 52px             |
| h1          | 28px  | 36px             | 40px             |
| h2          | 18px  | 26px             | 28px             |
| h3          | 15px  | 22px             | 24px             |
| body        | 14px  | 22px             | 24px             |
| small       | 13px  | 20px             | 22px             |
| label (mono)| 11px  | 16px             | 18px             |
| mono-sm     | 12px  | 18px             | 18px             |

Reusable classes wrapping these: `.syfo-display`, `.syfo-h1`, `.syfo-h2`, `.syfo-h3`, `.syfo-body`, `.syfo-small`, `.syfo-label`, `.syfo-mono`, `.syfo-link`.

### 3.8 Weights / Tracking

| Token             | Value   |
|-------------------|---------|
| `--weight-regular` | 400    |
| `--weight-medium`  | 500    |
| `--weight-semibold`| 600    |
| `--weight-bold`    | 700    |
| `--track-tight`    | -0.01em (en) / 0 (zh) |
| `--track-normal`   | 0      |
| `--track-label`    | 0.04em (en) / 0.05em (zh) |
| `--track-mono`     | 0      |

### 3.9 Spacing (4px base)

`--space-1` 4px · `--space-2` 8 · `--space-3` 12 · `--space-4` 16 · `--space-5` 20 · `--space-6` 24 · `--space-7` 32 · `--space-8` 40 · `--space-9` 56 · `--space-10` 80.

### 3.10 Radii

`--radius-xs` 4 · `--radius-sm` 6 · `--radius-md` 8 · `--radius-lg` 12 · `--radius-xl` 16.

Pills (chips, toggle buttons) use literal `border-radius: 999px`.

### 3.11 Shadows

| Token       | Definition                                                  |
|-------------|-------------------------------------------------------------|
| `--shadow-1`| `0 1px 0 rgba(17,19,26,0.04), 0 1px 2px rgba(17,19,26,0.04)`|
| `--shadow-2`| `0 4px 12px rgba(17,19,26,0.06), 0 1px 2px rgba(17,19,26,0.04)`|
| `--shadow-3`| `0 16px 40px rgba(17,19,26,0.10), 0 2px 6px rgba(17,19,26,0.06)`|

### 3.12 Focus ring

```
--focus-ring: 0 0 0 2px var(--bg-paper), 0 0 0 4px var(--accent);
```
Apply via `.syfo-focusable:focus-visible`.

### 3.13 Layout constants

| Token            | Value   | Use                              |
|------------------|---------|----------------------------------|
| `--rail-w`       | 56px    | Left vertical rail width         |
| `--sidebar-w`    | 280px   | Channels/DMs sidebar width       |
| `--topbar-h`     | 56px    | View topbar height               |
| `--content-max`  | 980px   | Reading-column max-width         |

### 3.14 Motion

| Token        | Value                          |
|--------------|--------------------------------|
| `--ease-out` | `cubic-bezier(0.2, 0.7, 0.3, 1)` |
| `--dur-fast` | 120ms                          |
| `--dur-base` | 160ms                          |
| `--dur-slow` | 240ms                          |

Apply to any `transition: <property> var(--dur-fast) var(--ease-out)`.

---

## 4. Component Inventory

All components live in `prototype/en/syfo/*.jsx`. Translations live in `prototype/zh/syfo/*.jsx`. Components are plain function components; props are positional via destructuring. **No TypeScript** — props are documented inline below.

### 4.1 Atoms (`Atoms.jsx`)

| Component       | Props                                                                                                 | Notes                                                                |
|-----------------|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| `Icon`          | `name`, `size = 16`, `stroke = 1.5`, `color`, `style`, `className`                                    | Lucide-style SVG icon lookup by name. Renders `<svg>` with currentColor stroke. |
| `Avatar`        | `name = '?'`, `kind = 'human' \| 'agent'`, `size = 'sm' \| 'md' \| 'lg'`, `presence`                  | Initials avatar with deterministic tint (hash of seed). Optional presence dot overlay. |
| `Chip`          | `tone = 'neutral' \| 'accent' \| 'info' \| 'success' \| 'warning' \| 'danger'`, `children`, `leading` | Inline pill for status / label.                                      |
| `Button`        | `variant = 'primary' \| 'secondary' \| 'ghost'`, `size`, `leading`, `trailing`, `children`, `onClick`, `title`, `icon` | If `icon` is truthy, render icon-only button with `title` tooltip.   |
| `PresenceDot`   | `presence = 'online' \| 'busy' \| 'offline' \| 'thinking'`                                            | Small status indicator next to avatars / member rows.                |

Helper: `tintFor(seed)` returns a deterministic HSL pair for avatar backgrounds.

### 4.2 Shell (`Shell.jsx`)

| Component | Props | Notes |
|-----------|-------|-------|
| `Rail`    | `view`, `onView(viewId)` | Left vertical rail; renders icon buttons for: home, members, activity, settings, computers. The `view` of `'computers'` highlights the runtime stack item. |
| `Sidebar` | `view`, `activeChannel`, `activeDM`, `onChannel(id)`, `onDM(id)`, `onTopView(view)`, `onOpenWsSwitch()`, `onOpenSearch()` | 280px-wide left panel. Contains: workspace header (clickable for `WorkspaceSwitcher`), search input (opens `SearchOverlay`), channels list, DMs list. |

### 4.3 ChannelView (`ChannelView.jsx`)

Top-level view shown when `view ∈ { 'home', 'dm' }`. Props: `channelId`.

Internal panes:

| Pane              | Selector                  | What it shows                                                  |
|-------------------|---------------------------|----------------------------------------------------------------|
| `ChannelTopbar`   | always                    | Channel name + member count + tab strip                        |
| `ChatPane`        | tab = `'chat'` (default)  | `Message` list + `DayDivider("Today")` + `ThinkingIndicator` + `Composer` |
| `TasksPane`       | tab = `'tasks'`           | `TaskCard` grid grouped by status                              |
| `FilesPane`       | tab = `'files'`           | File table                                                     |
| `AuditPane`       | tab = `'audit'`           | Activity feed                                                  |

Subcomponents: `Message({ m })`, `DayDivider({ label })`, `ThinkingIndicator({ agent })`, `ThinkingDots()`, `Composer()`, `TaskCard({ task })`.

**Composer** has placeholder text: `"Message #${channel} · @ to mention an agent · / for commands"` (en) / `"在 #${channel} 发送消息 · @ 提及 AI · / 使用命令"` (zh).

### 4.4 MembersView (`MembersView.jsx`)

| Component        | Props                                       | Notes                                                                                          |
|------------------|---------------------------------------------|------------------------------------------------------------------------------------------------|
| `MembersView`    | (none)                                      | Splits left into `MemberRow` list, right into `AgentProfile` or `HumanProfileBody`.            |
| `MemberRow`      | `member`, `active`, `onClick`               | Avatar + name + handle + presence; highlighted when active.                                    |
| `AgentProfile`   | `member`                                    | Header: avatar+name + Message/Pause/Restart icon buttons. Tabs: Agent DMs / Profile / Workspace / Permissions / Reminders / Activity. Default tab is Activity. |
| `HumanProfileBody` | `member`                                  | Display name / Handle / Role / Email fields.                                                   |
| `AgentStateLog`  | (none)                                      | Renders `StateLogRow` items for state transitions.                                             |
| `Field`          | `label`, `value`                            | Read-only labeled field.                                                                       |
| `Row`            | `k`, `v`                                    | Key-value row used in computer/agent meta panels.                                              |
| `KVStack`        | `label`, `children`                         | Vertical stacked label + chip cluster (Runtime / Model / Reasoning).                           |
| `EmptyState`     | `title`, `body`, `icon = 'inbox'`           | Padded centered placeholder.                                                                   |

### 4.5 ActivitySettings (`ActivitySettings.jsx`)

Two top-level views in one file.

`ActivityView` — full notifications feed (`NotificationCard` × N) + activity log (`ActivityList`).

`SettingsView` — left rail of section labels (Account / Workspace / Members / Permissions / Runtimes / Audit log / Billing); right is the selected section body. Subviews: `AccountSettings`, `WorkspaceSettings`, `MembersSettings`, `RuntimesSettings`, `AuditSettings`. Each is presentational only.

Helpers: `ConnectedAccountRow({ label, status })`, `Toggle({ defaultOn })`, `ActivityTag({ kind })`.

### 4.6 ComputersView (`ComputersView.jsx`)

| Component          | Props                                     | Notes                                                          |
|--------------------|-------------------------------------------|----------------------------------------------------------------|
| `ComputersView`    | (none)                                    | Left: list of `ComputerListItem`. Right: `ComputerDetail`.     |
| `ComputerListItem` | `computer`, `active`, `onClick`           | Name + presence + agent count.                                 |
| `ComputerDetail`   | `computer`                                | Daemon meta + agents on this computer.                         |

### 4.7 Overlays (`Overlays.jsx`)

| Component           | Props                          | Notes                                                                                |
|---------------------|--------------------------------|--------------------------------------------------------------------------------------|
| `SearchOverlay`     | `onClose`                      | Cmd-K invokes this. Fuzzy-ish match across channels/DMs/members/tasks.               |
| `SearchResultRow`   | `r`, `query`, `highlight`      | Single row in the search result list with highlighted query span.                    |
| `WorkspaceSwitcher` | `onClose`                      | Workspace dropdown rendered with backdrop `.syfo-scrim`.                             |

### 4.8 Mobile (`Mobile.jsx`)

Mobile is a parallel implementation of the same product surface inside the iOS frame (390×800 pill device shell). The desktop and mobile views are toggled by the floating mode pill `.syfo-mode-toggle` at the top-right.

Key components (props omitted for brevity — match Sections 4.3-4.7 semantics):

`MobileApp`, `MobileHeader`, `MobileHome`, `MobileTabBtn`, `SidebarSection`, `MobileTasks`, `MobileTaskList`, `MobileTaskBoard`, `MobileTaskCard`, `MobileMembers`, `MobileMember`, `MobileChannel`, `MobileNotifications`, `MobileActivity`, `MobileSettings`, `MobileServerSettings`, `MobileSettingsGroup`, `MobileSettingsRow`, `MobileSettingsDetail`, `MobileComputer`, `MobileKV`, `MobileFilterChip`, `MobileMemberRow`.

Stateful navigation uses a `stack` of view IDs + `setStack`; "back" pops one.

### 4.9 iOS frame helpers (`ios-frame.jsx`)

Used inside `MobileStage` to render the iPhone chrome:

| Helper          | Use                                                       |
|-----------------|-----------------------------------------------------------|
| `IOSStatusBar`  | Top status bar (9:41, signal/battery icons)               |
| `IOSGlassPill`  | Frosted-glass capsule for compact controls                |
| `IOSNavBar`     | Title bar with optional trailing icon                     |
| `IOSList`       | Grouped list container with header                        |
| `IOSListRow`    | Single list row with optional icon/chevron                |

### 4.10 Data (`data.jsx`)

Seed data only — **not a component**. Defines:

- `WORKSPACE` (name, slug, description)
- `HUMANS` array (3 entries)
- `AGENTS` array (11 entries with runtime + model + reasoning metadata)
- `MEMBERS = [...HUMANS, ...AGENTS]`
- `CHANNELS` array (9 entries: hash/lock glyphs + unread counts)
- `DMS = AGENTS.slice(0, 8)`
- `MESSAGES` (chat fixtures for #GoFindBird)
- `TASKS` (8 task fixtures with status, channel, assignee)
- `ACTIVITY` (audit feed)
- `memberById(id)` lookup helper

When implementing in a real product, replace with API-driven state; **the field names above are the contract** that components consume.

---

## 5. Layouts & Page Templates

### 5.1 Desktop shell

```
┌──────┬──────────────────┬───────────────────────────────┐
│ Rail │     Sidebar      │           Content view        │
│ 56   │      280         │                               │
│      │                  │  (ChannelView / MembersView / │
│      │                  │   ActivityView / SettingsView │
│      │                  │   / ComputersView)            │
│      │                  │                               │
└──────┴──────────────────┴───────────────────────────────┘
```

Wrapper class: `.syfo-app`. Layout grid uses `--rail-w`, `--sidebar-w`. Topbar inside content is `--topbar-h`.

### 5.2 Mobile shell

iPhone frame: 390×800. Inside `.syfo-iphone-content` the `MobileApp` is rendered with a bottom tab bar (4 tabs: Home / Activity / Members / Settings) and a `stack`-based modal sub-navigation.

### 5.3 Overlays

- `SearchOverlay`: full-viewport scrim + centered search panel. Triggered by `⌘K` / `Ctrl+K`. Dismissed by `Esc`.
- `WorkspaceSwitcher`: backdrop `.syfo-scrim` + anchored dropdown. Dismissed by `Esc` or outside-click.

### 5.4 Top-right floating controls

Stacked from right to left at `top: 14px`:
1. **Mode toggle** `.syfo-mode-toggle` — `[Desktop | Mobile]` segmented control. `right: 16px`. Rendered inside React `App`.
2. **Language toggle** `.syfo-lang-toggle` — `[中文 | EN]` segmented control. Rendered OUTSIDE `#root` (so it's never re-rendered by React). Positioned via JS at runtime so it sits to the left of the mode toggle with an 8px gap, regardless of mode-toggle width or font load timing.

The language toggle is wired by an inline `<script>` that measures `.syfo-mode-toggle.getBoundingClientRect()` on `DOMContentLoaded`, `+50/250/1000ms`, `document.fonts.ready`, and `window.resize`. The two pills share `.syfo-mode-toggle` button styling so heights match exactly.

### 5.5 Keyboard shortcuts

| Key            | Action                       |
|----------------|------------------------------|
| `⌘K` / `Ctrl+K`| Toggle SearchOverlay         |
| `Esc`          | Close any open overlay       |

Implemented in `App` via `useEffect` + `keydown` listener.

---

## 6. Internationalization

### 6.1 Variants

The prototype ships two parallel directories under `prototype/`:
- `en/` — Inter-first sans, `lang="en"`, English UI strings.
- `zh/` — PingFang/Noto Sans SC-first, `lang="zh-Hans"`, Chinese UI strings.

Both share identical HTML scaffold, identical component file names, and identical data fixtures. Only typography tokens and string literals differ.

### 6.2 CJK typography rules (zh variant)

| Rule                         | en value                                                     | zh value                                                                                                                                  |
|------------------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `--font-sans` (first match)  | `Inter`                                                      | `'PingFang SC', 'Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', 'Heiti SC', 'Inter'` (Mac/iOS→PingFang, Win→YaHei, Linux→Noto)   |
| `--font-serif` (first match) | `Noto Serif SC`                                              | `'Songti SC', 'Source Han Serif SC', 'Noto Serif SC'`                                                                                     |
| Line-heights                 | tight (1.4-1.5)                                              | +10% (body 22→24, h1 36→40, display 48→52, small 20→22, label 16→18) — CJK needs more breathing room                                      |
| `--track-tight`              | `-0.01em` (negative tracking on display/h1)                  | `0` (CJK does not tolerate negative tracking)                                                                                             |
| `font-feature-settings`      | `"kern" 1`                                                   | `"palt" 1, "kern" 1` (proportional CJK punctuation + Latin kerning)                                                                       |
| `text-spacing`               | not set                                                      | `auto` (modern CSS spec; pads CJK ↔ Latin/numerals)                                                                                       |
| Font smoothing               | `-webkit-font-smoothing: antialiased`                         | same                                                                                                                                      |

These overrides live in the appended block of `prototype/zh/syfo/colors_and_type.css`, gated by `:lang(zh)`, `:lang(zh-Hans)`, `html[lang^="zh"]`.

### 6.3 Translation strategy

The prototype hardcodes UI strings in JSX (no i18n framework). The zh-variant is produced by string substitution against an enumerated EN→ZH map (see `prototype/zh/syfo/*.jsx` for the result; see `docs/04-i18n-cjk.md` for the canonical map).

**Coding-agent rule:** when adding new UI copy, write the EN string in the EN variant first, then add the ZH counterpart to `prototype/zh/...` in the matching file at the matching line. Do not introduce a single string that has no ZH counterpart.

Workspace/agent/channel content data (in `data.jsx`) is intentionally bilingual already; do not auto-translate it.

### 6.4 Language toggle UX

`[中文 | EN]` pill, mirrored from the mode toggle. The active button has `class="is-active"` and is `disabled` (no-op click); the other navigates via `window.location.href`. This is intentional — the toggle is a router, not a runtime locale switch.

---

## 7. Voice & Tone (writing rules)

### 7.1 Microcopy

- **Brief, declarative.** "Mark read", "Open task", "Define roles". No "Click here", no exclamation marks unless quoting a user.
- **No jargon without context.** "Runtime" appears on the Settings rail; the first place a user encounters it is on a Computers row, where it is contextualized by an icon and a model chip.
- **Person-first** when referring to humans, **role-first** when referring to agents. E.g., `@tonyren` vs `Lisa@codex — Key developer for TheHot`.
- **No emoji in production microcopy.** Emoji are reserved for reactions and explicit fixture content.

### 7.2 Empty states

`<EmptyState title body />` — `title` is 3-6 words, action-oriented or status. `body` is 1-2 sentences explaining what the area is and what populates it.

### 7.3 Activity verbs

`deployed`, `merged`, `restarted`, `opened`, `completed`, `approved`. In ZH: `部署了`, `合并了`, `重启了`, `创建了`, `完成了`, `通过了`.

### 7.4 Tone in Chinese

- 简洁、平和、信息导向。避免感叹号 (除非引用)、第二人称命令式 ("点击此处"❌)。
- 标点统一: 句号 `。`、逗号 `，`、冒号 `：` 用全角；URL/代码段内保留半角。
- 中英混排时, CSS `text-spacing: auto` 已处理视觉间距, 不要手动插半角空格。

---

## 8. Accessibility

| Element                        | ARIA                                                                |
|--------------------------------|---------------------------------------------------------------------|
| `.syfo-mode-toggle`            | `role="tablist"`, buttons `role="tab"` + `aria-selected`            |
| `.syfo-lang-toggle`            | `role="tablist"`, buttons `role="tab"` + `aria-selected`            |
| Search input                   | `aria-label="Search workspace"` (zh: `搜索工作区`)                  |
| Overlay scrim                  | clickable; focus traps managed by overlay component                 |
| Icon-only buttons              | `title=…` (tooltip) + visually-hidden `aria-label` mirror           |

Focus styling: `.syfo-focusable:focus-visible` → `--focus-ring`. Always layer focus rings via box-shadow (not outline) so they respect the pill `border-radius`.

Color contrast: every `--fg-*` on `--bg-paper` ≥ 4.5:1 (verified). `--accent` on `--bg-paper` passes AA for body text.

---

## 9. Deployment

### 9.1 Hosting reference

`syfo.secondlife.today` is served by Caddy on HK box `129.226.144.118` from `/srv/syfo/`. Zh variant lives at `/srv/syfo/zh/`. Caddy site block:

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

The `.jsx` MIME override is **required** — strict browsers will block `<script type="text/babel" src="*.jsx">` if the file is served as `application/octet-stream`. Babel itself only cares about the response body, but Chrome's CSP/MIME-checking layer will refuse to hand it off.

### 9.2 Local development

```bash
cd prototype/en
python3 -m http.server 8080
# open http://localhost:8080/
```

Or any static server. No build step. Hot reload via browser refresh.

### 9.3 Adding a new prototype variant

1. Copy `prototype/en/` → `prototype/<lang>/`.
2. Update `<html lang="…">`, `<title>`.
3. Append a `:lang(...)` block to `colors_and_type.css` with font + line-height overrides.
4. Update JSX strings against the translation map (see `docs/04-i18n-cjk.md` for the EN→ZH example).
5. Update the language toggle in both variants to include the new option.
6. Add `<lang>/` to Caddy if subdomain split is needed (path-based works without config).

### 9.4 Cache strategy

Files served with default Caddy `etag`/`last-modified`. No fingerprinting yet. Future production deploy SHOULD add content hashes to file names — see `docs/06-deployment.md` (note: future).

---

## 10. Extension Guide

### 10.1 Adding a component

1. Place the function component in the topical file (`Atoms.jsx` for primitives, `Shell.jsx` for chrome, etc.) or create a new file under `prototype/<lang>/syfo/`.
2. If creating a new file, add a `<script type="text/babel" src="syfo/NewFile.jsx">` to BOTH `Syfo Prototype.html` AND `index.html` for BOTH languages.
3. Style with existing tokens. Avoid hardcoded hex/rem values — use `var(--…)`.
4. If the component takes user content, ensure it works under both EN and ZH typography (test in `prototype/zh/`).
5. Add an entry under §4 in this spec.

### 10.2 Adding a page / view

1. Implement the view component (it should accept the same `view` callback pattern: nothing required beyond rendering JSX).
2. Add a `Rail` entry in `Shell.jsx` (icon + `onView('newview')`).
3. Branch on `view === 'newview'` in `DesktopApp`'s body switch.
4. Add a mobile counterpart in `Mobile.jsx` if needed.
5. Add §5 layout notes here if the view introduces a new shell pattern.

### 10.3 Adding a design token

1. Add the variable to `:root` in `colors_and_type.css`.
2. Document under §3 here.
3. If it's a typography token, add a semantic class (`.syfo-…`) at the bottom of the file.
4. Update both EN and ZH variants; ensure no zh-only divergence unless intentional (line-heights are the only legitimate fork).

### 10.4 Refreshing the design from Claude Design

When the user provides a new Claude Design URL:
1. `curl -L -o /tmp/new.zip "<URL>"` and `tar -xzf` it.
2. `diff -rq <old> <new>` to identify changed files.
3. `rsync --checksum` only the changed files into `prototype/en/` (and patch the localization mirror in `prototype/zh/` if those files moved).
4. Re-run any custom patches (language toggle inline HTML/CSS/JS, ZH typography overrides) by replaying `tools/patch-lang-toggle.py` and `tools/patch-zh-typography.py` (see `tools/`).
5. Update §1 with the new Claude Design hash.
6. Commit + push.

(The `tools/` scripts referenced above are the canonical patch sequence and live alongside `OPENSPEC.md`. Refer to them as the **executable spec**; this Markdown is the **narrative spec**.)

---

## 11. What This Spec Does NOT Cover

Out of scope for v1.0:

- Real-time data plumbing (websocket / SSE for messages, presence, task status).
- Persistence layer (where MESSAGES / TASKS / ACTIVITY actually live in prod).
- Identity / auth (no login flow specified; the prototype assumes you are `@tonyren` as set in `data.jsx`).
- The actual Slock / Syfo backend protocol (separate spec).
- Production build pipeline (Vite/Next/etc.) — current prototype is intentionally build-less.

When implementing the real product, the design system above is the visual and interaction contract. The data shape in `data.jsx` is the **prop-level** contract; replace storage and transport freely.

---

## 12. Versioning

- This spec follows semver. v1.x = same core layout + tokens; v2.x will indicate intentional breaking visual/token changes.
- Every change to tokens or component APIs MUST update §3 / §4 here in the same commit.
- The hashes of source Claude Design bundles are recorded in commit messages (e.g. `claude-design: refresh from 6c4vFeWZygedfhEU-Bak-w`).

---

## 13. Contacts / Ownership

| Area                       | Owner                                                                  |
|----------------------------|------------------------------------------------------------------------|
| Design direction           | @tonyren                                                               |
| Implementation maintenance | (assigned coding agents per task)                                      |
| This spec                  | @Alein (`@Alein@opus` in the Slock workspace) — keep this current.     |

If you (the coding agent reading this) find this spec out of date relative to the code, **trust the code in `prototype/en/`** and file an issue / PR to update §3-§5 of this document. The code is the runtime; this spec is the contract.
