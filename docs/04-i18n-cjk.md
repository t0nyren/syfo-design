# 04 · Internationalization — CJK rules

Expands §6 of `OPENSPEC.md`.

## Variant philosophy

Syfo treats each language as a **parallel deployment** rather than a runtime locale switch. Reasoning:

1. The prototype has no i18n framework (no react-intl, no LinguiJS, etc.).
2. Typography for CJK is meaningfully different from Latin — fonts, line-heights, tracking, punctuation. A runtime switch would mean mounting both font stacks and trying to swap, which fights browser font caching.
3. Two static deployments are observable: the user knows which URL they're on, search engines index them separately, and you can tell at a glance which copy a user is looking at.

The cost: maintaining the EN→ZH string map (see below). For the prototype scale this is tractable; for production scale, port to an i18n framework.

## Font stacks

### `en/` variant
```
--font-sans:  'Inter', 'Noto Sans SC', 'Source Han Sans SC', system-ui, -apple-system, 'Segoe UI', sans-serif;
--font-serif: 'Noto Serif SC', 'Source Han Serif SC', Georgia, 'Times New Roman', serif;
```

### `zh/` variant
```
--font-sans:  'PingFang SC', 'Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', 'Heiti SC', 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
--font-serif: 'Songti SC', 'Source Han Serif SC', 'Noto Serif SC', Georgia, 'Times New Roman', serif;
```

Inter is kept as a Latin-only fallback so ASCII characters (e.g. code identifiers, mono numerals) still render in Inter inside a CJK-first paragraph.

## Line-height bumps for CJK

| Token         | en value | zh value |
|---------------|----------|----------|
| `--lh-display`| 48px     | 52px     |
| `--lh-h1`     | 36px     | 40px     |
| `--lh-h2`     | 26px     | 28px     |
| `--lh-h3`     | 22px     | 24px     |
| `--lh-body`   | 22px     | 24px     |
| `--lh-small`  | 20px     | 22px     |
| `--lh-label`  | 16px     | 18px     |

Why: CJK glyphs are dense and tall; the visual rhythm wants ~10% more vertical air between rows.

## Tracking adjustments

- `--track-tight`: en `-0.01em`, zh `0`. Negative tracking on CJK is visually broken (characters touch).
- `--track-label`: en `0.04em`, zh `0.05em`. Mono labels stay uppercase-tracked for both; CJK uses slightly more.

## `:lang(zh)` block

Appended to `colors_and_type.css` in the `zh/` variant:

```css
:lang(zh), :lang(zh-Hans), html[lang^="zh"] {
  font-feature-settings: "palt" 1, "kern" 1;
  text-spacing: auto;
}
```

- `"palt"` (proportional alternate widths) — CJK punctuation gets proper proportional widths instead of full-width boxes.
- `text-spacing: auto` — modern CSS spec that pads the boundary between CJK glyphs and Latin/digits. Removes the need to hand-insert spaces in "你好world" style strings.

## Translation map (EN → ZH)

Below is the canonical translation map used by `tools/patch-zh.py` (run when refreshing from a new Claude Design bundle).

### Settings sections
| EN              | ZH       |
|-----------------|----------|
| Account         | 账户     |
| Workspace       | 工作区   |
| Members         | 成员     |
| Permissions     | 权限     |
| Runtimes        | 运行时   |
| Audit log       | 审计日志 |
| Billing         | 账单     |

### Sidebar / Rail
| EN     | ZH     |
|--------|--------|
| Chat   | 聊天   |
| Tasks  | 任务   |
| Files  | 文件   |
| Audit  | 审计   |

### Member tabs
| EN          | ZH       |
|-------------|----------|
| Agent DMs   | AI 私聊  |
| Profile     | 资料     |
| Workspace   | 工作区   |
| Permissions | 权限     |
| Reminders   | 提醒     |
| Activity    | 动态     |

### Task statuses
| EN          | ZH      |
|-------------|---------|
| Backlog     | 待办    |
| In progress | 进行中  |
| In review   | 审核中  |
| Done        | 已完成  |
| Blocked     | 阻塞    |

### Buttons / tooltips
| EN           | ZH       |
|--------------|----------|
| Mark read    | 标为已读 |
| Mention      | 提及     |
| Attach file  | 附件     |
| Attach image | 图片     |
| Command      | 命令     |
| Refresh      | 刷新     |
| Add          | 添加     |
| Pause        | 暂停     |
| Restart      | 重启     |

### File table headers
| EN          | ZH     |
|-------------|--------|
| Name        | 名称   |
| Type        | 类型   |
| Size        | 大小   |
| Uploaded by | 上传者 |
| When        | 时间   |

### Activity verbs
| EN         | ZH       |
|------------|----------|
| deployed   | 部署了   |
| merged     | 合并了   |
| restarted  | 重启了   |
| opened     | 创建了   |
| completed  | 完成了   |
| approved   | 通过了   |

### Roles
| EN     | ZH     |
|--------|--------|
| Owner  | 拥有者 |
| Member | 成员   |

### Misc
| EN              | ZH      |
|-----------------|---------|
| Connected       | 已连接  |
| Not connected   | 未连接  |
| Today           | 今日    |
| Display name    | 显示名  |
| Description     | 描述    |
| Handle          | 账号    |
| Email           | 邮箱    |
| Computer        | 计算机  |
| Daemon version  | 守护版本|
| Created         | 创建于  |
| Creator         | 创建者  |
| Runtime         | 运行时  |
| Model           | 模型    |
| Reasoning       | 推理深度|

## Skill-row terms (kept English with select translations)

| EN          | ZH       |
|-------------|----------|
| Bash        | Bash     |
| Python      | Python   |
| Git         | Git      |
| Read code   | 读取代码 |
| Edit code   | 编辑代码 |
| Run tests   | 运行测试 |
| Deploy      | 部署     |

## Composer placeholder

- EN: `Message #${channel} · @ to mention an agent · / for commands`
- ZH: `在 #${channel} 发送消息 · @ 提及 AI · / 使用命令`

## Empty states

| EN title                       | ZH title          |
|--------------------------------|-------------------|
| No custom permissions yet      | 暂无自定义权限    |
| Free plan                      | 免费版            |
| Nothing here yet               | 暂无内容          |

(Bodies translated alongside; see the JSX files in `prototype/zh/syfo/` for the canonical wording.)

## When you add new copy

1. Write the EN string in `prototype/en/syfo/<file>.jsx`.
2. Add the matching ZH string at the same location in `prototype/zh/syfo/<file>.jsx`.
3. If it's a recurring chrome term, append to the map above and to `tools/patch-zh.py` (in repo root).
4. Don't ship EN-only or ZH-only strings.

## Notes on punctuation

- Use full-width punctuation in long CJK prose: `。，：；！？`.
- Half-width punctuation is OK inside parenthetical English / inline code: `(see §6)`, `(en: ...)`.
- Quotation marks: prefer `「」` for nested quotes; `“”` for primary quotes; mixed contexts allow `""`. Be consistent within a paragraph.
