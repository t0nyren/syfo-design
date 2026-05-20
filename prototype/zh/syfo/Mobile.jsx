// Syfo UI Kit — Mobile shell
// Stack-based navigation. Tab bar: Home, Tasks, Members, Settings (matches reference).
// Screens: Home (channels + DMs) · Tasks · Members · Settings (Server profile etc.)
//          + push views: Channel chat · Agent profile · Computer detail · Activity diagnostics · Notifications

function MobileApp() {
  const [tab, setTab] = React.useState('home');
  // navigation stack of pushed views, each { type: 'channel'|'dm'|'member'|'computer'|'activity'|'notifications', id?: string }
  const [stack, setStack] = React.useState([]);
  const push = (view) => setStack(s => [...s, view]);
  const pop  = () => setStack(s => s.slice(0, -1));

  const top = stack[stack.length - 1];

  // Tab body
  let body;
  if (top) {
    if (top.type === 'channel')        body = <MobileChannel channelId={top.id} onBack={pop} />;
    else if (top.type === 'dm')        body = <MobileChannel channelId={top.id} onBack={pop} isDM />;
    else if (top.type === 'member')    body = <MobileMember memberId={top.id} onBack={pop} />;
    else if (top.type === 'computer')  body = <MobileComputer computerId={top.id} onBack={pop} />;
    else if (top.type === 'activity')  body = <MobileActivity onBack={pop} />;
    else if (top.type === 'notifications') body = <MobileNotifications onBack={pop} />;
  } else {
    if (tab === 'home')      body = <MobileHome     onOpen={push} />;
    else if (tab === 'tasks')body = <MobileTasks />;
    else if (tab === 'members') body = <MobileMembers onOpen={push} />;
    else if (tab === 'settings') body = <MobileSettings onOpen={push} />;
  }

  return (
    <div className="syfo-phone">
      <div style={{ flex: 1, minHeight: 0, display: 'flex', flexDirection: 'column' }}>
        {body}
      </div>
      <nav className="syfo-phone-tabbar">
        <MobileTabBtn label="主页"     icon="message-square" active={!top && tab === 'home'}     onClick={() => { setStack([]); setTab('home'); }} />
        <MobileTabBtn label="任务"    icon="list-todo"      active={!top && tab === 'tasks'}    onClick={() => { setStack([]); setTab('tasks'); }} />
        <MobileTabBtn label="成员"  icon="users"          active={!top && tab === 'members'}  onClick={() => { setStack([]); setTab('members'); }} />
        <MobileTabBtn label="设置" icon="settings"       active={!top && tab === 'settings'} onClick={() => { setStack([]); setTab('settings'); }} />
      </nav>
    </div>
  );
}

function MobileTabBtn({ label, icon, active, onClick }) {
  return (
    <button className={active ? 'is-active' : ''} onClick={onClick}>
      <Icon name={icon} size={18} />
      <span>{label}</span>
    </button>
  );
}

// Shared mobile header
function MobileHeader({ title, subtitle, back, right }) {
  return (
    <header className="syfo-phone-header" style={{ paddingTop: back ? 10 : 6 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0, flex: 1 }}>
        {back ? (
          <button className="btn btn-ghost btn-icon" onClick={back} title="Back" style={{ width: 32, height: 32, marginLeft: -6 }}>
            <Icon name="arrow-left" size={18} />
          </button>
        ) : null}
        <div style={{ minWidth: 0 }}>
          <div className="title" style={{ fontSize: back ? 20 : 26 }}>{title}</div>
          {subtitle ? <div className="subtitle">{subtitle}</div> : null}
        </div>
      </div>
      {right ? <div style={{ display: 'flex', gap: 4, flexShrink: 0 }}>{right}</div> : null}
    </header>
  );
}

