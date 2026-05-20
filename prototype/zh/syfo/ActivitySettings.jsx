// Syfo UI Kit — Activity (audit) + Settings views

function ActivityView() {
  const [filter, setFilter] = React.useState('all');
  const filtered = NOTIFICATIONS.filter(n => filter === 'all' || (filter === 'unread' && n.newCount > 0) || (filter === 'mentions' && n.mentions));
  return (
    <section className="syfo-content">
      <header className="syfo-topbar">
        <div className="title-block">
          <Icon name="activity" size={16} style={{ color: 'var(--fg-2)' }} />
          <div className="title">Activity</div>
          <div className="subtitle">240 active · 13 unread</div>
        </div>
        <div className="actions">
          <Button variant="secondary" size="sm">Mark all read</Button>
        </div>
      </header>
      <div style={{ padding: '12px 24px 0' }}>
        <div style={{ display: 'inline-flex', border: '1px solid var(--border-2)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
          {['all','unread','mentions'].map(k => (
            <button
              key={k}
              onClick={() => setFilter(k)}
              className="btn btn-sm"
              style={{
                borderRadius: 0, border: 0,
                background: filter === k ? 'var(--bg-sunken)' : 'transparent',
                color: filter === k ? 'var(--fg-1)' : 'var(--fg-2)',
                fontWeight: filter === k ? 500 : 400,
                textTransform: 'capitalize',
                borderLeft: k !== 'all' ? '1px solid var(--border-2)' : 0,
              }}
            >{k}</button>
          ))}
        </div>
      </div>
      <div className="syfo-panel" style={{ padding: '16px 24px 32px', maxWidth: 940, margin: '0 auto', width: '100%' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {filtered.map(n => <NotificationCard key={n.id} n={n} />)}
        </div>
      </div>
    </section>
  );
}

function NotificationCard({ n }) {
  return (
    <article className="card" style={{ padding: '14px 16px', display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13 }}>
        <span style={{ color: 'var(--accent-strong)', fontWeight: 600 }}>{n.channel}</span>
        <span className="meta">{n.ts}</span>
        <div style={{ flex: 1 }} />
        <button className="btn btn-ghost btn-icon" title="标为已读" style={{ width: 26, height: 26 }}>
          <Icon name="check" size={13} />
        </button>
      </div>
      {n.body ? (
        <div style={{ fontSize: 13.5, lineHeight: '20px', color: 'var(--fg-1)', display: 'flex', alignItems: 'flex-start', gap: 8 }}>
          <Icon name="message-square" size={13} style={{ color: 'var(--accent)', marginTop: 4, flexShrink: 0 }} />
          <span>{n.body}</span>
        </div>
      ) : null}
      {n.replyText ? (
        <div style={{ fontSize: 13, lineHeight: '19px', color: 'var(--fg-2)' }}>
          <span style={{ color: 'var(--fg-1)', fontWeight: 500 }}>{n.replyAuthor}:</span> {n.replyText}
        </div>
      ) : null}
      {(n.replies > 0 || n.newCount > 0 || n.mentions) ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 2 }}>
          {n.replies > 0 ? <span className="meta">{n.replies} replies</span> : null}
          {n.mentions ? <Chip tone="accent">@ you</Chip> : null}
          {n.newCount > 0 ? <Chip tone="accent">{n.newCount} new</Chip> : null}
        </div>
      ) : null}
    </article>
  );
}

function ActivityList({ compact }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {ACTIVITY.map((a, i) => {
        const actor = memberById(a.actorId);
        return (
          <div key={a.id} style={{
            display: 'flex', alignItems: 'center', gap: 12,
            padding: compact ? '8px 0' : '12px 8px',
            borderBottom: i < ACTIVITY.length - 1 ? '1px solid var(--border-1)' : 0,
          }}>
            <Avatar name={actor.name} kind={actor.kind} size="sm" />
            <div style={{ flex: 1, minWidth: 0, fontSize: 13.5, lineHeight: '20px' }}>
              <span style={{ fontWeight: 500, color: 'var(--fg-1)' }}>{actor.name}</span>{' '}
              <span style={{ color: 'var(--fg-2)' }}>{a.verb}</span>{' '}
              <span style={{ color: 'var(--fg-1)', fontFamily: a.kind === 'system' || a.kind === 'git' ? 'var(--font-mono)' : 'var(--font-sans)' }}>{a.object}</span>
            </div>
            <ActivityTag kind={a.kind} />
            <span className="meta" style={{ minWidth: 64, textAlign: 'right' }}>{a.ts}</span>
          </div>
        );
      })}
    </div>
  );
}

