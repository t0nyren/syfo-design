#!/usr/bin/env python3
"""Apply Chinese typography + UI translation to a copy of the Syfo prototype."""
import re
import sys
from pathlib import Path

ROOT = Path("/tmp/syfo-zh")

# ===== 1. CSS: Chinese-first font stack + CJK-tuned spacing =====
CSS_PATH = ROOT / "syfo" / "colors_and_type.css"
css = CSS_PATH.read_text(encoding="utf-8")

# Swap font-sans: put CJK first, Latin fallback after
css = css.replace(
    "--font-sans:    'Inter', 'Noto Sans SC', 'Source Han Sans SC', system-ui, -apple-system, 'Segoe UI', sans-serif;",
    "--font-sans:    'PingFang SC', 'Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', 'Heiti SC', 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;",
)
css = css.replace(
    "--font-serif:   'Noto Serif SC', 'Source Han Serif SC', Georgia, 'Times New Roman', serif;",
    "--font-serif:   'Songti SC', 'Source Han Serif SC', 'Noto Serif SC', Georgia, 'Times New Roman', serif;",
)

# Bump line-heights for CJK breathing room (~+10%)
lh_bumps = {
    "--lh-display: 48px": "--lh-display: 52px",
    "--lh-h1:      36px": "--lh-h1:      40px",
    "--lh-h2:      26px": "--lh-h2:      28px",
    "--lh-h3:      22px": "--lh-h3:      24px",
    "--lh-body:    22px": "--lh-body:    24px",
    "--lh-small:   20px": "--lh-small:   22px",
    "--lh-label:   16px": "--lh-label:   18px",
}
for old, new in lh_bumps.items():
    css = css.replace(old, new)

# Append a CJK-tuning block at the bottom
css += """
/* ============================================================
   Chinese (zh-Hans) typography overrides
   - palt: proportional alt widths for CJK punctuation
   - text-spacing: pad CJK ↔ Latin / numerals (modern browsers)
   - heading tracking eased back (CJK doesn't want negative tracking)
   ============================================================ */
:lang(zh), :lang(zh-Hans), html[lang^="zh"] {
  font-feature-settings: "palt" 1, "kern" 1;
  text-spacing: auto;
}
:root {
  --track-tight: 0;          /* CJK: avoid negative tracking on headings */
  --track-normal: 0;
  --track-label: 0.05em;     /* small labels: slightly wider for CJK uppercase */
}
body, .syfo-app, .syfo-iphone-content {
  font-family: var(--font-sans);
  font-feature-settings: "palt" 1, "kern" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
"""

CSS_PATH.write_text(css, encoding="utf-8")

# ===== 2. HTML: add lang="zh-Hans", keep viewport, swap title =====
HTML_PATH = ROOT / "Syfo Prototype.html"
html = HTML_PATH.read_text(encoding="utf-8")
html = html.replace('<html lang="en">', '<html lang="zh-Hans">')
html = html.replace("<title>Syfo — interactive prototype</title>", "<title>Syfo — 中文版交互原型</title>")
# Also localize the mode toggle button labels
html = html.replace(">\n              Desktop\n", ">\n              桌面\n")
html = html.replace(">\n              Mobile\n", ">\n              手机\n")
HTML_PATH.write_text(html, encoding="utf-8")

# Also write to index.html
(ROOT / "index.html").write_text(html, encoding="utf-8")

