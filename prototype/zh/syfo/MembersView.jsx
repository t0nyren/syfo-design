// Syfo UI Kit — Members + Agent profile

function MembersView() {
  const [selectedId, setSelectedId] = React.useState('lisa');
  const selected = memberById(selectedId);

  return (
    <section className="syfo-content">
      <header className="syfo-topbar">
        <div className="title-block">
          <Icon name="users" size={16} style={{ color: 'var(--fg-2)' }} />
          <div className="title">Members</div>
          <div className="subtitle">{HUMANS.length} humans · {AGENTS.length} agents</div>
        </div>
        <div className="actions">
          <Button variant="secondary" size="sm" leading={<Icon name="git-branch" size={12} />}>Graph</Button>
          <Button variant="primary" size="sm" leading={<Icon name="plus" size={13} />}>Invite</Button>
        </div>
      </header>

      <div style={{ flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: '320px 1fr' }}>
        <aside style={{ borderRight: '1px solid var(--border-1)', overflowY: 'auto', padding: '12px 8px' }}>
          <SectionLabel>Agents · {AGENTS.length}</SectionLabel>
          {AGENTS.map(a => (
            <MemberRow key={a.id} member={a} active={a.id === selectedId} onClick={() => setSelectedId(a.id)} />
          ))}
          <SectionLabel style={{ marginTop: 16 }}>Humans · {HUMANS.length}</SectionLabel>
          {HUMANS.map(h => (
            <MemberRow key={h.id} member={h} active={h.id === selectedId} onClick={() => setSelectedId(h.id)} />
          ))}
        </aside>
        <AgentProfile member={selected} />
      </div>
    </section>
  );
}

function SectionLabel({ children, style }) {
  return (
    <div style={{
      padding: '8px 12px 6px', fontFamily: 'var(--font-mono)', fontSize: 11,
      letterSpacing: '0.04em', textTransform: 'uppercase', color: 'var(--fg-3)',
      ...style
    }}>{children}</div>
  );
}

function MemberRow({ member, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className="syfo-dm-item"
      style={{
        width: '100%', textAlign: 'left',
        background: active ? 'var(--accent-soft)' : 'transparent',
        color: active ? 'var(--accent-strong)' : 'var(--fg-1)',
      }}
    >
      <Avatar name={member.name} kind={member.kind} size="sm" presence={member.presence} />
      <span className="name-wrap">
        <span className="name">{member.name}</span>
        <span className="desc">{member.desc || member.role}</span>
      </span>
    </button>
  );
}

function AgentProfile({ member }) {
  const isAgent = member.kind === 'agent';
  const [tab, setTab] = React.useState('profile');
  const tabs = [
    { id: 'dms',         label: 'AI 私聊',   icon: 'message-square' },
    { id: 'profile',     label: '资料',     icon: 'info' },
    { id: 'workspace',   label: '工作区',   icon: 'hash' },
    { id: 'permissions', label: '权限', icon: 'shield' },
    { id: 'reminders',   label: '提醒',   icon: 'clock' },
    { id: 'activity',    label: '动态',    icon: 'activity' },
  ];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: 0, overflowY: 'auto' }}>
      {/* Profile header */}
      <div style={{ padding: '24px 32px 0' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 18 }}>
          <Avatar name={member.name} kind={member.kind} size="xl" presence={member.presence} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <h1 className="syfo-h1" style={{ margin: 0 }}>{member.name}</h1>
              <PresenceDot presence={member.presence} />
              <span style={{ fontSize: 13, color: 'var(--fg-2)', textTransform: 'capitalize' }}>{member.presence}</span>
            </div>
            <div className="meta" style={{ marginTop: 4 }}>{member.handle}</div>
            <div style={{ marginTop: 12, fontSize: 14, color: 'var(--fg-1)', maxWidth: 560 }}>
              {member.desc || `${member.role} on ${WORKSPACE.name}.`}
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <Button variant="secondary" leading={<Icon name="message-square" size={14} />}>Message</Button>
            <Button variant="secondary" icon title="暂停"><Icon name="minus" size={14} /></Button>
            <Button variant="secondary" icon title="重启"><Icon name="activity" size={14} /></Button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="syfo-tabs" style={{ marginTop: 24, padding: '0 32px' }}>
        {tabs.map(t => (
          <button
            key={t.id}
            className={'syfo-tab' + (tab === t.id ? ' is-active' : '')}
            onClick={() => setTab(t.id)}
          >
            <Icon name={t.icon} size={14} />
            <span>{t.label}</span>
          </button>
        ))}
      </div>

      {/* Tab body */}
      <div style={{ padding: '24px 32px', maxWidth: tab === 'activity' ? 920 : 720 }}>
        {tab === 'profile' && (isAgent ? <AgentProfileBody member={member} /> : <HumanProfileBody member={member} />)}
        {tab === 'activity' && <AgentStateLog />}
        {tab !== 'profile' && tab !== 'activity' && <EmptyState title="暂无内容" body="此视图来自设计系统；连接工作区后会自动填充真实数据。" />}
      </div>
    </div>
  );
}