// ============================================================
//   HOME — workspace pill + channels + direct messages
// ============================================================
function MobileHome({ onOpen }) {
  return (
    <>
      {/* Workspace header (replaces title in this screen) */}
      <div style={{ padding: '8px 16px 0', flexShrink: 0 }}>
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10,
          padding: '10px 12px', borderRadius: 'var(--radius-md)',
          background: 'var(--bg-surface)', border: '1px solid var(--border-1)',
        }}>
          <button style={{
            display: 'inline-flex', alignItems: 'center', gap: 8, border: 0, background: 'transparent',
            cursor: 'pointer', padding: 0,
          }}>
            <span style={{
              width: 24, height: 24, borderRadius: 'var(--radius-xs)',
              background: 'var(--fg-1)', color: 'var(--fg-inverse)',
              fontSize: 12, fontWeight: 600,
              display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
            }}>M</span>
            <span style={{ fontSize: 15, fontWeight: 600, color: 'var(--fg-1)' }}>{WORKSPACE.name}</span>
            <Icon name="chevron-down" size={14} style={{ color: 'var(--fg-3)' }} />
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent)', marginLeft: 2 }} />
          </button>
          <button
            className="btn btn-ghost btn-icon"
            title="Notifications"
            style={{ width: 30, height: 30, position: 'relative' }}
            onClick={() => onOpen({ type: 'notifications' })}
          >
            <Icon name="activity" size={16} />
            <span style={{
              position: 'absolute', top: 4, right: 4, width: 6, height: 6,
              borderRadius: '50%', background: 'var(--accent)',
            }} />
          </button>
        </div>
      </div>

      <div className="syfo-phone-body" style={{ paddingTop: 14 }}>
        <SidebarSection label="Channels" count={CHANNELS.length} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 1, marginBottom: 18 }}>
          {CHANNELS.map(c => (
            <button
              key={c.id}
              className="syfo-mobile-row"
              onClick={() => onOpen({ type: 'channel', id: c.id })}
            >
              <Icon name={c.glyph} size={15} style={{ color: c.unread > 0 ? 'var(--accent)' : 'var(--fg-3)', flexShrink: 0 }} />
              <span style={{ fontSize: 15, flex: 1, color: c.unread > 0 ? 'var(--fg-1)' : 'var(--fg-2)', fontWeight: c.unread > 0 ? 600 : 400, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', textAlign: 'left' }}>
                {c.name}
              </span>
              {c.unread > 0 ? (
                <span style={{
                  fontFamily: 'var(--font-mono)', fontSize: 11, fontWeight: 600,
                  background: 'var(--accent)', color: 'var(--fg-inverse)',
                  padding: '2px 7px', borderRadius: 999,
                }}>{c.unread}</span>
              ) : null}
            </button>
          ))}
        </div>

        <SidebarSection label="Direct messages" count={DMS.length} trailing={
          <button className="btn btn-ghost btn-icon" style={{ width: 22, height: 22 }} title="Sort">
            <Icon name="chevron-down" size={12} />
          </button>
        } />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {DMS.map(d => (
            <button
              key={d.id}
              className="syfo-mobile-row"
              onClick={() => onOpen({ type: 'dm', id: d.id })}
              style={{ padding: '8px 4px' }}
            >
              <Avatar name={d.name} kind="agent" size="sm" />
              <span style={{ display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, textAlign: 'left' }}>
                <span style={{ fontSize: 14, color: 'var(--fg-1)', fontWeight: 500, lineHeight: '18px' }}>{d.name}</span>
                <span className="meta" style={{ fontSize: 11.5, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{d.desc}</span>
              </span>
              <PresenceDot presence={d.presence === 'thinking' ? 'online' : d.presence} />
            </button>
          ))}
        </div>
      </div>
    </>
  );
}

function SidebarSection({ label, count, trailing }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 8, padding: '4px 4px 10px',
      fontFamily: 'var(--font-mono)', fontSize: 10.5, letterSpacing: '0.08em',
      textTransform: 'uppercase', color: 'var(--fg-3)', fontWeight: 500,
    }}>
      <Icon name="chevron-down" size={11} style={{ color: 'var(--fg-3)' }} />
      <span>{label}</span>
      {count != null ? <span style={{ color: 'var(--fg-3)' }}>{count}</span> : null}
      <div style={{ flex: 1 }} />
      {trailing}
    </div>
  );
}

