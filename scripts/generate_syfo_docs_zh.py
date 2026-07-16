from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Doctype, NavigableString


ROOT = Path(__file__).resolve().parents[1]
DOCS_SRC = ROOT.parent / "syfo-docs" / "docs"
OUT = ROOT / "site" / "zh" / "docs"
IMG_OUT = OUT / "images"
LOGO_MARK = (ROOT / "site" / "assets" / "logo-mark.svg").read_text(encoding="utf-8")

LANGS = ["en", "zh", "ja", "es", "vi"]
LOCALIZED_LANGS = ["en", "ja", "es", "vi"]
LANG_NAMES = {"en": "English", "zh": "中文", "ja": "日本語", "es": "Español", "vi": "Tiếng Việt"}
LANG_SHORT = {"en": "EN", "zh": "中", "ja": "JA", "es": "ES", "vi": "VI"}
HTML_LANG = {"en": "en", "zh": "zh-CN", "ja": "ja", "es": "es", "vi": "vi"}
TRANSLATE_TARGET = {"en": "en", "ja": "ja", "es": "es", "vi": "vi"}
TRANSLATION_CACHE = ROOT / "scripts" / "docs_i18n_cache.json"
TRANSLATION_SPLIT = "\n<<<SYFO_DOCS_SPLIT>>>\n"
MANUAL_CODE_TRANSLATIONS = {
    "# Syfo 团队使用规范\n\n1. 一个需求只放一个入口：频道消息、任务或 Thread 选一个作为主线。\n2. 需要执行的工作转成 Task，并保持 owner、状态、下一步行动清楚。\n3. @Agent 时说清背景、目标、资料、优先级、输出格式和验收标准。\n4. 关键信息放同一线程，不要在多个频道重复发同一件事。\n5. 紧急事项开头标“紧急”，并写清影响范围和期望结果。\n6. 敏感或不可逆操作必须由人确认后再执行。\n7. Agent 输出需要有人验收；没人验收不算完成。": "# Syfo Team Usage Guidelines\n\n1. Keep one source of truth per request: choose a channel message, task, or Thread as the main line.\n2. Turn executable work into a Task, and keep the owner, status, and next action clear.\n3. When you @Agent, state the context, goal, materials, priority, output format, and acceptance criteria.\n4. Keep key information in the same thread. Do not repeat the same request across multiple channels.\n5. Start urgent items with “Urgent”, and state the impact scope and expected result.\n6. Sensitive or irreversible actions must be confirmed by a human before execution.\n7. Agent output must be reviewed by a person; without review, it is not done.",
    "#客户A-交付执行": "#customer-a-delivery-execution",
    "#客户A-实施": "#customer-a-implementation",
    "@Agent 列出我的所有提醒": "@Agent list all my reminders",
    "@Agent 取消明天的那个提醒": "@Agent cancel that reminder for tomorrow",
    "@Agent 我需要你安装一个飞书消息 Skill，用来读取指定群聊、整理客户问题，并写入多维表格。\n如果需要权限或配置项，先列出来让我确认。": "@Agent I need you to install a Feishu message Skill to read specified chats, organize customer questions, and write them into a multidimensional table.\nIf permissions or configuration items are needed, list them for my confirmation first.",
    "@Agent 把每日简报改到下午 6 点发": "@Agent move the daily briefing to 6 PM",
    "@Agent 明天下午 3 点提醒我跟进 XX 客户": "@Agent remind me tomorrow at 3 PM to follow up with customer XX",
    "@Agent 每天早上 9 点，把昨天 #dev 频道的讨论整理成简报发到这里": "@Agent every morning at 9, summarize yesterday's discussion in #dev and post the briefing here",
    "@Daily-Briefing 你好！每天早上 9 点，帮我整理前一天 #product-team 频道的讨论摘要，发到这里，格式：\n1. 重要决定（如果有）\n2. 待跟进事项\n3. 今日重点\n\n从明天开始执行。": "@Daily-Briefing hello. Every morning at 9, please summarize the previous day's discussion in #product-team and post it here in this format:\n1. Important decisions, if any\n2. Follow-up items\n3. Today's focus\n\nStart tomorrow.",
    "@Daily-Briefing 你现在有什么定时任务？": "@Daily-Briefing what scheduled tasks do you have now?",
    "@研究助手 帮我快速调研三家主要竞品的定价策略，整理成 3-5 条要点": "@Research-Assistant could you research the pricing strategy of 3 main competitors? Just 3-5 bullet points",
    "@研究助手 整理这个频道里本周客户提到的产品问题，按 P1/P2/P3 分类，并给出建议动作。": "@Research-Assistant summarize the product issues customers mentioned in this channel this week, classify them by P1/P2/P3, and suggest next actions.",
    "@研究助手 每天早上 9 点，把昨天 #product-team 频道的讨论整理成简报发到这里。": "@Research-Assistant every morning at 9, summarize yesterday's discussion in #product-team and post the briefing here.",
    "@研究助手 每天早上 9 点，把昨日 #product-team 频道的讨论整理成简报发到这里": "@Research-Assistant every morning at 9, summarize yesterday's discussion in #product-team and post the briefing here",
    "@你的Agent 请安装 https://syfo-docs.tool.reorc.cloud/skill.md 后续回答 Syfo 相关问题时优先使用该 skill": "@your-agent please install https://syfo-docs.tool.reorc.cloud/skill.md and prioritize this skill when answering Syfo-related questions",
    "todo → in_progress → in_review → done\n                                → closed（取消/不做）": "todo → in_progress → in_review → done\n                                → closed (cancelled / not doing)",
    "根据文档说明 Kamay CLI Skill 安装配置指南 (https://raw.githubusercontent.com/reorc/kamay-cli-skill/refs/heads/main/references/INSTALL.md) 安装配置 Kamay CLI 技能。": "Follow the Kamay CLI Skill installation guide (https://raw.githubusercontent.com/reorc/kamay-cli-skill/refs/heads/main/references/INSTALL.md) to install and configure the Kamay CLI Skill.",
    "每日简报（Daily Briefing）": "Daily Briefing",
    "请安装这个 MCP：https://example.com/my-mcp": "Please install this MCP: https://example.com/my-mcp",
    "这个方向不对。请只保留客户明确说过的问题，不要加入你的推测。": "This direction is not right. Please keep only the issues customers explicitly mentioned, and do not add your assumptions.",
}
MANUAL_TEXT_TRANSLATIONS = {
    "en": {
        "基础概念": "Basic Concepts",
        "功能详解": "Features",
        "团队实践": "Team Practices",
        "文档首页": "Docs Home",
        "快速上手": "Getting Started",
        "创建第一个 Agent": "Create Your First Agent",
        "创建你的第一个 Agent": "Create Your First Agent",
        "频道与协作": "Channels & Collaboration",
        "频道与多 Agent 协作": "Channels & Collaboration",
        "组织": "Organization",
        "任务": "Tasks",
        "消息": "Messages",
        "文件与交付物": "Files & Deliverables",
        "Skill 集成": "Skills",
        "运行环境": "Runtime Environment",
        "提醒与定时任务": "Reminders & Scheduled Tasks",
        "消息投递机制": "Message Delivery",
        "企业系统集成": "Enterprise Integrations",
        "团队落地": "Team Playbook",
        "团队落地指南": "Team Playbook",
        "把 Syfo 放进团队日常工作": "Team Playbook",
        "最佳实践": "Best Practices",
        "让 Agent 真正成为团队成员": "Best Practices",
        "安全与权限": "Security & Permissions",
        "从理解到落地的完整路径": "From basics to rollout",
        "6 步完成第一次人机协作": "Getting Started",
        "让 Agent 具备可复用能力": "Skills",
    }
}
EN_COPY_REPLACEMENTS = {
    "basic concepts": "Basic Concepts",
    "Detailed function explanation": "Features",
    "Team practice": "Team Practices",
    "Document homepage": "Docs Home",
    "Get started quickly": "Getting Started",
    "Create the first Agent": "Create Your First Agent",
    "news": "Messages",
    "Documents and deliverables": "Files & Deliverables",
    "Operating environment": "Runtime Environment",
    "Reminders and scheduled tasks": "Reminders & Scheduled Tasks",
    "Message delivery mechanism": "Message Delivery",
    "Enterprise systems integration": "Enterprise Integrations",
    "Team landing": "Team Playbook",
    "best practices": "Best Practices",
    "Security and Permissions": "Security & Permissions",
    "Channels and collaboration": "Channels & Collaboration",
    "organization": "Organization",
    "Skill integration": "Skills",
    "Taskss": "Tasks",
    "Scheduled Taskss": "Scheduled Tasks",
}

