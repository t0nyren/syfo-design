# 05 · Voice & Tone

Expands §7 of `OPENSPEC.md`.

## Tone summary

| Trait              | Yes                                              | No                                                 |
|--------------------|--------------------------------------------------|----------------------------------------------------|
| Direct             | "Mark read" / "Send" / "Open task"                | "Click here to mark as read" / "Submit!"           |
| Confident          | "We'll spawn the agent when a message arrives." | "We hope to spawn the agent…"                      |
| Specific           | "1,666 species detected" / "8,910 / 142,861"    | "Lots of species" / "Many images"                  |
| Quiet              | sentences end on `.`                              | excessive `!` / emoji punctuation                  |
| Bilingual-ready    | English copy that translates cleanly             | idioms / wordplay that doesn't survive translation |

## English microcopy patterns

### Verb-first imperatives
- "Mark read"
- "Open task"
- "Send"
- "Add member"

### Status, not commentary
- ✅ `Connected · daemon v0.51.1`
- ❌ `Successfully connected!`

### Tooltips
- Short. Just enough to confirm the icon's action.
- ✅ `Mention` / `Attach file` / `Refresh`
- ❌ `Click here to mention someone` / `Use this button to refresh the list`

## Chinese microcopy patterns

### 命令式 / 信息式
- ✅ "标为已读" / "暂停" / "重启"
- ❌ "请点击这里标记为已读"

### 状态短语
- ✅ "已连接"
- ❌ "成功连接了！"

### 标点
- 中文长句: 全角句号 `。`、全角逗号 `，`、全角冒号 `：`。
- URL / 代码 / 英文术语包裹时: 半角符号。
- 不要在中英之间手动插半角空格 (CSS `text-spacing: auto` 处理)。

## Empty states

```jsx
<EmptyState
  title="No custom permissions yet"
  body="Define roles and scopes for humans and agents in this workspace."
/>
```

- Title: ≤ 6 words. Status or call-to-action.
- Body: 1-2 sentences. Explain WHAT this area is + WHAT populates it.
- Don't write "Loading..." (that's a spinner). Don't write "There's nothing here." (that's the title, not the body).

## Notification phrasing

- `<actor> <verb> <object> <time>`
- ✅ "@Lisa deployed thehot · v0.51.1 · 2m ago"
- ❌ "@Lisa has successfully deployed thehot version 0.51.1 just now"

## Terminology

| Concept | EN term | ZH term |
|---------|---------|---------|
| AI agent | agent | AI / agent (用 agent 时不翻) |
| Direct message | DM | 私聊 |
| Channel | channel | 频道 (但 Syfo 内部直接保留 channel 名) |
| Task | task | 任务 |
| Computer/host | computer | 计算机 |
| Runtime | runtime | 运行时 |
| Permission | permission | 权限 |
| Audit log | audit log | 审计日志 |
| Reasoning effort | reasoning | 推理深度 |

When in doubt, **mirror the existing JSX strings**. Don't invent a new term for the same concept.

## Forbidden in production microcopy

- Emoji as decoration (`📋`, `✅` in button labels). Emoji ARE allowed in user content reactions and fixture data.
- Exclamation marks unless inside a quote.
- Title-case for sentence-level copy. Use sentence case (`Mark read`, not `Mark Read`).
- "Please" / "请" prefixes on UI actions.
