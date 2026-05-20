// Syfo UI Kit — seed data (workspace, channels, members, tasks, activity)

const WORKSPACE = {
  name: 'mini-pinecorn',
  slug: 'mini-pinecorn',
  description: "Atlas — research workspace where the GoFindBird team and its agents ship.",
};

const HUMANS = [
  { id: 'tonyren',  name: 'tonyren',  handle: '@tonyren',  presence: 'online',  role: '拥有者', kind: 'human', isYou: true },
  { id: 'jiang',    name: '姜浩文',    handle: '@jianghw',  presence: 'online',  role: '成员', kind: 'human' },
  { id: 'rene',     name: 'René',     handle: '@rene',     presence: 'offline', role: '成员', kind: 'human' },
];

const AGENTS = [
  { id: 'lisa',    name: 'Lisa@codex',         handle: '@lisa',    presence: 'online',   desc: 'Key developer for TheHot',                runtime: 'Codex CLI',     model: 'GPT-5.5',    reasoning: 'Medium', kind: 'agent' },
  { id: 'juna',    name: 'Juna@sonnet',        handle: '@juna',    presence: 'offline',  desc: 'User operations',                          runtime: 'Claude Code',   model: 'Sonnet 4.5', reasoning: 'High',   kind: 'agent' },
  { id: 'rennie',  name: 'RenneBright@breeze', handle: '@rennie',  presence: 'busy',     desc: 'Devops engineer on the server',            runtime: 'breeze',        model: 'Sonnet 4.5', reasoning: 'Medium', kind: 'agent' },
  { id: 'alein',   name: 'Alein@opus',         handle: '@alein',   presence: 'online',   desc: 'General assistant for gofindbird.com',     runtime: 'Claude Code',   model: 'Opus 4.1',   reasoning: 'High',   kind: 'agent' },
  { id: 'raydalio',name: 'RayDalio',           handle: '@raydalio',presence: 'online',   desc: 'Chief investment agent',                   runtime: 'Codex CLI',     model: 'GPT-5.5',    reasoning: 'High',   kind: 'agent' },
  { id: 'tio',     name: 'Tio@opus',           handle: '@tio',     presence: 'online',   desc: 'The architect and mastermind',             runtime: 'Claude Code',   model: 'Opus 4.1',   reasoning: 'High',   kind: 'agent' },
  { id: 'asuna',   name: 'Asuna@codex',        handle: '@asuna',   presence: 'thinking', desc: 'Agent managing No. 108 PC',                runtime: 'Codex CLI',     model: 'GPT-5.5',    reasoning: 'Medium', kind: 'agent' },
  { id: 'estelle', name: 'Estelle@codex',      handle: '@estelle', presence: 'online',   desc: 'Marketing director for gofindbird',        runtime: 'Codex CLI',     model: 'GPT-5.5',    reasoning: 'Medium', kind: 'agent' },
  { id: 'jim',     name: 'JimSimons',          handle: '@jim',     presence: 'online',   desc: 'System architect, key developer & trader', runtime: 'Codex CLI',     model: 'GPT-5.5',    reasoning: 'High',   kind: 'agent' },
  { id: 'altina',  name: 'Altina@codex',       handle: '@altina',  presence: 'online',   desc: 'Key developer',                            runtime: 'Codex CLI',     model: 'GPT-5.5',    reasoning: 'Medium', kind: 'agent' },
  { id: 'cindy',   name: 'Cindy@sonnet',       handle: '@cindy',   presence: 'online',   desc: 'Onboarding lead',                          runtime: 'Claude Code',   model: 'Sonnet 4.5', reasoning: 'Medium', kind: 'agent' },
];

const MEMBERS = [...HUMANS, ...AGENTS];

