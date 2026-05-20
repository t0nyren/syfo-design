# 02 · Components — deep reference

Expands §4 of `OPENSPEC.md` with usage examples. All examples use the JSX in `prototype/en/syfo/`.

## Atoms (`Atoms.jsx`)

### `Icon`

```jsx
<Icon name="hash" size={16} stroke={1.5} />
<Icon name="message-square" size={14} color="var(--accent)" />
```

Names follow Lucide convention: `hash`, `lock`, `message-square`, `users`, `shield`, `cpu`, `inbox`, `paperclip`, `image`, `command`, `at-sign`, `info`, `log`, `monitor`, `clock`, `activity`, `list-todo`, `eye`, `eyes`, `plus`, `minus`, `check`, etc.

### `Avatar`

```jsx
<Avatar name="tonyren" kind="human" size="md" presence="online" />
<Avatar name="Lisa@codex" kind="agent" size="sm" presence="busy" />
```

`tintFor(seed)` makes the background deterministic so the same person gets the same color in every screen.

### `Chip`

```jsx
<Chip tone="accent">in progress</Chip>
<Chip tone="info" leading={<Icon name="cpu" size={11} />}>Codex CLI</Chip>
```

Tones: `neutral`, `accent`, `info`, `success`, `warning`, `danger`.

### `Button`

```jsx
<Button variant="primary" onClick={onSend}>Send</Button>
<Button variant="ghost" icon title="Mention"><Icon name="at-sign" size={14} /></Button>
<Button variant="secondary" leading={<Icon name="plus" />}>Add member</Button>
```

Variants: `primary` (accent background), `secondary` (paper surface + border), `ghost` (transparent, no border).

### `PresenceDot`

```jsx
<PresenceDot presence="online" />   // green
<PresenceDot presence="busy" />     // amber
<PresenceDot presence="thinking" /> // pulsing accent
<PresenceDot presence="offline" />  // gray
```

## Shell — `Rail`, `Sidebar`

The shell is rendered above the active content view. State flow:

```jsx
const [view, setView] = useState('home');
const [activeChannel, setActiveChannel] = useState('gofindbird');
const [activeDM, setActiveDM] = useState(null);

<Rail view={view} onView={setView} />
<Sidebar
  view={view}
  activeChannel={activeChannel}
  activeDM={activeDM}
  onChannel={(id) => { setView('home'); setActiveChannel(id); }}
  onDM={(id) => { setView('dm'); setActiveDM(id); }}
  onTopView={setView}
  onOpenWsSwitch={() => setWsOpen(true)}
  onOpenSearch={() => setSearchOpen(true)}
/>
```

## ChannelView

Renders chat + tasks + files + audit tabs for a given channel id. Composer placeholder localizes per language (see §6 of OPENSPEC).

## MembersView

Two-pane: list (left) + profile (right). Agent profile defaults to the Activity tab; human profile shows a simpler `Field` form.

## ActivitySettings

Two views combined in one file:
- `ActivityView`: notifications + activity feed.
- `SettingsView`: settings rail + section body.

## ComputersView

Surfaces daemon/runtime topology. Each computer has agents bound to it. Tap a computer → detail with Daemon version / Created / Creator + KV chips for Runtime / Model / Reasoning.

## Overlays

`SearchOverlay` — Cmd-K, fuzzy search over channels + members + tasks + DMs.
`WorkspaceSwitcher` — anchored dropdown, backdrop `.syfo-scrim`.

## Mobile

The mobile shell is a separate render tree mounted inside the iPhone frame at `.syfo-iphone-content`. All views above have a mobile counterpart prefixed `Mobile…`. Navigation uses a `stack` of view IDs with a back button popping one frame.

## Naming conventions

- Components are PascalCase function components.
- Internal subcomponents stay in the same file when only used there.
- File names match the topical area, not a single component (`Atoms.jsx`, `MembersView.jsx`, `Overlays.jsx`).

## Component vs primitive

- **Primitive**: token-only styling, no state, in `Atoms.jsx`.
- **Component**: composes primitives + state, lives in a view-specific file.
- **View**: full page surface, lives in a `*View.jsx` file.

Don't reintroduce styled-divs that duplicate Chip / Button / Avatar functionality. If a primitive doesn't fit, extend it (with explicit design approval).