// ============================================================
//   TASKS — filter chips + Board/List toggle + cards
// ============================================================
function MobileTasks() {
  const [view, setView] = React.useState('list');
  return (
    <>
      <MobileHeader
        title="Tasks"
        subtitle={`${TASKS.length} channel tasks`}
        right={<button className="btn btn-ghost btn-icon"><Icon name="more-horizontal" size={16} /></button>}
      />
      <div style={{ padding: '0 16px 10px', display: 'flex', flexDirection: 'column', gap: 8, flexShrink: 0 }}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <MobileFilterChip icon="hash"   label="Channel" />
          <MobileFilterChip icon="users"  label="Creator" />
          <MobileFilterChip icon="users"  label="Assignee" />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
          <div style={{ display: 'inline-flex', border: '1px solid var(--border-2)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
            <button onClick={() => setView('board')} className="btn btn-sm" style={{
              borderRadius: 0, border: 0,
              background: view === 'board' ? 'var(--accent)' : 'transparent',
              color: view === 'board' ? 'var(--fg-inverse)' : 'var(--fg-2)',
              fontWeight: view === 'board' ? 600 : 500,
            }}>
              <Icon name="sliders" size={12} /> Board
            </button>
            <button onClick={() => setView('list')} className="btn btn-sm" style={{
              borderRadius: 0, border: 0,
              background: view === 'list' ? 'var(--accent)' : 'transparent',
              color: view === 'list' ? 'var(--fg-inverse)' : 'var(--fg-2)',
              fontWeight: view === 'list' ? 600 : 500,
              borderLeft: '1px solid var(--border-2)',
            }}>
              <Icon name="list-todo" size={12} /> List
            </button>
          </div>
          <button className="btn btn-primary btn-sm">
            <Icon name="plus" size={13} /> New
          </button>
        </div>
      </div>
      <div className="syfo-phone-body" style={{ paddingTop: 4 }}>
        {view === 'list' ? <MobileTaskList /> : <MobileTaskBoard />}
      </div>
    </>
  );
}

function MobileFilterChip({ icon, label }) {
  return (
    <button style={{
      border: '1px solid var(--border-2)', background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)',
      padding: '6px 10px', cursor: 'pointer',
      display: 'inline-flex', alignItems: 'center', gap: 6,
      fontFamily: 'var(--font-mono)', fontSize: 10.5, letterSpacing: '0.06em',
      textTransform: 'uppercase', color: 'var(--fg-2)', fontWeight: 500,
    }}>
      <Icon name={icon} size={12} />
      {label}
      <Icon name="chevron-down" size={11} style={{ color: 'var(--fg-3)' }} />
    </button>
  );
}

function MobileTaskList() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {TASKS.map(t => <MobileTaskCard key={t.id} task={t} />)}
    </div>
  );
}
function MobileTaskBoard() {
  const cols = ['in-progress', 'in-review', 'done'];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {cols.map(s => {
        const meta = STATUS_META[s];
        const items = TASKS.filter(t => t.status === s);
        return (
          <div key={s}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '0 4px 8px' }}>
              <Chip tone={meta.tone}>{meta.label}</Chip>
              <span className="meta">{items.length}</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {items.map(t => <MobileTaskCard key={t.id} task={t} />)}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function MobileTaskCard({ task }) {
  const a = memberById(task.assigneeId);
  const meta = STATUS_META[task.status];
  return (
    <article className="syfo-phone-card" style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 0 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <span style={{ color: 'var(--accent-strong)', fontWeight: 600, fontSize: 12.5 }}>#{task.channel}</span>
        <span className="meta">#{task.id}</span>
        <div style={{ flex: 1 }} />
      </div>
      <div style={{ fontSize: 14, lineHeight: '19px', color: 'var(--fg-1)' }}>{task.title}</div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Avatar name={a.name} kind={a.kind} size="sm" />
          <span style={{ fontSize: 12.5, color: 'var(--fg-2)' }}>{a.name}</span>
        </div>
        <Chip tone={meta.tone}>{meta.label}</Chip>
      </div>
    </article>
  );
}

// ============================================================
//   MEMBERS — directory grouped agents/humans
// ============================================================
function MobileMembers({ onOpen }) {
  const [filter, setFilter] = React.useState('all');
  const show = (kind) => filter === 'all' || filter === kind;
  return (
    <>
      <MobileHeader
        title="Members"
        subtitle={`${HUMANS.length} humans · ${AGENTS.length} agents`}
        right={<button className="btn btn-primary btn-sm" style={{ height: 30 }}><Icon name="plus" size={13} /> Invite</button>}
      />
      <div style={{ padding: '0 16px 10px', flexShrink: 0 }}>
        <div style={{ display: 'inline-flex', border: '1px solid var(--border-2)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
          {[['all','All'],['agent','Agents'],['human','Humans']].map(([k, label], i) => (
            <button
              key={k} onClick={() => setFilter(k)}
              className="btn btn-sm" style={{
                borderRadius: 0, border: 0,
                background: filter === k ? 'var(--bg-sunken)' : 'transparent',
                color: filter === k ? 'var(--fg-1)' : 'var(--fg-2)',
                fontWeight: filter === k ? 500 : 400,
                borderLeft: i > 0 ? '1px solid var(--border-2)' : 0,
              }}
            >{label}</button>
          ))}
        </div>
      </div>
      <div className="syfo-phone-body" style={{ paddingTop: 4 }}>
        {show('agent') ? (
          <>
            <SidebarSection label={`Agents · ${AGENTS.length}`} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 18 }}>
              {AGENTS.map(a => <MobileMemberRow key={a.id} m={a} onClick={() => onOpen({ type: 'member', id: a.id })} />)}
            </div>
          </>
        ) : null}
        {show('human') ? (
          <>
            <SidebarSection label={`Humans · ${HUMANS.length}`} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {HUMANS.map(h => <MobileMemberRow key={h.id} m={h} onClick={() => onOpen({ type: 'member', id: h.id })} />)}
            </div>
          </>
        ) : null}
      </div>
    </>
  );
}

function MobileMemberRow({ m, onClick }) {
  return (
    <button onClick={onClick} className="syfo-mobile-row" style={{ padding: '8px 4px' }}>
      <Avatar name={m.name} kind={m.kind} size="sm" presence={m.presence} />
      <span style={{ display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0, textAlign: 'left' }}>
        <span style={{ fontSize: 14, fontWeight: 500, color: 'var(--fg-1)', lineHeight: '18px' }}>{m.name}</span>
        <span className="meta" style={{ fontSize: 11.5, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{m.desc || m.role}</span>
      </span>
      <Icon name="chevron-right" size={14} style={{ color: 'var(--fg-3)' }} />
    </button>
  );
}

// Member detail
function MobileMember({ memberId, onBack }) {
  const m = memberById(memberId);
  const isAgent = m.kind === 'agent';
  const computer = isAgent ? COMPUTERS.find(c => c.id === AGENT_COMPUTER[memberId]) : null;
  return (
    <>
      <MobileHeader title={m.name} subtitle={m.handle} back={onBack}
        right={<button className="btn btn-ghost btn-icon"><Icon name="more-horizontal" size={16} /></button>}
      />
      <div className="syfo-phone-body">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 16 }}>
          <Avatar name={m.name} kind={m.kind} size="xl" presence={m.presence} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <PresenceDot presence={m.presence} />
              <span style={{ fontSize: 13, color: 'var(--fg-2)', textTransform: 'capitalize' }}>{m.presence}</span>
            </div>
            <div style={{ fontSize: 13, color: 'var(--fg-1)', marginTop: 6, lineHeight: '18px' }}>
              {m.desc || `${m.role} on ${WORKSPACE.name}.`}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <Button variant="primary" leading={<Icon name="message-square" size={14} />}>Message</Button>
          {isAgent ? <Button variant="secondary" icon><Icon name="minus" size={14} /></Button> : null}
          {isAgent ? <Button variant="secondary" icon><Icon name="activity" size={14} /></Button> : null}
        </div>

        {isAgent ? (
          <>
            <SidebarSection label="运行时" />
            <article className="syfo-phone-card" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              <MobileKV k="Runtime"   v={<Chip tone="info">{m.runtime}</Chip>} />
              <MobileKV k="Model"     v={<Chip tone="accent">{m.model}</Chip>} />
              <MobileKV k="Reasoning" v={<Chip>{m.reasoning}</Chip>} />
              {computer ? (
                <MobileKV k="计算机" v={
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontFamily: 'var(--font-mono)', fontSize: 12.5 }}>
                    <PresenceDot presence={computer.presence} />
                    {computer.name}
                  </span>
                } />
              ) : null}
            </article>

            <SidebarSection label="Skills" />
            <article className="syfo-phone-card" style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {AGENT_SKILLS.map(s => <Chip key={s}>{s}</Chip>)}
            </article>

            <SidebarSection label="Environment variables" />
            <article className="syfo-phone-card" style={{ color: 'var(--fg-3)', fontSize: 13 }}>
              No environment variables configured.
            </article>
          </>
        ) : (
          <>
            <SidebarSection label="Info" />
            <article className="syfo-phone-card" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              <MobileKV k="Handle" v={<span style={{ fontFamily: 'var(--font-mono)' }}>{m.handle}</span>} />
              <MobileKV k="Role"   v={m.role} />
              <MobileKV k="Email"  v={<span style={{ fontFamily: 'var(--font-mono)' }}>{m.id}@example.com</span>} />
            </article>
          </>
        )}
      </div>
    </>
  );
}

function MobileKV({ k, v }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
      <span style={{
        fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.06em',
        textTransform: 'uppercase', color: 'var(--fg-3)', fontWeight: 500,
      }}>{k}</span>
      <span style={{ fontSize: 13.5, color: 'var(--fg-1)' }}>{v}</span>
    </div>
  );
}