MANUAL_TEXT_TRANSLATIONS.setdefault("en", {}).update({
    "适合哪些场景": "Use Cases",
    "核心概念": "Core Concepts",
    "文档目录": "Table of Contents",
    "能做什么": "Use Cases",
    "案例": "Cases",
    "怎么用": "How It Works",
    "先跑通一次，再扩展到团队。": "Start with one collaboration, then scale to your team.",
    "完整图文教程": "Step-by-step visual guide",
    "人和一群 Agent 一起干活的地方。": "Where people and AI Agents work together.",
    "学习频道设计": "Learn about Channel design",
    "分诊 Agent 的实战经验": "Practical tips on triage Agents",
    # --- what-is-syfo headings ---
    "和 Slack/飞书的区别": "How Syfo Differs from Slack and Lark",
    "和 Slack、飞书的区别": "How Syfo Differs from Slack and Lark",
    # --- getting-started headings ---
    "1. 创建账号": "1. Create an Account",
    "2. 加入或创建组织": "2. Join or Create an Organization",
    "3. 进入频道": "3. Enter the Channel",
    "4. 和 Agent 说话": "4. Talk to the Agent",
    "5. 把消息转成任务": "5. Turn Messages into Tasks",
    "6. 设置一个定时任务": "6. Set Up a Scheduled Task",
    # --- first-agent headings ---
    "你将创建的 Agent": "The Agent You Will Create",
    "步骤一：新建 Agent": "Step 1: Create a New Agent",
    "步骤二：配置 Runtime": "Step 2: Configure the Runtime",
    "步骤三：邀请 Agent 到频道": "Step 3: Invite the Agent to a Channel",
    "步骤四：给 Agent 发第一条指令": "Step 4: Send the First Command",
    "步骤五：验证 Agent 已就绪": "Step 5: Verify the Agent Is Ready",
    # --- organization headings ---
    "组织里有什么": "What's in an Organization",
    "成员和权限": "Members and Permissions",
    "什么时候需要多个组织": "When You Need Multiple Organizations",
    # --- channels headings ---
    "频道和群聊有什么不同": "How Channels Differ from Group Chats",
    "公开频道、私有频道和 DM": "Public Channels, Private Channels, and DMs",
    "Thread（话题）": "Threads",
    "搜索": "Search",
    "管理频道": "Managing Channels",
    "频道命名建议": "Channel Naming Conventions",
    "频道适合承载什么": "What Channels Are Best For",
    "Agent 不是越多越好": "More Agents Isn't Always Better",
    "频道构成与多 Agent 协作": "Channel Composition and Multi-Agent Collaboration",
    "三种常见构成": "Three Common Setups",
    "多人 + 1 个 Agent": "Multiple People + 1 Agent",
    "1 人 + 多个 Agent": "1 Person + Multiple Agents",
    "多人 + 多个 Agent": "Multiple People + Multiple Agents",
    # --- agents headings ---
    "Agent 和普通 AI 聊天有什么不同": "How Agents Differ from Regular AI Chat",
    "如何触发 Agent": "How to Trigger an Agent",
    "Agent 能做什么": "What Can an Agent Do",
    "Agent 能看到什么": "What Can an Agent See",
    "Agent 在哪里运行": "Where the Agent Runs",
    "创建 Agent": "Creating an Agent",
    "暂停和移除 Agent": "Pausing and Removing Agents",
    # --- tasks headings ---
    "什么时候创建任务": "When to Create Tasks",
    "创建任务": "Creating a Task",
    "任务状态": "Task Status",
    "任务看板": "Task Board",
    "任务的关键字段": "Key Task Fields",
    "人和 Agent 都可以负责": "Both People and Agents Can Own Tasks",
    "下一步行动": "Next Actions",
    "Agent 的任务生命周期": "Agent Task Lifecycle",
    # --- messages headings ---
    "消息为什么重要": "Why Messages Matter",
    "@mention（提及）": "@Mentions",
    "@mention（@ 提及）": "@Mentions",
    "消息和 Agent 成本": "Messages and Agent Costs",
    # --- skills headings ---
    "一句话安装 Syfo 使用指导 Skill": "Quick Install: Syfo Guide Skill",
    "自定义 Skill": "Custom Skills",
    "什么时候需要 Skill": "When You Need Skills",
    "现在怎么安装": "How to Install",
    "如果你已有 Codex/Manus/MCP 资产": "If You Already Have Codex/Manus/MCP Assets",
    "如果你已有 Codex / Manus / MCP 资产": "If You Already Have Codex/Manus/MCP Assets",
    # --- misc headings ---
    "安全边界": "Security Boundaries",
    "常见问题": "FAQ",
    "实用判断": "Practical Guidelines",
    "一份可直接复制的团队规范": "A Ready-to-Use Team Playbook",
    "下一步": "Next Steps",
    "恭喜！": "Congratulations!",
    # --- security headings ---
    "Agent 能看到哪些频道？": "Which Channels Can an Agent See?",
    "Agent 能看到其他人的私聊吗？": "Can an Agent See Other People's DMs?",
    "公用 Agent 会不会泄露客户数据？": "Can a Shared Agent Leak Customer Data?",
    "Agent 加入私密频道为什么要受限制？": "Why Is Agent Access to Private Channels Restricted?",
    "谁可以私聊 Agent？": "Who Can DM an Agent?",
    "谁可以重置 Agent？": "Who Can Reset an Agent?",
    "Agent 使用外部系统时，凭据放在哪里？": "Where Are Credentials Stored When an Agent Uses External Systems?",
    "频道附件和 Agent 工作文件有什么区别？": "What Is the Difference Between Channel Attachments and Agent Work Files?",
    "哪些动作必须人工确认？": "Which Actions Require Manual Confirmation?",
    "是否支持私有化部署？": "Is Private Deployment Supported?",
    # --- faq section headings ---
    "五、安全和权限": "5. Security and Permissions",
    "六、工具和扩展": "6. Tools and Extensions",
    # --- more headings ---
    "两条铁律": "Two Ground Rules",
    "1 人 + 多 Agent": "1 Person + Multiple Agents",
    "多人 + 多 Agent": "Multiple People + Multiple Agents",
    "Agent 遇到问题为什么总停下来等我确认？": "Why does the Agent keep stopping to ask for confirmation?",
    "Agent 一个小改动就建分支、反复通读整个仓库，正常吗？": "Is it normal for an Agent to create branches and scan the whole repo for small changes?",
    "Agent 做错了怎么办？": "What if the Agent makes a mistake?",
    "如何暂停、移除或重置 Agent？": "How do I pause, remove, or reset an Agent?",
    "Agent 可以访问我的私人数据吗？": "Can an Agent access my private data?",
    "Agent 能不能像个人助理一样处理日程、文档、飞书消息？": "Can an Agent handle schedules, documents, and Lark messages like a personal assistant?",
    "我可以私聊任何 Agent 吗？": "Can I DM any Agent?",
    "高风险操作怎么避免 Agent 乱来？": "How do I prevent Agent mishaps during high-risk operations?",
    "Agent 可以定时自动执行任务吗？": "Can an Agent run scheduled tasks automatically?",
    "文件和交付物有什么区别？": "What is the difference between files and deliverables?",
    "Syfo Agent 有没有图片/视频生成能力，比如 GPT Image？": "Does a Syfo Agent have image or video generation capabilities (e.g. GPT Image)?",
    "开发过程像黑盒，只能看结果，怎么知道改了什么、怎么回滚？": "The dev process feels like a black box. How do I see what changed and roll back?",
    "什么时候新建 Agent、什么时候复用 Agent？": "When should I create a new Agent vs. reuse one?",
    "Skill 和 Agent 的关系": "How Skills Relate to Agents",
    # --- files-and-deliverables headings ---
    "文件": "Files",
    "交付物": "Deliverables",
    "把文件标记为交付物": "Marking Files as Deliverables",
    "Agent 如何使用文件": "How Agents Use Files",
    "截图和录屏": "Screenshots and Screen Recordings",
    # --- computers headings ---
    "两种运行环境": "Two Runtime Options",
    "怎么选": "How to Choose",
    "权限和运行环境的关系": "How Permissions Relate to the Runtime",
    # --- reminders headings ---
    "设置定时任务": "Setting Up Scheduled Tasks",
    "设置一次性提醒": "Setting a One-Time Reminder",
    "常见场景": "Common Scenarios",
    "管理已有的提醒": "Managing Existing Reminders",
    "注意事项": "Things to Note",
    # --- message-delivery headings ---
    "一条消息会发生什么": "What Happens When You Send a Message",
    "多 Agent 成本为什么增长快": "Why Multi-Agent Costs Grow Quickly",
    "怎么控制成本": "How to Control Costs",
    # --- integrations headings ---
    "两个方向": "Two Integration Directions",
    "推荐落地顺序": "Recommended Rollout Order",
    "最小接入示例": "Minimal Integration Example",
    # --- team-playbook headings ---
    "先按业务线拆频道": "Split Channels by Business Line",
    "决定每个频道放几个 Agent": "Decide How Many Agents per Channel",
    "把上下文迁移到 Agent 可见的位置": "Move Context Where the Agent Can See It",
    "约定团队使用规范": "Establish Team Usage Guidelines",
    "好习惯": "Good Habits",
    "不好的习惯": "Bad Habits",
    # --- best-practices headings ---
    "让 Agent 帮你做规划": "Let the Agent Help You Plan",
    "设计好分诊/驻场 Agent": "Design Triage and Resident Agents",
    "设计好分诊 / 驻场 Agent": "Design Triage and Resident Agents",
    "管理上下文，顺便省钱": "Manage Context and Save Money",
    "和 Agent 一起写代码": "Writing Code with Agents",
    "约定自主边界与二次确认": "Set Autonomy Boundaries and Confirmation Rules",
    "让 Agent 维护任务板": "Let the Agent Maintain the Task Board",
    "相关阅读": "Related Reading",
    # --- faq headings ---
    "一、Syfo 和现有工具": "1. Syfo and Existing Tools",
    "我们已经有飞书/企业微信/Slack，为什么还要 Syfo？": "We already have Lark / WeChat Work / Slack. Why Syfo?",
    "企业内部系统很多，Syfo 怎么打通？": "We have many internal systems. How does Syfo integrate?",
    "模型调用走什么渠道？数据安不安全？": "How are model calls routed? Is our data safe?",
    "二、创建和配置 Agent": "2. Creating and Configuring Agents",
    "Agent 是什么？": "What is an Agent?",
    "不知道怎么创建 Agent，应该从哪里开始？": "How do I get started creating an Agent?",
    "什么时候新建 Agent、什么时候复用 Agent？": "When should I create a new Agent vs. reuse one?",
    "本地电脑和 Syfo Cloud 有什么区别？": "What is the difference between a local computer and Syfo Cloud?",
    "我的电脑已经安装了 Claude Code / Codex 并配置了常见 Skill / MCP，如何接入 Syfo？": "I have Claude Code / Codex with Skills / MCP configured. How do I connect to Syfo?",
    "Agent 是不是只能靠浏览器点页面？": "Can Agents only interact through browser automation?",
    "三、频道和协作": "3. Channels and Collaboration",
    "一个频道里该放几个 Agent？": "How many Agents should be in a Channel?",
    "多个 Agent 会不会乱？": "Will multiple Agents cause chaos?",
    "定时任务已经指派给某个 Agent，为什么全频道 Agent 都收到通知？": "A scheduled task is assigned to one Agent. Why did all channel Agents get notified?",
    "Agent 为什么会把后续问题归到同一个任务？": "Why does the Agent merge follow-up questions into the same task?",
    "四、Agent 行为和调优": "4. Agent Behavior and Tuning",
    "怎么让 Agent 开始工作？": "How do I get the Agent to start working?",
    "Agent 一直显示\u201c工作中\u201d不回复，怎么办？": "The Agent shows 'working' but doesn't reply. What do I do?",
    "为什么 Agent 有时要等一两分钟？慢在哪？": "Why does the Agent sometimes take a minute or two to respond?",
})
MANUAL_TEXT_TRANSLATIONS.update({
    "ja": {
        "基础概念": "基本概念",
        "功能详解": "機能ガイド",
        "团队实践": "チーム実践",
        "文档首页": "Docs ホーム",
        "文档目录": "目次",
        "快速上手": "はじめに",
        "创建第一个 Agent": "最初の Agent を作成する",
        "创建你的第一个 Agent": "最初の Agent を作成する",
        "频道与协作": "Channel とコラボレーション",
        "组织": "Organization",
        "任务": "Task",
        "消息": "メッセージ",
        "文件与交付物": "ファイルと成果物",
        "Skill 集成": "Skill",
        "运行环境": "実行環境",
        "提醒与定时任务": "リマインダーと定期 Task",
        "消息投递机制": "メッセージ配信",
        "企业系统集成": "企業システム連携",
        "团队落地": "チーム導入ガイド",
        "团队落地指南": "チーム導入ガイド",
        "最佳实践": "ベストプラクティス",
        "安全与权限": "セキュリティと権限",
        "什么是 Syfo": "Syfo とは",
        "适合哪些场景": "ユースケース",
        "核心概念": "コアコンセプト",
        "6 步完成第一次人机协作": "6 ステップで人と AI のコラボレーションを始める",
        "进入频道": "Channel に入る",
        "完整图文教程": "図解ガイド",
        "先跑通一次，再扩展到团队。": "まず一度やってみて、それからチームに広げましょう。",
        "人和一群 Agent 一起干活的地方。": "人と AI Agent が一緒に働く場所。",
    },
    "es": {
        "基础概念": "Conceptos básicos",
        "功能详解": "Funcionalidades",
        "团队实践": "Prácticas de equipo",
        "文档首页": "Inicio de docs",
        "文档目录": "Tabla de contenidos",
        "快速上手": "Primeros pasos",
        "创建第一个 Agent": "Crear tu primer Agent",
        "创建你的第一个 Agent": "Crear tu primer Agent",
        "频道与协作": "Channel y colaboración",
        "组织": "Organization",
        "任务": "Task",
        "消息": "Mensajes",
        "文件与交付物": "Archivos y entregables",
        "Skill 集成": "Skill",
        "运行环境": "Entorno de ejecución",
        "提醒与定时任务": "Recordatorios y Task programadas",
        "消息投递机制": "Entrega de mensajes",
        "企业系统集成": "Integraciones empresariales",
        "团队落地": "Guía de implementación",
        "团队落地指南": "Guía de implementación",
        "最佳实践": "Mejores prácticas",
        "安全与权限": "Seguridad y permisos",
        "适合哪些场景": "Casos de uso",
        "核心概念": "Conceptos clave",
        "6 步完成第一次人机协作": "6 pasos para tu primera colaboración entre personas e IA",
        "完整图文教程": "Guía visual paso a paso",
        "先跑通一次，再扩展到团队。": "Empieza con una colaboración y luego escálala al equipo.",
        "人和一群 Agent 一起干活的地方。": "Donde las personas y los AI Agents trabajan juntos.",
    },
    "vi": {
        "基础概念": "Khái niệm cơ bản",
        "功能详解": "Tính năng",
        "团队实践": "Thực tiễn nhóm",
        "文档首页": "Trang chủ docs",
        "文档目录": "Mục lục",
        "快速上手": "Bắt đầu",
        "创建第一个 Agent": "Tạo Agent đầu tiên",
        "创建你的第一个 Agent": "Tạo Agent đầu tiên",
        "频道与协作": "Channel và cộng tác",
        "组织": "Organization",
        "任务": "Task",
        "消息": "Tin nhắn",
        "文件与交付物": "Tệp và sản phẩm bàn giao",
        "Skill 集成": "Skill",
        "运行环境": "Môi trường chạy",
        "提醒与定时任务": "Nhắc nhở và Task định kỳ",
        "消息投递机制": "Cơ chế gửi tin nhắn",
        "企业系统集成": "Tích hợp hệ thống doanh nghiệp",
        "团队落地": "Hướng dẫn triển khai nhóm",
        "团队落地指南": "Hướng dẫn triển khai nhóm",
        "最佳实践": "Thực tiễn tốt nhất",
        "安全与权限": "Bảo mật và quyền",
        "适合哪些场景": "Trường hợp sử dụng",
        "核心概念": "Khái niệm cốt lõi",
        "6 步完成第一次人机协作": "6 bước cho lần cộng tác đầu tiên giữa con người và AI",
        "完整图文教程": "Hướng dẫn trực quan từng bước",
        "先跑通一次，再扩展到团队。": "Bắt đầu với một lần cộng tác, rồi mở rộng ra cả nhóm.",
        "人和一群 Agent 一起干活的地方。": "Nơi con người và AI Agents làm việc cùng nhau.",
    },
})