function ActivityTag({ kind }) {
  const map = {
    deploy:   { tone: 'success', label: 'deploy' },
    git:      { tone: 'info',    label: 'git' },
    system:   { tone: 'neutral', label: 'system' },
    task:     { tone: 'accent',  label: 'task' },
    approval: { tone: 'success', label: 'approval' },
    settings: { tone: 'neutral', label: 'settings' },
    invite:   { tone: 'info',    label: 'invite' },
  };
  const m = map[kind] || { tone: 'neutral', label: kind };
  return <Chip tone={m.tone}>{m.label}</Chip>;
}

// ---------- Settings ----------
function SettingsView() {
  const sections = [
    { id: 'account',     label: '账户',   icon: 'users' },
    { id: 'workspace',   label: '工作区', icon: 'monitor' },
    { id: 'members',     label: '成员',   icon: 'users' },
    { id: 'permissions', label: '权限', icon: 'shield' },
    { id: 'runtimes',    label: '运行时',  icon: 'cpu' },
    { id: 'audit',       label: '审计日志', icon: 'log' },
    { id: 'billing',     label: '账单',   icon: 'inbox' },
  ];
  const [section, setSection] = React.useState('account');
  return (
    <section className="syfo-content">
      <header className="syfo-topbar">
        <div className="title-block">
          <Icon name="settings" size={16} style={{ color: 'var(--fg-2)' }} />
          <div className="title">Settings</div>
          <div className="subtitle">{WORKSPACE.name}</div>
        </div>
      </header>
      <div style={{ flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: '240px 1fr' }}>
        <aside style={{ borderRight: '1px solid var(--border-1)', padding: '16px 12px', overflowY: 'auto' }}>
          {sections.map(s => (
            <button
              key={s.id}
              onClick={() => setSection(s.id)}
              className="syfo-channel-item"
              style={{
                background: section === s.id ? 'var(--accent-soft)' : 'transparent',
                color: section === s.id ? 'var(--accent-strong)' : 'var(--fg-1)',
                fontWeight: section === s.id ? 500 : 400,
                marginBottom: 2,
              }}
            >
              <Icon name={s.icon} size={14} className="glyph" />
              <span className="name">{s.label}</span>
            </button>
          ))}
        </aside>
        <div style={{ overflowY: 'auto', padding: '24px 32px 48px', maxWidth: 760 }}>
          {section === 'account'     && <AccountSettings />}
          {section === 'workspace'   && <WorkspaceSettings />}
          {section === 'members'     && <MembersSettings />}
          {section === 'permissions' && <EmptyState title="暂无自定义权限" body="为此工作区中的人类与 AI 设定角色与权限范围。" icon="shield" />}
          {section === 'runtimes'    && <RuntimesSettings />}
          {section === 'audit'       && <AuditSettings />}
          {section === 'billing'     && <EmptyState title="免费版" body="当前为免费版。升级后可添加更多 AI 运行时与更长的审计保留时间。" icon="inbox" />}
        </div>
      </div>
    </section>
  );
}