function AgentStateLog() {
  return (
    <div>
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        marginBottom: 14,
      }}>
        <SectionLabel style={{ padding: 0 }}>Activity diagnostics</SectionLabel>
        <Button variant="secondary" size="sm" leading={<Icon name="paperclip" size={12} />}>Copy diagnostic info</Button>
      </div>
      <div className="card" style={{ padding: '8px 0', fontFamily: 'var(--font-mono)' }}>
        {AGENT_STATE_LOG.map((row, i) => (
          <StateLogRow key={i} row={row} />
        ))}
      </div>
    </div>
  );
}

function StateLogRow({ row }) {
  const dotColor = {
    thinking: 'var(--warning)',
    idle:     'var(--success)',
    working:  'var(--warning)',
    output:   'var(--info)',
    command:  'var(--warning)',
    offline:  'var(--fg-3)',
  }[row.state] || 'var(--fg-3)';
  return (
    <div style={{
      display: 'grid', gridTemplateColumns: '88px 14px 130px 1fr',
      alignItems: 'baseline', gap: 8, padding: '6px 16px',
      fontSize: 12, lineHeight: '18px',
    }}>
      <span style={{ color: 'var(--fg-3)' }}>{row.ts}</span>
      <span style={{ width: 8, height: 8, borderRadius: '50%', background: dotColor, display: 'inline-block', alignSelf: 'center' }} />
      <span style={{ color: 'var(--fg-1)', fontWeight: 500 }}>{row.label}</span>
      <span style={{
        color: 'var(--fg-2)',
        overflow: 'hidden', whiteSpace: 'nowrap', textOverflow: 'ellipsis',
      }}>{row.detail}</span>
    </div>
  );
}

function AgentProfileBody({ member }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <Field label="显示名" value={member.name} />
      <Field label="描述" value={member.desc} />

      <div>
        <SectionLabel style={{ padding: '0 0 12px' }}>Info</SectionLabel>
        <div className="card" style={{ padding: '14px 16px', display: 'flex', flexDirection: 'column', gap: 12 }}>
          <Row k="计算机" v={<><PresenceDot presence="online" /> <span style={{ fontFamily: 'var(--font-mono)' }}>breeze-cobra-99</span> <span className="meta">· Connected · daemon v0.51.1</span></>} />
          <Row k="创建于" v={<span className="mono" style={{ fontSize: 13, color: 'var(--fg-1)' }}>2026 年 5 月 13 日</span>} />
          <Row k="创建者" v={<span style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}><Avatar name="tonyren" size="sm" /> <span>tonyren</span> <span className="meta">@tonyren</span></span>} />
        </div>
      </div>

      <div>
        <SectionLabel style={{ padding: '0 0 12px' }}>Runtime configuration</SectionLabel>
        <div className="card" style={{ padding: '14px 16px', display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
            <KVStack label="运行时"><Chip tone="info">{member.runtime}</Chip></KVStack>
            <KVStack label="模型"><Chip tone="accent">{member.model}</Chip></KVStack>
            <KVStack label="推理深度"><Chip>{member.reasoning}</Chip></KVStack>
          </div>
        </div>
      </div>

      <div>
        <SectionLabel style={{ padding: '0 0 12px' }}>Environment variables</SectionLabel>
        <div className="card" style={{ padding: '14px 16px', color: 'var(--fg-3)', fontSize: 13.5 }}>
          No environment variables configured.
        </div>
      </div>

      <div>
        <SectionLabel style={{ padding: '0 0 12px' }}>Skills · 7</SectionLabel>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          {['Bash', 'Python', 'Git', '读取代码', '编辑代码', '运行测试', '部署'].map(s => (
            <Chip key={s}>{s}</Chip>
          ))}
        </div>
      </div>
    </div>
  );
}

function HumanProfileBody({ member }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <Field label="显示名" value={member.name} />
      <Field label="账号" value={member.handle} />
      <Field label="角色" value={member.role} />
      <Field label="Email" value={`${member.id}@example.com`} />
    </div>
  );
}

function Field({ label, value }) {
  return (
    <div>
      <SectionLabel style={{ padding: '0 0 6px' }}>{label}</SectionLabel>
      <div style={{ fontSize: 14, color: 'var(--fg-1)' }}>{value}</div>
    </div>
  );
}

function Row({ k, v }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 16, fontSize: 13.5 }}>
      <div style={{ width: 110, color: 'var(--fg-2)', flexShrink: 0 }}>{k}</div>
      <div style={{ color: 'var(--fg-1)', display: 'flex', alignItems: 'center', gap: 6 }}>{v}</div>
    </div>
  );
}

function KVStack({ label, children }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.04em', textTransform: 'uppercase', color: 'var(--fg-3)' }}>{label}</div>
      <div>{children}</div>
    </div>
  );
}

function EmptyState({ title, body, icon = 'inbox' }) {
  return (
    <div style={{ textAlign: 'center', padding: '40px 24px' }}>
      <div style={{ width: 48, height: 48, margin: '0 auto 16px', display: 'flex', alignItems: 'center', justifyContent: 'center',
                    background: 'var(--bg-sunken)', borderRadius: 'var(--radius-md)', color: 'var(--fg-3)' }}>
        <Icon name={icon} size={20} />
      </div>
      <div className="syfo-h2" style={{ marginBottom: 6 }}>{title}</div>
      <p style={{ fontSize: 13.5, color: 'var(--fg-2)', maxWidth: 360, margin: '0 auto' }}>{body}</p>
    </div>
  );
}

Object.assign(window, { MembersView, EmptyState, SectionLabel, Row });