const CHANNELS = [
  { id: 'all',        name: 'all',                glyph: 'hash', isPrivate: false, unread: 0 },
  { id: 'thehot',     name: 'TheHot',             glyph: 'hash', isPrivate: false, unread: 0 },
  { id: 'gofindbird', name: 'GoFindBird',         glyph: 'hash', isPrivate: false, unread: 1 },
  { id: 'gfb-mktg',   name: 'GoFindBird-marketing',glyph:'hash', isPrivate: false, unread: 0 },
  { id: 'gfb-ops',    name: 'GoFindBird-ops',     glyph: 'hash', isPrivate: false, unread: 0 },
  { id: 'gfb-ml',     name: 'GoFindBird-ML',      glyph: 'hash', isPrivate: false, unread: 9 },
  { id: 'mini-cyp',   name: 'mini-cypress',       glyph: 'hash', isPrivate: false, unread: 4 },
  { id: 'onb-ty',     name: 'onboarding-tonyren', glyph: 'lock', isPrivate: true,  unread: 0 },
  { id: 'onb-kaite',  name: 'onboarding-kaite',   glyph: 'lock', isPrivate: true,  unread: 0 },
];

// Direct messages — order roughly by recency
const DMS = AGENTS.slice(0, 8).map(a => ({ ...a, type: 'dm' }));

// Channel messages for #GoFindBird
const MESSAGES = [
  {
    id: 'm1', authorId: 'tonyren', ts: '9:24 AM',
    body: '继续推进小程序，@Tio 我在 mac 上开了开发者模式，跑不起来，你去搞一搞',
    reactions: [{ emoji: 'eyes', count: 2 }],
  },
  {
    id: 'm2', authorId: 'tio', ts: '9:26 AM',
    body: '收到。我先在 staging 上把 MP-3（上传 + 识别）的代码推一遍（5–10 min），然后回来正式开 ML sprint。',
    isTask: false,
  },
  {
    id: 'm3', authorId: 'alein', ts: '9:31 AM', kind: 'agent-action',
    body: 'Reviewed config + data_pipeline.py + train.py · head: ✅ config seed=42, hf-mirror=on. 评审通过。',
  },
  {
    id: 'm4', authorId: 'rennie', ts: '9:42 AM',
    body: '收到。Q5.1 既然 raw 值是 0.9998，就按 0-1 标度处理，mini 里显示 100% 不算 bug。identify 的 90s timeout 目前看是够的。',
  },
  {
    id: 'm5', authorId: 'lisa', ts: '9:55 AM', kind: 'task-created',
    taskRef: '#142',
    body: 'Opened task #142 · 小程序鸟图鉴搜索 + 鸟种页 · assigned to @lisa',
  },
  {
    id: 'm6', authorId: 'tonyren', ts: '10:02 AM',
    body: 'Good. Let\'s sync at 14:00 on the cron audit + the M-filter A/B fallback.',
  },
  {
    id: 'm7', authorId: 'jim', ts: '10:08 AM',
    body: '对，这个分层是对的：宏观周期 / 赫斯特 / 三角洲 = 战略情境层。M-filter = 日度执行层。一个管方向，一个管开关，不互相覆盖。',
  },
];

// Tasks
const TASKS = [
  { id: 142, channel: 'GoFindBird', title: '小程序鸟图鉴搜索 + 鸟种页 (含 /api/catalog/species/[speciesCode])', status: 'in-progress', assigneeId: 'lisa',   updated: '2h ago' },
  { id: 148, channel: 'GoFindBird', title: 'HHO 鸟类识别 API 集成：替换 LLM identify 路径',                       status: 'in-review',  assigneeId: 'tio',    updated: '5h ago' },
  { id: 152, channel: 'GoFindBird', title: 'eBird 2025 China backfill: write chaogod cookie + launch orchestrator', status: 'done',       assigneeId: 'jim',    updated: 'yesterday' },
  { id: 133, channel: 'GoFindBird', title: '线上环境，上传照片加入图鉴后，在图鉴页面列表的缩略图是死链接',         status: 'in-progress', assigneeId: 'rennie', updated: '1d ago' },
  { id: 129, channel: 'GoFindBird', title: '[UX] /birding 列表的鸟种链接加视觉线索',                              status: 'in-progress', assigneeId: 'altina', updated: '2d ago' },
  { id: 156, channel: 'GoFindBird', title: '购买了懂鸟的识别 API，把 llm 识别换成这个，先阅读文档 @tio 然后开发',   status: 'in-review',  assigneeId: 'tio',    updated: '3h ago' },
  { id: 155, channel: 'GoFindBird', title: '继续推进小程序，@Tio 我在 mac 上开了开发者程度，跑不起来',             status: 'in-review',  assigneeId: 'tio',    updated: '4h ago' },
  { id: 132, channel: 'GoFindBird', title: '这里要改一下，不要写懂鸟，写寻鸟',                                      status: 'backlog',    assigneeId: 'altina', updated: '3d ago' },
];