// ============================================================
//   CHANNEL chat (push view)
// ============================================================
function MobileChannel({ channelId, onBack, isDM }) {
  const channel = isDM ? memberById(channelId) : (CHANNELS.find(c => c.id === channelId) || CHANNELS[0]);
  return (
    <>
      <MobileHeader
        title={channel.name}
        subtitle={isDM ? channel.desc : "It's the core team"}
        back={onBack}
        right={<>
          <button className="btn btn-ghost btn-icon"><Icon name="users" size={16} /></button>
          <button className="btn btn-ghost btn-icon"><Icon name="more-horizontal" size={16} /></button>
        </>}
      />
      <div className="syfo-phone-body" style={{ paddingBottom: 0 }}>
        {MESSAGES.map(m => {
          const a = memberById(m.authorId);
          if (m.kind === 'task-created' || m.kind === 'agent-action') {
            return (
              <div key={m.id} style={{ display: 'flex', gap: 8, padding: '6px 4px 6px 32px', alignItems: 'flex-start' }}>
                <Icon name={m.kind === 'task-created' ? 'list-todo' : 'check'} size={12} style={{ color: 'var(--fg-3)', marginTop: 3 }} />
                <span style={{ fontSize: 12, color: 'var(--fg-2)', lineHeight: '17px' }}>
                  <strong style={{ fontWeight: 500, color: 'var(--fg-1)' }}>{a.name}</strong> {m.body}
                </span>
              </div>
            );
          }
          return (
            <div key={m.id} style={{ display: 'flex', gap: 10, padding: '8px 0' }}>
              <Avatar name={a.name} kind={a.kind} size="sm" presence={a.presence} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
                  <span style={{ fontSize: 13, fontWeight: 600 }}>{a.name}</span>
                  {a.kind === 'agent' ? <span style={{
                    fontFamily: 'var(--font-mono)', fontSize: 9.5, letterSpacing: '0.06em',
                    textTransform: 'uppercase', color: 'var(--accent-strong)',
                    background: 'var(--accent-soft)', padding: '0 5px', borderRadius: 3, fontWeight: 500,
                  }}>AGENT</span> : null}
                  <span className="meta" style={{ fontSize: 10.5 }}>{m.ts}</span>
                </div>
                <div style={{ fontSize: 13, lineHeight: '19px', color: 'var(--fg-1)', marginTop: 1 }}>{m.body}</div>
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ padding: '8px 12px 10px', borderTop: '1px solid var(--border-1)', flexShrink: 0 }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          padding: '6px 10px', border: '1px solid var(--border-2)',
          borderRadius: 999, background: 'var(--bg-surface)',
        }}>
          <Icon name="plus" size={16} style={{ color: 'var(--fg-3)' }} />
          <span style={{ flex: 1, fontSize: 13, color: 'var(--fg-3)' }}>Message {isDM ? '@' + channel.name : '#' + channel.name}</span>
          <Icon name="at-sign" size={15} style={{ color: 'var(--fg-3)' }} />
          <Icon name="send" size={15} style={{ color: 'var(--accent)' }} />
        </div>
      </div>
    </>
  );
}

// ============================================================
//   ACTIVITY (diagnostics) and NOTIFICATIONS
// ============================================================
function MobileNotifications({ onBack }) {
  const [filter, setFilter] = React.useState('all');
  return (
    <>
      <MobileHeader title="Activity" subtitle="240 active · 13 unread" back={onBack}
        right={<button className="btn btn-ghost btn-icon"><Icon name="check" size={16} /></button>}
      />
      <div style={{ padding: '0 16px 10px', flexShrink: 0 }}>
        <div style={{ display: 'inline-flex', border: '1px solid var(--border-2)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
          {['all','unread','mentions'].map((k, i) => (
            <button key={k} onClick={() => setFilter(k)} className="btn btn-sm" style={{
              borderRadius: 0, border: 0,
              background: filter === k ? 'var(--bg-sunken)' : 'transparent',
              color: filter === k ? 'var(--fg-1)' : 'var(--fg-2)',
              fontWeight: filter === k ? 500 : 400, textTransform: 'capitalize',
              borderLeft: i > 0 ? '1px solid var(--border-2)' : 0,
            }}>{k}</button>
          ))}
        </div>
      </div>
      <div className="syfo-phone-body" style={{ paddingTop: 4 }}>
        {NOTIFICATIONS.map(n => (
          <article key={n.id} className="syfo-phone-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
              <span style={{ color: 'var(--accent-strong)', fontWeight: 600, fontSize: 12.5 }}>{n.channel}</span>
              <span className="meta">{n.ts}</span>
              {n.mentions ? <Chip tone="accent">@you</Chip> : null}
            </div>
            {n.body ? (
              <div style={{ fontSize: 13, lineHeight: '18px', color: 'var(--fg-1)', marginBottom: 4 }}>
                {n.body.length > 110 ? n.body.slice(0, 110) + '…' : n.body}
              </div>
            ) : null}
            {n.replyText ? (
              <div style={{ fontSize: 12.5, lineHeight: '18px', color: 'var(--fg-2)' }}>
                <span style={{ color: 'var(--fg-1)', fontWeight: 500 }}>{n.replyAuthor}:</span>{' '}
                {n.replyText.length > 80 ? n.replyText.slice(0, 80) + '…' : n.replyText}
              </div>
            ) : null}
            {(n.replies > 0 || n.newCount > 0) ? (
              <div style={{ display: 'flex', gap: 6, marginTop: 6 }}>
                {n.replies > 0 ? <span className="meta">{n.replies} replies</span> : null}
                {n.newCount > 0 ? <Chip tone="accent">{n.newCount} new</Chip> : null}
              </div>
            ) : null}
          </article>
        ))}
      </div>
    </>
  );
}

function MobileActivity({ onBack }) {
  return (
    <>
      <MobileHeader title="Activity" subtitle="Asuna@codex · last 24h" back={onBack}
        right={<button className="btn btn-ghost btn-icon"><Icon name="paperclip" size={16} /></button>}
      />
      <div className="syfo-phone-body">
        <article className="syfo-phone-card" style={{ padding: '8px 0', fontFamily: 'var(--font-mono)' }}>
          {AGENT_STATE_LOG.map((row, i) => {
            const dotColor = {
              thinking: 'var(--warning)', idle: 'var(--success)', working: 'var(--warning)',
              output: 'var(--info)', command: 'var(--warning)', offline: 'var(--fg-3)',
            }[row.state] || 'var(--fg-3)';
            return (
              <div key={i} style={{
                display: 'grid', gridTemplateColumns: '64px 10px 1fr',
                alignItems: 'baseline', gap: 8, padding: '5px 14px',
                fontSize: 11, lineHeight: '15px',
              }}>
                <span style={{ color: 'var(--fg-3)' }}>{row.ts}</span>
                <span style={{ width: 7, height: 7, borderRadius: '50%', background: dotColor, display: 'inline-block', alignSelf: 'center' }} />
                <span style={{ color: 'var(--fg-1)' }}>
                  <strong style={{ fontWeight: 500 }}>{row.label}</strong>
                  {row.detail ? <span style={{ color: 'var(--fg-3)' }}> · {row.detail.length > 30 ? row.detail.slice(0, 30) + '…' : row.detail}</span> : null}
                </span>
              </div>
            );
          })}
        </article>
      </div>
    </>
  );
}

// ============================================================
//   SETTINGS — Server profile, pre-join, owners (matches reference screen 3)
// ============================================================
function MobileSettings({ onOpen }) {
  const [section, setSection] = React.useState('server'); // server | account | runtimes | computers | audit | billing

  if (section !== 'server' && section !== 'menu') {
    return (
      <MobileSettingsDetail section={section} onBack={() => setSection('menu')} onOpen={onOpen} />
    );
  }

  if (section === 'menu') {
    return (
      <>
        <MobileHeader title="Settings" subtitle={WORKSPACE.name} />
        <div className="syfo-phone-body">
          <MobileSettingsGroup title="Server">
            <MobileSettingsRow icon="monitor" label="Server profile" onClick={() => setSection('server')} />
            <MobileSettingsRow icon="users"   label="成员" trailing={`${MEMBERS.length}`} onClick={() => setSection('members')} />
            <MobileSettingsRow icon="shield"  label="Permissions" />
            <MobileSettingsRow icon="cpu"     label="Runtimes" trailing="3" onClick={() => setSection('runtimes')} />
            <MobileSettingsRow icon="monitor" label="Computers" trailing={`${COMPUTERS.length}`} onClick={() => setSection('computers')} />
          </MobileSettingsGroup>
          <MobileSettingsGroup title="Activity">
            <MobileSettingsRow icon="activity" label="Audit log" onClick={() => setSection('audit')} />
            <MobileSettingsRow icon="log"      label="Diagnostics" onClick={() => onOpen({ type: 'activity' })} />
          </MobileSettingsGroup>
          <MobileSettingsGroup title="Account">
            <MobileSettingsRow icon="users" label="Profile" trailing="tonyren" onClick={() => setSection('account')} />
            <MobileSettingsRow icon="inbox" label="Billing" trailing="Free" />
            <MobileSettingsRow icon="x"     label="Sign out" tone="danger" />
          </MobileSettingsGroup>
        </div>
      </>
    );
  }

  // section === 'server' (default landing — matches reference)
  return <MobileServerSettings onMenu={() => setSection('menu')} />;
}

function MobileServerSettings({ onMenu }) {
  const [agreement, setAgreement] = React.useState(false);
  const [role, setRole] = React.useState('Admin');
  return (
    <>
      <MobileHeader title="Server" subtitle={`/${WORKSPACE.slug}`}
        right={<button className="btn btn-ghost btn-icon" onClick={onMenu} title="All settings"><Icon name="more-horizontal" size={16} /></button>}
      />
      <div className="syfo-phone-body">
        {/* Profile */}
        <SidebarSection label={<span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}><Icon name="monitor" size={12} /> Profile</span>} />
        <article className="syfo-phone-card" style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 14 }}>
          <div>
            <label className="field-label">Name</label>
            <input className="input" defaultValue={WORKSPACE.name} />
          </div>
          <div>
            <label className="field-label">Slug</label>
            <input className="input" defaultValue={WORKSPACE.slug} readOnly style={{ background: 'var(--bg-sunken)', color: 'var(--fg-2)' }} />
          </div>
          <div>
            <Button variant="primary">Save profile</Button>
          </div>
        </article>

        {/* Pre-join agreement */}
        <SidebarSection label={<span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}><Icon name="log" size={12} /> Pre-join agreement</span>} />
        <article className="syfo-phone-card" style={{ marginBottom: 14 }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: 'var(--fg-1)', marginBottom: 6 }}>Require agreement before joining</div>
          <p style={{ fontSize: 12.5, color: 'var(--fg-2)', margin: '0 0 12px', lineHeight: '17px' }}>
            New invite-link and community joins must accept the current version before membership is created.
          </p>
          <button
            onClick={() => setAgreement(a => !a)}
            className="btn"
            style={{
              width: '100%', justifyContent: 'center',
              background: agreement ? 'var(--accent)' : 'var(--bg-sunken)',
              color: agreement ? 'var(--fg-inverse)' : 'var(--fg-2)',
              border: '1px solid ' + (agreement ? 'var(--accent)' : 'var(--border-2)'),
              fontWeight: 600,
            }}
          >
            {agreement ? 'Enabled' : 'Disabled'}
          </button>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 12, gap: 10 }}>
            <span className="meta" style={{ fontSize: 11, flex: 1, lineHeight: '15px' }}>Saving creates a new version; previous accepted versions remain auditable.</span>
            <Button variant="primary" size="sm">Save</Button>
          </div>
        </article>

        {/* Owners & Admins */}
        <SidebarSection label={<span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}><Icon name="shield" size={12} /> Owners & admins · 2</span>} />
        <article className="syfo-phone-card" style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 14 }}>
          <div style={{ fontSize: 13, color: 'var(--fg-2)', fontWeight: 500 }}>Add owner/admin</div>
          <div>
            <label className="field-label">Member</label>
            <select className="input">
              <option>Select member…</option>
              {MEMBERS.slice(0, 6).map(m => <option key={m.id}>{m.name}</option>)}
            </select>
          </div>
          <div>
            <label className="field-label">Role</label>
            <select className="input" value={role} onChange={e => setRole(e.target.value)}>
              <option>Admin</option>
              <option>Owner</option>
            </select>
          </div>
          <Button variant="secondary">Update role</Button>
        </article>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 12 }}>
          {HUMANS.map(h => (
            <div key={h.id} style={{
              display: 'flex', alignItems: 'center', gap: 10, padding: '8px 10px',
              background: 'var(--bg-surface)', border: '1px solid var(--border-1)',
              borderRadius: 'var(--radius-sm)',
            }}>
              <Avatar name={h.name} size="sm" presence={h.presence} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13.5, fontWeight: 500 }}>{h.name}</div>
                <div className="meta">{h.handle}</div>
              </div>
              <Chip tone={h.role === 'Owner' ? 'accent' : 'neutral'}>{h.role}</Chip>
            </div>
          ))}
        </div>

        <button onClick={onMenu} className="btn btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
          All settings <Icon name="chevron-right" size={13} />
        </button>
      </div>
    </>
  );
}