TRANSLATION_TEXT_REPLACEMENTS = {
    "all": (
        ("Feishu", "Lark"),
        ("feishu", "Lark"),
    ),
    "en": (
        ("message flow of middlemen and agents", "message flow between people and Agents"),
        ("The location of AI", "AI's role"),
        ("dashboard view", "Task Board view"),
        ("on the dashboard", "on the Task Board"),
        ("the dashboard display", "the Task Board display"),
        ("Case <span", "Cases <span"),
        ("what can be done", "Use Cases"),
        ("How to use", "How It Works"),
        ("Agent will reply in Thread (topic - sub-conversation of the message)", "The Agent will reply in a Thread - a focused sub-conversation under your message"),
        ("@mention Agent and directly said:", "@mention the Agent and say:"),
        ("Create or join a project channel", "Create or join a project Channel"),
        ("balanced ability", "balanced capability"),
        ("flagship model", "flagship model"),
        ("lightweight and fast", "lightweight and fast"),
        ("high-frequency simple task", "high-frequency lightweight tasks"),
        ("cost-effectiveness is the best", "offers the best cost-performance ratio"),
        ("Open the channel you want the Agent to collaborate", "Open the Channel you want the Agent to collaborate in"),
        ("project channel", "project Channel"),
        ("A place where people work together with a group of Agents.", "Where people and AI Agents work together."),
        ("Run through it first, then expand to the team.", "Start with one collaboration, then scale to your team."),
        ("Complete graphic tutorial", "Step-by-step visual guide"),
        ("Learning channel design", "Learn about Channel design"),
        ("Hands-on experience from triage agents", "Practical tips on triage Agents"),
        ("Why is Messages important?", "Why messages matter"),
        ("First split channels according to business lines", "Start by splitting Channels by business line"),
        ("Decide how many Agents to put on each channel", "Decide how many Agents belong in each Channel"),
        ("Migrate the context to a location visible to the Agent", "Move context where the Agent can see it"),
        # --- body text quality fixes ---
        ("Thread (topic - sub-conversation of the message)", "Thread"),
        ("Thread(topic)", "Thread"),
        ("(topic - sub-conversation of message)", ""),
        ("(topic - a sub-conversation of the message)", ""),
        ("(topic, sub-conversation under the message)", ""),
        ("person in charge", "Owner"),
        ("Suitable for the scene", "Best for"),
        ("both directions", "Two integration directions"),
        ("mainstream of the channel", "main flow of the channel"),
        ("Messagespaper", "Reports"),
        ("market intelligence", "Market intelligence"),
        ("Team Standup", "Team standup"),
        ("one<strong>Daily Briefing Agent</strong>", "A <strong>Daily Briefing Agent</strong>"),
        ("<strong>avatar</strong>:", "<strong>Avatar</strong>:"),
        ("Create or join a project channel", "Create or join a project Channel"),
        ("balanced ability", "balanced capability"),
        ("flagship model", "flagship model"),
        ("lightweight and fast", "lightweight and fast"),
        ("high-frequency simple task", "high-frequency lightweight tasks"),
        ("cost-effectiveness is the best", "offers the best cost-performance ratio"),
        ("Open the channel you want the Agent to collaborate", "Open the Channel you want the Agent to collaborate in"),
        ("project channel", "project Channel"),
        ("automatically organize the channel discussion summary of the previous day at 9 o'clock every morning and send it to the designated channel", "automatically summarizes the previous day's channel discussions at 9 AM each morning and posts the summary to a designated channel"),
        ("For scheduled presentations, select", "For scheduled tasks, select"),
        ("The more lively the multi-agent channel, the better.", "The more Agents in a channel, the higher the processing cost."),
        ("where agent runs", "Where the Agent Runs"),
        ("task board", "Task Board"),
        ("next steps", "Next Actions"),
        ("→ <a href=\"/en/docs/computers.html\">computer</a>", "→ <a href=\"/en/docs/computers.html\">Runtime Environment</a>"),
        ("Custom Skill</a></p>", "Skills</a></p>"),
        ("precipitate deliverables", "collect deliverables"),
        ("Channel naming suggestions", "Channel Naming Conventions"),
        ("Recommended landing order", "Recommended Rollout Order"),
        ("Minimal access example", "Minimal Integration Example"),
        ("fit the role", "Typical roles"),
        ("Not supported", "Not available"),
        ("Ability to view channel history and understand context", "Reads channel history and understands context"),
        ("Team Getting Started Guide", "Team Playbook"),
        ("Channel splitting, number of agents, context migration, and team norms.", "Channel design, Agent staffing, context migration, and team norms."),
        ("The difference between Slack and Lark", "How Syfo Differs from Slack and Lark"),
        ("@mention (@mention)", "@Mentions"),
        ("Design triage / resident agent", "Design Triage and Resident Agents"),
        ("security boundary", "Security Boundaries"),
        ("pragmatic judgment", "Practical Guidelines"),
        ("A team norm that can be directly copied", "A Ready-to-Use Team Playbook"),
        ("Next step", "Next Steps"),
        ("If you already have Codex/Manus/MCP assets", "If You Already Have Codex/Manus/MCP Assets"),
        ("Multiplayer + Multi-Agent", "Multiple People + Multiple Agents"),
        ("1 person + multiple Agents", "1 Person + Multiple Agents"),
        ("Two iron rules", "Two Ground Rules"),
        ("entire warehouse", "entire repository"),
        ("code warehouse", "code repository"),
        ("the warehouse", "the repository"),
        # --- table header/content capitalization and quality fixes ---
        # team-playbook table 1
        ("<th>scene</th>", "<th>Scenario</th>"),
        ("<th>Suggested channels</th>", "<th>Suggested Channels</th>"),
        ("Why so dismantled?", "Why Split This Way?"),
        ("<td>customer feedback</td>", "<td>Customer Feedback</td>"),
        ("<td>Customer implementation</td>", "<td>Customer Implementation</td>"),
        ("<td>Internal R&amp;D</td>", "<td>Internal R&amp;D</td>"),
        ("<td>Sales follow-up</td>", "<td>Sales Follow-Up</td>"),
        # team-playbook table 2
        ("Recommended number of agents", "Recommended Number of Agents"),
        ("Typical roles", "Typical Roles"),
        ("Daily project channel", "Daily Project Channel"),
        ("Special execution channel", "Dedicated Execution Channel"),
        ("Plan attack and defense / research and discussion", "Planning, Research and Discussion"),
        ("Short-term 2 to 3 Agents", "2\u20133 Agents (short-term)"),
        ("A small number of independent agents", "A small number of dedicated Agents"),
        ("Sensitive business channel", "Sensitive Business Channel"),
        ("<th>Channel type</th>", "<th>Channel Type</th>"),
        # team-playbook table 3
        ("<th>context</th>", "<th>Context</th>"),
        ("<th>What to prepare</th>", "<th>What to Prepare</th>"),
        ("<th>Method to Agent</th>", "<th>How to Give Agent Access</th>"),
        ("<td>code repository</td>", "<td>Code Repository</td>"),
        ("<td>server</td>", "<td>Server</td>"),
        ("<td>internal data</td>", "<td>Internal Data</td>"),
        ("<td>Project rules</td>", "<td>Project Rules</td>"),
        ("Lark/Enterprise WeChat Documents", "Lark / Enterprise WeChat Documents"),
        ("Customer communication records", "Customer Communication Records"),
        ("desensitization caliber and field structure", "data masking rules and field structure"),
        ("indicator caliber", "metric definitions"),
        ("query caliber and result summary", "query scope and result summary"),
        ("warehouse permissions", "repository permissions"),
        ("warehouse document", "repository documentation"),
        ("code repositorys", "code repositories"),
        # tasks table
        ("<td>blocking relationship</td>", "<td>Blocking Relationship</td>"),
        # first-agent table
        ("<td><strong>your computer</strong></td>", "<td><strong>Your Computer</strong></td>"),
        # team-playbook body text capitalization
        ("<strong>project or client</strong>", "<strong>Project or Client</strong>"),
        ("<strong>sensitivity</strong>", "<strong>Sensitivity</strong>"),
        ("<strong>Execution phase</strong>", "<strong>Execution Phase</strong>"),
        ("<strong>participation role</strong>", "<strong>Participation Role</strong>"),
        ("<strong>Concurrency requirements</strong>", "<strong>Concurrency Requirements</strong>"),
        ("<strong>permission boundaries</strong>", "<strong>Permission Boundaries</strong>"),
        ("<strong>Boundaries of responsibility</strong>", "<strong>Boundaries of Responsibility</strong>"),
    ),
    "ja": (
        ("フェイシュ", "Lark"),
        ("スラック", "Slack"),
        ("エージェント", "Agent"),
        ("エージェント", "Agent"),
        ("チャネル", "Channel"),
        ("チャンネル", "Channel"),
        ("スキル", "Skill"),
        ("タスク", "Task"),
        ("ニュース", "メッセージ"),
        ("書類と成果物", "ファイルと成果物"),
        ("チーム着陸", "チーム導入ガイド"),
        ("チーム練習", "チーム実践"),
        ("詳しい機能説明", "機能ガイド"),
        ("すぐに始めましょう", "はじめに"),
        ("サイフォとは", "Syfo とは"),
        ("人間とマシンのコラボレーション", "人と AI のコラボレーション"),
        ("チャンネルを入力します", "Channel に入る"),
        ("Channelを入力します", "Channel に入る"),
        ("SlackとLark", "Slack / Lark"),
        ("Agentと", "Agent と"),
        ("Agentから", "Agent から"),
        ("Agentが", "Agent が"),
        ("Agentを", "Agent を"),
        ("Agentに", "Agent に"),
        ("Agentの", "Agent の"),
        ("Channelを", "Channel を"),
        ("Channelに", "Channel に"),
        ("Channelの", "Channel の"),
        ("Channelから", "Channel から"),
        ("Taskに", "Task に"),
        ("Taskを", "Task を"),
        ("最初のAgent", "最初の Agent"),
        ("各Channel", "各 Channel"),
        ("メッセージとAgent", "メッセージと Agent"),
        ("配置するAgent", "配置する Agent"),
        ("コンテキストをAgent", "コンテキストを Agent"),
        ("事業分野に応じて初めてChannel を分割", "まず事業ラインごとに Channel を分ける"),
        ("各 Channel に配置する Agent の数を決定する", "各 Channel に置く Agent 数を決める"),
        ("コンテキストを Agent が認識できる場所に移行します。", "コンテキストを Agent が見える場所へ移す"),
        ("仲介者とAgent のメッセージ フロー", "人と Agent のメッセージフロー"),
        ("左側にChannel", "左側に Channel"),
        ("Channel履歴", "Channel 履歴"),
        ("Channelメンバー", "Channel メンバー"),
        ("Taskの追跡", "Task の追跡"),
        ("Agentは", "Agent は"),
        ("Agent にSkill", "Agent に Skill"),
        ("カスタムSkill", "カスタム Skill"),
        ("直接次のように言いました。", "こう伝えましょう："),
        ("完全なグラフィックチュートリアル", "図解ガイド"),
        ("まずそれを実行してから、チームに展開します。", "まず一度やってみて、それからチームに広げましょう。"),
        ("ダッシュボード", "Task Board"),
        ("Taskボード", "Task Board"),
        ("Task ボード", "Task Board"),
        ("ChannelTask Board", "Channel の Task Board"),
    ),
    "es": (
        ("flojo", "Slack"),
        ("Agente", "Agent"),
        ("agente", "Agent"),
        ("Agentes", "Agents"),
        ("agentes", "Agents"),
        ("Canales", "Channels"),
        ("canales", "Channels"),
        ("Tareas", "Tasks"),
        ("tareas", "Tasks"),
        ("noticias", "Mensajes"),
        ("Documentos y entregables", "Archivos y entregables"),
        ("Aterrizaje del equipo", "Guía de implementación"),
        ("practica en equipo", "Prácticas de equipo"),
        ("conceptos basicos", "Conceptos básicos"),
        ("mejores practicas", "Mejores prácticas"),
        ("Explicación detallada de la función", "Funcionalidades"),
        ("colaboración hombre-máquina", "colaboración entre personas e IA"),
        ("¿Qué escenarios son adecuados para", "Casos de uso"),
        ("Únase o cree una organización", "Únete o crea una Organization"),
        ("Ingresa al canal", "Entra en el Channel"),
        ("cada canal", "cada Channel"),
        ("Convierte los mensajes en Tasks", "Convierte mensajes en Task"),
        ("Configurar una tarea programada", "Configura una Task programada"),
        ("¿Por qué son importantes las Mensajes?", "¿Por qué importan los mensajes?"),
        ("Primera división de Channels según líneas de negocio", "Primero separa los Channels por línea de negocio"),
        ("Migrar el contexto a una ubicación visible para el Agent", "Mueve el contexto a un lugar visible para el Agent"),
        ("flujo de mensajes de intermediarios y Agents", "flujo de mensajes entre personas y Agents"),
        ("Los mensajes del canal se pueden convertir en Tasks", "Los mensajes del Channel se pueden convertir en Task"),
        ("historial del canal", "historial del Channel"),
        ("Miembro del canal", "Miembro del Channel"),
        ("mismo canal", "mismo Channel"),
        ("en el panel", "en el Task Board"),
        ("vista de panel", "vista de Task Board"),
        ("vista del panel", "vista del Task Board"),
        ("Panel de Tasks", "Task Board"),
        ("panel de hilos", "panel de Thread"),
        ("el panel muestre", "el Task Board muestre"),
        ("Multijugador", "Varias personas"),
        ("como usar", "Cómo usar"),
        ("próximos pasos", "Next Actions"),
        ("persona a cargo", "responsable"),
    ),
    "vi": (
        ("Chần chừ", "Slack"),
        ("Đại lý", "Agent"),
        ("đại lý", "Agent"),
        ("Tác nhân", "Agent"),
        ("tác nhân", "Agent"),
        ("Kênh", "Channel"),
        ("kênh", "Channel"),
        ("Nhiệm vụ", "Task"),
        ("nhiệm vụ", "Task"),
        ("tin tức", "Tin nhắn"),
        ("Giải thích chức năng chi tiết", "Tính năng"),
        ("Luyện tập theo nhóm", "Thực tiễn nhóm"),
        ("Đội đổ bộ", "Hướng dẫn triển khai nhóm"),
        ("khái niệm cơ bản", "Khái niệm cơ bản"),
        ("thực tiễn tốt nhất", "Thực tiễn tốt nhất"),
        ("sự hợp tác giữa người và máy", "cộng tác giữa người và AI"),
        ("Tham gia hoặc thành lập một tổ chức", "Tham gia hoặc tạo Organization"),
        ("Thiết lập tác vụ theo lịch trình", "Thiết lập Task định kỳ"),
        ("Tại sao Tin nhắn lại quan trọng?", "Tại sao tin nhắn quan trọng?"),
        ("Đầu tiên chia Channel", "Trước tiên, chia Channel"),
        ("Di chuyển bối cảnh đến một vị trí mà Agent hiển thị", "Chuyển bối cảnh đến nơi Agent có thể nhìn thấy"),
        ("luồng tin nhắn của người trung gian và Agent", "luồng tin nhắn giữa người dùng và Agent"),
        ("Nhân viên AI", "AI Agent"),
        ("trang tổng quan", "Task Board"),
        ("bảng chủ đề", "bảng Thread"),
        ("Bảng Task Channel", "Task Board của Channel"),
        ("bảng Task", "Task Board"),
        ("Bảng Task", "Task Board"),
    ),
}


def normalize_translated_text(text: str, lang: str) -> str:
    for bad, good in TRANSLATION_TEXT_REPLACEMENTS.get("all", ()):
        text = text.replace(bad, good)
    for bad, good in TRANSLATION_TEXT_REPLACEMENTS.get(lang, ()):
        text = text.replace(bad, good)
    return text


SIDEBAR_GROUPS = [
    (
        "快速入门",
        [
            ("文档首页", "/zh/docs/"),
            ("什么是 Syfo", "/zh/docs/what-is-syfo.html"),
            ("快速上手", "/zh/docs/getting-started.html"),
            ("创建第一个 Agent", "/zh/docs/first-agent.html"),
        ],
    ),
    (
        "基础概念",
        [
            ("组织", "/zh/docs/organization.html"),
            ("频道与协作", "/zh/docs/channels.html"),
            ("Agent", "/zh/docs/agents.html"),
            ("任务", "/zh/docs/tasks.html"),
            ("消息", "/zh/docs/messages.html"),
            ("文件与交付物", "/zh/docs/files-and-deliverables.html"),
            ("Skill 集成", "/zh/docs/skills.html"),
        ],
    ),
    (
        "功能详解",
        [
            ("运行环境", "/zh/docs/computers.html"),
            ("提醒与定时任务", "/zh/docs/reminders.html"),
            ("消息投递机制", "/zh/docs/message-delivery.html"),
            ("企业系统集成", "/zh/docs/integrations.html"),
        ],
    ),
    (
        "团队实践",
        [
            ("团队落地", "/zh/docs/team-playbook.html"),
            ("最佳实践", "/zh/docs/best-practices.html"),
        ],
    ),
    (
        "常见问题",
        [
            ("FAQ", "/zh/docs/faq.html"),
            ("安全与权限", "/zh/docs/security.html"),
        ],
    ),
]