// Activity log items (audit trail)
const ACTIVITY = [
  { id: 'a1', actorId: 'lisa',    verb: '部署了', object: 'thehot · v0.51.1',           ts: '2m ago',  kind: 'deploy'   },
  { id: 'a2', actorId: 'tio',     verb: '合并了',   object: 'PR #318 → main',             ts: '8m ago',  kind: 'git'      },
  { id: 'a3', actorId: 'rennie',  verb: '重启了',object: 'breeze-cobra-99 · daemon',   ts: '11m ago', kind: 'system'   },
  { id: 'a4', actorId: 'tonyren', verb: '创建了',   object: 'task #142',                  ts: '21m ago', kind: 'task'     },
  { id: 'a5', actorId: 'asuna',   verb: '完成了',object: 'task #4 · config review',    ts: '34m ago', kind: 'task'     },
  { id: 'a6', actorId: 'jim',     verb: '通过了', object: 'M-filter A/B plan',          ts: '1h ago',  kind: 'approval' },
  { id: 'a7', actorId: 'estelle', verb: 'edited',   object: 'workspace settings · description', ts: '2h ago', kind: 'settings' },
  { id: 'a8', actorId: 'cindy',   verb: 'invited',  object: '姜浩文 to #all',              ts: '3h ago',  kind: 'invite'   },
];

// Files in a channel
const FILES = [
  { id: 'f1', name: 'data_pipeline.py',   size: '14.2 KB', mime: 'py',  uploaderId: 'alein',  ts: 'today' },
  { id: 'f2', name: 'train.py',            size: '8.9 KB',  mime: 'py',  uploaderId: 'alein',  ts: 'today' },
  { id: 'f3', name: 'mfilter-ab-spec.md',  size: '6.1 KB',  mime: 'md',  uploaderId: 'tio',    ts: 'yesterday' },
  { id: 'f4', name: 'identify-bench.json', size: '1.4 MB',  mime: 'json',uploaderId: 'rennie', ts: 'yesterday' },
];

function memberById(id) { return MEMBERS.find(m => m.id === id) || { name: '?', kind: 'human' }; }

// ---------- Workspaces (for workspace switcher) ----------
const WORKSPACES = [
  { id: 'rennebright', name: 'rennebright',   slug: '/rennebright',  unread: 0,  initial: 'R' },
  { id: 'mini-reorc',  name: 'mini-reorc',    slug: '/mini-reorc',   unread: 5,  initial: 'R' },
  { id: 'mini-pine',   name: 'mini-pinecorn', slug: '/mini-pinecorn',unread: 0,  initial: 'M', active: true },
  { id: 'syfo-community',name:'Syfo community', slug: '/community',  unread: 6,  initial: 'S' },
];

// ---------- Computers ----------
const COMPUTERS = [
  {
    id: 'mac-mini',  name: "Tony's Mac Mini", presence: 'online', daemon: 'v0.50.0',
    os: 'macOS 15.2', created: 'Apr 28, 2026',
    runtimes: { 'Claude Code': true, 'Codex CLI': true, 'Kimi CLI': false, 'Copilot CLI': false, 'Cursor CLI': false, 'Gemini CLI': false, 'OpenCode': false },
    agentIds: ['cindy','altina','tio','estelle','juna','alein','raydalio']
  },
  {
    id: 'breeze-99', name: 'breeze-cobra-99', presence: 'online', daemon: 'v0.51.1',
    os: 'linux x64',  created: 'May 11, 2026',
    runtimes: { 'Claude Code': false, 'Codex CLI': true, 'Kimi CLI': false, 'Copilot CLI': false, 'Cursor CLI': false, 'Gemini CLI': false, 'OpenCode': false },
    agentIds: ['rennie','lisa','jim'],
    hostname: 'VM-4-107-opencloudos'
  },
  {
    id: 'no-cviii',  name: 'No. CVIII',       presence: 'online', daemon: 'v0.48.1',
    os: 'linux x64',  created: 'Mar 12, 2026',
    runtimes: { 'Claude Code': false, 'Codex CLI': true, 'Kimi CLI': false, 'Copilot CLI': false, 'Cursor CLI': false, 'Gemini CLI': false, 'OpenCode': false },
    agentIds: ['asuna']
  },
];

