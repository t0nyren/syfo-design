// Syfo UI Kit — shared atoms (icons, avatars, chips, buttons)
// Loaded as text/babel; exposes atoms on `window` for other JSX files.

const ICONS = {
  // Lucide-derived; 1.5 stroke; 24 viewBox
  'message-square': 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z',
  'list-todo': 'M3 5h18 M3 12h12 M3 19h18 M19 12l2 2 4-4',
  'users': 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2 M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M22 21v-2a4 4 0 0 0-3-3.87 M16 3.13a4 4 0 0 1 0 7.75',
  'activity': 'M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.5.5 0 0 1-.95 0L9.24 2.18a.5.5 0 0 0-.95 0L5.93 10.54A2 2 0 0 1 4 12H2',
  'monitor': 'M12 17v4 M8 21h8 M2 17V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z',
  'settings': 'M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z',
  'search': 'm21 21-4.34-4.34 M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14z',
  'plus': 'M5 12h14 M12 5v14',
  'minus': 'M5 12h14',
  'more-horizontal': 'M12 12h.01 M19 12h.01 M5 12h.01',
  'hash': 'M4 9h16 M4 15h16 M10 3 8 21 M16 3l-2 18',
  'lock': 'M19 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2z M7 11V7a5 5 0 0 1 10 0v4',
  'paperclip': 'm21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 17.93 8.8l-8.58 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48',
  'image': 'M3 3h18v18H3z M9 9a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21',
  'send': 'm22 2-7 20-4-9-9-4z M22 2 11 13',
  'at-sign': 'M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0z M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-3.92 7.94',
  'command': 'M18 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3H6a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3h12a3 3 0 0 0 3-3 3 3 0 0 0-3-3z',
  'check': 'M20 6 9 17l-5-5',
  'clock': 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M12 6v6l4 2',
  'alert-triangle': 'm21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z M12 9v4 M12 17h.01',
  'info': 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M12 16v-4 M12 8h.01',
  'x': 'M18 6 6 18 M6 6l12 12',
  'chevron-down': 'm6 9 6 6 6-6',
  'chevron-right': 'm9 18 6-6-6-6',
  'chevron-left': 'm15 18-6-6 6-6',
  'arrow-left': 'm12 19-7-7 7-7 M19 12H5',
  'pencil': 'M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z M15 5l4 4',
  'terminal': 'm7 11 2-2-2-2 M11 13h4 M3 3h18v18H3z',
  'cpu': 'M16 8H8v8h8z M19 4h-2v2 M19 18v2h-2 M4 18v2h2 M4 4h2v2 M22 9v2h-2 M22 13v2h-2 M2 9v2h2 M2 13v2h2 M9 22h2v-2 M13 22h2v-2 M9 2v2h2 M13 2v2h2',
  'git-branch': 'M18 21a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M6 21a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M6 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M6 9v3a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V9',
  'play': 'm6 4 12 8-12 8z',
  'circle': 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z',
  'eye': 'M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z',
  'inbox': 'M22 12h-6l-2 3h-4l-2-3H2 M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z',
  'sliders': 'M4 21V14 M4 10V3 M12 21v-9 M12 8V3 M20 21v-5 M20 12V3 M1 14h6 M9 8h6 M17 16h6',
  'log': 'M9 12h6 M9 16h6 M9 8h6 M4 6V4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2',
  'shield': 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',
};

function Icon({ name, size = 16, stroke = 1.5, color, style, className }) {
  const d = ICONS[name];
  if (!d) return null;
  const paths = d.split(' M').map((p, i) => (i === 0 ? p : 'M' + p));
  return (
    <svg
      width={size} height={size} viewBox="0 0 24 24" fill="none"
      stroke={color || 'currentColor'} strokeWidth={stroke}
      strokeLinecap="round" strokeLinejoin="round"
      style={style} className={className}
      aria-hidden="true"
    >
      {paths.map((p, i) => <path key={i} d={p} />)}
    </svg>
  );
}

// ---------- Avatar ----------
// Deterministic background tint for human avatars (cool neutrals — against warm sienna accent and warm paper bg, humans read as quiet and the accent reads bold).
const HUMAN_TINTS = ['#DDE2EA', '#D8DEE6', '#E2E0E6', '#DBE3E6', '#E0DEE5'];
function tintFor(seed = '') {
  let h = 0;
  for (const ch of seed) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return HUMAN_TINTS[h % HUMAN_TINTS.length];
}

function Avatar({ name = '?', kind = 'human', size = 'md', presence }) {
  const initials = name
    .replace(/@.*/, '')
    .split(/[\s-_]/).filter(Boolean).slice(0, 2)
    .map(p => p[0]).join('').toUpperCase() || '?';
  const cls = ['avatar'];
  if (kind === 'agent') cls.push('is-agent');
  if (size === 'sm') cls.push('sm');
  if (size === 'lg') cls.push('lg');
  if (size === 'xl') cls.push('xl');
  const style = kind === 'human' ? { background: tintFor(name) } : undefined;
  const presenceColor = {
    online: 'var(--success)',
    busy: 'var(--warning)',
    offline: 'var(--fg-3)',
    thinking: 'var(--accent)'
  }[presence];
  return (
    <span className={cls.join(' ')} style={style}>
      {initials}
      {presence ? <span className="presence" style={{ background: presenceColor }} /> : null}
    </span>
  );
}

// ---------- Chip ----------
function Chip({ tone = 'neutral', children, leading }) {
  const cls = ['chip'];
  if (tone !== 'neutral') cls.push('chip-' + tone);
  return (
    <span className={cls.join(' ')}>
      {leading}
      {children}
    </span>
  );
}

// ---------- Button ----------
function Button({ variant = 'secondary', size, leading, trailing, children, onClick, title, icon }) {
  const cls = ['btn', 'btn-' + variant];
  if (size === 'sm') cls.push('btn-sm');
  if (icon) cls.push('btn-icon');
  return (
    <button className={cls.join(' ')} onClick={onClick} title={title} type="button">
      {leading}
      {children}
      {trailing}
    </button>
  );
}

// ---------- Status dot helper ----------
function PresenceDot({ presence }) {
  const color = {
    online: 'var(--success)',
    busy: 'var(--warning)',
    offline: 'var(--fg-3)',
    thinking: 'var(--accent)'
  }[presence] || 'var(--fg-3)';
  return <span className="dot" style={{ background: color }} />;
}

// ---------- Export to window ----------
Object.assign(window, { Icon, Avatar, Chip, Button, PresenceDot });
