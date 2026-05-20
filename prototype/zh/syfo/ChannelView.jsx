// Syfo UI Kit — Channel view (top bar + tabs + chat/tasks/files)

function ChannelView({ channelId }) {
  const channel = CHANNELS.find(c => c.id === channelId) || CHANNELS[0];
  const [tab, setTab] = React.useState('chat');
  const tabs = [
    { id: 'chat',     label: '聊天',     icon: 'message-square' },
    { id: 'tasks',    label: '任务',    icon: 'list-todo', count: TASKS.length },
    { id: 'files',    label: '文件',    icon: 'paperclip', count: FILES.length },
    { id: 'audit',    label: '审计',    icon: 'shield' },
  ];
  return (
    <section className="syfo-content">
      <ChannelTopbar channel={channel} />
      <div className="syfo-tabs">
        {tabs.map(t => (
          <button
            key={t.id}
            className={'syfo-tab' + (tab === t.id ? ' is-active' : '')}
            onClick={() => setTab(t.id)}
          >
            <Icon name={t.icon} size={14} />
            <span>{t.label}</span>
            {t.count != null ? <span className="count">{t.count}</span> : null}
          </button>
        ))}
      </div>
      {tab === 'chat'  ? <ChatPane /> : null}
      {tab === 'tasks' ? <TasksPane /> : null}
      {tab === 'files' ? <FilesPane /> : null}
      {tab === 'audit' ? <AuditPane /> : null}
    </section>
  );
}

function ChannelTopbar({ channel }) {
  return (
    <header className="syfo-topbar">
      <div className="title-block">
        <Icon name={channel.glyph} size={16} style={{ color: 'var(--accent)' }} />
        <div className="title">{channel.name}</div>
        <span style={{ width: 1, height: 14, background: 'var(--border-2)', display: 'inline-block' }} />
        <div className="subtitle">It's the core team of www.gofindbird.com</div>
      </div>
      <div className="actions">
        <Button variant="ghost" leading={<Icon name="users" size={14} />}>4</Button>
        <Button variant="ghost" icon><Icon name="search" size={14} /></Button>
        <Button variant="ghost" icon><Icon name="more-horizontal" size={14} /></Button>
      </div>
    </header>
  );
}

// ---------- Chat ----------
function ChatPane() {
  return (
    <div className="syfo-panel" style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, padding: '20px 24px 8px', maxWidth: 980, width: '100%', margin: '0 auto' }}>
        <DayDivider label="今日" />
        {MESSAGES.map(m => <Message key={m.id} m={m} />)}
        <ThinkingIndicator agent={memberById('tio')} />
      </div>
      <Composer />
    </div>
  );
}

function DayDivider({ label }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '8px 0 18px' }}>
      <div className="divider" style={{ flex: 1 }} />
      <span className="meta" style={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{label}</span>
      <div className="divider" style={{ flex: 1 }} />
    </div>
  );
}

function Message({ m }) {
  const a = memberById(m.authorId);
  if (m.kind === 'task-created' || m.kind === 'agent-action') {
    return (
      <div style={{ display: 'flex', gap: 12, padding: '6px 0 6px 36px', alignItems: 'center' }}>
        <Icon name={m.kind === 'task-created' ? 'list-todo' : 'check'} size={14} style={{ color: 'var(--fg-3)' }} />
        <span className="meta" style={{ color: 'var(--fg-2)', fontFamily: 'var(--font-sans)' }}>
          <strong style={{ fontWeight: 500, color: 'var(--fg-1)' }}>{a.name}</strong>
          {' '}
          {m.body}
        </span>
        <span className="meta" style={{ marginLeft: 'auto' }}>{m.ts}</span>
      </div>
    );
  }
  return (
    <div style={{ display: 'flex', gap: 12, padding: '10px 0' }}>
      <Avatar name={a.name} kind={a.kind} size="md" presence={a.presence} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
          <span style={{ fontWeight: 600, fontSize: 14, color: 'var(--fg-1)' }}>{a.name}</span>
          {a.kind === 'agent' ? <Chip tone="accent">Agent</Chip> : null}
          <span className="meta">{m.ts}</span>
        </div>
        <div style={{ fontSize: 14, lineHeight: '22px', color: 'var(--fg-1)', marginTop: 2 }}>
          {m.body}
        </div>
        {m.reactions ? (
          <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>
            {m.reactions.map((r, i) => (
              <span key={i} style={{
                fontFamily: 'var(--font-mono)', fontSize: 11,
                padding: '2px 8px', border: '1px solid var(--border-1)',
                borderRadius: 'var(--radius-xs)', background: 'var(--bg-surface)',
                color: 'var(--fg-2)'
              }}>👀 {r.count}</span>
            ))}
          </div>
        ) : null}
      </div>
    </div>
  );
}