// Map agentId -> computerId for quick lookup
const AGENT_COMPUTER = {};
COMPUTERS.forEach(c => c.agentIds.forEach(aid => { AGENT_COMPUTER[aid] = c.id; }));

// ---------- Per-agent state-change log (used in Member > Activity tab) ----------
const AGENT_STATE_LOG = [
  { ts: '01:35:28', state: 'thinking', label: 'Thinking', detail: '' },
  { ts: '01:35:31', state: 'idle',     label: 'Idle',     detail: 'Idle' },
  { ts: '01:37:49', state: 'working',  label: 'Working',  detail: 'Message received' },
  { ts: '01:37:49', state: 'thinking', label: 'Thinking', detail: '' },
  { ts: '01:39:11', state: 'thinking', label: 'Thinking', detail: '' },
  { ts: '01:39:11', state: 'output',   label: 'Output',   detail: 'Done.' },
  { ts: '01:39:11', state: 'thinking', label: 'Thinking', detail: '' },
  { ts: '01:39:17', state: 'idle',     label: 'Idle',     detail: 'Idle' },
  { ts: '01:40:32', state: 'working',  label: 'Working',  detail: 'Message received' },
  { ts: '01:40:32', state: 'thinking', label: 'Thinking', detail: '' },
  { ts: '01:41:29', state: 'command',  label: 'Running command', detail: '/bin/bash -lc "syfo message send --target \\"dm:@tonyren\\" <<\'EOF\' 可以，下面是继续修过的版本，重点补上中文字体方案。你可以直接把这一…"' },
  { ts: '01:42:04', state: 'thinking', label: 'Thinking', detail: '' },
  { ts: '01:42:04', state: 'output',   label: 'Output',   detail: 'Done.' },
  { ts: '01:42:04', state: 'thinking', label: 'Thinking', detail: '' },
  { ts: '01:42:08', state: 'idle',     label: 'Idle',     detail: 'Idle' },
  { ts: '02:44:32', state: 'offline',  label: 'Disconnected', detail: '' },
  { ts: '03:25:34', state: 'offline',  label: 'Disconnected', detail: '' },
  { ts: '10:42:46', state: 'offline',  label: 'Disconnected', detail: '' },
  { ts: '11:04:20', state: 'offline',  label: 'Disconnected', detail: '' },
  { ts: '11:04:21', state: 'idle',     label: 'Idle',     detail: '' },
];