function AccountSettings() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
      <div>
        <h1 className="syfo-h1" style={{ margin: '0 0 6px' }}>Account</h1>
        <p style={{ color: 'var(--fg-2)', fontSize: 13.5, margin: 0 }}>Your personal profile across workspaces.</p>
      </div>

      <div className="card card-pad">
        <SectionLabel style={{ padding: '0 0 14px' }}>Profile</SectionLabel>

        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 20 }}>
          <Avatar name="tonyren" size="xl" />
          <div>
            <div style={{ fontSize: 17, fontWeight: 600 }}>tonyren</div>
            <div className="meta">@tonyren</div>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
            <Button variant="secondary" size="sm">Change avatar</Button>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div>
            <label className="field-label">Name</label>
            <input className="input" defaultValue="tonyren" />
          </div>
          <div>
            <label className="field-label">Display name</label>
            <input className="input" defaultValue="tonyren" />
          </div>
          <div>
            <label className="field-label">Email</label>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <input className="input" defaultValue="ren.dongni@gmail.com" style={{ flex: 1 }} />
              <Chip tone="success" leading={<Icon name="shield" size={11} />}>Verified</Chip>
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
            <Button variant="primary">Save profile</Button>
            <Button variant="ghost">Discard</Button>
          </div>
        </div>
      </div>

      <div className="card card-pad">
        <SectionLabel style={{ padding: '0 0 14px' }}>Connected accounts</SectionLabel>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <ConnectedAccountRow label="Google" status="未连接" />
          <ConnectedAccountRow label="GitHub" status="未连接" />
        </div>
      </div>

      <div className="card card-pad" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <SectionLabel style={{ padding: '0 0 6px' }}>Change password</SectionLabel>
          <p style={{ fontSize: 13, color: 'var(--fg-2)', margin: 0 }}>Set or rotate your account password.</p>
        </div>
        <Button variant="secondary" trailing={<Icon name="chevron-right" size={13} />}>Open</Button>
      </div>

      <div>
        <SectionLabel style={{ padding: '0 0 10px' }}>Session</SectionLabel>
        <div className="card card-pad" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div style={{ fontSize: 13.5, color: 'var(--fg-1)', fontWeight: 500 }}>Active session · this browser</div>
            <div className="meta" style={{ marginTop: 2 }}>Last active just now · macOS · Chrome</div>
          </div>
          <Button variant="secondary" size="sm">Sign out</Button>
        </div>
      </div>
    </div>
  );
}

function ConnectedAccountRow({ label, status }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 12, padding: '12px 14px',
      border: '1px solid var(--border-1)', borderRadius: 'var(--radius-sm)',
      background: 'var(--bg-surface)',
    }}>
      <span style={{
        width: 28, height: 28, borderRadius: 'var(--radius-xs)',
        background: 'var(--bg-sunken)', color: 'var(--fg-1)', fontWeight: 600,
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
      }}>{label[0]}</span>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 13.5, fontWeight: 500 }}>{label}</div>
        <div className="meta">{status}</div>
      </div>
      <Button variant="secondary" size="sm">Connect</Button>
    </div>
  );
}

function WorkspaceSettings() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
      <div>
        <h1 className="syfo-h1" style={{ margin: '0 0 6px' }}>Workspace</h1>
        <p style={{ color: 'var(--fg-2)', fontSize: 13.5, margin: 0 }}>Profile and pre-join agreement.</p>
      </div>

      <div className="card card-pad">
        <SectionLabel style={{ padding: '0 0 14px' }}>Profile</SectionLabel>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div>
            <label className="field-label">Name</label>
            <input className="input" defaultValue="mini-pinecorn" />
          </div>
          <div>
            <label className="field-label">Slug</label>
            <input className="input" defaultValue="mini-pinecorn" style={{ background: 'var(--bg-sunken)', color: 'var(--fg-2)' }} readOnly />
            <div className="field-hint">Used in URLs and the @workspace handle. Contact support to change.</div>
          </div>
          <div>
            <label className="field-label">Description</label>
            <textarea
              className="input"
              defaultValue="Atlas — GoFindBird 团队与其 AI 协作研发的研究工作区。"
              rows={3}
              style={{ height: 'auto', padding: '10px 12px', resize: 'vertical', fontFamily: 'var(--font-sans)' }}
            />
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <Button variant="primary">Save profile</Button>
            <Button variant="ghost">Discard</Button>
          </div>
        </div>
      </div>

      <div className="card card-pad">
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16 }}>
          <div>
            <SectionLabel style={{ padding: '0 0 6px' }}>Pre-join agreement</SectionLabel>
            <h2 className="syfo-h3" style={{ margin: '0 0 6px' }}>Require agreement before joining</h2>
            <p style={{ fontSize: 13, color: 'var(--fg-2)', margin: 0, maxWidth: 460 }}>
              New invite-link and community joins must accept the current version before membership is created.
            </p>
          </div>
          <Toggle />
        </div>
        <div className="meta" style={{ marginTop: 18 }}>
          Saving creates a new version; previous accepted versions remain auditable.
        </div>
      </div>
    </div>
  );
}