function ThinkingIndicator({ agent }) {
  return (
    <div style={{ display: 'flex', gap: 12, padding: '10px 0', alignItems: 'center' }}>
      <Avatar name={agent.name} kind="agent" size="md" presence="thinking" />
      <span style={{ fontSize: 13.5, color: 'var(--fg-2)', display: 'flex', alignItems: 'center', gap: 6 }}>
        <strong style={{ color: 'var(--fg-1)', fontWeight: 600 }}>{agent.name}</strong> is thinking
        <ThinkingDots />
      </span>
    </div>
  );
}
function ThinkingDots() {
  return (
    <span style={{ display: 'inline-flex', gap: 3 }}>
      {[0,1,2].map(i => (
        <span key={i} style={{
          width: 4, height: 4, borderRadius: '50%', background: 'var(--accent)',
          animation: `syfoPulse 1.2s ${i*0.2}s infinite var(--ease-out)`
        }}/>
      ))}
      <style>{`@keyframes syfoPulse { 0%, 60%, 100% { opacity: 0.25 } 30% { opacity: 1 } }`}</style>
    </span>
  );
}

function Composer() {
  const [text, setText] = React.useState('');
  const [asTask, setAsTask] = React.useState(false);
  return (
    <div style={{ borderTop: '1px solid var(--border-1)', background: 'var(--bg-paper)', padding: '14px 24px 18px' }}>
      <div style={{ maxWidth: 980, margin: '0 auto', display: 'flex', flexDirection: 'column',
                    border: '1px solid var(--border-2)', borderRadius: 'var(--radius-md)',
                    background: 'var(--bg-surface)', overflow: 'hidden' }}>
        <textarea
          className="input"
          rows={2}
          value={text}
          placeholder="在 #GoFindBird 发送消息 · @ 提及 AI · / 使用命令"
          onChange={e => setText(e.target.value)}
          style={{ height: 'auto', minHeight: 52, border: 0, padding: '12px 14px',
                   resize: 'none', fontFamily: 'var(--font-sans)', fontSize: 14, lineHeight: '20px',
                   background: 'transparent', boxShadow: 'none' }}
        />
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                      padding: '6px 8px 8px', gap: 8 }}>
          <div style={{ display: 'flex', gap: 2 }}>
            <Button variant="ghost" icon title="提及"><Icon name="at-sign" size={14} /></Button>
            <Button variant="ghost" icon title="附件"><Icon name="paperclip" size={14} /></Button>
            <Button variant="ghost" icon title="图片"><Icon name="image" size={14} /></Button>
            <Button variant="ghost" icon title="命令"><Icon name="command" size={14} /></Button>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12.5, color: 'var(--fg-2)', cursor: 'pointer' }}>
              <input type="checkbox" checked={asTask} onChange={e => setAsTask(e.target.checked)} />
              As task
            </label>
            <Button variant="primary" leading={<Icon name="send" size={13} />}>Send</Button>
          </div>
        </div>
      </div>
    </div>
  );
}

// ---------- Tasks tab (board) ----------
const STATUS_META = {
  'backlog':     { label: '待办',     tone: 'neutral' },
  'in-progress': { label: '进行中', tone: 'accent'  },
  'in-review':   { label: '审核中',   tone: 'info'    },
  'done':        { label: '已完成',        tone: 'success' },
  'blocked':     { label: '阻塞',     tone: 'warning' },
};