function MobileSettingsGroup({ title, children }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{
        fontFamily: 'var(--font-mono)', fontSize: 10.5, letterSpacing: '0.08em',
        textTransform: 'uppercase', color: 'var(--fg-3)', fontWeight: 500,
        padding: '4px 4px 8px',
      }}>{title}</div>
      <div style={{
        background: 'var(--bg-surface)', border: '1px solid var(--border-1)',
        borderRadius: 'var(--radius-md)', overflow: 'hidden',
      }}>
        {children}
      </div>
    </div>
  );
}

function MobileSettingsRow({ icon, label, trailing, tone, onClick }) {
  return (
    <button onClick={onClick} style={{
      width: '100%', display: 'flex', alignItems: 'center', gap: 12, padding: '12px 14px',
      borderBottom: '1px solid var(--border-1)', border: 0, background: 'transparent',
      cursor: onClick ? 'pointer' : 'default', textAlign: 'left',
    }}>
      <Icon name={icon} size={16} style={{ color: tone === 'danger' ? 'var(--danger)' : 'var(--fg-2)' }} />
      <span style={{ flex: 1, fontSize: 14, color: tone === 'danger' ? 'var(--danger)' : 'var(--fg-1)' }}>{label}</span>
      {trailing ? <span className="meta">{trailing}</span> : null}
      <Icon name="chevron-right" size={14} style={{ color: 'var(--fg-3)' }} />
    </button>
  );
}