function Toggle({ defaultOn }) {
  const [on, setOn] = React.useState(!!defaultOn);
  return (
    <button
      onClick={() => setOn(!on)}
      style={{
        width: 36, height: 20, borderRadius: 999, border: 0, cursor: 'pointer', padding: 2,
        background: on ? 'var(--accent)' : 'var(--border-2)',
        position: 'relative', transition: 'background var(--dur-fast) var(--ease-out)',
        flexShrink: 0,
      }}
      aria-pressed={on}
    >
      <span style={{
        position: 'absolute', top: 2, left: on ? 18 : 2,
        width: 16, height: 16, borderRadius: '50%', background: 'var(--bg-surface)',
        transition: 'left var(--dur-fast) var(--ease-out)',
        boxShadow: '0 1px 2px rgba(17,19,26,0.12)'
      }}/>
    </button>
  );
}

function MembersSettings() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <h1 className="syfo-h1" style={{ margin: '0 0 6px' }}>Members</h1>
        <p style={{ color: 'var(--fg-2)', fontSize: 13.5, margin: 0 }}>Owners and admins · {HUMANS.length} humans, {AGENTS.length} agents.</p>
      </div>
      <div className="card" style={{ overflow: 'hidden' }}>
        {MEMBERS.slice(0, 8).map((m, i) => (
          <div key={m.id} style={{
            display: 'flex', alignItems: 'center', gap: 12, padding: '12px 16px',
            borderBottom: i < 7 ? '1px solid var(--border-1)' : 0,
          }}>
            <Avatar name={m.name} kind={m.kind} size="sm" presence={m.presence} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 13.5, color: 'var(--fg-1)', fontWeight: 500 }}>{m.name}</div>
              <div className="meta">{m.desc || m.role}</div>
            </div>
            <Chip tone={m.kind === 'agent' ? 'accent' : 'neutral'}>{m.kind}</Chip>
            <select className="input" style={{ width: 120, height: 28, padding: '0 10px', fontSize: 13 }}>
              <option>{m.role || '成员'}</option>
              <option>Admin</option>
              <option>Owner</option>
            </select>
          </div>
        ))}
      </div>
    </div>
  );
}

function RuntimesSettings() {
  const runtimes = [
    { id: 'codex',   label: 'Codex CLI',   status: 'online',  agents: 6, computer: 'breeze-cobra-99', version: 'daemon v0.51.1' },
    { id: 'cc',      label: 'Claude Code', status: 'online',  agents: 3, computer: "tony's mac mini", version: 'daemon v0.51.0' },
    { id: 'breeze',  label: 'breeze',      status: 'busy',    agents: 1, computer: 'no. cviii',        version: 'daemon v0.50.4' },
  ];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <h1 className="syfo-h1" style={{ margin: '0 0 6px' }}>Runtimes</h1>
        <p style={{ color: 'var(--fg-2)', fontSize: 13.5, margin: 0 }}>Connected daemons that execute agents on your behalf.</p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {runtimes.map(r => (
          <div key={r.id} className="card card-pad" style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <Icon name="cpu" size={20} style={{ color: 'var(--fg-2)' }} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ fontWeight: 600, fontSize: 14 }}>{r.label}</span>
                <PresenceDot presence={r.status} />
                <span style={{ fontSize: 12.5, color: 'var(--fg-2)', textTransform: 'capitalize' }}>{r.status}</span>
              </div>
              <div className="meta" style={{ marginTop: 4 }}>{r.computer} · {r.version} · {r.agents} agents</div>
            </div>
            <Button variant="secondary" size="sm">Configure</Button>
          </div>
        ))}
        <button className="card" style={{
          padding: 16, border: '1px dashed var(--border-2)', background: 'transparent',
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
          color: 'var(--fg-2)', cursor: 'pointer', fontFamily: 'var(--font-sans)', fontSize: 13.5
        }}>
          <Icon name="plus" size={14} /> Connect a new runtime
        </button>
      </div>
    </div>
  );
}

function AuditSettings() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div>
        <h1 className="syfo-h1" style={{ margin: '0 0 6px' }}>Audit log</h1>
        <p style={{ color: 'var(--fg-2)', fontSize: 13.5, margin: 0 }}>Every state change in the workspace, with actor and timestamp. Retention: 90 days on the current plan.</p>
      </div>
      <ActivityList />
    </div>
  );
}

Object.assign(window, { ActivityView, ActivityList, SettingsView, RuntimesSettings });
