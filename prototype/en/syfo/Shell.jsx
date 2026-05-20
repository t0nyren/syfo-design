// Syfo UI Kit — Shell (left rail + sidebar)

function Rail({ view, onView }) {
  const items = [
    { id: 'home',     icon: 'message-square', badge: true },
    { id: 'tasks',    icon: 'list-todo' },
    { id: 'members',  icon: 'users' },
    { id: 'activity', icon: 'activity' },
    { id: 'computers',icon: 'monitor' },
  ];
  return (
    <nav className="syfo-rail" aria-label="Workspace">
      <div className="syfo-rail-brand" title="mini-pinecorn workspace">
        <img src="syfo/assets/logo-mark.svg" alt="Syfo" width="28" height="28" />
      </div>
      {items.map(it => (
        <button
          key={it.id}
          className={'syfo-rail-item' + (view === it.id ? ' is-active' : '')}
          onClick={() => onView(it.id)}
          title={it.id}
        >
          <Icon name={it.icon} size={18} />
          {it.badge && view !== it.id ? <span className="badge" /> : null}
        </button>
      ))}
      <div className="syfo-rail-spacer" />
      <button className="syfo-rail-item" title="Settings" onClick={() => onView('settings')}>
        <Icon name="settings" size={18} />
      </button>
    </nav>
  );
}

function Sidebar({ view, activeChannel, activeDM, onChannel, onDM, onTopView, onOpenWsSwitch, onOpenSearch }) {
  return (
    <aside className="syfo-sidebar">
      <div className="syfo-sidebar-header">
        <button className="syfo-workspace-pill" title="Switch workspace" onClick={onOpenWsSwitch} style={{ border: 0 }}>
          <span style={{
            width: 22, height: 22, borderRadius: 'var(--radius-xs)',
            background: 'var(--fg-1)', color: 'var(--fg-inverse)',
            fontSize: 11, fontWeight: 600, letterSpacing: 0,
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center'
          }}>M</span>
          <span className="name">{WORKSPACE.name}</span>
          <Icon name="chevron-down" size={14} style={{ color: 'var(--fg-3)' }} />
        </button>
        <button className="btn btn-ghost btn-icon" title="New" style={{ width: 28, height: 28 }}>
          <Icon name="pencil" size={14} />
        </button>
      </div>

      <button className="syfo-search" onClick={onOpenSearch} style={{ border: 0, width: 'calc(100% - 24px)', textAlign: 'left' }}>
        <Icon name="search" size={14} />
        <span>Search</span>
        <span className="kbd">⌘K</span>
      </button>

      <div style={{ display: 'flex', flexDirection: 'column', padding: '0 8px', gap: 1 }}>
        <button
          className={'syfo-channel-item' + (view === 'activity' ? ' is-active' : '')}
          onClick={() => onTopView('activity')}
        >
          <Icon name="activity" size={14} className="glyph" />
          <span className="name">Activity</span>
          <span className="count">13</span>
        </button>
        <button
          className={'syfo-channel-item' + (view === 'saved' ? ' is-active' : '')}
          onClick={() => onTopView('saved')}
        >
          <Icon name="inbox" size={14} className="glyph" />
          <span className="name">Saved</span>
        </button>
      </div>

      <div className="syfo-section-label">
        <span>Channels</span>
        <div className="actions">
          <button title="New channel"><Icon name="plus" size={12} /></button>
        </div>
      </div>
      <div className="syfo-channel-list">
        {CHANNELS.map(c => (
          <button
            key={c.id}
            className={'syfo-channel-item' + (view === 'home' && activeChannel === c.id ? ' is-active' : '')}
            onClick={() => onChannel(c.id)}
          >
            <Icon name={c.glyph} size={12} className="glyph" />
            <span className="name">{c.name}</span>
            {c.unread > 0 ? <span className="count">{c.unread}</span> : null}
          </button>
        ))}
      </div>

      <div className="syfo-section-label">
        <span>Direct messages</span>
        <div className="actions">
          <button title="New DM"><Icon name="plus" size={12} /></button>
        </div>
      </div>
      <div className="syfo-channel-list" style={{ paddingBottom: 8 }}>
        {DMS.map(d => (
          <button
            key={d.id}
            className={'syfo-dm-item' + (view === 'dm' && activeDM === d.id ? ' is-active' : '')}
            onClick={() => onDM(d.id)}
          >
            <Avatar name={d.name} kind="agent" size="sm" presence={d.presence} />
            <span className="name-wrap">
              <span className="name">{d.name}</span>
              <span className="desc">{d.desc}</span>
            </span>
          </button>
        ))}
      </div>

      <div style={{ marginTop: 'auto', padding: '10px 16px 14px', display: 'flex', alignItems: 'center', gap: 10 }}>
        <Avatar name="tonyren" kind="human" size="sm" presence="online" />
        <div style={{ minWidth: 0, flex: 1 }}>
          <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--fg-1)' }}>tonyren</div>
          <div className="meta" style={{ fontSize: 11, color: 'var(--fg-3)' }}>Active now</div>
        </div>
        <Icon name="chevron-down" size={13} style={{ color: 'var(--fg-3)' }} />
      </div>
    </aside>
  );
}

Object.assign(window, { Rail, Sidebar });