function MobileSettingsDetail({ section, onBack, onOpen }) {
  const titles = {
    account: 'Account', members: 'Members', runtimes: 'Runtimes', computers: 'Computers', audit: 'Audit log',
  };
  if (section === 'computers') {
    return (
      <>
        <MobileHeader title="Computers" subtitle={`${COMPUTERS.length} connected`} back={onBack} />
        <div className="syfo-phone-body">
          {COMPUTERS.map(c => (
            <button key={c.id} onClick={() => onOpen({ type: 'computer', id: c.id })}
              className="syfo-phone-card" style={{ width: '100%', textAlign: 'left', display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer' }}>
              <span style={{
                width: 36, height: 36, borderRadius: 'var(--radius-xs)',
                background: 'var(--accent-soft)', color: 'var(--accent-strong)',
                display: 'inline-flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
              }}>
                <Icon name="monitor" size={18} />
              </span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 14, fontWeight: 600, display: 'flex', alignItems: 'center', gap: 6 }}>
                  {c.name} <PresenceDot presence={c.presence} />
                </div>
                <div className="meta">{c.os} · daemon {c.daemon} · {c.agentIds.length} agents</div>
              </div>
              <Icon name="chevron-right" size={14} style={{ color: 'var(--fg-3)' }} />
            </button>
          ))}
        </div>
      </>
    );
  }
  if (section === 'runtimes') {
    const runtimes = [
      { name: 'Codex CLI',   status: 'online', agents: 7 },
      { name: 'Claude Code', status: 'online', agents: 3 },
      { name: 'breeze',      status: 'busy',   agents: 1 },
    ];
    return (
      <>
        <MobileHeader title="Runtimes" subtitle="3 connected" back={onBack} />
        <div className="syfo-phone-body">
          {runtimes.map(r => (
            <article key={r.name} className="syfo-phone-card" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <Icon name="cpu" size={18} style={{ color: 'var(--fg-2)' }} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 14, fontWeight: 600 }}>{r.name}</div>
                <div className="meta" style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                  <PresenceDot presence={r.status} />{r.status} · {r.agents} agents
                </div>
              </div>
              <Button variant="secondary" size="sm">Configure</Button>
            </article>
          ))}
        </div>
      </>
    );
  }
  if (section === 'account') {
    return (
      <>
        <MobileHeader title="Account" subtitle="@tonyren" back={onBack} />
        <div className="syfo-phone-body">
          <article className="syfo-phone-card" style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <Avatar name="tonyren" size="xl" />
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 15, fontWeight: 600 }}>tonyren</div>
              <div className="meta">@tonyren</div>
            </div>
          </article>
          <article className="syfo-phone-card" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <div><label className="field-label">Name</label><input className="input" defaultValue="tonyren" /></div>
            <div><label className="field-label">Email</label><input className="input" defaultValue="ren.dongni@gmail.com" /></div>
            <Button variant="primary">Save</Button>
          </article>
        </div>
      </>
    );
  }
  if (section === 'audit') {
    return (
      <>
        <MobileHeader title="Audit log" subtitle="90-day retention" back={onBack} />
        <div className="syfo-phone-body">
          {ACTIVITY.map(a => {
            const actor = memberById(a.actorId);
            return (
              <article key={a.id} className="syfo-phone-card" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <Avatar name={actor.name} kind={actor.kind} size="sm" />
                <div style={{ flex: 1, minWidth: 0, fontSize: 13, lineHeight: '18px' }}>
                  <span style={{ fontWeight: 500 }}>{actor.name}</span>{' '}
                  <span style={{ color: 'var(--fg-2)' }}>{a.verb}</span>{' '}
                  <span style={{ color: 'var(--fg-1)' }}>{a.object}</span>
                </div>
                <span className="meta" style={{ fontSize: 10.5 }}>{a.ts}</span>
              </article>
            );
          })}
        </div>
      </>
    );
  }
  return (
    <>
      <MobileHeader title={titles[section] || 'Settings'} back={onBack} />
      <div className="syfo-phone-body">
        <article className="syfo-phone-card" style={{ color: 'var(--fg-3)', fontSize: 13, textAlign: 'center', padding: '24px 16px' }}>
          {titles[section] || 'Settings'} mobile view.
        </article>
      </div>
    </>
  );
}

