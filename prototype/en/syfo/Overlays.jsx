// Syfo UI Kit — Search overlay + Workspace switcher dropdown

// ---------- Search overlay ----------
function SearchOverlay({ onClose }) {
  const [query, setQuery] = React.useState('ab');
  const [sort, setSort] = React.useState('relevant');
  return (
    <div className="syfo-search-overlay" role="dialog" aria-modal="true">
      <div className="syfo-search-overlay-bar">
        <div className="syfo-search-input">
          <Icon name="search" size={16} style={{ color: 'var(--fg-2)' }} />
          <input
            autoFocus
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search messages, files, tasks…"
            style={{
              flex: 1, border: 0, background: 'transparent', outline: 'none',
              fontFamily: 'var(--font-sans)', fontSize: 15, color: 'var(--fg-1)',
            }}
          />
          <button className="btn btn-ghost btn-icon" title="Clear" onClick={onClose} style={{ width: 28, height: 28 }}>
            <Icon name="x" size={14} />
          </button>
          <span style={{
            fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--fg-3)',
            border: '1px solid var(--border-2)', borderRadius: 4, padding: '2px 6px',
          }}>ESC</span>
        </div>
      </div>
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '12px 24px 8px', maxWidth: 1080, margin: '0 auto', width: '100%',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Button variant="secondary" size="sm" leading={<Icon name="message-square" size={12} />}>My messages</Button>
          <Button variant="secondary" size="sm" leading={<Icon name="hash" size={12} />} trailing={<Icon name="chevron-down" size={12} />}>Channel</Button>
          <Button variant="secondary" size="sm" leading={<Icon name="clock" size={12} />} trailing={<Icon name="chevron-down" size={12} />}>Any time</Button>
        </div>
        <div style={{ display: 'inline-flex', border: '1px solid var(--border-2)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
          {['relevant','recent'].map(k => (
            <button
              key={k}
              onClick={() => setSort(k)}
              className="btn btn-sm"
              style={{
                borderRadius: 0, border: 0,
                background: sort === k ? 'var(--bg-sunken)' : 'transparent',
                color: sort === k ? 'var(--fg-1)' : 'var(--fg-2)',
                fontWeight: sort === k ? 500 : 400,
                textTransform: 'capitalize',
                borderLeft: k !== 'relevant' ? '1px solid var(--border-2)' : 0,
              }}
            >{k}</button>
          ))}
        </div>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '8px 24px 40px' }}>
        <div style={{ maxWidth: 1080, margin: '0 auto' }}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            margin: '12px 0',
          }}>
            <span style={{
              fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.06em',
              textTransform: 'uppercase', color: 'var(--fg-3)', fontWeight: 500,
            }}>{SEARCH_RESULTS.length} results · messages</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {SEARCH_RESULTS.map((r, i) => (
              <SearchResultRow key={r.id} r={r} query={query} highlight={i === 0} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function SearchResultRow({ r, query, highlight }) {
  // Highlight occurrences of `query` (case-insensitive) in r.body
  const parts = [];
  if (!query) {
    parts.push({ text: r.body, hit: false });
  } else {
    const re = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    let last = 0;
    let m;
    while ((m = re.exec(r.body)) !== null) {
      if (m.index > last) parts.push({ text: r.body.slice(last, m.index), hit: false });
      parts.push({ text: m[0], hit: true });
      last = m.index + m[0].length;
    }
    if (last < r.body.length) parts.push({ text: r.body.slice(last), hit: false });
  }
  return (
    <article className="card" style={{
      padding: '12px 16px',
      border: highlight ? '1px solid var(--border-2)' : '1px solid var(--border-1)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 12.5, marginBottom: 6 }}>
        <span style={{ color: 'var(--accent-strong)', fontWeight: 600 }}>{r.channel}</span>
        {r.isThread ? (
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, color: 'var(--fg-3)' }}>
            <Icon name="message-square" size={11} /> thread
          </span>
        ) : null}
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
          <Avatar name={r.author} kind="agent" size="sm" />
          <span style={{ color: 'var(--fg-1)', fontWeight: 500 }}>{r.author}</span>
        </span>
        <span className="meta">{r.ts}</span>
      </div>
      <div style={{
        fontSize: 13, lineHeight: '20px', color: 'var(--fg-2)',
        fontFamily: 'var(--font-mono)',
        wordBreak: 'break-all',
      }}>
        {parts.map((p, i) => p.hit
          ? <mark key={i} style={{ background: 'var(--accent-soft)', color: 'var(--accent-press)', borderRadius: 2, padding: '0 2px' }}>{p.text}</mark>
          : <span key={i}>{p.text}</span>)}
      </div>
    </article>
  );
}

// ---------- Workspace switcher dropdown ----------
function WorkspaceSwitcher({ onClose }) {
  return (
    <div className="syfo-ws-dropdown" role="menu">
      <div style={{ padding: '6px 0 4px' }}>
        {WORKSPACES.map(w => (
          <button key={w.id} role="menuitem" className="syfo-ws-item" style={{
            background: w.active ? 'var(--accent-soft)' : 'transparent',
          }}>
            <span style={{
              width: 22, height: 22, borderRadius: 'var(--radius-xs)',
              background: 'var(--fg-1)', color: 'var(--fg-inverse)',
              fontSize: 11, fontWeight: 600,
              display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0,
            }}>{w.initial}</span>
            <span style={{ display: 'flex', flexDirection: 'column', minWidth: 0, flex: 1, textAlign: 'left' }}>
              <span style={{
                fontSize: 13.5, fontWeight: 500,
                color: w.active ? 'var(--accent-strong)' : 'var(--fg-1)',
              }}>{w.name}</span>
              <span className="meta" style={{ fontSize: 11 }}>{w.slug}</span>
            </span>
            {w.active ? <Icon name="check" size={14} style={{ color: 'var(--accent)' }} /> : null}
            {!w.active && w.unread > 0 ? (
              <span style={{
                fontFamily: 'var(--font-mono)', fontSize: 10.5,
                background: 'var(--accent)', color: 'var(--fg-inverse)',
                padding: '1px 6px', borderRadius: 999, fontWeight: 600,
              }}>{w.unread}</span>
            ) : null}
          </button>
        ))}
      </div>
      <div style={{ borderTop: '1px solid var(--border-1)', padding: '6px 0 4px' }}>
        <button role="menuitem" className="syfo-ws-item">
          <Icon name="plus" size={14} style={{ color: 'var(--fg-2)' }} />
          <span style={{ fontSize: 13.5, color: 'var(--fg-1)', fontWeight: 500 }}>Switch or create server</span>
        </button>
        <button role="menuitem" className="syfo-ws-item">
          <Icon name="log" size={14} style={{ color: 'var(--fg-2)' }} />
          <span style={{ fontSize: 13.5, color: 'var(--fg-1)' }}>Release notes</span>
        </button>
      </div>
    </div>
  );
}

Object.assign(window, { SearchOverlay, WorkspaceSwitcher });