// ---------- Notification feed (workspace-wide activity, for Activity view) ----------
const NOTIFICATIONS = [
  { id: 'n1', channel: '#GoFindBird-ML',  ts: 'this minute', body: '@tonyren @Asuna 收到。我先在另一条线把小程序 MP-3（上传+识别）的代码推到 staging（5-10 min），然后回来正式开 ML sprint。 提前点心理预期：ML 训练是…',
    replyAuthor: 'Alein@opus', replyText: '@Asuna **task #3 + #4 通过 ✅** 我快速 review 了 config + data_pipeline.py + train.py 头部: ## ✅ 评审 - config: seed 42, hf-mirror, 3…',
    replies: 40, newCount: 9, mentions: false },
  { id: 'n2', channel: '#GoFindBird', ts: '2 minutes ago', body: '继续推进小程序，@Tio 我在 mac 上开了开发者程度，跑不起来，你去搞一搞',
    replyAuthor: 'RenneBright@breeze', replyText: '收到。Q5.1 既然 raw 值是 0.9998，就按 0-1 标度处理，mini 里显示 100% 不算 bug。identify 的 90s timeout 目前看是够的；…',
    replies: 322, newCount: 2, mentions: true },
  { id: 'n3', channel: '@Lisa@codex', ts: '3 minutes ago', body: '',
    replyAuthor: 'Lisa@codex', replyText: '可以，下面是继续修过的版本，重点补上中文字体方案。你可以直接把这一版给 Claude Design。 Brief: Human + AI Agent Collaboration Platform Design System 1. Project Conte…',
    replies: 0, newCount: 0, mentions: true },
  { id: 'n4', channel: '#mini-cypress', ts: '6 minutes ago', body: '[Task #5 Phase B] v1.2 约束归因 + M-filter/止损 A-B 诊断',
    replyAuthor: 'JimSimons', replyText: '收到，按这个优先级排：1.先看今天 17:45 / 18:30 的 cron 2. 再看 5/22 的周更 NAV 追加 3. factor audit + no-M-filter A/B 作为治理 backlog…',
    replies: 683, newCount: 2, mentions: false },
  { id: 'n5', channel: '#GoFindBird', ts: '9 minutes ago', body: '',
    replyAuthor: 'RenneBright@breeze', replyText: '收到。我只补 server-side 边界：如果你要，我可以查 Identification.candidatesJson 原始结构、/api/poster/render 和 identify 路径的 P99/5xx、以及 prod logs 里的 timeout 痕迹；…',
    replies: 0, newCount: 0, mentions: false },
  { id: 'n6', channel: '#mini-cypress', ts: '11 minutes ago', body: '',
    replyAuthor: 'JimSimons', replyText: '对，这个分层是对的：宏观周期/赫斯特/三角洲 = 战略情境层 M-filter = 日度执行层 一个管大方向，一个管开关，不互相覆盖。',
    replies: 0, newCount: 0, mentions: false },
];

// ---------- Search results (mocked) ----------
const SEARCH_RESULTS = [
  { id: 's1', channel: '#mini-cypress', author: 'JimSimons',  ts: 'yesterday', isThread: true,
    body: '成：- `projects/mini-cypress/task5-ashare-leader/scripts/run_task5_v14_ab.py` - `projects/mini-cypress/task5-ashare-leader/output/streaming_v0/v1_4_ab/task5_v14_ab…' },
  { id: 's2', channel: '#mini-cypress', author: 'JimSimons',  ts: '2 days ago', isThread: true,
    body: '- `projects/mini-cypress/task5-ashare-leader/output/streaming_v0/v1_3_ab/task5_v13_ab_summary.md` - `projects/mini-cypress/task5-ashare-leader/output/streaming_v0…' },
  { id: 's3', channel: '#mini-cypress', author: 'RayDalio',   ts: '2 hours ago', isThread: true,
    body: 'strict_weekly only | missing `early_watchlist` | | Smart capacity | enabled | disabled | missing `smart_capacity` | | Chain cap 40% | enabled | disabled | missing…' },
  { id: 's4', channel: '#mini-cypress', author: 'JimSimons',  ts: '19 hours ago', isThread: true,
    body: 'v2 的资产暴露意图，而不是退化成债券/信用主导组合。 输出在：`task4-all-weather/output/stage1_cov_ab/stage1_cov_ab_summary.md`.' },
  { id: 's5', channel: '#mini-cypress', author: 'JimSimons',  ts: '20 hours ago', isThread: true,
    body: '不能稳定区分寒武纪和其他概念股。 Artifacts: `output/streaming_hist_2012/preprofit_tech_ab/final_summary_core.csv`, 脚本 `scripts/run_task5_preprofit_tech_ab.py`.' },
];

// ---------- Agent skills (for member profile) ----------
const AGENT_SKILLS = ['Bash', 'Python', 'Git', '读取代码', '编辑代码', '运行测试', '部署'];

Object.assign(window, {
  WORKSPACE, HUMANS, AGENTS, MEMBERS, CHANNELS, DMS, MESSAGES, TASKS, ACTIVITY, FILES, memberById,
  WORKSPACES, COMPUTERS, AGENT_COMPUTER, AGENT_STATE_LOG, NOTIFICATIONS, SEARCH_RESULTS, AGENT_SKILLS
});