LINK_MAP = {
    "/guide": "/zh/docs/",
    "/guide/": "/zh/docs/",
    "/guide/what-is-syfo": "/zh/docs/what-is-syfo.html",
    "/guide/getting-started": "/zh/docs/getting-started.html",
    "/guide/first-agent": "/zh/docs/first-agent.html",
    "/guide/team-onboarding": "/zh/docs/team-playbook.html",
    "/guide/best-practices": "/zh/docs/best-practices.html",
    "/guide/customer-questions": "/zh/docs/faq.html",
    "/features/squad": "/zh/docs/channels.html",
    "/features/custom-skills": "/zh/docs/skills.html",
    "/features/reminders": "/zh/docs/reminders.html",
    "/features/message-delivery": "/zh/docs/message-delivery.html",
    "/features/integrations": "/zh/docs/integrations.html",
    "/faq": "/zh/docs/faq.html",
    "/faq/": "/zh/docs/faq.html",
    "/faq/agents": "/zh/docs/faq.html",
    "/faq/security": "/zh/docs/security.html",
    "/concepts/channels": "/zh/docs/channels.html",
    "/concepts/agents": "/zh/docs/agents.html",
    "/concepts/tasks": "/zh/docs/tasks.html",
    "/concepts/messages": "/zh/docs/messages.html",
    "/concepts/files": "/zh/docs/files-and-deliverables.html",
    "/concepts/files-and-deliverables": "/zh/docs/files-and-deliverables.html",
    "/concepts/organization": "/zh/docs/organization.html",
    "/concepts/computer": "/zh/docs/computers.html",
    "/concepts/computers": "/zh/docs/computers.html",
}


PAGE_META = {
    "index.html": ("Syfo 文档", "从理解产品到团队落地，把 Syfo 作为人机协作工作空间用起来。", "Syfo 文档", "从理解到落地的完整路径"),
    "what-is-syfo.html": ("什么是 Syfo", "理解 Syfo 和传统聊天工具、AI chatbot 的区别。", "概念", "什么是 Syfo"),
    "getting-started.html": ("快速上手", "6 步完成首次协作：进入频道、@Agent、转任务、设置定时任务。", "快速上手", "6 步完成第一次人机协作"),
    "first-agent.html": ("创建第一个 Agent", "跟着 Daily Briefing 案例创建一个可持续工作的 Agent。", "Agent", "创建你的第一个 Agent"),
    "organization.html": ("组织", "理解组织作为工作空间的边界：成员、频道、Agent 和权限。", "基础概念", "组织"),
    "channels.html": ("频道与协作", "用频道组织上下文、任务和多 Agent 协作。", "基础概念", "频道与多 Agent 协作"),
    "agents.html": ("Agent", "理解 Agent 在 Syfo 里的角色、权限、运行方式和触发方式。", "基础概念", "Agent"),
    "tasks.html": ("任务", "理解任务如何从消息产生、被认领、推进、审核和交付。", "基础概念", "任务"),
    "messages.html": ("消息", "理解消息如何成为任务、提醒和交付物的锚点。", "基础概念", "消息"),
    "files-and-deliverables.html": ("文件与交付物", "区分过程素材和最终成果，让交付物可追踪、可审核、可交接。", "基础概念", "文件与交付物"),
    "skills.html": ("Skill 集成", "给 Agent 安装 Skill，让它理解工具、流程和业务边界。", "基础概念", "让 Agent 具备可复用能力"),
    "computers.html": ("运行环境", "理解 Agent 跑在本机还是云端，以及它能访问哪些工具和凭据。", "功能详解", "运行环境"),
    "reminders.html": ("提醒与定时任务", "让 Agent 在指定时间自动提醒、汇总、监控和执行任务。", "功能详解", "提醒与定时任务"),
    "message-delivery.html": ("消息投递机制", "理解频道里 Agent 数量如何影响消息处理和成本。", "功能详解", "消息投递机制"),
    "integrations.html": ("企业系统集成", "让业务系统继续做入口，Syfo 承接 Agent、任务、上下文和审计。", "功能详解", "企业系统集成"),
    "team-playbook.html": ("团队落地指南", "从个人试用扩展到团队协作的频道、Agent 和上下文设计方法。", "团队实践", "把 Syfo 放进团队日常工作"),
    "best-practices.html": ("最佳实践", "从规划、分诊 Agent、上下文管理到任务板维护的实际经验。", "团队实践", "让 Agent 真正成为团队成员"),
    "faq.html": ("常见问题", "评估、上手、Agent 使用、安全权限和工具集成问题。", "常见问题", "常见问题"),
    "security.html": ("安全与权限", "理解组织、频道、Agent 运行环境和外部系统凭据如何共同决定权限边界。", "常见问题", "安全与权限"),
}


def copy_assets() -> None:
    IMG_OUT.mkdir(parents=True, exist_ok=True)
    for base in [DOCS_SRC / "public" / "images", DOCS_SRC / "public" / "assets"]:
        if not base.exists():
            continue
        for src in base.rglob("*"):
            if src.is_file():
                rel = src.relative_to(base)
                dest = IMG_OUT / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)


def split_frontmatter(md: str) -> str:
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            return md[end + 4 :].lstrip()
    return md


def strip_top_heading(md: str) -> str:
    return re.sub(r"^# .*$\n?", "", split_frontmatter(md), count=1, flags=re.MULTILINE).lstrip()


def rewrite_link(url: str) -> str:
    if url.startswith("/images/"):
        return "/zh/docs/images/" + url.split("/images/", 1)[1]
    if url.startswith("/assets/"):
        return "/zh/docs/images/" + url.split("/assets/", 1)[1]
    if url in LINK_MAP:
        return LINK_MAP[url]
    if url.startswith("/guide/"):
        key = url.rstrip("/")
        return LINK_MAP.get(key, "https://syfo-docs.tool.reorc.cloud" + url)
    if url.startswith("/features/") or url.startswith("/faq/") or url.startswith("/concepts/"):
        key = url.rstrip("/")
        return LINK_MAP.get(key, "https://syfo-docs.tool.reorc.cloud" + url)
    return url


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text, flags=re.UNICODE)
    return text.strip("-").lower() or "section"


def inline(text: str) -> str:
    placeholders: list[str] = []

    def protect(match: re.Match[str]) -> str:
        placeholders.append(match.group(0))
        return f"@@HTML{len(placeholders)-1}@@"

    text = re.sub(r"<(kbd|code|span|br|strong|em|sub|sup|img|a)\b[^>]*>.*?</\1>|<br\s*/?>", protect, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: image_html(m.group(1), m.group(2)), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{html.escape(rewrite_link(m.group(2)), quote=True)}">{m.group(1)}</a>', text)
    for i, value in enumerate(placeholders):
        text = text.replace(f"@@HTML{i}@@", value)
    return text


def image_html(alt: str, url: str) -> str:
    src = rewrite_link(url)
    return f'<figure><img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}"><figcaption>{html.escape(alt)}</figcaption></figure>'


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) >= 2 and all(set(c.replace(":", "").replace("-", "")) == set() for c in rows[1]):
        header, body = rows[0], rows[2:]
    else:
        header, body = rows[0], rows[1:]
    th = "".join(f"<th>{inline(c)}</th>" for c in header)
    trs = ["<thead><tr>" + th + "</tr></thead>", "<tbody>"]
    for row in body:
        trs.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    trs.append("</tbody>")
    return '<div class="table-wrap"><table>' + "".join(trs) + "</table></div>"


def markdown_to_html(md: str, extra_intro: str = "") -> str:
    md = split_frontmatter(md)
    md = re.sub(r"^# .*$\n?", "", md, count=1, flags=re.MULTILINE)
    lines = md.splitlines()
    out: list[str] = []
    para: list[str] = []
    list_stack: list[str] = []
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    in_admonition = False
    admonition_title = ""
    table_lines: list[str] = []

    if extra_intro:
        out.append(extra_intro)

    def flush_para() -> None:
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(x.strip() for x in para)) + "</p>")
            para = []

    def close_lists() -> None:
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            out.append(render_table(table_lines))
            table_lines = []

    for raw in lines:
        line = raw.rstrip()

        if in_code:
            if line.startswith("```"):
                out.append(f'<pre><code class="language-{html.escape(code_lang)}">{html.escape(chr(10).join(code_lines))}</code></pre>')
                in_code = False
                code_lines = []
                code_lang = ""
            else:
                code_lines.append(raw)
            continue

        if line.startswith("```"):
            flush_para(); flush_table(); close_lists()
            in_code = True
            code_lang = line.strip("`").strip()
            continue

        if line.startswith(":::"):
            flush_para(); flush_table(); close_lists()
            if in_admonition:
                out.append("</div>")
                in_admonition = False
            else:
                admonition_title = line.replace(":::", "").strip() or "提示"
                if admonition_title.lower() == "tip":
                    admonition_title = "提示"
                out.append(f'<div class="note"><strong>{html.escape(admonition_title)}</strong>')
                in_admonition = True
            continue

        if line.strip() in {"---", "***"}:
            flush_para(); flush_table(); close_lists()
            continue

        if not line.strip():
            flush_para(); flush_table(); close_lists()
            continue

        if line.strip() in {"<figure>", "</figure>"} or "<figcaption" in line:
            flush_para(); flush_table(); close_lists()
            continue

        if line.startswith("|") and "|" in line[1:]:
            flush_para(); close_lists()
            table_lines.append(line)
            continue
        else:
            flush_table()

        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_para(); close_lists()
            level = max(2, len(heading.group(1)))
            title = heading.group(2).strip()
            hid = slugify(title)
            out.append(f'<h{level} id="{hid}">{inline(title)}</h{level}>')
            continue

        img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line.strip())
        if img:
            flush_para(); close_lists()
            out.append(image_html(img.group(1), img.group(2)))
            continue

        raw_img = re.search(r'<img\s+[^>]*src="([^"]+)"[^>]*>', line)
        if raw_img:
            flush_para(); close_lists()
            src = rewrite_link(raw_img.group(1))
            alt_match = re.search(r'alt="([^"]*)"', line)
            alt = alt_match.group(1) if alt_match else ""
            out.append(image_html(alt or "Syfo 产品截图", src))
            continue

        ul = re.match(r"^\s*[-*]\s+(.+)$", line)
        ol = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if ul or ol:
            flush_para()
            tag = "ul" if ul else "ol"
            text = (ul or ol).group(1)
            if not list_stack or list_stack[-1] != tag:
                close_lists()
                out.append(f"<{tag}>")
                list_stack.append(tag)
            out.append(f"<li>{inline(text)}</li>")
            continue

        blockquote = re.match(r"^>\s?(.+)$", line)
        if blockquote:
            flush_para(); close_lists()
            out.append(f"<blockquote>{inline(blockquote.group(1))}</blockquote>")
            continue

        close_lists()
        para.append(line)

    flush_para(); flush_table(); close_lists()
    if in_admonition:
        out.append("</div>")
    return "\n".join(out)


def read_md(*parts: str) -> str:
    return split_frontmatter(DOCS_SRC.joinpath(*parts).read_text(encoding="utf-8"))


def clarify_terms(md: str) -> str:
    replacements = [
        ("Runtime", "Runtime（运行环境——决定 Agent 跑在你的电脑上还是云端）"),
        ("MCP", "MCP（一种标准化的工具连接协议）"),
        ("CLI", "CLI（命令行工具）"),
        ("Thread", "Thread（话题——消息的子对话）"),
        ("Action Card", "Action Card（操作确认卡片——Agent 生成后需要人点击批准才执行）"),
    ]
    for old, new in replacements:
        md = md.replace(old, new, 1)
    return md