# ===== 3. JSX: translate UI chrome strings =====
TRANSLATIONS = {
    # ActivitySettings sections
    "label: 'Account'": "label: '账户'",
    "label: 'Workspace'": "label: '工作区'",
    "label: 'Members'": "label: '成员'",
    "label: 'Permissions'": "label: '权限'",
    "label: 'Runtimes'": "label: '运行时'",
    "label: 'Audit log'": "label: '审计日志'",
    "label: 'Billing'": "label: '账单'",
    "label: 'Codex CLI'": "label: 'Codex CLI'",
    "label: 'Claude Code'": "label: 'Claude Code'",
    "label: 'Chat'": "label: '聊天'",
    "label: 'Tasks'": "label: '任务'",
    "label: 'Files'": "label: '文件'",
    "label: 'Audit'": "label: '审计'",
    "label: 'Agent DMs'": "label: 'AI 私聊'",
    "label: 'Profile'": "label: '资料'",
    "label: 'Reminders'": "label: '提醒'",
    "label: 'Activity'": "label: '动态'",
    # Title attributes
    'title="Mark read"': 'title="标为已读"',
    'title="Mention"': 'title="提及"',
    'title="Attach file"': 'title="附件"',
    'title="Attach image"': 'title="图片"',
    'title="Command"': 'title="命令"',
    'title="Refresh"': 'title="刷新"',
    'title="Add"': 'title="添加"',
    'title="Pause"': 'title="暂停"',
    'title="Restart"': 'title="重启"',
    # Task status labels
    "label: 'Backlog'": "label: '待办'",
    "label: 'In progress'": "label: '进行中'",
    "label: 'In review'": "label: '审核中'",
    "label: 'Done'": "label: '已完成'",
    "label: 'Blocked'": "label: '阻塞'",
    # Day divider
    'label="Today"': 'label="今日"',
    # Empty states
    'title="No custom permissions yet"': 'title="暂无自定义权限"',
    'body="Define roles and scopes for humans and agents in this workspace."': 'body="为此工作区中的人类与 AI 设定角色与权限范围。"',
    'title="Free plan"': 'title="免费版"',
    'body="You\'re on the free plan. Upgrade to add more agent runtimes and longer audit retention."': 'body="当前为免费版。升级后可添加更多 AI 运行时与更长的审计保留时间。"',
    'title="Nothing here yet"': 'title="暂无内容"',
    'body="This view is part of the design system; live data populates once the workspace is connected."': 'body="此视图来自设计系统；连接工作区后会自动填充真实数据。"',
    # Form field labels
    'label="Display name"': 'label="显示名"',
    'label="Description"': 'label="描述"',
    'label="Handle"': 'label="账号"',
    'label="Role"': 'label="角色"',
    'label="Google" status="Not connected"': 'label="Google" status="未连接"',
    'label="GitHub" status="Not connected"': 'label="GitHub" status="未连接"',
    # Row keys
    'k="Name"': 'k="名称"',
    'k="Daemon version"': 'k="守护版本"',
    'k="Created"': 'k="创建于"',
    'k="Creator"': 'k="创建者"',
    'k="Computer"': 'k="计算机"',
    # KVStack labels
    'label="Runtime"': 'label="运行时"',
    'label="Model"': 'label="模型"',
    'label="Reasoning"': 'label="推理深度"',
    # Mobile tabs
    'label="Home"': 'label="主页"',
    'label="Activity"': 'label="动态"',
    'label="Members"': 'label="成员"',
    'label="Settings"': 'label="设置"',
    'label="Tasks"': 'label="任务"',
    # Default member role
    "m.role || 'Member'": "m.role || '成员'",
    # File table headers
    "['Name','Type','Size','Uploaded by','When']": "['名称','类型','大小','上传者','时间']",
    # Skills row
    "['Bash', 'Python', 'Git', 'Read code', 'Edit code', 'Run tests', 'Deploy']": "['Bash', 'Python', 'Git', '读取代码', '编辑代码', '运行测试', '部署']",
    # Composer placeholder
    'placeholder="Message #GoFindBird · @ to mention an agent · / for commands"':
        'placeholder="在 #GoFindBird 发送消息 · @ 提及 AI · / 使用命令"',
    # Workspace description default
    'defaultValue="Atlas — research workspace where the GoFindBird team and its agents ship."':
        'defaultValue="Atlas — GoFindBird 团队与其 AI 协作研发的研究工作区。"',
    # Connected meta
    "'Connected · daemon v0.51.1'": "'已连接 · 守护 v0.51.1'",
    "May 13, 2026": "2026 年 5 月 13 日",
    # Audit Owner role string (in data.jsx)
    "role: 'Owner'": "role: '拥有者'",
    "role: 'Member'": "role: '成员'",
    # Activity verbs (best-effort)
    "verb: 'deployed'": "verb: '部署了'",
    "verb: 'merged'": "verb: '合并了'",
    "verb: 'restarted'": "verb: '重启了'",
    "verb: 'opened'": "verb: '创建了'",
    "verb: 'completed'": "verb: '完成了'",
    "verb: 'approved'": "verb: '通过了'",
}

# Apply translations to every JSX file
jsx_files = list((ROOT / "syfo").glob("*.jsx"))
total_changes = 0
for jsx in jsx_files:
    txt = jsx.read_text(encoding="utf-8")
    orig = txt
    for en, zh in TRANSLATIONS.items():
        if en in txt:
            txt = txt.replace(en, zh)
            total_changes += 1
    if txt != orig:
        jsx.write_text(txt, encoding="utf-8")

print(f"Applied {total_changes} string replacements across {len(jsx_files)} JSX files")
print(f"CSS updated: {CSS_PATH}")
print(f"HTML updated: {HTML_PATH} + index.html")