// ============================================================
//   COMPUTER detail
// ============================================================
function MobileComputer({ computerId, onBack }) {
  const c = COMPUTERS.find(x => x.id === computerId) || COMPUTERS[0];
  return (
    <>
      <MobileHeader title={c.name} subtitle={c.os} back={onBack}
        right={<button className="btn btn-ghost btn-icon"><Icon name="pencil" size={16} /></button>}
      />
      <div className="syfo-phone-body">
        <article className="syfo-phone-card" style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 16 }}>
          <span style={{
            width: 48, height: 48, borderRadius: 'var(--radius-sm)',
            background: 'var(--accent-soft)', color: 'var(--accent-strong)',
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Icon name="monitor" size={22} />
          </span>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 15, fontWeight: 600 }}>{c.name}</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 4 }}>
              <PresenceDot presence={c.presence} />
              <span style={{ fontSize: 12.5, color: 'var(--fg-2)' }}>Connected</span>
            </div>
          </div>
        </article>

        <SidebarSection label="Info" />
        <article className="syfo-phone-card" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <MobileKV k="OS"      v={<span style={{ fontFamily: 'var(--font-mono)' }}>{c.os}</span>} />
          <MobileKV k="Daemon"  v={<span style={{ fontFamily: 'var(--font-mono)' }}>{c.daemon}</span>} />
          <MobileKV k="创建于" v={<span style={{ fontFamily: 'var(--font-mono)' }}>{c.created}</span>} />
        </article>

        <SidebarSection label="Detected runtimes" />
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 14 }}>
          {Object.entries(c.runtimes).map(([name, installed]) => (
            <span key={name} style={{
              display: 'inline-flex', alignItems: 'center', gap: 4,
              padding: '4px 8px', borderRadius: 'var(--radius-xs)',
              fontFamily: 'var(--font-mono)', fontSize: 11,
              background: installed ? 'var(--accent-soft)' : 'var(--bg-sunken)',
              color: installed ? 'var(--accent-strong)' : 'var(--fg-3)',
            }}>
              {installed ? <Icon name="check" size={10} /> : null}
              {name}
            </span>
          ))}
        </div>

        <SidebarSection label={`Agents on this computer · ${c.agentIds.length}`} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
          {c.agentIds.map(aid => {
            const a = memberById(aid);
            return (
              <div key={aid} style={{
                display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px',
                background: 'var(--bg-surface)', border: '1px solid var(--border-1)',
                borderRadius: 'var(--radius-sm)', marginBottom: 6,
              }}>
                <Avatar name={a.name} kind="agent" size="sm" />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 13.5, fontWeight: 500 }}>{a.name}</div>
                  <div className="meta">{a.runtime}</div>
                </div>
                <PresenceDot presence={a.presence === 'thinking' ? 'online' : a.presence} />
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}

Object.assign(window, { MobileApp });