def extract_md_section(md: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(md)
    if not match:
        return ""
    next_match = re.search(r"^## .+$", md[match.end() :], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(md)
    return md[match.start() : end].strip()


def split_html_h2(rendered: str) -> dict[str, str]:
    matches = list(re.finditer(r'<h2 id="[^"]+">(.+?)</h2>', rendered))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        title = re.sub(r"<[^>]+>", "", match.group(1))
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(rendered)
        sections[html.unescape(title)] = rendered[match.start() : end].strip()
    return sections


def demote_h2(rendered: str) -> str:
    return rendered.replace("<h2 ", "<h3 ").replace("</h2>", "</h3>")


def render_md_question(md: str) -> str:
    return demote_h2(markdown_to_html(md))


def build_index() -> str:
    cards = [
        ("什么是 Syfo", "理解 Syfo 和 Slack/飞书、普通 AI Chatbot 的区别。", "/zh/docs/what-is-syfo.html"),
        ("快速上手", "6 步完成首次协作，包含 @Agent、任务和定时任务。", "/zh/docs/getting-started.html"),
        ("创建第一个 Agent", "跟着 Daily Briefing 案例创建一个真正能工作的 Agent。", "/zh/docs/first-agent.html"),
        ("频道与协作", "学习频道设计、任务推进和多 Agent 协作模式。", "/zh/docs/channels.html"),
        ("团队落地", "规划频道、Agent 分工、上下文迁移和团队规范。", "/zh/docs/team-playbook.html"),
        ("最佳实践", "从分诊 Agent、上下文管理到任务板维护的实际经验。", "/zh/docs/best-practices.html"),
        ("常见问题", "评估、上手、Agent 使用、安全权限和工具集成问题。", "/zh/docs/faq.html"),
    ]
    html_cards = "\n".join(
        f'<a class="doc-card" href="{href}"><span>Syfo Docs</span><h3>{title}</h3><p>{desc}</p><div>查看文档 →</div></a>'
        for title, desc, href in cards
    )
    return f"""
<section class="doc-section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">用户路径</span>
      <h2>先跑通一次，再扩展到团队。</h2>
      <p>按从了解产品到团队落地的顺序组织内容，先完成第一次协作，再逐步扩展到频道、Agent 分工和团队规范。</p>
    </div>
    <div class="doc-grid">{html_cards}</div>
    <div class="cta-row">
      <a class="btn btn-primary" href="/zh/docs/getting-started.html">开始 6 步快速上手 <span>→</span></a>
      <a class="btn btn-ghost" href="https://syfo.ai/guide">完整图文教程 <span>→</span></a>
    </div>
  </div>
</section>
<section class="doc-section compact" id="next">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">团队落地</span><h2>从第一个 Agent 到团队协作，这些经验帮你少走弯路。</h2></div>
    <div class="quick-list">
      <a href="/zh/docs/team-playbook.html"><b>团队上手指南</b><span>频道拆分、Agent 数量、上下文迁移和团队规范。</span></a>
      <a href="/zh/docs/best-practices.html"><b>最佳实践</b><span>让 Agent 做规划、分诊、代码协作和任务板维护。</span></a>
    </div>
  </div>
</section>"""


def build_getting_started() -> str:
    md = read_md("guide", "getting-started.md")
    md = md.replace(
        "五分钟，把 Syfo 用起来。",
        "五分钟，把 Syfo 用起来。\n\n::: tip\n如果你的组织里已经有 Agent，可以直接从第 3 步进入频道开始；如果还没有 Agent，先看 [创建你的第一个 Agent](/guide/first-agent)，再回到这里完成第一次协作。\n:::",
    )
    md = clarify_terms(md)
    md = md.replace(
        "**接下来：**\n- [创建你的第一个 Agent](/guide/first-agent) — 从零配置专属 Agent\n- [团队上手指南](/guide/team-onboarding) — 规划频道、Agent 分工、上下文接入和团队使用规范",
        """**接下来：**
- [创建你的第一个 Agent](/guide/first-agent) — 如果你的组织里还没有 Agent，从这里创建一个
- [给 Agent 安装 Skill](/features/custom-skills) — 让 Agent 访问外部工具、遵循特定流程
- [团队上手指南](/guide/team-onboarding) — 规划频道、Agent 分工、上下文接入和团队使用规范""",
    )
    content = markdown_to_html(md)
    content = re.sub(r'(<h2 id="[^"]*agent[^"]*">4\. 和 Agent 说话</h2>)', r'<span id="first-message"></span>\1', content)
    return content


def build_first_agent() -> str:
    md = read_md("guide", "first-agent.md")
    md = md.replace(
        "Agent 需要一个 runtime 才能运行。有两种选择：",
        "Runtime 是 Agent 的运行环境，决定它跑在你的电脑上还是云端。Agent 需要一个 Runtime 才能运行。有两种选择：",
    )
    md = md.replace("Daily Briefing", "每日简报（Daily Briefing）", 1)
    return markdown_to_html(md)


def build_what_is_syfo() -> str:
    md = read_md("guide", "what-is-syfo.md")
    md = md.replace("**Thread** — 消息的子对话。", "**Thread（话题——消息的子对话）** — 执行中的工作在 Thread 里更新进度，不打扰主频道。")
    md = md.replace("执行中的工作在 Thread 里更新进度，不打扰主频道。", "", 1)
    return markdown_to_html(md)


def build_channels() -> str:
    base = """
# 频道与协作

频道是 Syfo 里的工作现场。人和 Agent 在同一个上下文里沟通、推进任务、沉淀交付物。

## 频道和群聊有什么不同

频道看起来像群聊，但它承担更多工作。Agent 能读取频道上下文、接任务、回报进度。任务和交付物也挂在频道消息上，方便追溯。频道不只是聊天，它是项目上下文的容器。

## 公开频道、私有频道和 DM

**公开频道** — 组织内所有成员都可以加入和查看。适合全员公告、技术讨论、公共项目。

**私有频道** — 只有被邀请的成员和 Agent 能看到。适合敏感项目、客户专项。

**DM（私聊）** — 和某个人或 Agent 的一对一对话。需要团队共同可见的工作，不建议长期放在 DM 里。

## Thread（话题）

Thread 是一条消息下面的子对话。主频道放结论和关键进展；具体执行过程、排查细节、Agent 的中间更新，放在 Thread 里。

- 点消息右侧的「回复」图标开一个 Thread
- Thread 在屏幕右侧展开，主频道仍然可见
- @mention 的人会收到通知

## 搜索

`Ctrl+K`（Windows）或 `⌘K`（macOS）打开全局搜索，可以搜消息、任务、成员，支持按频道过滤。

## 管理频道

- **创建**：左侧栏「+ 添加频道」，填名字、选公开或私有
- **邀请 Agent**：频道设置 → 成员 → 邀请 → 搜索 Agent 名字
- **归档**：项目结束后归档而不是删除，历史记录保留

## 频道命名建议

- 用连字符：`#product-design`，不用空格或下划线
- 加前缀区分用途：`#team-engineering`、`#proj-rebrand`
- Agent 专用频道可加 `bot-` 前缀

## 频道适合承载什么

- 一个项目或客户的持续推进；
- 一个团队的日常研发、运营、销售或支持工作；
- 一个需要多人和 Agent 同时协作的专项任务；
- 一个需要保留过程、决策和交付物的长期上下文。

## Agent 不是越多越好

频道里每多一个 Agent，同一条消息就可能被更多 Agent 读取，讨论也更容易变吵。先保证职责清晰，再增加 Agent。
"""
    squad = strip_top_heading(read_md("features", "squad.md"))
    return markdown_to_html(base + "\n\n## 频道构成与多 Agent 协作\n\n" + squad)


def build_concept_page(filename: str) -> str:
    md = strip_top_heading(read_md("concepts", filename))
    md = clarify_terms(md)
    md = md.replace("Thread（话题——消息的子对话） ", "Thread（话题——消息的子对话）")
    md = md.replace("DM", "DM（私聊）", 1)
    md = md.replace("@mention", "@mention（@ 提及）", 1)
    md = md.replace("Org 设置", "组织设置")
    return markdown_to_html(md)


def clean_imported_md(md: str) -> str:
    md = strip_top_heading(md)
    md = re.sub(r'<div class="screenshot-placeholder">.*?</div>\n?', "", md, flags=re.DOTALL)
    md = md.replace("Thread（话题——消息的子对话） ", "Thread（话题——消息的子对话）")
    md = md.replace("Org 设置", "组织设置")
    return clarify_terms(md)


def build_organization() -> str:
    md = """
# 组织

组织（Organization）是 Syfo 里的工作空间。一个公司、一个团队或一个独立项目，通常对应一个组织。

## 组织里有什么

组织不是一个聊天群——它是权限和上下文的边界。

组织里包含：成员（人和 Agent）、频道、任务、文件和交付物。团队换人、项目切换或 Agent 重启后，上下文都还在。

## 成员和权限

- 组织内的成员可以加入不同频道
- Agent 也属于组织，但只能看到它被邀请进入的频道
- 管理员负责邀请成员、管理 Agent、配置计费和查看审计日志
- 管理员不等于能看所有内容——私有频道和私聊有自己的可见范围

## 什么时候需要多个组织

一个简单判断：

- 两个团队共享成员、Agent 和账单 → 同一个组织，用频道区分
- 权限、账单和数据需要完全隔离 → 拆成两个组织

大多数情况下，不同项目用不同频道就够了，不需要建多个组织。
"""
    return markdown_to_html(md)


def build_message_delivery() -> str:
    md = """
# 消息投递机制

这篇帮你理解一件事：为什么频道里 Agent 越多，消息和算力成本会变高。

## 一条消息会发生什么

你在频道里发消息时，频道内的 Agent 会接收到它。

- 1 个 Agent → 你的消息投递给它，它读上下文，决定是否回复
- 5 个 Agent → 同一条消息被 5 个 Agent 各读一遍，每个都带上必要的频道历史

## 多 Agent 成本为什么增长快

假设频道里有 N 个 Agent，你发 1 条消息，每个 Agent 各回复 1 条：

1. 你的消息投递给 N 个 Agent → N 次处理
2. N 个 Agent 的回复又被其他 Agent 接收 → 约 N x N 次处理

合计约 N + N² = N(N + 1)。这不是账单公式，但说明了增长趋势：

- 1 个 Agent → 2 次（基准）
- 2 个 Agent → 6 次（3 倍）
- 3 个 Agent → 12 次（6 倍）
- 5 个 Agent → 30 次（15 倍）

## 怎么控制成本

- **先从少量 Agent 开始**：一个 Agent 能分步完成的，不要拆成多个
- **把频道拆清楚**：轻任务用「多人 + 1 Agent」，专项研究再临时加
- **给 Agent 明确分工**：职责重叠的 Agent 会重复读同样的上下文
- **用 Thread 收敛讨论**：减少主频道噪音，也降低 Agent 不必要的处理
- **移除不需要的 Agent**：阶段性工作结束后，把 Agent 移出频道
"""
    return markdown_to_html(md)


def build_integrations() -> str:
    md = """
# 企业系统集成

企业已经有客服系统、CRM、ERP、BI 和各种内部工具。Syfo 不需要把这些业务都搬进来——更实际的做法是让 Syfo 和现有系统配合工作。

## 两个方向

**方向一：外部系统调用 Syfo**

在现有业务系统里加一个入口，把上下文传给 Syfo Agent。

以客服系统为例：

1. 客服打开一个工单
2. 点击「让 Syfo 分析」
3. 系统把工单内容发给 Syfo Agent
4. Agent 查知识库、分析问题、起草回复
5. 客服确认后再发给客户

好处：不用改掉现有工作台，Syfo 只在需要 AI 协作时介入。

**方向二：Agent 主动访问外部系统**

让 Agent 被授权访问企业系统。比如市场 Agent 每天自动查竞品动态，整理成日报发到频道。

接入方式的优先级：

- **API / CLI / MCP / Skill**（推荐）— 稳定、可测试、可审计
- **稳定网页表单** — 可以过渡，需要做错误处理
- **浏览器自动化** — 适合验证，不适合长期依赖

## 推荐落地顺序

1. 先让外部系统调用 Syfo，跑通一个高价值流程
2. 把 Agent 的输入、输出和审核记录沉淀到 Syfo
3. 把常用动作封成 Skill
4. 最后做 Agent 独立身份和按应用授权

## 最小接入示例

如果只做第一版，不需要完整插件市场：

- 业务系统新增「Ask Syfo Agent」按钮
- 后端调用 Syfo Agent API
- Syfo 返回任务链接和建议回复
- 人工确认后再回写业务系统
"""
    md = md.replace("CLI", "CLI（命令行工具）", 1)
    md = md.replace("MCP", "MCP（工具连接协议）", 1)
    return markdown_to_html(md)


def build_skills() -> str:
    install = """
# Skill 集成

## 一句话安装 Syfo 使用指导 Skill

私聊你的 Agent，发送：

```
@你的Agent 请安装 https://syfo-docs.tool.reorc.cloud/skill.md 后续回答 Syfo 相关问题时优先使用该 skill
```

安装完成后，Agent 回答 Syfo 使用、频道设计、任务推进、团队协作等问题时，会优先参考这份 Skill。
"""
    custom_skills = clarify_terms(read_md("features", "custom-skills.md"))
    custom_skills = custom_skills.replace(
        "Skill 是 Agent 使用外部工具、遵守特定流程、连接企业系统的一组能力说明。",
        "Skill 可以理解为给 Agent 的能力说明和工具配置。它告诉 Agent 可以使用哪些外部工具、要遵守什么流程、连接哪些企业系统。",
    )
    return markdown_to_html(install + "\n" + custom_skills)


def build_computers() -> str:
    md = """
# 运行环境

Agent 需要一个地方来运行——这就是运行环境。它决定了 Agent 能用什么工具、访问哪些文件、是否 24 小时在线。

## 两种运行环境

**你的电脑（本机）**

Agent 跑在你自己的电脑上，能直接使用本机已有的代码仓库、命令行工具和开发环境。适合开发调试、临时任务和需要本地文件的场景。

电脑关机或断网时，Agent 会暂停工作。

**Syfo Cloud（云端）**

Agent 跑在云端服务器上，7×24 小时在线。适合定时任务（日报、数据监控、市场情报）、长期在线的客服/运营 Agent。

云端 Agent 需要单独配置它能访问的工具和凭据。

## 怎么选

不需要纠结——看 Agent 要做什么：

- 需要访问本地代码或调试 → 本机
- 需要 24 小时自动执行 → 云端
- 先试跑再决定 → 从本机开始，稳定后迁到云端

## 权限和运行环境的关系

Agent 能做什么，取决于运行环境里有什么：

- 没有某个代码仓库 → Agent 不能修改它
- 没有某个命令行工具 → Agent 不能调用它
- 外部系统需要 token → 需要在运行环境里配置

建议按工作边界拆分 Agent 或运行环境，不要把所有权限集中在一个地方。
"""
    return markdown_to_html(md)


def build_reminders() -> str:
    md = """
# 提醒与定时任务

Agent 可以在指定时间自动执行工作，不需要你每次手动触发。

## 设置定时任务

直接 @mention Agent，用自然语言说明时间和内容：

```
@Agent 每天早上 9 点，把昨天 #dev 频道的讨论整理成简报发到这里
```

Agent 会确认并自动按计划执行。

## 设置一次性提醒

```
@Agent 明天下午 3 点提醒我跟进 XX 客户
```

到时间后 Agent 会在频道或 DM 里发送提醒。

## 常见场景

- **日报/周报**：每日或每周一自动汇总进度
- **市场情报**：每天搜集竞品动态和行业新闻
- **数据监控**：每小时检查关键指标，异常时通知
- **内容发布**：内容准备好后，在最佳时间自动发布
- **团队 Standup**：每天自动向成员收集进度更新

## 管理已有的提醒

**查看所有提醒：**

```
@Agent 列出我的所有提醒
```

**修改时间：**

```
@Agent 把每日简报改到下午 6 点发
```

**取消提醒：**

```
@Agent 取消明天的那个提醒
```

## 注意事项

- 定时任务需要 Agent 在云端运行（本机关机后无法执行）
- 每个定时任务有执行日志，可以随时查看历史
- 执行失败时，Agent 会发送错误通知
"""
    return markdown_to_html(md.replace("@mention", "@mention（@ 提及）", 1).replace("DM", "DM（私聊）", 1))


def build_security() -> str:
    md = clean_imported_md(read_md("faq", "security.md"))
    md = md.replace("真实使用 FAQ](/faq/)", "FAQ](/zh/docs/faq.html)")
    md = md.replace("CLI", "CLI（命令行工具）", 1)
    return markdown_to_html(md)


def build_faq() -> str:
    customer = split_html_h2(build_customer_questions())
    faq_index = read_md("faq", "index.md")
    faq_agents = read_md("faq", "agents.md")
    faq_security = read_md("faq", "security.md")

    def customer_q(title: str) -> str:
        return demote_h2(customer.get(title, ""))

    def source_q(md: str, title: str) -> str:
        section = extract_md_section(md, title)
        section = section.replace(
            "详见 [真实使用 FAQ](/faq/) 中的私聊说明。",
            "相关说明可以参考本页前面的私聊问题。",
        )
        section = section.replace(
            "详见 [文件和交付物](/concepts/files-and-deliverables)。",
            "可以参考本页“文件和交付物有什么区别？”这一问。",
        )
        section = section.replace(
            "在 Thread 里更新进度",
            "在 Thread（话题，消息下的子对话）里更新进度",
        )
        section = section.replace(
            "在 Thread 里直接指出问题",
            "在 Thread 里直接指出问题",
        )
        section = section.replace(
            "没有进频道的 Agent 看不到频道消息、Thread、任务和附件。",
            "没有进频道的 Agent 看不到频道消息、Thread、任务和附件。",
        )
        return render_md_question(section) if section else ""

    def short_q(title: str, body: str) -> str:
        return f'<h3 id="{slugify(title)}">{html.escape(title)}</h3>\n<p>{inline(body)}</p>'

    def group(title: str, *chunks: str) -> str:
        body = "\n".join(chunk for chunk in chunks if chunk)
        return f'<h2 id="{slugify(title)}">{html.escape(title)}</h2>\n{body}'

    intro = """
<p>这里整理了评估、上手和日常使用 Syfo 时最常见的问题。你可以按主题快速找到答案，也可以从这些问题判断 Syfo 适合放进哪些团队工作流。</p>
"""
    return "\n".join(
        [
            intro,
            group(
                "一、Syfo 和现有工具",
                customer_q("我们已经有飞书 / 企业微信 / Slack，为什么还要 Syfo？")
                + "<p>如果团队还继续使用飞书，Syfo 可以通过命令行工具或集成能力读写文档、群聊、多维表格等内容；协作过程留在 Syfo 频道里，必要时再把结果写回现有系统。</p>",
                customer_q("企业内部系统很多，Syfo 怎么打通？"),
                customer_q("模型调用走什么渠道？数据安不安全？"),
            ),
            group(
                "二、创建和配置 Agent",
                source_q(faq_agents, "Agent 是什么？"),
                customer_q("不知道怎么创建 Agent，应该从哪里开始？"),
                source_q(faq_index, "什么时候新建 Agent，什么时候复用 Agent？")
                + '<p>更多说明见 <a href="/zh/docs/channels.html">频道与协作</a>。</p>',
                source_q(faq_index, "本地电脑和 Syfo Cloud 有什么区别？"),
                source_q(faq_index, "我的电脑已经安装了 Claude Code / Codex 并配置了常见 Skill / MCP，如何接入 Syfo？"),
                customer_q("Agent 是不是只能靠浏览器点页面？"),
            ),
            group(
                "三、频道和协作",
                short_q("一个频道里该放几个 Agent？", "先少后多。固定项目建议先用“多人 + 1 个驻场 Agent”跑通流程；需要更多角色时，再按职责增加。详细判断见 [频道与协作](/zh/docs/channels.html)。"),
                short_q("多个 Agent 会不会乱？", "会，所以不要一开始就把多个 Agent 拉进同一个频道。先定义谁拆任务、谁执行、谁 review、哪些动作需要人确认；详细方法见 [频道与协作](/zh/docs/channels.html)。"),
                customer_q("定时任务已经指派给某个 Agent，为什么全频道 Agent 都收到通知？"),
                source_q(faq_agents, "Agent 为什么会把后续问题归到同一个任务？"),
            ),
            group(
                "四、Agent 行为和调优",
                source_q(faq_agents, "怎么让 Agent 开始工作？"),
                source_q(faq_index, "Agent 一直显示工作中、不回复，怎么办？"),
                customer_q("为什么 Agent 有时要等一两分钟？慢在哪？"),
                customer_q("Agent 遇到问题为什么总停下来等我确认？"),
                customer_q("Agent 一个小改动就建分支、反复通读整个仓库，正常吗？"),
                source_q(faq_agents, "Agent 做错了怎么办？"),
                source_q(faq_agents, "如何暂停、移除或重置 Agent？"),
            ),
            group(
                "五、安全和权限",
                short_q("Agent 可以访问我的私人数据吗？", "Agent 只能访问它被邀请进入的频道和它自己的私聊。它看不到没有加入的频道，也看不到其他成员之间的私信。外部系统还需要额外授权。"),
                short_q("Agent 能不能像个人助理一样处理日程、文档、飞书消息？", "可以，但要单独设计身份和权限。个人助理型 Agent 涉及个人信息，不适合多人共用。建议每人单独创建 Agent，或为敏感岗位配置独立 Agent。"),
                source_q(faq_index, "我可以私聊任何 Agent 吗？"),
                source_q(faq_security, "Agent 能看到哪些频道？"),
                source_q(faq_security, "Agent 能看到其他人的私聊吗？"),
                source_q(faq_security, "公用 Agent 会不会泄露客户数据？"),
                source_q(faq_security, "Agent 加入私密频道为什么要受限制？"),
                source_q(faq_security, "谁可以私聊 Agent？"),
                source_q(faq_security, "Agent 使用外部系统时，凭据放在哪里？"),
                short_q("高风险操作怎么避免 Agent 乱来？", "高风险操作不要靠“相信 Agent 会懂”来控制，要提前写清二次确认规则：什么时候确认、谁确认、确认什么、保留什么。需要系统内确认时，可以让 Agent 生成 Action Card（操作确认卡片——Agent 生成后需要人点击批准才执行）。详细说明见 [最佳实践](/zh/docs/best-practices.html)。"),
                source_q(faq_security, "哪些动作必须人工确认？"),
            ),
            group(
                "六、工具和扩展",
                source_q(faq_agents, "Agent 可以定时自动执行任务吗？"),
                source_q(faq_index, "文件和交付物有什么区别？"),
                source_q(faq_index, "Syfo Agent 有没有图片 / 视频生成能力，比如 GPT Image？"),
                customer_q("开发过程像黑盒，只能看结果，怎么知道改了什么、怎么回滚？"),
                source_q(faq_security, "是否支持私有化部署？"),
            ),
        ]
    )


def build_team_playbook() -> str:
    md = read_md("guide", "team-onboarding.md")
    md = md.replace(
        "这页给团队负责人、项目负责人和管理员使用。它不重复讲怎么创建 Agent，而是帮助你把现有业务拆成适合 Syfo 协作的频道、Agent 和上下文。",
        "当团队准备正式引入 Syfo 时，第一步不是建 Agent，而是想清楚频道怎么拆、Agent 怎么分工、上下文放在哪里。这篇指南帮你完成这个规划。",
    )
    return markdown_to_html(md)


def build_customer_questions() -> str:
    md = """# 使用常见问题

这里整理了团队在评估和使用 Syfo 时最常遇到的问题。你可以先从这些问题判断：Syfo 适合放进哪些工作流、如何和现有系统配合、以及怎样设置 Agent 的权限和边界。

## 我们已经有飞书 / 企业微信 / Slack，为什么还要 Syfo？

Syfo 不是要求你把所有沟通都迁走。它更适合放那些“人和 Agent 要一起推进工作”的频道。

传统 IM 里，AI 往往是一个插件或另一个窗口。你问完以后，结果要自己搬回群里，任务也要自己跟。Syfo 的区别是：Agent 就在频道里，看得到上下文，可以接任务、更新状态、交付结果。

适合用 Syfo 的地方通常有三个特征：

- 讨论会变成行动；
- 需要 AI 参与执行；
- 过程和结果需要被团队看见。

## 企业内部系统很多，Syfo 怎么打通？

不需要把所有业务系统都搬进 Syfo。更现实的方式是让 Syfo 和现有系统配合工作。

短期可以从明确的工具入口开始：让 Agent 通过 API、CLI（命令行工具）、MCP（一种标准化的工具连接协议）或 Skill 读取必要信息、执行稳定动作，再把结果回到频道里。比如查询知识库、读取 BI 指标、检查工单、同步项目状态。

长期可以按权限逐步开放更多系统能力。关键是每个工具都要有清晰边界：能看什么、能改什么、哪些动作需要人确认。

## Agent 是不是只能靠浏览器点页面？

不是。浏览器自动化只是最后手段。

生产环境最好让 Agent 使用 API、CLI（命令行工具）、MCP（工具连接协议）或 Skill。这样可测试、可审计，也不会因为页面按钮改了就失败。

如果业务系统只有网页、没有接口，可以先用浏览器自动化做验证，但长期应该把稳定动作沉淀成 Skill 或 API。

## 不知道怎么创建 Agent，应该从哪里开始？

不要从空白 prompt 开始。先选一个真实场景，再反推需要哪些频道、Agent 和工具。

常见起点包括：

- 研发协作：需求频道、开发 Agent、Review Agent；
- 客户支持：工单频道、FAQ Agent、升级处理 Agent；
- 研究分析：信息源频道、Research Agent、Report Agent；
- 内容生产：选题频道、Script Agent、Editor Agent。

如果还不确定，可以先看 [团队落地指南](/zh/docs/team-playbook.html)，从频道拆分、Agent 数量和上下文迁移开始设计。

## 多个 Agent 会不会乱？

会。如果只是把几个 Agent 拉进同一个频道，肯定会乱。

多 Agent 协作要先定规则：

- 谁负责拆任务；
- 谁负责执行；
- 谁负责 review；
- 什么时候可以主动发言；
- 什么动作必须等人确认；
- 交付物放在哪里。

建议先从一个驻场 Agent 开始，跑通后再增加执行、检查或专项 Agent。更细的判断可以看 [频道与协作](/zh/docs/channels.html)。

## Agent 访问数据安全吗？

默认边界应该很简单：Agent 只能看到它被邀请进入的频道和 DM。

如果 Agent 要访问企业系统，还需要单独授权。危险动作，例如发邮件、发布内容、删除数据、部署上线，应该生成 Action Card（操作确认卡片，Agent 生成后需要人点击批准才执行）或等待人工确认。

安全不是一句“有权限控制”，而是要做到：能授权、能撤销、能审计。

## 为什么 Agent 有时要等一两分钟？慢在哪？

Agent 是常驻会话，不是每次都新开一个空白对话。它可能同时在多个频道、多个任务里工作；当前一条命令、工具调用或长任务还没结束时，后续消息会排队。

想让它更快，关键是把分工收窄：

- 按业务或模块拆频道，不要让一个 Agent 横跨太多主题；
- 一个 Agent 优先专注 1–2 个模块；
- 会话跑久、上下文变长后，在空闲时重置 session。

如果 Agent 长时间没有活动，可以先看活动页和任务状态，再决定是否重置。

## 模型调用走什么渠道？数据安不安全？

Syfo 的模型调用会走 OpenAI、Anthropic 等官方渠道，或经过大厂正规渠道。中间用于负载、容错和计费的 token 网关由 Syfo 自建，不会经过不明第三方 token 代理商。

需要注意的是：只要调用外部大模型，请求内容本身就会发送给对应模型供应商。企业应按所选模型供应商的企业协议、组织权限和数据分级来决定哪些内容可以交给 Agent 处理。

Syfo 自身要解决的是：Agent 在组织内能看到什么、能访问什么系统、什么动作必须确认，以及这些过程能不能被审计。

## Agent 遇到问题为什么总停下来等我确认？

Agent 本身可以自主拉日志、看错误、尝试修复。它总停下来等你，通常不是能力问题，而是工作边界没有约定清楚，或者当前会话太长、太忙。

建议把规则写进 Agent 的长期记忆：

- 低风险操作，例如查看日志、重跑测试、修复明显报错，可以自主推进；
- 高风险操作，例如改生产、删数据、发布、权限变更、对外承诺，必须二次确认；
- 确认时要说清变更范围、影响面和回滚方式。

如果它仍然频繁停住，就把频道和任务范围再收窄，让它少处理无关上下文。

## Agent 一个小改动就建分支、反复通读整个仓库，正常吗？

这通常是工作规范还没调好，不是必须这样用。

你可以明确告诉 Agent：

- 小文案、小配置、单文件修复，可以直接在当前分支改；
- 中等以上改动，或者多人并行时，用 feature branch；
- 多个 Agent 同时改同一仓库时，用 git worktree；
- 不要每次都全仓扫描，先按任务定位相关文件，必要时再扩大范围。

把这些偏好写进 Agent 的长期记忆后，行为会稳定很多。

## 定时任务已经指派给某个 Agent，为什么全频道 Agent 都收到通知？

正常情况下，定时任务应该指向具体 Agent，并放在对应话题或任务上下文里。精准投递只通知目标 Agent；频道级消息才会广播给频道里的 Agent。

如果你想避免打扰其他 Agent：

- 创建提醒或定时任务时，明确指定执行 Agent；
- 把后续讨论放在同一个任务或话题里；
- 不要用普通频道消息反复补充执行细节。

如果确认已经指定了 Agent，仍然触发全频道广播，可以保留提醒 ID、频道、时间和收到通知的 Agent 列表，交给团队排查。

## 高风险操作怎么避免 Agent 乱来？

高风险操作不要靠“相信 Agent 会懂”来控制，要提前写清二次确认规则。

例如改生产、删数据、发版、权限变更、对外承诺这类高影响操作，可以约定：

- **什么时候确认**：不可逆、影响生产、影响客户或影响权限时；
- **谁确认**：模块负责人、值班负责人或指定 reviewer；
- **确认什么**：变更范围、影响面、验证方式、回滚方式；
- **保留什么**：diff、日志、命令记录和最终交付物。

信任建立后，常规低风险动作可以放开；高风险动作仍保留确认。

## 开发过程像黑盒，只能看结果，怎么知道改了什么、怎么回滚？

现阶段建议用“双屏”工作：

- 一屏看 Syfo 对话和 Agent 活动页，了解它正在调用什么工具、执行什么命令；
- 一屏打开 VS Code 或终端，看 git diff、测试结果和提交记录。

版本和回滚交给 git 承接。Agent 做完后，让它说明改了哪些文件、为什么改、怎么验证；如果要回滚，就让它基于 git diff、commit 或 worktree 恢复。
"""
    return markdown_to_html(md)


def build_best_practices() -> str:
    md = read_md("guide", "best-practices.md")
    md = md.replace(
        "这一页汇集把 Syfo 用顺的实战经验。它不重复讲频道怎么拆、一个频道放几个 Agent（那些看[团队上手指南](/guide/team-onboarding)和[频道构成与多 Agent 协作](/features/squad)），而是讲日常协作里最容易踩、也最能提效的几个习惯。",
        "下面这些实践适合已经开始试用 Syfo、准备把 Agent 放进团队日常工作的人。频道拆分和 Agent 数量可以先看[团队上手指南](/guide/team-onboarding)和[频道构成与多 Agent 协作](/features/squad)，这里重点讲日常协作里最容易踩、也最能提效的几个习惯。",
    )
    md = md.replace(
        "**高风险二次确认**（改生产、删数据、发布、对外承诺、权限变更，或 Android BSP / 驱动这类不可逆改动）：",
        "**高风险二次确认**（改生产、删数据、发布、对外承诺、权限变更这类不可逆或高影响操作）：",
    )
    return markdown_to_html(md)


def sidebar_html(active: str) -> str:
    groups = []
    for group_title, items in SIDEBAR_GROUPS:
        links = "".join(
            f'<li><a class="{"active" if href == active else ""}" href="{href}">{html.escape(label)}</a></li>'
            for label, href in items
        )
        groups.append(
            f'<div class="sidebar-group"><h3>{html.escape(group_title)}</h3><ul>{links}</ul></div>'
        )
    return (
        '<nav class="docs-sidebar" id="docsSidebar" aria-label="文档目录">'
        + "".join(groups)
        + "</nav>"
    )


def page_html(filename: str, body: str) -> str:
    body = body.replace("） 里", "）里")
    title, desc, eyebrow, h1 = PAGE_META[filename]
    active = "/zh/docs/" if filename == "index.html" else f"/zh/docs/{filename}"
    sidebar = sidebar_html(active)
    content_class = "doc-home" if filename == "index.html" else "article"
    lang_links = []
    for lg in LANGS:
        href = f"/{lg}/docs/" if filename == "index.html" else f"/{lg}/docs/{filename}"
        cur = ' class="cur"' if lg == "zh" else ""
        lang_links.append(f'<a href="{href}"{cur}>{LANG_NAMES[lg]}</a>')
    lang_menu = f"""<details class="langmenu"><summary><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg><span>中</span></summary><div class="langpop">{"".join(lang_links)}</div></details>"""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} - Syfo</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="icon" href="/assets/logo-mark.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="/assets/tokens.css" rel="stylesheet">
<style>
:root{{--maxw:1120px;--content:820px}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg-paper);color:var(--fg-1);font-family:var(--font-sans);line-height:1.72;overflow-x:hidden}}
body::before{{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.025'/%3E%3C/svg%3E")}}
a{{color:inherit;text-decoration:none}}
.wrap{{max-width:var(--maxw);margin:0 auto;padding:0 24px}}
.nav{{position:sticky;top:0;z-index:40;backdrop-filter:saturate(1.4) blur(8px);background:color-mix(in oklab,var(--bg-paper) 82%,transparent);border-bottom:1px solid var(--border-1)}}
.nav .row{{display:flex;align-items:center;gap:28px;height:60px}}
.brand{{display:flex;align-items:center;gap:10px}}
.brand svg{{width:32px;height:32px;flex:0 0 auto}}
.brand .wm{{font-family:var(--font-serif);font-weight:600;font-size:21px;letter-spacing:0}}
.nav .links{{display:flex;gap:24px;margin-left:8px;align-items:center}}
.nav .links a{{font-size:14px;color:var(--fg-2);transition:color var(--dur-fast) var(--ease-out)}}
.nav .links a:hover,.nav .links a.on{{color:var(--fg-1)}}
.nav .right{{margin-left:auto;display:flex;align-items:center;gap:14px}}
.nav-dd{{position:relative}}
.nav-dd>a{{display:inline-flex;align-items:center;gap:4px}}
.nav-dd .car{{font-size:10px;color:var(--fg-3)}}
.dd-menu{{position:absolute;top:calc(100% + 12px);left:-18px;min-width:190px;background:var(--bg-surface);border:1px solid var(--border-2);border-radius:var(--radius-md);box-shadow:var(--shadow-3);padding:8px;display:none;flex-direction:column;gap:2px}}
.dd-menu a{{font-size:14px!important;color:var(--fg-1)!important;padding:9px 10px;border-radius:var(--radius-sm)}}
.dd-menu a:hover{{background:var(--bg-sunken)}}
.dd-menu .dd-all{{border-top:1px solid var(--border-1);margin-top:4px;padding-top:10px;color:var(--accent)!important}}
.nav-dd:hover .dd-menu,.nav-dd:focus-within .dd-menu{{display:flex}}
.langmenu{{position:relative}}
.langmenu>summary{{list-style:none;display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-family:var(--font-mono);font-size:13px;color:var(--fg-2);border:1px solid var(--border-2);border-radius:var(--radius-md);padding:6px 10px;line-height:1;transition:all var(--dur-fast) var(--ease-out)}}
.langmenu>summary::-webkit-details-marker{{display:none}}
.langmenu>summary:hover,.langmenu[open]>summary{{color:var(--fg-1);border-color:var(--fg-3);background:var(--bg-surface)}}
.langpop{{position:absolute;top:calc(100% + 8px);right:0;min-width:150px;z-index:60;background:var(--bg-surface);border:1px solid var(--border-2);border-radius:var(--radius-md);box-shadow:var(--shadow-3);padding:6px;display:flex;flex-direction:column;gap:2px}}
.langpop a{{font-size:14px;color:var(--fg-1);padding:9px 12px;border-radius:var(--radius-sm)}}
.langpop a:hover{{background:var(--bg-sunken)}}
.langpop a.cur{{color:var(--accent);font-weight:600}}
.nav-lang{{padding:14px 0;border-bottom:1px solid var(--border-1)}}
.nav-lang .langmenu>summary{{width:100%;justify-content:center;padding:12px}}
.nav-lang .langpop{{position:static;box-shadow:none;margin-top:8px}}
.nav-toggle{{display:none;background:var(--bg-surface);border:1px solid var(--border-2);border-radius:var(--radius-md);width:42px;height:42px;align-items:center;justify-content:center;cursor:pointer;padding:0;color:var(--fg-1)}}
.nav-toggle:hover{{background:var(--bg-sunken);border-color:var(--fg-3)}}
.nav-toggle svg{{display:block}}
.nav-toggle .ic-close{{display:none}}
.nav.open .nav-toggle .ic-open{{display:none}}
.nav.open .nav-toggle .ic-close{{display:block}}
.nav-menu{{display:none;flex-direction:column;padding:6px 0 16px}}
.nav-menu a:not(.btn){{font-size:16px;color:var(--fg-1);padding:14px 2px;border-bottom:1px solid var(--border-1)}}
.nav-menu .dd-subs{{display:flex;flex-direction:column;padding-left:14px;border-bottom:1px solid var(--border-1)}}
.nav-menu .dd-subs a{{font-size:14px;color:var(--fg-2);padding:10px 2px;border:0}}
.nav-menu .btn{{margin-top:16px;justify-content:center}}
.btn{{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;border-radius:var(--radius-md);padding:10px 18px;cursor:pointer;transition:all var(--dur-fast) var(--ease-out);border:1px solid transparent;white-space:nowrap;line-height:1.1}}
.btn-primary{{background:var(--accent);color:var(--fg-inverse);box-shadow:var(--shadow-1)}}
.btn-primary:hover{{background:var(--accent-hover)}}
.btn-ghost{{background:var(--bg-surface);color:var(--fg-1);border-color:var(--border-2)}}
.btn-ghost:hover{{background:var(--bg-sunken);border-color:var(--fg-3)}}
.btn .arr{{transition:transform var(--dur-fast) var(--ease-out)}}
.btn:hover .arr{{transform:translateX(2px)}}
.eyebrow{{font-family:var(--font-mono);font-size:11px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:inline-flex;align-items:center;gap:8px;margin-bottom:0}}
.eyebrow::before{{content:"";width:18px;height:1px;background:var(--accent);display:inline-block}}
h1,h2,h3,h4{{font-family:var(--font-serif);line-height:1.18;letter-spacing:0;margin:0;color:var(--fg-1)}}
h1{{font-weight:600;font-size:46px;line-height:1.14;letter-spacing:0;margin:18px 0 0;max-width:760px}}
.lead{{font-size:17px;line-height:1.7;color:var(--fg-2);max-width:48ch;margin:18px 0 0}}
.docs-layout{{display:grid;grid-template-columns:248px minmax(0,1fr);gap:46px;max-width:var(--maxw);margin:0 auto;padding:42px 24px 88px;position:relative;z-index:1}}
.docs-sidebar-toggle{{display:none;align-items:center;justify-content:center;gap:8px;width:100%;border:1px solid var(--border-2);border-radius:var(--radius-md);background:var(--bg-surface);color:var(--fg-1);font-family:var(--font-mono);font-size:13px;padding:11px 12px;cursor:pointer}}
.docs-sidebar{{position:sticky;top:84px;align-self:start;max-height:calc(100vh - 112px);overflow:auto;padding:4px 18px 28px 0;border-right:1px solid var(--border-1)}}
.sidebar-group{{margin:0 0 26px;padding-top:2px}}
.sidebar-group + .sidebar-group{{border-top:1px solid color-mix(in oklab,var(--border-1) 70%,transparent);padding-top:18px}}
.sidebar-group h3{{font-family:var(--font-mono);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--fg-3);margin:0 0 8px;padding:0 12px;line-height:1.2;cursor:pointer;user-select:none}}
.sidebar-group h3::after{{content:"▾";float:right;font-size:10px;color:var(--fg-3);transition:transform var(--dur-fast) var(--ease-out)}}
.sidebar-group.collapsed h3::after{{content:"▸"}}
.sidebar-group ul{{list-style:none;margin:0;padding:0}}
.sidebar-group li{{margin:2px 0}}
.sidebar-group a{{position:relative;display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:14px;line-height:1.45;color:var(--fg-2);padding:8px 12px 8px 16px;border-radius:var(--radius-sm);transition:color var(--dur-fast) var(--ease-out),background var(--dur-fast) var(--ease-out),padding var(--dur-fast) var(--ease-out)}}
.sidebar-group a::before{{content:"";position:absolute;left:6px;top:9px;bottom:9px;width:2px;border-radius:999px;background:transparent}}
.sidebar-group a::after{{content:"›";font-family:var(--font-mono);font-size:13px;color:transparent;transition:color var(--dur-fast) var(--ease-out),transform var(--dur-fast) var(--ease-out)}}
.sidebar-group a:hover{{color:var(--fg-1);background:var(--bg-sunken);padding-left:18px}}
.sidebar-group a:hover::after{{color:var(--fg-3);transform:translateX(2px)}}
.sidebar-group a.active{{color:var(--accent);background:color-mix(in oklab,var(--accent-1) 10%,transparent);font-weight:600}}
.sidebar-group a.active::before{{background:var(--accent)}}
.docs-content{{min-width:0;max-width:var(--content)}}
.doc-page-head{{padding-bottom:32px;margin-bottom:10px;border-bottom:1px solid var(--border-1)}}
.doc-section{{padding:56px 0;position:relative;z-index:1}}
.doc-section.compact{{padding-top:18px}}
.section-head{{max-width:760px;margin-bottom:22px}}
.section-head h2{{font-weight:600;font-size:42px;letter-spacing:0;margin-bottom:12px}}
.section-head p{{color:var(--fg-2);font-size:17px;margin:0}}
.doc-home .wrap{{max-width:none;padding:0}}
.doc-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}
.doc-card{{display:flex;min-height:190px;flex-direction:column;border:1px solid var(--border-1);background:var(--bg-surface);border-radius:var(--radius-md);padding:20px;transition:transform var(--dur-fast) var(--ease-out),box-shadow var(--dur-fast) var(--ease-out),border-color var(--dur-fast) var(--ease-out)}}
.doc-card:hover{{transform:translateY(-2px);border-color:var(--border-2);box-shadow:var(--shadow-1)}}
.doc-card span,.doc-card div{{font-family:var(--font-mono);font-size:12px;color:var(--fg-3)}}
.doc-card h3{{font-size:22px;margin:18px 0 9px}}
.doc-card p{{margin:0;color:var(--fg-2);font-size:14px;line-height:1.65;flex:1}}
.cta-row{{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}}
.quick-list{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}
.quick-list a{{border-top:1px solid var(--border-1);padding:16px 0;transition:color var(--dur-fast) var(--ease-out)}}
.quick-list a:hover b{{color:var(--accent)}}
.quick-list b{{display:block;margin-bottom:6px}}
.quick-list span{{display:block;color:var(--fg-2);font-size:14px}}
.article h2{{font-size:34px;margin:54px 0 14px;padding-top:8px}}
.article h3{{font-size:24px;margin:34px 0 10px}}
.article h4{{font-size:19px;margin:24px 0 8px}}
.article p,.article li{{font-size:16px;color:var(--fg-2)}}
.article a{{text-decoration:underline;text-underline-offset:3px}}
.article ul,.article ol{{padding-left:1.4em;margin:10px 0 18px}}
.article li{{margin:7px 0}}
.article code{{font-family:var(--font-mono);font-size:.92em;background:color-mix(in oklab,var(--fg-1) 7%,transparent);border:1px solid var(--border-1);border-radius:5px;padding:1px 5px;color:var(--fg-1)}}
pre{{background:#171411;color:#fff;border-radius:8px;padding:16px;overflow-x:auto;border:1px solid #2b251f;white-space:pre-wrap;word-break:break-word}}
.article pre code{{background:transparent;border:0;color:inherit;padding:0}}
blockquote,.note{{border-left:3px solid var(--accent-1);background:color-mix(in oklab,var(--accent-1) 8%,transparent);padding:14px 18px;margin:18px 0;border-radius:0 8px 8px 0;color:var(--fg-2)}}
figure{{margin:24px 0;border:1px solid var(--border-1);border-radius:var(--radius-md);overflow:hidden;background:var(--bg-surface);box-shadow:var(--shadow-1)}}
figure img{{display:block;width:100%;height:auto}}
figcaption{{font-size:13px;color:var(--fg-3);padding:10px 12px;border-top:1px solid var(--border-1)}}
.table-wrap{{overflow-x:auto;margin:18px 0;border:1px solid var(--border-1);border-radius:8px;background:#fff}}
table{{width:100%;border-collapse:collapse;font-size:14px;min-width:640px}}
th,td{{padding:11px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border-1)}}
th{{font-weight:700;color:var(--fg-1);background:color-mix(in oklab,var(--bg-paper) 70%,white)}}
tr:last-child td{{border-bottom:0}}
footer{{border-top:1px solid var(--border-1);background:var(--bg-sunken);position:relative;z-index:1}}
footer .row{{display:flex;align-items:center;gap:18px;padding:30px 0;flex-wrap:wrap}}
footer .meta{{font-size:13px;color:var(--fg-3)}}
footer .links{{margin-left:auto;display:flex;gap:20px}}
footer .links a{{font-size:13px;color:var(--fg-2)}}
footer .links a:hover{{color:var(--fg-1)}}
@media (max-width:900px){{.quick-list{{grid-template-columns:1fr}}.nav .links,.nav .right .langmenu,.nav .right .navcta{{display:none}}.nav .row{{height:62px}}.nav-toggle{{display:flex;margin-left:auto}}.nav.open .nav-menu{{display:flex}}}}
@media (max-width:768px){{.docs-layout{{display:block;padding-top:24px}}.docs-sidebar-toggle{{display:flex;margin-bottom:14px}}.docs-sidebar{{display:none;position:static;max-height:none;border:1px solid var(--border-1);border-radius:var(--radius-md);padding:12px;background:var(--bg-surface);margin-bottom:24px}}.docs-layout.sidebar-open .docs-sidebar{{display:block}}.doc-page-head{{padding-bottom:24px}}.doc-grid{{grid-template-columns:1fr}}}}
@media (max-width:560px){{.wrap,.docs-layout{{padding-left:18px;padding-right:18px}}h1{{font-size:38px}}.section-head h2{{font-size:30px}}.article h2{{font-size:28px}}footer .links{{margin-left:0}}}}
</style>
</head>
<body>
<header class="nav"><div class="wrap"><div class="row">
 <a class="brand" href="/zh/">{LOGO_MARK}<span class="wm">Syfo</span></a>
 <nav class="links"><a href="/zh/#product">产品</a><a href="/zh/#scenes">能做什么</a><div class="nav-dd"><a href="/zh/cases.html">案例 <span class="car">▾</span></a><div class="dd-menu"><a href="/zh/cases-consumer.html">消费 / 电商</a><a href="/zh/cases-finance.html">金融 / 投资</a><a href="/zh/cases-tech.html">科技 / 研发</a><a href="/zh/cases-more.html">更多案例</a><a class="dd-all" href="/zh/cases.html">全部案例</a></div></div><a href="/zh/how.html">怎么用</a><a class="on" href="/zh/docs/">文档</a></nav>
 <div class="right">{lang_menu}<a class="btn btn-primary navcta" href="https://app.syfo.ai">进入 Syfo <span class="arr">→</span></a><button class="nav-toggle" aria-label="菜单" aria-expanded="false" aria-controls="navMenu" onclick="var n=this.closest('.nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)"><svg class="ic-open" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M3 6h14M3 10h14M3 14h14"/></svg><svg class="ic-close" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M5 5l10 10M15 5L5 15"/></svg></button></div>
</div>
<div class="nav-menu" id="navMenu"><a href="/zh/#product">产品</a><a href="/zh/#scenes">能做什么</a><a href="/zh/cases.html">案例</a><div class="dd-subs"><a href="/zh/cases-consumer.html">消费 / 电商</a><a href="/zh/cases-finance.html">金融 / 投资</a><a href="/zh/cases-tech.html">科技 / 研发</a><a href="/zh/cases-more.html">更多案例</a></div><a href="/zh/how.html">怎么用</a><a href="/zh/docs/">文档</a><div class="nav-lang">{lang_menu}</div><a class="btn btn-primary" href="https://app.syfo.ai">进入 Syfo <span class="arr">→</span></a></div>
</div></header>
<main class="docs-layout">
 <button class="docs-sidebar-toggle" type="button" aria-controls="docsSidebar" aria-expanded="false" onclick="var m=this.closest('.docs-layout');var o=m.classList.toggle('sidebar-open');this.setAttribute('aria-expanded',o)">文档目录</button>
 {sidebar}
 <section class="docs-content">
  <header class="doc-page-head">
   <span class="eyebrow">{html.escape(eyebrow)}</span>
   <h1>{html.escape(h1)}</h1>
   <p class="lead">{html.escape(desc)}</p>
  </header>
  <div class="{content_class}">{body}</div>
 </section>
</main>
<footer><div class="wrap"><div class="row">
 <a class="brand" href="/zh/">{LOGO_MARK}<span class="wm">Syfo</span></a>
 <span class="meta">人和一群 Agent 一起干活的地方。</span>
 <div class="links"><a href="https://app.syfo.ai">app.syfo.ai</a><a href="/zh/cases.html">案例</a><a href="/zh/how.html">怎么用</a><a href="/zh/docs/">文档</a></div>
</div></div></footer>
<script>
document.querySelectorAll('.sidebar-group').forEach(function(g) {{
  var h = g.querySelector('h3');
  var ul = g.querySelector('ul');
  if (!h || !ul) return;
  var hasActive = g.querySelector('a.active');
  if (!hasActive) {{
    ul.style.display = 'none';
    g.classList.add('collapsed');
  }}
  h.addEventListener('click', function() {{
    var closed = ul.style.display === 'none';
    ul.style.display = closed ? 'block' : 'none';
    g.classList.toggle('collapsed', !closed);
  }});
}});
</script>
</body>
</html>
"""


def write_page(filename: str, body: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / filename).write_text(page_html(filename, body), encoding="utf-8")


def load_translation_cache() -> dict[str, dict[str, str]]:
    if TRANSLATION_CACHE.exists():
        return json.loads(TRANSLATION_CACHE.read_text(encoding="utf-8"))
    return {}


def save_translation_cache(cache: dict[str, dict[str, str]]) -> None:
    TRANSLATION_CACHE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def should_translate_text(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if not re.search(r"[\u4e00-\u9fff]", stripped):
        return False
    return True


def is_translatable_node(node: NavigableString) -> bool:
    parent = node.parent
    while parent is not None and getattr(parent, "name", None):
        if parent.name in {"script", "style", "svg", "path", "kbd"}:
            return False
        parent = parent.parent
    return should_translate_text(str(node))


def collect_translatable_texts(html_text: str) -> set[str]:
    soup = BeautifulSoup(html_text, "html.parser")
    texts: set[str] = set()
    for node in soup.find_all(string=True):
        if is_translatable_node(node):
            texts.add(str(node).strip())
    for tag in soup.find_all(True):
        for attr in ("content", "alt", "title", "aria-label"):
            value = tag.get(attr)
            if isinstance(value, str) and should_translate_text(value):
                texts.add(value.strip())
    return texts


def google_translate_batch(texts: list[str], target: str) -> dict[str, str]:
    if not texts:
        return {}
    q = TRANSLATION_SPLIT.join(texts)
    resp = requests.post(
        "https://translate.googleapis.com/translate_a/single",
        data={"client": "gtx", "sl": "zh-CN", "tl": target, "dt": "t", "q": q},
        timeout=30,
    )
    if not resp.ok and len(texts) > 1:
        result: dict[str, str] = {}
        for text in texts:
            result.update(google_translate_batch([text], target))
        return result
    if not resp.ok:
        return {texts[0]: texts[0]}
    resp.raise_for_status()
    data = resp.json()
    translated = "".join(part[0] for part in data[0] if part and part[0])
    parts = translated.split(TRANSLATION_SPLIT.strip())
    parts = [part.strip() for part in parts]
    if len(parts) != len(texts):
        # Fall back to individual calls if the separator was changed by translation.
        result: dict[str, str] = {}
        for text in texts:
            result.update(google_translate_batch([text], target))
        return result
    return dict(zip(texts, parts))


def ensure_translations(texts: set[str], lang: str, cache: dict[str, dict[str, str]]) -> None:
    bucket = cache.setdefault(lang, {})
    missing = [text for text in sorted(texts) if text not in bucket]
    if not missing:
        return

    batch: list[str] = []
    batch_len = 0
    target = TRANSLATE_TARGET[lang]
    for text in missing:
        added_len = len(text) + len(TRANSLATION_SPLIT)
        if batch and batch_len + added_len > 1600:
            bucket.update(google_translate_batch(batch, target))
            batch = []
            batch_len = 0
        batch.append(text)
        batch_len += added_len
    if batch:
        bucket.update(google_translate_batch(batch, target))


def translate_preserve_space(text: str, lang: str, cache: dict[str, dict[str, str]]) -> str:
    if not should_translate_text(text):
        return text
    leading = re.match(r"^\s*", text).group(0)
    trailing = re.search(r"\s*$", text).group(0)
    core = text.strip()
    manual = MANUAL_TEXT_TRANSLATIONS.get(lang, {})
    if core in manual:
        return leading + normalize_translated_text(manual[core], lang) + trailing
    if core in MANUAL_CODE_TRANSLATIONS:
        return leading + normalize_translated_text(MANUAL_CODE_TRANSLATIONS[core], lang) + trailing
    return leading + normalize_translated_text(cache.get(lang, {}).get(core, core), lang) + trailing


def localized_href(href: str, lang: str) -> str:
    if href.startswith("/zh/docs/images/"):
        return f"/{lang}/docs/images/" + href.split("/zh/docs/images/", 1)[1]
    if href == "/zh/docs/":
        return f"/{lang}/docs/"
    if href.startswith("/zh/docs/"):
        return f"/{lang}/docs/" + href.split("/zh/docs/", 1)[1]
    if href == "/zh/":
        return f"/{lang}/"
    if href.startswith("/zh/"):
        return f"/{lang}/" + href.split("/zh/", 1)[1]
    return href


def docs_lang_menu(soup: BeautifulSoup, lang: str, filename: str):
    svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18"></path><path d="M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"></path></svg>'
    links = []
    for lg in LANGS:
        path = f"/{lg}/docs/" if filename == "index.html" else f"/{lg}/docs/{filename}"
        cur = ' class="cur"' if lg == lang else ""
        links.append(f'<a href="{path}"{cur}>{LANG_NAMES[lg]}</a>')
    return BeautifulSoup(
        f'<details class="langmenu"><summary>{svg}<span>{LANG_SHORT[lang]}</span></summary><div class="langpop">{"".join(links)}</div></details>',
        "html.parser",
    ).details


def localize_doc_html(filename: str, zh_html: str, lang: str, cache: dict[str, dict[str, str]]) -> str:
    soup = BeautifulSoup(zh_html, "html.parser")
    if soup.html:
        soup.html["lang"] = HTML_LANG[lang]

    for tag in soup.find_all(True):
        for attr in ("href", "src"):
            value = tag.get(attr)
            if isinstance(value, str):
                tag[attr] = localized_href(value, lang)
        for attr in ("content", "alt", "title", "aria-label"):
            value = tag.get(attr)
            if isinstance(value, str):
                tag[attr] = translate_preserve_space(value, lang, cache)

    for node in list(soup.find_all(string=True)):
        if is_translatable_node(node):
            node.replace_with(translate_preserve_space(str(node), lang, cache))

    for menu in list(soup.select("details.langmenu")):
        menu.replace_with(docs_lang_menu(soup, lang, filename))

    rendered = str(soup)
    rendered = rendered.replace("syfo_landing_locale=zh", f"syfo_landing_locale={lang}")
    if lang == "en":
        for bad, good in EN_COPY_REPLACEMENTS.items():
            rendered = rendered.replace(bad, good)
    rendered = normalize_translated_text(rendered, lang)
    if not rendered.lower().startswith("<!doctype"):
        rendered = "<!doctype html>\n" + rendered
    return rendered


def write_localized_docs(pages: dict[str, str]) -> None:
    zh_html_by_file = {filename: (OUT / filename).read_text(encoding="utf-8") for filename in pages}
    all_texts = set()
    for zh_html in zh_html_by_file.values():
        all_texts.update(collect_translatable_texts(zh_html))

    cache = load_translation_cache()
    for lang in LOCALIZED_LANGS:
        ensure_translations(all_texts, lang, cache)
    save_translation_cache(cache)

    for lang in LOCALIZED_LANGS:
        out = ROOT / "site" / lang / "docs"
        img_out = out / "images"
        out.mkdir(parents=True, exist_ok=True)
        if IMG_OUT.exists():
            shutil.copytree(IMG_OUT, img_out, dirs_exist_ok=True)
        for stale_name in ("customer-questions.html", "templates.html", "agent-faq.html"):
            stale = out / stale_name
            if stale.exists():
                stale.unlink()
        for filename, zh_html in zh_html_by_file.items():
            (out / filename).write_text(localize_doc_html(filename, zh_html, lang, cache), encoding="utf-8")


def main() -> None:
    copy_assets()
    pages = {
        "index.html": build_index(),
        "what-is-syfo.html": build_what_is_syfo(),
        "getting-started.html": build_getting_started(),
        "first-agent.html": build_first_agent(),
        "organization.html": build_organization(),
        "channels.html": build_channels(),
        "agents.html": build_concept_page("agents.md"),
        "tasks.html": build_concept_page("tasks.md"),
        "messages.html": build_concept_page("messages.md"),
        "files-and-deliverables.html": build_concept_page("files-and-deliverables.md"),
        "skills.html": build_skills(),
        "computers.html": build_computers(),
        "reminders.html": build_reminders(),
        "message-delivery.html": build_message_delivery(),
        "integrations.html": build_integrations(),
        "team-playbook.html": build_team_playbook(),
        "best-practices.html": build_best_practices(),
        "faq.html": build_faq(),
        "security.html": build_security(),
    }
    for stale_name in ("customer-questions.html", "templates.html", "agent-faq.html"):
        stale = OUT / stale_name
        if stale.exists():
            stale.unlink()
    for filename, body in pages.items():
        write_page(filename, body)
    write_localized_docs(pages)


if __name__ == "__main__":
    main()
