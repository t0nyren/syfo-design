// Syfo UI Kit — Computers (was Runtimes)
// Left list of computers; right detail with daemon info, detected runtimes, and agents on this computer.

function ComputersView() {
  const [selectedId, setSelectedId] = React.useState('breeze-99');
  const selected = COMPUTERS.find(c => c.id === selectedId) || COMPUTERS[0];

  return (
    <section className="syfo-content">
      <header className="syfo-topbar">
        <div className="title-block">
          <Icon name="monitor" size={16} style={{ color: 'var(--fg-2)' }} />
          <div className="title">{selected.name}</div>
          <span style={{ width: 1, height: 14, background: 'var(--border-2)', display: 'inline-block' }} />
          <div className="subtitle">{COMPUTERS.length} connected</div>
        </div>
        <div className="actions">
          <Button variant="ghost" icon title="刷新"><Icon name="activity" size={14} /></Button>
        </div>
      </header>

      <div style={{ flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: '320px 1fr' }}>
        {/* Left list */}
        <aside style={{ borderRight: '1px solid var(--border-1)', overflowY: 'auto', padding: '14px 10px' }}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '4px 10px 10px',
          }}>
            <span style={{
              fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.06em',
              textTransform: 'uppercase', color: 'var(--fg-3)', fontWeight: 500
            }}>Computers · {COMPUTERS.length}</span>
            <button className="btn btn-ghost btn-icon" style={{ width: 22, height: 22 }} title="添加">
              <Icon name="plus" size={12} />
            </button>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {COMPUTERS.map(c => (
              <ComputerListItem
                key={c.id}
                computer={c}
                active={c.id === selectedId}
                onClick={() => setSelectedId(c.id)}
              />
            ))}
          </div>
        </aside>

        {/* Detail */}
        <ComputerDetail computer={selected} />
      </div>
    </section>
  );
}

function ComputerListItem({ computer, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className="syfo-dm-item"
      style={{
        background: active ? 'var(--accent-soft)' : 'transparent',
        color: active ? 'var(--accent-strong)' : 'var(--fg-1)',
        padding: '10px 10px',
      }}
    >
      <span style={{
        width: 28, height: 28, borderRadius: 'var(--radius-xs)',
        background: active ? 'var(--bg-paper)' : 'var(--bg-surface)',
        border: '1px solid var(--border-1)',
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        color: active ? 'var(--accent)' : 'var(--fg-2)', flexShrink: 0,
      }}>
        <Icon name="monitor" size={14} />
      </span>
      <span className="name-wrap" style={{ alignItems: 'baseline' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 6, minWidth: 0 }}>
          <span className="name" style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{computer.name}</span>
          <PresenceDot presence={computer.presence} />
        </span>
        <span className="desc mono" style={{ fontFamily: 'var(--font-mono)', fontSize: 11 }}>daemon {computer.daemon}</span>
      </span>
    </button>
  );
}

function ComputerDetail({ computer }) {
  return (
    <div style={{ overflowY: 'auto', padding: '24px 32px 40px' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 18, marginBottom: 28 }}>
        <div style={{
          width: 56, height: 56, borderRadius: 'var(--radius-sm)',
          background: 'var(--accent-soft)', color: 'var(--accent-strong)',
          display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <Icon name="monitor" size={22} />
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h1 className="syfo-h1" style={{ margin: 0 }}>{computer.name}</h1>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6 }}>
            <PresenceDot presence={computer.presence} />
            <span style={{ fontSize: 13, color: 'var(--fg-2)' }}>Connected</span>
          </div>
          {computer.hostname ? (
            <div className="meta" style={{ marginTop: 6, fontFamily: 'var(--font-mono)' }}>{computer.hostname}</div>
          ) : null}
        </div>
        <Button variant="secondary" leading={<Icon name="pencil" size={13} />}>Rename</Button>
      </div>

      {/* Info card */}
      <SectionLabel style={{ padding: '0 0 12px' }}>Info</SectionLabel>
      <div className="card" style={{ padding: '14px 18px', display: 'flex', flexDirection: 'column', gap: 14, marginBottom: 28 }}>
        <Row k="名称"           v={<span className="mono" style={{ color: 'var(--fg-1)' }}>{computer.name}</span>} />
        <Row k="OS"             v={<span className="mono" style={{ color: 'var(--fg-1)' }}>{computer.os}</span>} />
        <Row k="守护版本" v={<span className="mono" style={{ color: 'var(--fg-1)' }}>{computer.daemon}</span>} />
        <Row k="创建于"        v={<span className="mono" style={{ color: 'var(--fg-1)' }}>{computer.created}</span>} />
      </div>

      {/* Detected runtimes */}
      <SectionLabel style={{ padding: '0 0 12px' }}>Detected runtimes</SectionLabel>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 28 }}>
        {Object.entries(computer.runtimes).map(([name, installed]) => (
          <span key={name} style={{
            display: 'inline-flex', alignItems: 'center', gap: 6,
            padding: '6px 10px', borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-1)',
            background: installed ? 'var(--accent-soft)' : 'var(--bg-surface)',
            color: installed ? 'var(--accent-strong)' : 'var(--fg-3)',
            fontSize: 12.5, fontFamily: 'var(--font-mono)', letterSpacing: '0.01em',
          }}>
            {installed ? <Icon name="check" size={12} /> : null}
            {name}
            {!installed ? <span style={{ color: 'var(--fg-3)' }}>(not installed)</span> : null}
          </span>
        ))}
      </div>

      {/* Agents on this computer */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12
      }}>
        <SectionLabel style={{ padding: 0 }}>Agents on this computer · {computer.agentIds.length}</SectionLabel>
        <div style={{ display: 'flex', gap: 8 }}>
          <Button variant="secondary" size="sm" leading={<Icon name="check" size={12} />}>Select</Button>
          <Button variant="primary"   size="sm" leading={<Icon name="plus" size={13} />}>Create</Button>
        </div>
      </div>
      <div className="card" style={{ overflow: 'hidden' }}>
        {computer.agentIds.map((aid, i) => {
          const a = memberById(aid);
          return (
            <div key={aid} style={{
              display: 'flex', alignItems: 'center', gap: 12, padding: '12px 16px',
              borderBottom: i < computer.agentIds.length - 1 ? '1px solid var(--border-1)' : 0,
            }}>
              <Avatar name={a.name} kind="agent" size="sm" />
              <div style={{ flex: 1, minWidth: 0, display: 'flex', alignItems: 'baseline', gap: 8 }}>
                <span style={{ fontSize: 13.5, fontWeight: 500, color: 'var(--fg-1)' }}>{a.name}</span>
                <span className="meta" style={{ fontFamily: 'var(--font-mono)' }}>{a.runtime}</span>
              </div>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12.5 }}>
                <PresenceDot presence={a.presence === 'thinking' ? 'online' : a.presence} />
                <span className="mono" style={{ color: 'var(--fg-2)' }}>{a.presence === 'thinking' ? 'online' : a.presence}</span>
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

Object.assign(window, { ComputersView });