function TasksPane() {
  const cols = ['in-progress', 'in-review', 'done'];
  return (
    <div className="syfo-panel" style={{ padding: '20px 24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Button variant="secondary" size="sm" leading={<Icon name="users" size={12} />} trailing={<Icon name="chevron-down" size={12} />}>Assignee</Button>
          <Button variant="secondary" size="sm" leading={<Icon name="sliders" size={12} />} trailing={<Icon name="chevron-down" size={12} />}>Filter</Button>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{ display: 'flex', border: '1px solid var(--border-2)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
            <button className="btn btn-sm" style={{ borderRadius: 0, background: 'var(--bg-sunken)', border: 0 }}>Board</button>
            <button className="btn btn-sm" style={{ borderRadius: 0, border: 0, borderLeft: '1px solid var(--border-2)' }}>List</button>
          </div>
          <Button variant="primary" size="sm" leading={<Icon name="plus" size={13} />}>New task</Button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
        {cols.map(status => {
          const items = TASKS.filter(t => t.status === status);
          const meta = STATUS_META[status];
          return (
            <div key={status} style={{ display: 'flex', flexDirection: 'column', gap: 10, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 4px' }}>
                <Chip tone={meta.tone}>{meta.label}</Chip>
                <span className="meta">{items.length}</span>
              </div>
              {items.map(t => <TaskCard key={t.id} task={t} />)}
              <button className="btn btn-ghost" style={{ justifyContent: 'flex-start', color: 'var(--fg-3)', fontWeight: 400 }}>
                <Icon name="plus" size={13} /> Add task
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function TaskCard({ task }) {
  const a = memberById(task.assigneeId);
  const meta = STATUS_META[task.status];
  return (
    <div className="card card-hover" style={{ padding: '12px 14px', display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div className="meta" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <span style={{ color: 'var(--fg-1)' }}>#{task.id}</span>
        <span>·</span>
        <span>#{task.channel}</span>
      </div>
      <div style={{ fontSize: 13.5, lineHeight: '20px', color: 'var(--fg-1)' }}>{task.title}</div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 4 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Avatar name={a.name} kind={a.kind} size="sm" />
          <span style={{ fontSize: 12.5, color: 'var(--fg-2)' }}>{a.name}</span>
        </div>
        <span className="meta">{task.updated}</span>
      </div>
    </div>
  );
}

// ---------- Files tab ----------
function FilesPane() {
  return (
    <div className="syfo-panel" style={{ padding: '20px 24px' }}>
      <div className="card" style={{ overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13.5 }}>
          <thead>
            <tr style={{ background: 'var(--bg-paper)' }}>
              {['名称','类型','大小','上传者','时间'].map(h => (
                <th key={h} style={{
                  textAlign: 'left', padding: '10px 14px',
                  fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.04em',
                  textTransform: 'uppercase', color: 'var(--fg-2)', fontWeight: 500,
                  borderBottom: '1px solid var(--border-1)'
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {FILES.map((f, i) => {
              const u = memberById(f.uploaderId);
              return (
                <tr key={f.id} style={{ borderBottom: i < FILES.length - 1 ? '1px solid var(--border-1)' : 0 }}>
                  <td style={{ padding: '12px 14px', display: 'flex', alignItems: 'center', gap: 10 }}>
                    <Icon name="paperclip" size={14} style={{ color: 'var(--fg-3)' }} />
                    <span style={{ color: 'var(--fg-1)' }}>{f.name}</span>
                  </td>
                  <td style={{ padding: '12px 14px' }}><Chip>{f.mime}</Chip></td>
                  <td style={{ padding: '12px 14px', fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--fg-2)' }}>{f.size}</td>
                  <td style={{ padding: '12px 14px' }}>
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                      <Avatar name={u.name} kind={u.kind} size="sm" />
                      <span style={{ color: 'var(--fg-2)' }}>{u.name}</span>
                    </span>
                  </td>
                  <td style={{ padding: '12px 14px', fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--fg-3)' }}>{f.ts}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AuditPane() {
  return (
    <div className="syfo-panel" style={{ padding: '20px 24px', maxWidth: 720, margin: '0 auto', width: '100%' }}>
      <div className="syfo-h2" style={{ marginBottom: 4 }}>Channel audit</div>
      <p className="meta" style={{ marginBottom: 18 }}>Every state change in #GoFindBird, with actor and timestamp.</p>
      <ActivityList />
    </div>
  );
}

Object.assign(window, { ChannelView, TaskCard, TasksPane, STATUS_META });
