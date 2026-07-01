#!/usr/bin/env python3
# Syfo 官网 (双语 中文 + English) — 基于 syfo-design 设计系统，面向各行各业的业务团队。
# 产出 (root = zh): index.html / cases.html / how.html / case-*.html
# 产出 (en/  = en): en/index.html / en/cases.html / en/how.html / en/case-*.html
# 设计 token 来自 /assets/tokens.css。内容已抽象，不含具体客户/持仓/敏感数字。
#
# 双语结构 (maintainable):
#   - LANGS = ["zh","en"]; 一次 `python3 build_site.py` 跑两种语言。
#   - 所有面向用户的中文字符串都做成 per-language 查表：
#       * T[lang][key]          —— 页面内联文案 (hero / sec-head / 标签 / footer 等)
#       * CASES[lang] / SCENES[lang] / STEPS[lang] / RELAY[lang] / HOW_STEPS[lang]
#       * DETAILS[lang][slug]   —— 案例内页数据
#   - 页面构造函数都接收 lang 参数。
#   - 内部链接一律 root-absolute：zh -> "/..."、en -> "/en/..."  (见 url())。
#   - 资源一律 root-absolute："/assets/..."。
#   - 语言切换器在 nav() 里，指向另一语言的同一页面 (toggle 由 page builder 传入)。
import os
import json

HERE = os.path.dirname(__file__)
EN_DIR = os.path.join(HERE, "en")
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
         "&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700"
         "&family=Noto+Serif+SC:wght@400;500;600;700"
         "&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@400;500;600;700"
         "&family=Noto+Serif:wght@400;500;600;700"
         "&display=swap")
APP = "https://app.syfo.ai"
# 产品目前只有 中/英。非中文页的「进入 Syfo」CTA 指向英文入口。
# app.syfo.ai 目前只按浏览器语言切换（?lang= 等参数暂被忽略、/en 404）；此 URL 是前向兼容占位，
# 一旦 app 支持该覆盖参数即自动强制英文，今天无害（非中文浏览器本就 fallback 英文）。
APP_EN = "https://app.syfo.ai/?lang=en"
LOGO_MARK = open(os.path.join(HERE, "assets/logo-mark.svg")).read()

LANGS = ["zh", "en", "ja", "es", "vi"]
# root-absolute 前缀：zh 在站点根，其余在 /<lang>/ 子目录
PREFIX = {"zh": "/", "en": "/en/", "ja": "/ja/", "es": "/es/", "vi": "/vi/"}
# 输出目录：zh=站点根，其余=子目录
DIRS = {lg: (HERE if lg == "zh" else os.path.join(HERE, lg)) for lg in LANGS}
# 语言切换器展示名 / 短标签
LANG_NAMES = {"zh": "中文", "en": "English", "ja": "日本語", "es": "Español", "vi": "Tiếng Việt"}
LANG_SHORT = {"zh": "中", "en": "EN", "ja": "JA", "es": "ES", "vi": "VI"}


def app_url(lang):
    """进入产品的 CTA 目标：中文页→中文 app；其余语言→英文 app 入口。"""
    return APP if lang == "zh" else APP_EN


# 日语页面：优先 Noto Sans/Serif JP，避免日文汉字被 SC 字体渲染成中文字形。
JA_FONT_OVERRIDE = ("<style>:root{--font-sans:'Inter','Noto Sans JP','Noto Sans SC',system-ui,sans-serif;"
                    "--font-serif:'Noto Serif JP','Noto Serif SC',Georgia,serif;}</style>")
# 越南语页面：衬线用 Noto Serif(拉丁, 含越南语变音符)，避免 SC 字体缺越南语字形回退到 Georgia。
VI_FONT_OVERRIDE = ("<style>:root{--font-serif:'Noto Serif','Noto Serif SC',Georgia,serif;}</style>")
FONT_OVERRIDE = {"ja": JA_FONT_OVERRIDE, "vi": VI_FONT_OVERRIDE}


def url(lang, page):
    """内部链接 -> root-absolute clean URL (无 .html)。page 形如 'index.html'、'cases.html#x'、'' (=首页)。
    文件在磁盘上仍是 *.html；clean URL 由 edge try_files {path}.html 提供。"""
    p = PREFIX[lang]
    anchor = ""
    if "#" in page:
        page, frag = page.split("#", 1)
        anchor = "#" + frag
    if page.endswith(".html"):
        page = page[:-5]
    if page in ("", "index"):
        return p + anchor          # "/" 或 "/en/"
    return p + page + anchor       # "/cases"、"/en/case-fund" ...


# ── 案例数据 (已抽象, 不含具体内容) ────────────────────────────
# 每条: (行业标签, 标题, 描述, [标签...], slug)
CASES = {
 "zh": [
 ("金融投资 · 私募基金", "一个人带一支 Agent 团队，跑一只系统化私募",
  "一位 CIO 加一组各司其职的 Agent：财报审阅、期权情绪监控、每日盈亏归因、每日解读、风控择时、持仓退出监控。每天自动产出机构级日度研究，机械化止盈止损纪律，全部在一个频道里协同。",
  ["每日盈亏归因","风控择时","财报审阅","期权情绪"], "fund"),
 ("金融科技 · 组合管理", "一支 Agent 团队，自建并运营组合管理平台",
  "设计、合规、风控展示、前端、部署、上线验证分工协作。健康度卡、合规灯、调仓表、来源溯源带，统一设计系统与合规红线，契约校验防止数据漂移。",
  ["平台开发","合规风控","设计系统","上线验证"], "platform"),
 ("内容创作 · 漫画", "把剧本变成连载漫画的 Agent 流水线",
  "一个人定方向，Agent 团队负责分镜设计、角色一致性、AI 配图、并行出图、自动发布。多章连载，每章约 28 页，角色跨页保持一致。",
  ["分镜设计","AI 配图","角色一致","自动发布"], "comic"),
 ("移动产品 · vibe coding", "一个创始人加一支 Agent 团队，端到端做一款 App",
  "一款 AI 识别类消费 App 的产品、后端、基础设施全包：服务器迁移、网络打通、登录配置、照片处理、上传链路优化、依赖修复，问题随提随修。",
  ["全栈交付","基础设施","问题排障","上线运维"], "app"),
 ("零售 · 销售与客服", "让 Agent 把客户沟通变成可跟进的纪要与话术",
  "销售把客户会议录音交给 Agent 转写、提炼诉求、规划切入点与服务话术，逐步把一线销售与客服接入 Agent 协作。",
  ["会议转写","诉求提炼","客户跟进","销售赋能"], "sales"),
 ("新媒体 · 内容运营", "一支 Agent 团队，既写内容也建平台",
  "总编 Agent 统筹两位写手 Agent，把数百份课程与会议纪要批量改写成公众号文章，去重、合并系列、敏感脱敏、分类归档；另一个 Agent 自建内容管理平台，集中管理与发布。",
  ["批量写作","去重合并","敏感脱敏","内容平台"], "content"),
 ],
 "en": [
 ("Finance · Private fund", "One person runs a systematic fund with a team of Agents",
  "A CIO plus a crew of specialized Agents: earnings review, options sentiment, daily P&L attribution, a daily read, risk timing, and exit monitoring. Every trading day they produce institutional-grade research and enforce mechanical stop-loss and take-profit discipline, all in one channel.",
  ["P&L attribution","Risk timing","Earnings review","Options sentiment"], "fund"),
 ("Fintech · Portfolio management", "A team of Agents builds and runs a portfolio platform",
  "Design, compliance, risk display, frontend, deployment, and release verification split the work. Health cards, compliance lights, rebalancing tables, source-provenance bands, one design system and clear compliance lines, with contract checks that stop data drift.",
  ["Platform build","Compliance","Design system","Release checks"], "platform"),
 ("Content · Comics", "An Agent pipeline that turns a script into a serialized comic",
  "One person sets the direction, the Agent team handles paneling, character consistency, AI artwork, parallel rendering, and automated publishing. Multi-chapter runs of about 28 pages each, with characters that stay consistent across spreads.",
  ["Paneling","AI artwork","Consistency","Auto-publish"], "comic"),
 ("Mobile · Vibe coding", "A founder and an Agent team ship an app end to end",
  "Product, backend, and infrastructure for a consumer AI-recognition app: server migration, networking, login setup, photo processing, upload-path tuning, and dependency fixes, all triaged and resolved as issues come in.",
  ["Full-stack delivery","Infrastructure","Troubleshooting","Operations"], "app"),
 ("Retail · Sales & support", "Agents turn customer conversations into follow-ups and playbooks",
  "Sales hands meeting recordings to Agents that transcribe them, distill what the customer needs, and plan talking points and service scripts, gradually bringing frontline sales and support into Agent collaboration.",
  ["Transcription","Needs analysis","Follow-ups","Sales enablement"], "sales"),
 ("Media · Content operations", "An Agent team writes the content and builds the platform",
  "An editor-in-chief Agent directs two writer Agents that rewrite hundreds of course and meeting notes into published articles, deduplicating, merging series, redacting sensitive figures, and filing everything. A separate Agent builds a content-management platform to manage and publish it all.",
  ["Bulk writing","Dedup & merge","Redaction","Content platform"], "content"),
 ],
}

# ── 场景能力 (能为你做什么) ────────────────────────────────────
SCENES = {
 "zh": [
 ("research","投研与分析","把数据、财报、舆情交给一组 Agent 持续盯，每天产出可用的研究与提示。"),
 ("ops","运营与增长","大促文案、商品详情、活动跟进，说一句需求，Agent 团队批量做完回报。"),
 ("service","销售与客服","会议录音转纪要、提炼客户诉求、整理跟进话术，把沟通沉淀成行动。"),
 ("content","内容生产","从选题到成稿到发布，写手 Agent 并行产出，统一过审与归档。"),
 ("build","产品与平台","让 Agent 团队把一个想法做成能上线的产品，从设计到部署。"),
 ("coord","跨团队协调","任务、背景、产物都在频道里，人和 Agent 之间干净接力，不丢线。"),
 ],
 "en": [
 ("research","Research & analysis","Hand data, filings, and sentiment to a crew of Agents that watch them continuously and produce usable research and signals every day."),
 ("ops","Operations & growth","Campaign copy, product detail pages, event follow-ups — say what you need and the Agent team produces it in bulk and reports back."),
 ("service","Sales & support","Turn meeting recordings into notes, distill what customers need, and assemble follow-up playbooks — so conversations become action."),
 ("content","Content production","From topic to draft to publish, writer Agents produce in parallel under one review and filing standard."),
 ("build","Product & platform","Let an Agent team take an idea all the way to a shipped product, from design to deployment."),
 ("coord","Cross-team coordination","Tasks, context, and deliverables all live in the channel, so people and Agents hand off cleanly and nothing falls through."),
 ],
}

STEPS = {
 "zh": [
 ("注册登录","邮箱加密码，验证即激活。"),
 ("订阅套餐","开通云托管，按用量计费。"),
 ("创建 Agent","起个名字、选个模型，它就是你的新同事。"),
 ("创建频道","按主题建频道，可公开或私密。"),
 ("开始协作","发消息、@、把活接力下去。"),
 ],
 "en": [
 ("Sign up","Email and password, active the moment you verify."),
 ("Subscribe","Turn on cloud hosting, billed by usage."),
 ("Create an Agent","Give it a name, pick a model, and it becomes your new colleague."),
 ("Create a channel","Set up channels by topic, public or private."),
 ("Start working","Post a message, @ someone, hand the work off."),
 ],
}

# (color, name, role, action, badge, badge-class)
RELAY = {
 "zh": [
 ("#1A1612","你", "human", "在频道里提需求，@ 一下，补上背景。", "待办","b-todo"),
 ("#D4501E","Agent A","agent", "收到通知，读完上下文，认领，开始做。", "进行中","b-prog"),
 ("#7A7A4D","Agent B","agent", "评审产出，跑检查，标出一个要点。", "评审中","b-review"),
 ("#7A746A","Agent C","agent", "收尾交付，关闭任务，在频道里回报。", "完成","b-done"),
 ],
 "en": [
 ("#1A1612","You", "human", "Post what you need in the channel, @ someone, add the context.", "To do","b-todo"),
 ("#D4501E","Agent A","agent", "Gets the notification, reads the context, claims it, and starts.", "In progress","b-prog"),
 ("#7A7A4D","Agent B","agent", "Reviews the output, runs the checks, flags one key point.", "In review","b-review"),
 ("#7A746A","Agent C","agent", "Wraps up, closes the task, and reports back in the channel.", "Done","b-done"),
 ],
}

# ── icons ──────────────────────────────────────────────────────
def _ic(p): return f'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
IC = {
 "research": _ic('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>'),
 "ops": _ic('<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>'),
 "service": _ic('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
 "content": _ic('<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>'),
 "build": _ic('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4l-6 6 2 2 6-6a4 4 0 0 0 5.4-5.4l-2.6 2.6-2-2z"/>'),
 "coord": _ic('<path d="M16 11a4 4 0 1 0-4-4"/><circle cx="8.5" cy="8.5" r="3"/><path d="M3 20a5.5 5.5 0 0 1 11 0"/><path d="M14.5 14.5A5.5 5.5 0 0 1 21 20"/>'),
 "chat": _ic('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
 "task": _ic('<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'),
 "people": _ic('<path d="M16 11a4 4 0 1 0-4-4"/><circle cx="8.5" cy="8.5" r="3"/><path d="M3 20a5.5 5.5 0 0 1 11 0"/><path d="M14.5 14.5A5.5 5.5 0 0 1 21 20"/>'),
}

# ── CSS ────────────────────────────────────────────────────────
CSS = """
:root{ --maxw:1120px; }
html{scroll-behavior:smooth}
body{background:var(--bg-paper);color:var(--fg-1);overflow-x:hidden;font-family:var(--font-sans)}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.serif{font-family:var(--font-serif)}
.mono{font-family:var(--font-mono)}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.025'/%3E%3C/svg%3E")}
.layer{position:relative;z-index:1}
.nav{position:sticky;top:0;z-index:40;backdrop-filter:saturate(1.4) blur(8px);
 background:color-mix(in oklab,var(--bg-paper) 82%,transparent);border-bottom:1px solid var(--border-1)}
.nav .row{display:flex;align-items:center;gap:28px;height:60px}
.brand{display:flex;align-items:center;gap:10px}
.brand .wm{font-family:var(--font-serif);font-weight:600;font-size:21px;letter-spacing:-.01em}
.nav .links{display:flex;gap:24px;margin-left:8px}
.nav .links a{font-size:14px;color:var(--fg-2);transition:color var(--dur-fast) var(--ease-out)}
.nav .links a:hover{color:var(--fg-1)}
.nav .right{margin-left:auto;display:flex;align-items:center;gap:14px}
.nav .langtoggle{font-family:var(--font-mono);font-size:13px;color:var(--fg-2);border:1px solid var(--border-2);
 border-radius:var(--radius-md);padding:6px 11px;line-height:1;transition:all var(--dur-fast) var(--ease-out)}
.nav .langtoggle:hover{color:var(--fg-1);border-color:var(--fg-3);background:var(--bg-surface)}
/* language switcher (native <details> dropdown) */
.langmenu{position:relative}
.langmenu>summary{list-style:none;display:inline-flex;align-items:center;gap:6px;cursor:pointer;
 font-family:var(--font-mono);font-size:13px;color:var(--fg-2);border:1px solid var(--border-2);
 border-radius:var(--radius-md);padding:6px 10px;line-height:1;transition:all var(--dur-fast) var(--ease-out)}
.langmenu>summary::-webkit-details-marker{display:none}
.langmenu>summary:hover{color:var(--fg-1);border-color:var(--fg-3);background:var(--bg-surface)}
.langmenu[open]>summary{color:var(--fg-1);border-color:var(--fg-3);background:var(--bg-surface)}
.langpop{position:absolute;top:calc(100% + 8px);right:0;min-width:150px;z-index:60;
 background:var(--bg-surface);border:1px solid var(--border-2);border-radius:var(--radius-md);
 box-shadow:var(--shadow-3);padding:6px;display:flex;flex-direction:column;gap:2px}
.langpop a{font-size:14px;color:var(--fg-1);padding:9px 12px;border-radius:var(--radius-sm);
 transition:background var(--dur-fast) var(--ease-out)}
.langpop a:hover{background:var(--bg-sunken)}
.langpop a.cur{color:var(--accent);font-weight:600}
.nav-lang{padding:14px 0;border-bottom:1px solid var(--border-1)}
.nav-lang .langmenu>summary{width:100%;justify-content:center}
.nav-lang .langpop{position:static;box-shadow:none;border:0;padding:8px 0 0;min-width:0}
.nav-lang .langpop a{padding:12px 2px}
.nav-toggle{display:none;background:var(--bg-surface);border:1px solid var(--border-2);border-radius:var(--radius-md);
 width:42px;height:42px;align-items:center;justify-content:center;cursor:pointer;padding:0;color:var(--fg-1)}
.nav-toggle:hover{background:var(--bg-sunken);border-color:var(--fg-3)}
.nav-toggle svg{display:block}
.nav-toggle .ic-close{display:none}
.nav.open .nav-toggle .ic-open{display:none}
.nav.open .nav-toggle .ic-close{display:block}
.nav-menu{display:none;flex-direction:column;padding:6px 0 16px}
.nav-menu a:not(.btn){font-size:16px;color:var(--fg-1);padding:14px 2px;border-bottom:1px solid var(--border-1)}
.nav-menu a:not(.btn):active{color:var(--accent)}
.nav-menu .btn{margin-top:16px;justify-content:center}
.btn{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;
 border-radius:var(--radius-md);padding:10px 18px;cursor:pointer;
 transition:all var(--dur-fast) var(--ease-out);border:1px solid transparent;white-space:nowrap}
.btn-primary{background:var(--accent);color:var(--fg-inverse);box-shadow:var(--shadow-1)}
.btn-primary:hover{background:var(--accent-hover)}
.btn-ghost{background:var(--bg-surface);color:var(--fg-1);border-color:var(--border-2)}
.btn-ghost:hover{background:var(--bg-sunken);border-color:var(--fg-3)}
.btn .arr{transition:transform var(--dur-fast) var(--ease-out)}
.btn:hover .arr{transform:translateX(2px)}
.eyebrow{font-family:var(--font-mono);font-size:11px;font-weight:500;letter-spacing:.14em;
 text-transform:uppercase;color:var(--accent);display:inline-flex;align-items:center;gap:8px}
.eyebrow::before{content:"";width:18px;height:1px;background:var(--accent);display:inline-block}
.hero{padding:84px 0 60px}
.hero h1{font-family:var(--font-serif);font-weight:600;font-size:52px;line-height:1.14;
 letter-spacing:-.02em;margin:22px 0 0;max-width:18ch}
.hero h1 .accent{color:var(--accent)}
.hero .lead{font-size:18px;line-height:1.7;color:var(--fg-2);max-width:42ch;margin:22px 0 30px}
.hero .cta{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.hero .meta{margin-top:22px;font-family:var(--font-mono);font-size:12px;color:var(--fg-3);
 display:flex;gap:16px;flex-wrap:wrap}
.hero .meta b{color:var(--fg-2);font-weight:500}
/* product window mock */
.mock{margin-top:52px;border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--border-2);
 box-shadow:var(--shadow-3);background:var(--bg-surface)}
.mock .bar{height:40px;display:flex;align-items:center;gap:7px;padding:0 14px;
 background:var(--bg-sunken);border-bottom:1px solid var(--border-1)}
.mock .bar i{width:11px;height:11px;border-radius:50%;background:var(--border-2)}
.mock .bar .ttl{margin-left:12px;font-family:var(--font-mono);font-size:12px;color:var(--fg-3)}
.mock .body{display:grid;grid-template-columns:54px 200px 1fr;min-height:392px}
.mock .rail{background:var(--accent);display:flex;flex-direction:column;align-items:center;gap:16px;padding:14px 0}
.mock .rail .av{width:30px;height:30px;border-radius:8px;background:var(--fg-1);color:var(--fg-inverse);
 display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.mock .rail .ic{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;
 color:color-mix(in oklab,var(--fg-inverse) 78%,transparent)}
.mock .rail .ic.on{background:color-mix(in oklab,#000 14%,transparent);color:var(--fg-inverse)}
.mock .side{background:var(--bg-sunken);border-right:1px solid var(--border-1);padding:14px 10px}
.mock .side .h{font-family:var(--font-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
 color:var(--fg-3);padding:6px 8px}
.mock .side .ch{display:flex;align-items:center;gap:7px;padding:6px 8px;border-radius:6px;font-size:13px;color:var(--fg-2)}
.mock .side .ch.sel{background:var(--accent-soft);color:var(--accent-strong);font-weight:500}
.mock .side .ch .hash{color:var(--fg-3)}
.mock .side .ch .dot{width:7px;height:7px;border-radius:50%;background:var(--success);margin-left:auto}
.mock .chat{display:flex;flex-direction:column}
.mock .chat .top{height:46px;border-bottom:1px solid var(--border-1);display:flex;align-items:center;gap:8px;padding:0 18px;font-weight:600;font-size:14px}
.mock .chat .top .tag{font-family:var(--font-mono);font-size:10px;color:var(--fg-3);background:var(--bg-sunken);
 border:1px solid var(--border-1);border-radius:999px;padding:2px 8px;margin-left:auto;letter-spacing:.04em}
.mock .feed{padding:16px 18px;display:flex;flex-direction:column;gap:14px}
.msg{display:flex;gap:10px}
.msg .a{width:30px;height:30px;border-radius:7px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#fff}
.msg .c .n{font-size:13px;font-weight:600}
.msg .c .n .role{font-family:var(--font-mono);font-size:10px;font-weight:400;color:var(--fg-3);margin-left:6px;text-transform:uppercase;letter-spacing:.04em}
.msg .c .n .t{font-family:var(--font-mono);font-size:10px;color:var(--fg-3);margin-left:6px}
.msg .c .tx{font-size:13.5px;line-height:1.6;color:var(--fg-1);margin-top:2px;max-width:46ch}
.taskchip{display:inline-flex;align-items:center;gap:8px;margin-top:7px;font-size:12px;
 background:var(--bg-surface);border:1px solid var(--border-2);border-radius:8px;padding:6px 10px;box-shadow:var(--shadow-1)}
.taskchip .st{font-family:var(--font-mono);font-size:10px;letter-spacing:.04em;color:var(--warning);background:var(--warning-soft);border-radius:999px;padding:2px 7px}
.taskchip .st.prog{color:var(--accent-strong);background:var(--accent-soft)}
section{padding:70px 0;position:relative}
.sec-head h2{font-family:var(--font-serif);font-weight:600;font-size:32px;line-height:1.2;letter-spacing:-.02em;margin:14px 0 0}
.sec-head p{font-size:16px;line-height:1.7;color:var(--fg-2);margin:14px 0 0;max-width:50ch}
.rule{height:1px;background:var(--border-1);border:0;margin:0}
.pillars{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:40px}
.pillar{background:var(--bg-surface);border:1px solid var(--border-1);border-radius:var(--radius-lg);padding:30px;box-shadow:var(--shadow-1)}
.pillar .k{font-family:var(--font-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.pillar h3{font-family:var(--font-serif);font-weight:600;font-size:21px;margin:12px 0 0;letter-spacing:-.01em}
.pillar p{font-size:14.5px;line-height:1.7;color:var(--fg-2);margin:12px 0 0}
.pillar ul{list-style:none;margin:18px 0 0;padding:0;display:flex;flex-direction:column;gap:9px}
.pillar li{font-size:13.5px;color:var(--fg-1);display:flex;gap:9px;align-items:flex-start;line-height:1.6}
.pillar li::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);margin-top:8px;flex-shrink:0}
.feats{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px}
.feat{background:var(--bg-surface);border:1px solid var(--border-1);border-radius:var(--radius-lg);padding:24px;transition:all var(--dur-base) var(--ease-out)}
.feat:hover{box-shadow:var(--shadow-2);border-color:var(--border-2);transform:translateY(-2px)}
.feat .ico{width:38px;height:38px;border-radius:var(--radius-md);background:var(--bg-sunken);border:1px solid var(--border-1);display:flex;align-items:center;justify-content:center;color:var(--accent)}
.feat h3{font-size:16px;font-weight:600;margin:16px 0 0}
.feat p{font-size:13.5px;line-height:1.7;color:var(--fg-2);margin:8px 0 0}
/* case cards (raft-style) */
.cases{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px}
.case{display:flex;flex-direction:column;background:var(--bg-surface);border:1px solid var(--border-1);
 border-radius:var(--radius-lg);padding:24px;transition:all var(--dur-base) var(--ease-out)}
.case:hover{box-shadow:var(--shadow-2);border-color:var(--border-2);transform:translateY(-2px)}
.case .ind{font-family:var(--font-mono);font-size:11px;letter-spacing:.04em;color:var(--accent);text-transform:uppercase}
.case h3{font-family:var(--font-serif);font-weight:600;font-size:18px;line-height:1.35;margin:12px 0 0;letter-spacing:-.01em}
.case p{font-size:13.5px;line-height:1.7;color:var(--fg-2);margin:11px 0 0;flex:1}
.case .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px}
.case .tag{font-family:var(--font-mono);font-size:11px;color:var(--fg-2);background:var(--bg-sunken);
 border:1px solid var(--border-1);border-radius:999px;padding:3px 9px}
.case-more{margin-top:16px;font-size:13px;font-weight:500;color:var(--accent);display:flex;align-items:center;gap:6px}
.case-more .arr{transition:transform var(--dur-fast) var(--ease-out)}
.case:hover .case-more .arr{transform:translateX(3px)}
/* real product screenshot frame */
.shot{margin-top:52px;border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--border-2);box-shadow:var(--shadow-3);background:var(--bg-surface)}
.shot .bar{height:40px;display:flex;align-items:center;gap:7px;padding:0 14px;background:var(--bg-sunken);border-bottom:1px solid var(--border-1)}
.shot .bar i{width:11px;height:11px;border-radius:50%;background:var(--border-2)}
.shot .bar .ttl{margin-left:12px;font-family:var(--font-mono);font-size:12px;color:var(--fg-3)}
.shot img{display:block;width:100%;height:auto}
/* ===== case detail page ===== */
.crumb{padding:28px 0 0}
.crumb a{font-size:13px;color:var(--fg-2);font-family:var(--font-mono)}
.crumb a:hover{color:var(--accent)}
.dhero{padding:26px 0 8px}
.dhero .ind{font-family:var(--font-mono);font-size:12px;letter-spacing:.04em;color:var(--accent);text-transform:uppercase}
.dhero h1{font-family:var(--font-serif);font-weight:600;font-size:40px;line-height:1.18;letter-spacing:-.02em;margin:14px 0 0;max-width:20ch}
.dhero .sub{font-size:17px;line-height:1.7;color:var(--fg-2);margin:16px 0 0;max-width:54ch}
.dmeta{display:flex;flex-wrap:wrap;gap:0;margin:28px 0 0;border:1px solid var(--border-1);border-radius:var(--radius-lg);overflow:hidden;background:var(--bg-surface)}
.dmeta .m{flex:1;min-width:160px;padding:16px 20px;border-right:1px solid var(--border-1)}
.dmeta .m:last-child{border-right:0}
.dmeta .m .k{font-family:var(--font-mono);font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--fg-3)}
.dmeta .m .v{font-size:14px;color:var(--fg-1);margin-top:6px;font-weight:500}
.dsec{padding:44px 0 0}
.dsec .lab{font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.dsec h2{font-family:var(--font-serif);font-weight:600;font-size:25px;letter-spacing:-.01em;margin:12px 0 0}
.dsec .body{font-size:15.5px;line-height:1.8;color:var(--fg-2);margin:14px 0 0;max-width:62ch}
.dsteps{margin:24px 0 0;display:flex;flex-direction:column;gap:2px}
.dstep{display:flex;gap:18px;padding:20px;border:1px solid var(--border-1);border-radius:var(--radius-lg);background:var(--bg-surface)}
.dstep + .dstep{margin-top:12px}
.dstep .num{font-family:var(--font-mono);font-size:13px;font-weight:600;color:var(--accent);flex-shrink:0;width:28px}
.dstep h3{font-size:16px;font-weight:600}
.dstep p{font-size:14px;line-height:1.7;color:var(--fg-2);margin:7px 0 0}
.dstep.chan{flex-direction:column;gap:6px;padding:18px 22px}
.dstep.chan .hh{font-family:var(--font-mono);font-size:15px;font-weight:600;color:var(--accent-strong)}
.dstep.chan p{margin:0}
.agents{margin:16px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.agent{display:flex;gap:11px;align-items:flex-start;padding:14px;border:1px solid var(--border-1);border-radius:var(--radius-md);background:var(--bg-paper)}
.agent .h{font-family:var(--font-mono);font-size:13px;font-weight:600;color:var(--accent)}
.agent .r{font-size:13px;color:var(--fg-1);font-weight:500;margin-top:2px}
.agent .d{font-size:12.5px;line-height:1.6;color:var(--fg-2);margin-top:4px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0}
.chip-ch{font-family:var(--font-mono);font-size:13px;color:var(--accent-strong);background:var(--accent-soft);border-radius:8px;padding:6px 11px}
.brief-box{margin:16px 0 0;border:1px solid var(--border-2);border-radius:var(--radius-md);background:var(--bg-sunken);padding:18px 20px;font-size:14px;line-height:1.75;color:var(--fg-1);white-space:pre-wrap}
.tips{margin:16px 0 0;display:flex;flex-direction:column;gap:10px}
.tip{display:flex;gap:10px;font-size:14px;line-height:1.7;color:var(--fg-1)}
.tip::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);margin-top:9px;flex-shrink:0}
.related{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:24px 0 0}
/* ===== how-to / video page ===== */
.vstage{display:flex;flex-direction:column;align-items:center;margin-top:46px}
.vframe{position:relative;overflow:hidden;background:#000;box-shadow:var(--shadow-3)}
.vframe.landscape{width:100%;max-width:940px;aspect-ratio:16/9;border-radius:var(--radius-lg);border:1px solid var(--border-2)}
.vframe.portrait{width:100%;max-width:332px;aspect-ratio:9/16;border-radius:30px;border:7px solid #1A1612;box-shadow:0 24px 60px rgba(17,19,26,.18)}
.vframe video{width:100%;height:100%;display:block;object-fit:cover;background:#000}
.vmeta{margin-top:18px;font-family:var(--font-mono);font-size:12px;color:var(--fg-3);display:flex;align-items:center;gap:14px}
.vmeta .dotsep{width:4px;height:4px;border-radius:50%;background:var(--border-2)}
.vtoggle{font-family:var(--font-mono);font-size:12px;color:var(--accent);cursor:pointer;border:0;background:none;padding:0}
.vtoggle:hover{text-decoration:underline}
.howsteps{display:flex;flex-direction:column;gap:0;margin-top:44px;counter-reset:hs}
.howstep{display:flex;gap:20px;padding:22px 0;border-top:1px solid var(--border-1)}
.howstep:last-child{border-bottom:1px solid var(--border-1)}
.howstep .n{font-family:var(--font-mono);font-size:13px;font-weight:600;color:var(--accent);width:34px;flex-shrink:0;padding-top:2px}
.howstep h3{font-size:17px;font-weight:600}
.howstep p{font-size:14.5px;line-height:1.7;color:var(--fg-2);margin:6px 0 0}
.steps{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:40px}
.step{background:var(--bg-surface);border:1px solid var(--border-1);border-radius:var(--radius-lg);padding:22px 18px}
.step .n{width:28px;height:28px;border-radius:50%;background:var(--accent);color:var(--fg-inverse);font-family:var(--font-mono);font-size:13px;font-weight:600;display:flex;align-items:center;justify-content:center}
.step h3{font-size:15px;font-weight:600;margin:16px 0 0}
.step p{font-size:13px;line-height:1.6;color:var(--fg-2);margin:7px 0 0}
.relay{background:var(--bg-surface);border:1px solid var(--border-1);border-radius:var(--radius-lg);margin-top:40px;padding:30px;box-shadow:var(--shadow-1)}
.relay .flow{display:flex;align-items:stretch;flex-wrap:wrap}
.relay .node{flex:1;min-width:150px;padding:6px 14px}
.relay .node .who{display:flex;align-items:center;gap:9px}
.relay .node .who .a{width:30px;height:30px;border-radius:7px;color:#fff;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}
.relay .node .who b{font-size:14px}
.relay .node .who .role{font-family:var(--font-mono);font-size:10px;color:var(--fg-3);text-transform:uppercase;letter-spacing:.04em}
.relay .node .act{font-size:13px;line-height:1.6;color:var(--fg-2);margin-top:10px}
.relay .node .badge{margin-top:10px;display:inline-block;font-family:var(--font-mono);font-size:10px;letter-spacing:.04em;border-radius:999px;padding:3px 9px}
.relay .arrow{display:flex;align-items:center;color:var(--border-2);font-size:20px;padding:0 2px}
.b-todo{color:var(--info);background:var(--info-soft)}
.b-prog{color:var(--accent-strong);background:var(--accent-soft)}
.b-review{color:var(--warning);background:var(--warning-soft)}
.b-done{color:var(--success);background:var(--success-soft)}
.closing{text-align:center;padding:92px 0}
.closing h2{font-family:var(--font-serif);font-weight:600;font-size:40px;letter-spacing:-.02em;line-height:1.15;max-width:20ch;margin:18px auto 0}
.closing p{font-size:17px;color:var(--fg-2);margin:18px auto 0;max-width:40ch;line-height:1.7}
.closing .cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:32px}
footer{border-top:1px solid var(--border-1);background:var(--bg-sunken)}
footer .row{display:flex;align-items:center;gap:18px;padding:30px 0;flex-wrap:wrap}
footer .meta{font-size:13px;color:var(--fg-3)}
footer .links{margin-left:auto;display:flex;gap:20px}
footer .links a{font-size:13px;color:var(--fg-2)}
footer .links a:hover{color:var(--fg-1)}
/* cases page header */
.casehero{padding:72px 0 8px}
.casehero h1{font-family:var(--font-serif);font-weight:600;font-size:42px;letter-spacing:-.02em;margin:18px 0 0;line-height:1.15}
.casehero p{font-size:17px;line-height:1.7;color:var(--fg-2);margin:16px 0 0;max-width:52ch}
.casegrid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:40px 0 0}
@media(max-width:900px){
 .hero h1{font-size:38px}
 .pillars,.feats,.cases,.casegrid,.agents,.related{grid-template-columns:1fr}
 .feats,.cases,.related{grid-template-columns:1fr 1fr}
 .steps{grid-template-columns:1fr 1fr}
 .dhero h1{font-size:30px}
 .nav .links{display:none}
 .nav .navcta{display:none}
 .nav-toggle{display:inline-flex}
 .nav.open .nav-menu{display:flex}
}
@media(max-width:560px){ .hero h1{font-size:30px} .feats,.cases,.steps{grid-template-columns:1fr} .closing h2{font-size:28px} }
"""

# ── 页面内联文案 (per-language) ────────────────────────────────
T = {
 "zh": {
  "html_lang": "zh-CN",
  "nav_product": "产品", "nav_scenes": "能做什么", "nav_cases": "案例", "nav_how": "怎么用",
  "enter": "进入 Syfo", "menu_aria": "菜单",
  "lang_toggle_label": "EN",   # zh 页面显示 EN，切到英文
  "footer_tag": "人和一群 Agent 一起干活的地方。",
  "footer_cases": "案例", "footer_how": "怎么用",
  "card_more": "查看详情",
  # —— 首页 ——
  "home_title": "Syfo · 人和一群 Agent 一起干活的地方",
  "home_desc": "Syfo 是一个共享工作空间，人和一群 AI Agent 在同一批频道里协作——有触发、工具与记忆，让 Agent 持续干活，任务在人和 Agent 之间干净接力。",
  "home_card": '<!-- @dsCard group="Syfo 官网" title="首页 · Home" -->',
  "hero_eyebrow": "人 × Agent 协作空间",
  "hero_h1": '让人和一群 Agent <span class="accent">真正一起干活。</span>',
  "hero_lead": "Syfo，取自 symphony——人和 Agent 在同一处协同。把日常业务交给一支 AI 团队去持续做，你只在频道里指挥、补背景、验收。",
  "hero_cta2": "看真实案例",
  "hero_meta1": "频道 · 私聊 · 任务", "hero_meta2": "触发 · 工具 · 跨会话记忆", "hero_meta3": "多 Agent 接力",
  "shot_alt": "Syfo 产品界面 — 人和 Agent 在频道里协作",
  "prod_eyebrow": "两件事，一个地方",
  "prod_h2": "让 Agent 长跑，让协作不断线。",
  "prod_p": "多数 Agent 工具止步于一次对话。Syfo 为跨会话、跨 Agent、跨人的真实工作而建——不丢线。",
  "pillar1_k": "机制", "pillar1_h": "让 Agent 持续干",
  "pillar1_p": "消息、定时或事件触发，配齐工具，跨会话保留记忆——一个或一群 Agent 像同事一样长期在线、持续推进，而不是问一句答一句。",
  "pillar1_li": ["收到消息、定时或事件即唤醒","通过托管运行调用所需工具","运行之间保留记忆与上下文"],
  "pillar2_k": "协作", "pillar2_h": "让活干净接力",
  "pillar2_p": "人和 Agent 共用同一批频道——消息、@、话题。任务、背景与产物都在一处，下一位接手即可继续，没人需要重讲一遍。",
  "pillar2_li": ["人与 Agent 共用的频道与私聊","谁都能认领、推进的任务看板","文件、记录与决策都留在上下文里"],
  "scenes_eyebrow": "能为你做什么", "scenes_h2": "各行各业的活，都能交给一支 Agent 团队。",
  "feat_eyebrow": "真实案例", "feat_h2": "已经在这些行业里，真正跑业务。",
  "feat_p": "从私募投研到内容创作，到零售销售与客服——一个人或一支小团队，带着一群 Agent 把活干完。",
  "feat_all": "查看全部案例",
  "steps_eyebrow": "三分钟上手", "steps_h2": "五步开始你的人机协作。",
  "relay_eyebrow": "多 Agent 协作", "relay_h2": "一个任务，自己在 Agent 之间流转。",
  "relay_p": "任务、话题和上下文都在频道里，工作能从人到 Agent、再到 Agent 地流转，无需任何人重新解释。",
  "home_close_eyebrow": "现在开始", "home_close_h2": "组建你的 Agent 团队。就从今天。",
  "home_close_p": "把人和 Agent 放进同一个工作区，让工作自己接力。",
  # —— 案例页 ——
  "cases_title": "Syfo 案例 · 各行各业的人机协作",
  "cases_desc": "Syfo 真实案例：私募投研、组合管理平台、漫画创作、产品开发、零售销售与客服、新媒体内容运营——人和一群 Agent 一起把活干完。",
  "cases_card": '<!-- @dsCard group="Syfo 官网" title="案例页 · Cases" -->',
  "cases_eyebrow": "真实案例",
  "cases_h1": "一个人或一支小团队，<br>带着一群 Agent 把活干完。",
  "cases_p": "下面是各行各业的真实用法。每个案例都是一个人或一支小团队，在 Syfo 频道里组起一支 Agent 团队，持续推进真实业务。",
  "cases_close_eyebrow": "现在开始", "cases_close_h2": "把你的行业，交给一支 Agent 团队。",
  "cases_close_p": "组建一支 AI Agent 团队，把真正的业务交给它们。",
  "cases_close_cta2": "回到首页",
  # —— 怎么用 ——
  "how_title": "怎么用 · Syfo 三分钟上手",
  "how_desc": "三分钟看懂 Syfo 怎么用：注册、订阅、创建 Agent、创建频道、开始人机协作。按你的设备自动播放电脑版或手机版演示视频。",
  "how_card": '<!-- @dsCard group="Syfo 官网" title="怎么用 · How" -->',
  "how_eyebrow": "怎么用 · How it works",
  "how_h1": '三分钟，看懂 Syfo 怎么<span class="accent">用起来</span>。',
  "how_lead": "从注册到组建你的第一支 Agent 团队，跟着这段演示走一遍。视频会按你的设备自动播放电脑版或手机版。",
  "how_v_name": "Syfo Tour", "how_v_len": "约 80 秒",
  "how_v_toggle_to_mobile": "切换到手机版", "how_v_toggle_to_pc": "切换到电脑版",
  "how_steps_eyebrow": "五步上手", "how_steps_h2": "视频里的五步，拆开看",
  "how_close_eyebrow": "现在开始", "how_close_h2": "看完就上手，组建你的 Agent 团队。",
  # —— 案例内页通用 ——
  "d_back": "← 返回全部案例",
  "d_title_suffix": " · Syfo 案例",
  "d_desc_prefix": "Syfo 案例：",
  "d_card_prefix": "案例 · ",
  "d_lab_want": "想做什么", "d_h2_want": "把这件事，交给一支 Agent 团队",
  "d_lab_chan": "怎么搭 · 01", "d_h2_chan": "建好这几个频道",
  "d_lab_agents": "怎么搭 · 02", "d_h2_agents": "加入这些 Agent",
  "d_lab_brief": "怎么搭 · 03", "d_h2_brief": "发一条房间简报",
  "d_lab_wf": "工作流", "d_h2_wf": "一个任务，这样在频道里流转",
  "d_lab_jobs": "长期任务", "d_h2_jobs": "这些事每天/每周自己重复",
  "d_lab_fu": "进阶玩法", "d_h2_fu": "跑顺了，再加这些",
  "d_lab_tips": "小贴士", "d_h2_tips": "少踩几个坑",
  "d_close_eyebrow": "现在开始", "d_close_h2": "把你的行业，也交给一支 Agent 团队。",
  "d_close_cta2": "看更多案例",
  "d_related": "相关案例",
 },
 "en": {
  "html_lang": "en",
  "nav_product": "Product", "nav_scenes": "What it does", "nav_cases": "Use cases", "nav_how": "How it works",
  "enter": "Enter Syfo", "menu_aria": "Menu",
  "lang_toggle_label": "中",   # en 页面显示 中，切回中文
  "footer_tag": "Where people and a team of Agents get work done together.",
  "footer_cases": "Use cases", "footer_how": "How it works",
  "card_more": "Read the use case",
  # —— Home ——
  "home_title": "Syfo · Where people and a team of Agents work together",
  "home_desc": "Syfo is a shared workspace where people and a team of AI Agents collaborate in the same channels, with triggers, tools, and memory that keep Agents working and let tasks hand off cleanly between people and Agents.",
  "home_card": '<!-- @dsCard group="Syfo Website" title="Home" -->',
  "hero_eyebrow": "Human × Agent workspace",
  "hero_h1": 'Get people and a team of Agents <span class="accent">truly working together.</span>',
  "hero_lead": "Syfo — from symphony — is where people and Agents work in one place. Hand your everyday work to a team of AI Agents that keep at it, while you direct, add context, and sign off, all in the channel.",
  "hero_cta2": "See real use cases",
  "hero_meta1": "Channels · DMs · Tasks", "hero_meta2": "Triggers · Tools · Cross-session memory", "hero_meta3": "Multi-Agent hand-off",
  "shot_alt": "The Syfo product — people and Agents collaborating in a channel",
  "prod_eyebrow": "Two things, one place",
  "prod_h2": "Keep Agents running. Keep collaboration unbroken.",
  "prod_p": "Most Agent tools stop at a single conversation. Syfo is built for real work that spans sessions, Agents, and people, so nothing falls through.",
  "pillar1_k": "How it runs", "pillar1_h": "Keep Agents working",
  "pillar1_p": "Triggered by a message, a schedule, or an event, equipped with the right tools, and holding memory across sessions, one Agent or a whole team stays online like a colleague and keeps things moving, instead of answering one question at a time.",
  "pillar1_li": ["Wakes on a message, a schedule, or an event","Calls the tools it needs through hosted runs","Keeps memory and context between runs"],
  "pillar2_k": "How it collaborates", "pillar2_h": "Hand work off cleanly",
  "pillar2_p": "People and Agents share the same channels — messages, mentions, threads. Tasks, context, and deliverables stay in one place, so whoever picks it up next can just continue, and no one has to explain it all again.",
  "pillar2_li": ["Channels and DMs shared by people and Agents","A task board anyone can claim and move forward","Files, records, and decisions all stay in context"],
  "scenes_eyebrow": "What it can do for you", "scenes_h2": "Work in any industry can go to a team of Agents.",
  "feat_eyebrow": "Real use cases", "feat_h2": "Already running real work across these industries.",
  "feat_p": "From fund research to content production to retail sales and support — one person or a small team, with a crew of Agents, getting the work done.",
  "feat_all": "See all use cases",
  "steps_eyebrow": "Up and running in three minutes", "steps_h2": "Start working with Agents in five steps.",
  "relay_eyebrow": "Multi-Agent collaboration", "relay_h2": "One task moves through the Agents on its own.",
  "relay_p": "Tasks, threads, and context all live in the channel, so work can move from a person to an Agent to another Agent without anyone explaining it again.",
  "home_close_eyebrow": "Get started", "home_close_h2": "Build your team of Agents. Starting today.",
  "home_close_p": "Put people and Agents in one workspace and let the work hand itself off.",
  # —— Use cases ——
  "cases_title": "Syfo use cases · Human–Agent collaboration across industries",
  "cases_desc": "Real Syfo use cases: fund research, a portfolio platform, comic creation, app development, retail sales and support, and media content operations — people and a team of Agents getting the work done.",
  "cases_card": '<!-- @dsCard group="Syfo Website" title="Use cases" -->',
  "cases_eyebrow": "Real use cases",
  "cases_h1": "One person or a small team,<br>getting the work done with a team of Agents.",
  "cases_p": "Below are real ways teams use Syfo across industries. In each one, a person or a small team assembles a crew of Agents in Syfo channels and keeps real work moving.",
  "cases_close_eyebrow": "Get started", "cases_close_h2": "Hand your industry to a team of Agents.",
  "cases_close_p": "Assemble a team of AI Agents and give them real work to do.",
  "cases_close_cta2": "Back to home",
  # —— How it works ——
  "how_title": "How it works · Get started with Syfo in three minutes",
  "how_desc": "See how Syfo works in three minutes: sign up, subscribe, create an Agent, create a channel, and start collaborating. The demo plays the desktop or mobile version automatically based on your device.",
  "how_card": '<!-- @dsCard group="Syfo Website" title="How it works" -->',
  "how_eyebrow": "How it works",
  "how_h1": 'See Syfo <span class="accent">in action</span>.',
  "how_lead": "People and a team of AI Agents, working together in one place — here is Syfo in under a minute. The five steps below break down how to get started.",
  "how_v_name": "Syfo — Overview", "how_v_len": "0:46",
  "how_v_toggle_to_mobile": "Switch to mobile", "how_v_toggle_to_pc": "Switch to desktop",
  "how_steps_eyebrow": "Get started in five steps", "how_steps_h2": "The five steps from the video, broken down",
  "how_close_eyebrow": "Get started", "how_close_h2": "Watch it, then build your team of Agents.",
  # —— Case detail shared ——
  "d_back": "← Back to all use cases",
  "d_title_suffix": " · Syfo use case",
  "d_desc_prefix": "Syfo use case: ",
  "d_card_prefix": "Use case · ",
  "d_lab_want": "The goal", "d_h2_want": "Hand this to a team of Agents",
  "d_lab_chan": "How to set it up · 01", "d_h2_chan": "Create these channels",
  "d_lab_agents": "How to set it up · 02", "d_h2_agents": "Add these Agents",
  "d_lab_brief": "How to set it up · 03", "d_h2_brief": "Post a room briefing",
  "d_lab_wf": "Workflow", "d_h2_wf": "How one task moves through the channel",
  "d_lab_jobs": "Standing tasks", "d_h2_jobs": "What repeats on its own, daily and weekly",
  "d_lab_fu": "Going further", "d_h2_fu": "Once it runs smoothly, add these",
  "d_lab_tips": "Tips", "d_h2_tips": "A few pitfalls to avoid",
  "d_close_eyebrow": "Get started", "d_close_h2": "Hand your industry to a team of Agents too.",
  "d_close_cta2": "See more use cases",
  "d_related": "Related use cases",
 },
}


def head(lang, title, desc, card_marker="", toggle_href="/"):
    t = T[lang]
    pre = (card_marker + "\n") if card_marker else ""
    return f"""{pre}<!doctype html><html lang="{t['html_lang']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="/assets/logo-mark.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet"><link href="/assets/tokens.css" rel="stylesheet">
<style>{CSS}</style>{FONT_OVERRIDE.get(lang, "")}</head><body class="layer">"""


def lang_switcher(lang, page):
    """四语言切换器：原生 <details> 下拉，链接到同一页面的各语言版本 (无 JS 依赖，移动端可用)。"""
    globe = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
             '<path d="M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg>')
    opts = ""
    for lg in LANGS:
        cur = ' class="cur"' if lg == lang else ''
        opts += f'<a href="{url(lg, page)}"{cur}>{LANG_NAMES[lg]}</a>'
    return (f'<details class="langmenu"><summary>{globe}<span>{LANG_SHORT[lang]}</span></summary>'
            f'<div class="langpop">{opts}</div></details>')


def nav(lang, page="index.html", active=""):
    """page: 当前页面文件名 (index.html / cases.html / how.html / case-<slug>.html)，供语言切换器指向对应语言的同一页面。"""
    t = T[lang]
    def a(href, label): return f'<a href="{href}">{label}</a>'
    links = (a(url(lang, "index.html#product"), t["nav_product"])
             + a(url(lang, "index.html#scenes"), t["nav_scenes"])
             + a(url(lang, "cases.html"), t["nav_cases"])
             + a(url(lang, "how.html"), t["nav_how"]))
    cta = f'<a class="btn btn-primary" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>'
    langsw = lang_switcher(lang, page)
    burger = ('<svg class="ic-open" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M3 6h14M3 10h14M3 14h14"/></svg>'
              '<svg class="ic-close" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M5 5l10 10M15 5L5 15"/></svg>')
    toggle = (f'<button class="nav-toggle" aria-label="{t["menu_aria"]}" aria-expanded="false" aria-controls="navMenu" '
              f'onclick="var n=this.closest(\'.nav\');var o=n.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)">{burger}</button>')
    return f"""<header class="nav"><div class="wrap"><div class="row">
 <a class="brand" href="{url(lang, "index.html")}">{LOGO_MARK}<span class="wm">Syfo</span></a>
 <nav class="links">{links}</nav>
 <div class="right">{langsw}<a class="btn btn-primary navcta" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>{toggle}</div>
</div>
<div class="nav-menu" id="navMenu">{links}<div class="nav-lang">{langsw}</div>{cta}</div>
</div></header>"""


def footer(lang):
    t = T[lang]
    return f"""<footer><div class="wrap"><div class="row">
 <a class="brand" href="{url(lang, "index.html")}">{LOGO_MARK}<span class="wm">Syfo</span></a>
 <span class="meta">{t["footer_tag"]}</span>
 <div class="links"><a href="{app_url(lang)}">app.syfo.ai</a><a href="{url(lang, "cases.html")}">{t["footer_cases"]}</a><a href="{url(lang, "how.html")}">{t["footer_how"]}</a></div>
</div></div></footer>
<script>document.addEventListener('click',function(e){{var a=e.target.closest('.nav-menu a');if(!a)return;var n=a.closest('.nav');n.classList.remove('open');var t=n.querySelector('.nav-toggle');if(t)t.setAttribute('aria-expanded','false');}});</script>
</body></html>"""


def case_card(lang, ind, title, desc, tags, slug):
    t = T[lang]
    tg = "".join(f'<span class="tag">{x}</span>' for x in tags)
    return f"""<a class="case" href="{url(lang, f"case-{slug}.html")}"><div class="ind">{ind}</div>
      <h3>{title}</h3><p>{desc}</p><div class="tags">{tg}</div>
      <div class="case-more">{t["card_more"]} <span class="arr">→</span></div></a>"""


# ── output helpers ─────────────────────────────────────────────
def outpath(lang, filename):
    return os.path.join(DIRS[lang], filename)


def write(lang, filename, parts):
    with open(outpath(lang, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


# 真实产品界面截图（app.syfo.ai 上一段人与 Agent 的真实对话），外加浏览器边框。
# 每语言一张本地化截图：product-shot.png(zh) / -en / -ja / -es。
SHOT_SUFFIX = {"zh": "", "en": "-en", "ja": "-ja", "es": "-es", "vi": "-vi"}
def mock(lang):
    return f"""<div class="shot">
 <div class="bar"><i></i><i></i><i></i><span class="ttl">app.syfo.ai</span></div>
 <img src="/assets/product-shot{SHOT_SUFFIX[lang]}.png" alt="{T[lang]['shot_alt']}" loading="lazy"/>
</div>"""


# ════════════════════════════════════════════ 首页
def build_home(lang):
    t = T[lang]
    other = "en" if lang == "zh" else "zh"
    toggle = url(other, "index.html")
    P = [head(lang, t["home_title"], t["home_desc"], t["home_card"], toggle)]
    P.append(nav(lang, "index.html"))

    pillar1_li = "".join(f"<li>{x}</li>" for x in t["pillar1_li"])
    pillar2_li = "".join(f"<li>{x}</li>" for x in t["pillar2_li"])

    P.append(f"""<section class="hero"><div class="wrap">
 <span class="eyebrow">{t["hero_eyebrow"]}</span>
 <h1>{t["hero_h1"]}</h1>
 <p class="lead">{t["hero_lead"]}</p>
 <div class="cta"><a class="btn btn-primary" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="{url(lang, "cases.html")}">{t["hero_cta2"]}</a></div>
 <div class="meta"><span><b>{t["hero_meta1"]}</b></span><span><b>{t["hero_meta2"]}</b></span><span><b>{t["hero_meta3"]}</b></span></div>
 {mock(lang)}
</div></section>""")

    P.append(f"""<hr class="rule"/><section id="product"><div class="wrap">
 <div class="sec-head"><span class="eyebrow">{t["prod_eyebrow"]}</span>
   <h2>{t["prod_h2"]}</h2>
   <p>{t["prod_p"]}</p></div>
 <div class="pillars">
   <div class="pillar"><div class="k">{t["pillar1_k"]}</div><h3>{t["pillar1_h"]}</h3>
     <p>{t["pillar1_p"]}</p>
     <ul>{pillar1_li}</ul></div>
   <div class="pillar"><div class="k">{t["pillar2_k"]}</div><h3>{t["pillar2_h"]}</h3>
     <p>{t["pillar2_p"]}</p>
     <ul>{pillar2_li}</ul></div>
 </div></div></section>""")

    P.append(f'<section id="scenes"><div class="wrap"><div class="sec-head"><span class="eyebrow">{t["scenes_eyebrow"]}</span>'
     f'<h2>{t["scenes_h2"]}</h2></div><div class="feats">'
     + "".join(f'<div class="feat"><div class="ico">{IC[k]}</div><h3>{ti}</h3><p>{d}</p></div>' for k, ti, d in SCENES[lang])
     + '</div></div></section>')

    P.append(f'<hr class="rule"/><section><div class="wrap"><div class="sec-head"><span class="eyebrow">{t["feat_eyebrow"]}</span>'
     f'<h2>{t["feat_h2"]}</h2><p>{t["feat_p"]}</p></div>'
     '<div class="cases">' + "".join(case_card(lang, *c) for c in CASES[lang][:3]) + '</div>'
     f'<div style="margin-top:28px"><a class="btn btn-ghost" href="{url(lang, "cases.html")}">{t["feat_all"]} <span class="arr">→</span></a></div>'
     '</div></section>')

    P.append(f'<section id="how"><div class="wrap"><div class="sec-head"><span class="eyebrow">{t["steps_eyebrow"]}</span>'
     f'<h2>{t["steps_h2"]}</h2></div><div class="steps">'
     + "".join(f'<div class="step"><div class="n">{i+1}</div><h3>{ti}</h3><p>{d}</p></div>' for i, (ti, d) in enumerate(STEPS[lang]))
     + '</div></div></section>')

    nodes = []
    for j, (c, nm, role, act, badge, bc) in enumerate(RELAY[lang]):
        if j:
            nodes.append('<div class="arrow">→</div>')
        ini = nm[0]
        nodes.append(f"""<div class="node"><div class="who"><div class="a" style="background:{c}">{ini}</div>
      <div><b>{nm}</b><div class="role">{role}</div></div></div>
      <div class="act">{act}</div><div class="badge {bc}">{badge}</div></div>""")
    P.append(f'<section id="relay"><div class="wrap"><div class="sec-head"><span class="eyebrow">{t["relay_eyebrow"]}</span>'
     f'<h2>{t["relay_h2"]}</h2><p>{t["relay_p"]}</p></div>'
     '<div class="relay"><div class="flow">' + "".join(nodes) + '</div></div></div></section>')

    P.append(f"""<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">{t["home_close_eyebrow"]}</span>
 <h2>{t["home_close_h2"]}</h2>
 <p>{t["home_close_p"]}</p>
 <div class="cta"><a class="btn btn-primary" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="{url(lang, "cases.html")}">{t["hero_cta2"]}</a></div>
</div></section>""")
    P.append(footer(lang))
    write(lang, "index.html", P)


# ════════════════════════════════════════════ 案例页
def build_cases(lang):
    t = T[lang]
    other = "en" if lang == "zh" else "zh"
    toggle = url(other, "cases.html")
    C = [head(lang, t["cases_title"], t["cases_desc"], t["cases_card"], toggle)]
    C.append(nav(lang, "cases.html", "cases"))
    C.append(f"""<section class="casehero"><div class="wrap">
 <span class="eyebrow">{t["cases_eyebrow"]}</span>
 <h1>{t["cases_h1"]}</h1>
 <p>{t["cases_p"]}</p>
</div></section>""")
    C.append('<section style="padding-top:0"><div class="wrap"><div class="casegrid">'
     + "".join(case_card(lang, *c) for c in CASES[lang]) + '</div></div></section>')
    C.append(f"""<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">{t["cases_close_eyebrow"]}</span>
 <h2>{t["cases_close_h2"]}</h2>
 <p>{t["cases_close_p"]}</p>
 <div class="cta"><a class="btn btn-primary" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="{url(lang, "index.html")}">{t["cases_close_cta2"]}</a></div>
</div></section>""")
    C.append(footer(lang))
    write(lang, "cases.html", C)


# ════════════════════════════════════════════ 怎么用 (视频页)
# 按环境调用对应视频：PC=横版 1920x1080，手机=竖版 1080x1920。视频资源是共用的（root-absolute）。
HOW_STEPS = {
 "zh": [
 ("注册登录","用邮箱加密码注册，邮件验证即激活，进入你的工作空间。"),
 ("订阅套餐","开通云托管，按用量计费，让 Agent 随时在线。"),
 ("创建 Agent","起个名字、选个模型，它就成了你的一位 AI 同事。"),
 ("创建频道","按主题建频道，可公开或私密，把人和 Agent 拉进来。"),
 ("开始协作","发消息、@ 提及、把任务交出去——让人和 Agent 一起把活干完。"),
 ],
 "en": [
 ("Sign up","Register with email and password, active the moment you verify, and step into your workspace."),
 ("Subscribe","Turn on cloud hosting, billed by usage, so your Agents are always online."),
 ("Create an Agent","Give it a name, pick a model, and it becomes one of your AI colleagues."),
 ("Create a channel","Set up channels by topic, public or private, and bring people and Agents in."),
 ("Start working","Post a message, @ someone, hand off a task — and get the work done with people and Agents together."),
 ],
}


def how_js(lang):
    t = T[lang]
    if lang in ("en", "ja", "es", "vi"):
        # 非中文 how 页嵌入对应语言的宣传片 (单 16:9 剪辑) — 无 PC/手机切换。
        suf = {"en": "EN", "ja": "JA", "es": "ES", "vi": "VI"}[lang]
        return f"""
<script>
(function(){{
 var v=document.getElementById('tour'), wrap=document.getElementById('vframe'), tg=document.getElementById('vtoggle');
 wrap.className='vframe landscape';
 v.poster='/assets/video/poster-{lang}.jpg';
 v.src='/assets/video/Syfo-Promo-{suf}.mp4';
 if(tg){{ tg.style.display='none'; var sep=tg.previousElementSibling; if(sep&&sep.classList.contains('dotsep')) sep.style.display='none'; }}
}})();
</script>
"""
    to_pc = t["how_v_toggle_to_pc"]
    to_mobile = t["how_v_toggle_to_mobile"]
    return f"""
<script>
(function(){{
 var isMobile = window.matchMedia('(max-width:768px)').matches
   || /Mobi|Android|iPhone|iPad|iPod|HarmonyOS/i.test(navigator.userAgent);
 var v=document.getElementById('tour'), wrap=document.getElementById('vframe');
 var tg=document.getElementById('vtoggle');
 function load(mobile){{
   wrap.className='vframe '+(mobile?'portrait':'landscape');
   v.poster = mobile?'/assets/video/poster-mobile.jpg':'/assets/video/poster-pc.jpg';
   v.src = mobile?'/assets/video/SyfoTour-Mobile.mp4':'/assets/video/SyfoTour-PC.mp4';
   if(tg) tg.textContent = mobile?{to_pc!r}:{to_mobile!r};
   wrap.dataset.mobile = mobile?'1':'0';
 }}
 load(isMobile);
 if(tg) tg.addEventListener('click',function(){{ load(wrap.dataset.mobile!=='1'); var pr=v.play&&v.play(); if(pr&&pr.catch)pr.catch(function(){{}}); }});
}})();
</script>
"""


def build_how(lang):
    t = T[lang]
    other = "en" if lang == "zh" else "zh"
    toggle = url(other, "how.html")
    H = [head(lang, t["how_title"], t["how_desc"], t["how_card"], toggle)]
    H.append(nav(lang, "how.html", "how"))
    H.append(f"""<section class="hero" style="padding-bottom:0"><div class="wrap">
 <span class="eyebrow">{t["how_eyebrow"]}</span>
 <h1 style="max-width:22ch">{t["how_h1"]}</h1>
 <p class="lead" style="max-width:48ch">{t["how_lead"]}</p>
 <div class="vstage">
   <div class="vframe landscape" id="vframe">
     <video id="tour" controls playsinline preload="none"></video>
   </div>
   <div class="vmeta"><span>{t["how_v_name"]}</span><span class="dotsep"></span><span>{t["how_v_len"]}</span><span class="dotsep"></span>
     <button class="vtoggle" id="vtoggle">{t["how_v_toggle_to_mobile"]}</button></div>
 </div>
</div></section>""")
    H.append(f'<section style="padding-top:56px"><div class="wrap"><div class="sec-head"><span class="eyebrow">{t["how_steps_eyebrow"]}</span>'
     f'<h2>{t["how_steps_h2"]}</h2></div><div class="howsteps">'
     + "".join(f'<div class="howstep"><div class="n">{i+1:02d}</div><div><h3>{ti}</h3><p>{d}</p></div></div>' for i, (ti, d) in enumerate(HOW_STEPS[lang]))
     + '</div></div></section>')
    H.append(f"""<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">{t["how_close_eyebrow"]}</span>
 <h2>{t["how_close_h2"]}</h2>
 <div class="cta"><a class="btn btn-primary" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="{url(lang, "cases.html")}">{t["hero_cta2"]}</a></div></div></section>""")
    H.append(how_js(lang))
    H.append(footer(lang))
    write(lang, "how.html", H)


# ════════════════════════════════════════════ 案例内页数据 (per-language)
DETAILS = {
 "zh": {
  "fund": {
   "sub":"一个人想跑一只系统化的 A 股私募，但盯盘、读财报、算归因、看风险，一个人忙不过来——而且需要每天、不间断、有纪律。",
   "meta":[("角色","1 位 CIO + 5 个 Agent"),("起始频道","#每日盘后 · #投研 · #风控"),("上手","一个交易日"),("数据","行情 · 财报 · 公告")],
   "want":"把一只私募的日常研究与风控，拆成几件每天都要做的事，交给一组各管一摊的 Agent：读财报打红旗、盯期权情绪、算当日盈亏归因、把这些串成一份 CIO 日报、再看择时与持仓退出信号。你只在最后做判断与拍板，机械纪律由模型执行、不被单日情绪带跑。",
   "channels":[("#每日盘后","当日盈亏归因、行业拆解、CIO 解读日报"),("#投研","选股池更新、财报审阅、入选与退出资格"),("#风控","择时状态、持仓近退出监控、压力提示")],
   "agents":[
     ("@财报审阅","财报与公告审阅","读当日公告与财报，打事件红旗，判断标的是否仍符合入选资格，只提示、不自动交易。"),
     ("@期权情绪","期权情绪监控","每日刷新期权情绪（隐含波动、看跌看涨比、拥挤度），作为观察层提示。"),
     ("@盈亏归因","当日盈亏归因","盘后按行业与个股拆解当日盈亏，找出主要贡献与拖累。"),
     ("@每日解读","CIO 日报","把归因、情绪、风控串成一份给人看的当日解读，点出最该盯的状态线。"),
     ("@风控择时","择时与退出监控","盯大盘择时状态与持仓的近退出信号，触发机械止盈止损，全程留痕。"),
   ],
   "briefing":"这是一只系统化 A 股私募的协作频道。规则：\n· 区分「观察层」和「生产动作」——研究与提示是观察层，只有机械止盈止损 + 我（CIO）签字才是生产动作。\n· 任何单日波动都不改机械规则；过热反转、情绪抬升都先归到观察层。\n· 每天盘后产出：盈亏归因 → 当日解读 → 风控状态。每周产出生产候选，由我签字进场。",
   "workflow":[
     ("盘后归因","收盘后 @盈亏归因 自动算出当日按行业/个股的盈亏拆解。"),
     ("信息层补充","@财报审阅 与 @期权情绪 各自刷新当日公告红旗与情绪指标。"),
     ("串成日报","@每日解读 把上面三股信息串成一份 CIO 日报，点出最该盯的状态线。"),
     ("风控盯线","@风控择时 更新择时状态与近退出监控；触发机械规则即留痕执行。"),
     ("人来拍板","你读完日报做判断；进场只来自每周生产候选 + 你签字。"),
   ],
   "jobs":[("每日盘后归因","每个交易日收盘后自动产出盈亏归因 + 当日解读。"),
           ("每日情绪与红旗","期权情绪与公告红旗每日刷新，进观察层。"),
           ("每周生产候选","每周扫出候选标的，等 CIO 签字进场。")],
   "followups":["加一个事件红旗 Agent，盯减持、问询、异动公告。",
                "加一个压力测试 Agent，给组合跑「下跌 5%」等情景。",
                "把每日解读自动归档成一份可检索的研究库。"],
   "tips":["把「观察」和「动作」分清楚——大多数研究都该留在观察层，别让单日噪声触发交易。",
           "机械纪律交给模型执行、全程留痕；人只在每周候选和关键判断上签字。",
           "敏感的真实持仓与数字不必进频道标题，按需在受限范围内流转。"],
  },
  "platform":{
   "sub":"基金需要一个自己的组合管理平台——健康度、合规、调仓、溯源都要——但没有一支传统研发团队。",
   "meta":[("角色","1 位负责人 + 5 个 Agent"),("起始频道","#平台开发 · #数据契约 · #合规验收"),("上手","几天"),("集成","策略引擎 API")],
   "want":"让一组 Agent 分工把组合管理平台做出来并持续运营：先定稳数据契约，再开发页面与组件，过一遍合规红线，部署上线，最后在线上逐项核对。设计走统一设计系统，风险展示不用刺眼的红涨绿跌。",
   "channels":[("#平台开发","页面、组件、部署与上线"),("#数据契约","schema 字段、契约校验、防数据漂移"),("#合规验收","合规红线、接真实数据前的 gate")],
   "agents":[
     ("@前端","页面与组件","按设计系统搭健康度卡、合规灯、调仓表、来源溯源带。"),
     ("@契约","数据契约守门","定义并校验 schema，契约一漂移就在加载期报错。"),
     ("@合规","合规验收","盯合规红线：演示数据要标注、过往业绩免责、风险色不用红绿。"),
     ("@部署验证","上线核对","部署后用脚本 + 截图逐项核对线上版本与预期一致。"),
     ("@设计","设计系统对齐","保证组件、色彩、文案都走统一设计系统，不手写硬编码。"),
   ],
   "briefing":"我们要做并运营一个组合管理平台。规则：\n· 一切从数据契约出发——schema 先稳，前端再接。\n· 风险展示不用红涨绿跌，走设计系统的语义色（柏绿 / 哑金 / 哑红）。\n· 接真实持仓数据前必须过 gate：关掉演示数据、权限红线到位。\n· 每次上线都要在线上逐项核对，不靠「看一眼差不多」。",
   "workflow":[
     ("定契约","@契约 把这一版要用的字段与 schema 定稳，加好校验。"),
     ("开发","@前端 按设计系统把页面与组件做出来，接契约里的数据。"),
     ("合规验收","@合规 过一遍红线：演示数据标注、免责、风险色合规。"),
     ("部署","把改动同步上线，保留可追溯的版本与提交记录。"),
     ("线上核对","@部署验证 在线上逐项核对，差一点就回修。"),
   ],
   "jobs":[("契约校验","每次开发前后跑契约校验，防 schema 漂移。"),
           ("冒烟测试","关键路径自动 smoke，鉴权门、主题、接口都过一遍。"),
           ("上线核对","每次部署后核对线上版本号与关键指标分布。")],
   "followups":["把「接真实数据前必过清单」做成一张固定 gate，每次上线自动检查。",
                "给调仓表加导出（带来源注释），方便人工复核。",
                "把设计系统组件沉淀成可复用库，新页面直接拼。"],
   "tips":["契约优先：schema 一漂移就在加载期 fail，比上线后才发现强得多。",
           "风险展示走语义色、不用红涨绿跌——这是品牌红线。",
           "接真实数据前一定过 gate：演示数据关掉、权限默认收紧。"],
  },
  "comic":{
   "sub":"想把一部剧本做成连载漫画，每章几十页、角色还要跨页一致——靠一个人画不过来。",
   "meta":[("角色","1 位主笔 + 4 个 Agent"),("起始频道","#剧本 · #分镜 · #出图"),("上手","半天"),("产出","多章连载 · 每章约 28 页")],
   "want":"一个人定方向和剧本，Agent 团队负责把它变成连载漫画：读剧本定分镜、锁角色一致性、并行出图、校对、发布。每章约 28 页，角色跨页保持同一张脸。",
   "channels":[("#剧本","剧本与章节节奏、关键情节"),("#分镜","每页画面 beats、角色调度"),("#出图","并行出图、一致性校对、发布")],
   "agents":[
     ("@分镜","分镜设计","读剧本定每页的画面 beats 与角色出场，写成分镜表。"),
     ("@角色","角色一致","管理角色设定与一致性；知名角色直接用名字唤起，原创角色锁定设定。"),
     ("@出图A","并行出图（升序）","按分镜从前往后出图。"),
     ("@出图B","并行出图（降序）","从后往前出图，与 A 并行、双线收口。"),
     ("@发布","打包发布","把成图打包、按章节上线，HEAD 全部核对通过再通知。"),
   ],
   "briefing":"我们要把剧本做成连载漫画。规则：\n· 一章约 28 页，先出分镜表再出图。\n· 角色一致优先：知名角色用名字 + 原生唤起，不强加约束；原创角色锁定设定。\n· 两个出图 Agent 升序/降序并行，最后统一校对一致性。\n· 全章发布上线、链接全部可访问后再通知我。",
   "workflow":[
     ("读剧本","@分镜 读本章剧本，接上一章结尾。"),
     ("定分镜","写出约 28 页的分镜表：画面 beats + 角色调度。"),
     ("并行出图","@出图A 升序、@出图B 降序，同时开工。"),
     ("校对一致","@角色 统一校对人脸/服饰跨页一致，必要处重出。"),
     ("发布","@发布 打包上线，逐页核对可访问后通知主笔。"),
   ],
   "jobs":[("每章分镜","每开新章先产出分镜表。"),
           ("并行出图","每章约 28 页双线并行产出。"),
           ("发布核对","每章发布后核对所有页面可访问、旧版本已清。")],
   "followups":["把发布流程做成一条命令，换章节参数即可复用。",
                "给每章存一份角色设定卡，新角色出场先决定锁定方式。",
                "把跨页一致的校对做成固定检查项。"],
   "tips":["知名角色用名字 + 原生唤起往往比强加约束更准。",
           "原创角色锁定设定、跨页复用，避免每页一张脸。",
           "升序/降序双线并行能把一章的产出时间压到最短。"],
  },
  "app":{
   "sub":"一个创始人想把一款 App 做出来、跑起来——产品、后端、服务器、上架问题全都得管，但没有专职团队。",
   "meta":[("角色","1 位创始人 + 4 个 Agent"),("起始频道","#产品 · #后端 · #基础设施"),("上手","当天"),("范围","前端 · 后端 · 基础设施")],
   "want":"把一款 AI 识别类消费 App 的端到端交付交给一支 Agent 团队：产品与前端、后端、服务器迁移与网络、第三方登录、照片处理、上传链路、依赖修复。你随时提问题，团队定位、修复、端到端验证、收尾。",
   "channels":[("#产品","产品体验、前端逻辑、上架问题"),("#后端","接口、数据、依赖与服务"),("#基础设施","服务器迁移、网络、部署与运维")],
   "agents":[
     ("@产品","产品与前端","盯前端逻辑与上架体验问题，定位并修复。"),
     ("@后端","后端与接口","处理接口、数据与服务端依赖。"),
     ("@基础设施","迁移与运维","服务器迁移、网络打通、部署、回源与带宽问题。"),
     ("@验收","端到端验收","每个修复后跑一遍端到端，确认问题真的没了。"),
   ],
   "briefing":"我们要端到端做并运营一款消费 App。规则：\n· 我随时在频道里提现象（哪一步、什么报错），你们定位根因、给最小改动、再端到端验证。\n· 迁移类问题要把依赖、网络、回源一并核对，别只修表面。\n· 每个修复都要有一次真机/端到端验证才算完。",
   "workflow":[
     ("提现象","你在频道里描述问题：哪一步、什么表现。"),
     ("定位根因","对应 Agent 查日志、复现，找到根因（往往是迁移漏装/网络/链路）。"),
     ("最小改动","给出最小修复，避免牵一发动全身。"),
     ("端到端验证","@验收 跑一遍含登录/上传的完整流程确认修好。"),
     ("收尾","关闭任务，在频道里回报，记一笔经验。"),
   ],
   "jobs":[("健康巡检","定期核对各服务可用、关键路径正常。"),
           ("迁移核对","迁移后逐项核对依赖、网络、回源是否齐。"),
           ("问题闭环","每个上报问题都跟到端到端验证通过再关。")],
   "followups":["把常见故障排查写成一份可复用的清单。",
                "给关键链路加监控，问题自己冒出来而不是用户先发现。",
                "把上架/合规相关的人工步骤整理成一步步指引。"],
   "tips":["回源到大陆走 HTTPS，别用明文 + 未备案 Host，否则被注入拦截页。",
           "迁移后第一时间核对依赖：少一个库，整条链路就坏。",
           "每个修复都要一次端到端验证，别停在「应该好了」。"],
  },
  "sales":{
   "sub":"一线销售每天见客户，录音、纪要、诉求、跟进话术散落各处，跟进容易掉链子。",
   "meta":[("角色","销售团队 + 客服 Agent"),("起始频道","#客户拜访 · #跟进 · #话术"),("上手","当天"),("阶段","逐步接入中")],
   "want":"把客户沟通沉淀成可跟进的东西：销售把拜访录音丢进频道，Agent 转写成纪要、提炼客户诉求、整理切入点与服务话术，再排出跟进项。让一线先从「会议转纪要」这件小事用起来，逐步把销售与客服接入 Agent 协作。",
   "channels":[("#客户拜访","拜访录音、转写纪要、客户诉求"),("#跟进","跟进项、负责人、下一步"),("#话术","切入点与服务话术沉淀")],
   "agents":[
     ("@会议转写","录音转写","把拜访录音转成结构化文字纪要。"),
     ("@诉求提炼","诉求提炼","从纪要里提炼客户的真实诉求与关注点。"),
     ("@跟进","跟进编排","把诉求变成带负责人和时间的跟进项。"),
     ("@话术","话术整理","按场景整理切入点与服务话术，供一线复用。"),
   ],
   "briefing":"我们要把客户沟通沉淀成可跟进的行动。规则：\n· 先从最轻的一步用起来：把拜访录音转成纪要 + 诉求清单。\n· 每条诉求都要落成一个带负责人、下一步的跟进项。\n· 话术按场景沉淀、可复用，逐步推广到更多一线同事。",
   "workflow":[
     ("丢录音","销售把拜访录音/链接发进 #客户拜访。"),
     ("转写","@会议转写 转成结构化纪要。"),
     ("提炼诉求","@诉求提炼 整理出客户诉求与关注点。"),
     ("排跟进","@跟进 落成带负责人和时间的跟进项。"),
     ("沉淀话术","@话术 把好用的切入点与服务话术存进 #话术。"),
   ],
   "jobs":[("每次拜访转纪要","每次客户拜访后自动转写 + 诉求清单。"),
           ("周度跟进汇总","每周汇总未闭环的跟进项，提醒负责人。"),
           ("话术库维护","持续把有效话术沉淀进库。")],
   "followups":["把诉求按类别打标签，看清客户最关心什么。",
                "给跟进项加提醒，到点自动 @ 负责人。",
                "把高频问题整理成标准答复，客服直接用。"],
   "tips":["从最轻的一步切入（录音转纪要），让一线先尝到甜头再扩。",
           "每条诉求都要变成一个有人负责的跟进项，否则等于没记。",
           "客户敏感信息按需在受限范围内流转，不必全公开。"],
  },
  "content":{
   "sub":"几百份课程与会议纪要要变成公众号文章，还要去重、合并、脱敏、分类、统一管理——人工根本扛不动。",
   "meta":[("角色","1 位主编 + 总编 Agent + 写手/平台 Agent"),("起始频道","#选题 · #写作 · #平台"),("上手","半天"),("产出","数百份素材 → 300+ 篇精稿")],
   "want":"一个内容团队把几百份课程/会议纪要批量改写成公众号文章：总编 Agent 统筹分工、把关质量与去重，写手 Agent 并行成稿，再由另一个 Agent 自建内容管理平台，把稿子集中浏览、编辑、按状态流转、发布。",
   "channels":[("#选题","素材清单、分工、去重边界"),("#写作","并行成稿、逐批过审、合并系列"),("#平台","内容管理平台开发与维护")],
   "agents":[
     ("@总编","统筹与把关","分配任务、逐批审稿、去重、判断弃稿，最后做全局汇总。"),
     ("@写手A","批量成稿","按规则成稿：钩子标题→导语→正文→洞见→来源，事实只取原文。"),
     ("@写手B","批量成稿","与 A 并行，分担另一批素材，避免重复。"),
     ("@平台","内容平台开发","自建文章库：浏览、筛选、在线编辑、搜索、导出、状态流转。"),
   ],
   "briefing":"我们要把几百份纪要批量改写成公众号文章，并集中管理。规则：\n· 先筛（弃稿/同场重复/闭门敏感）再写；写完自检真实字数。\n· 系列课程合并成体系稿，合并不拼接。\n· 含未公开经营数字的稿子要数字脱敏、默认隐藏。\n· 写作与平台两条线并行：写手出稿，平台同步搭好集中管理。",
   "workflow":[
     ("理素材","@总编 把素材清单分批、定去重边界与分工。"),
     ("并行写","@写手A / @写手B 各领一批并行成稿，逐批贴线程。"),
     ("过审合并","@总编 逐批审，系列课程合并成体系稿，敏感稿隔离脱敏。"),
     ("建平台","@平台 同步把内容管理平台搭好：浏览/编辑/搜索/状态。"),
     ("上平台","全局去重后导入平台，按状态浏览、搜索、发布。"),
   ],
   "jobs":[("批量改写","把新增素材持续改写成稿，20 篇一批交付。"),
           ("去重与合并","定期全局去重，系列稿合并成体系稿。"),
           ("平台维护","文章库随新稿更新，状态流转保持准确。")],
   "followups":["按题材/讲者/状态打标签，建可检索的索引。",
                "给敏感稿单独一个仅管理员可见的视图。",
                "把发布排期也搬进平台，选首发、排日程。"],
   "tips":["先筛后写：弃稿、同场重复、闭门敏感先挑出来，省一大半返工。",
           "系列合并要「合并不拼接」——重新成体系，而不是拼接片段。",
           "含未公开数字的稿子一律脱敏、默认隐藏，按场景再定。"],
  },
 },
 "en": {
  "fund": {
   "sub":"One person wants to run a systematic equity fund, but watching the tape, reading filings, computing attribution, and tracking risk is too much for one person — and it has to happen every day, without breaks, with discipline.",
   "meta":[("Setup","1 CIO + 5 Agents"),("Starting channels","#after-close · #research · #risk"),("Ramp-up","One trading day"),("Data","Prices · Filings · Disclosures")],
   "want":"Break a fund's daily research and risk work into a few things that have to happen every day, and hand each to a dedicated Agent: read filings and raise flags, watch options sentiment, compute the day's P&L attribution, weave it all into a CIO daily read, and watch timing and exit signals. You only make the call at the end, while the mechanical discipline is executed by the models and never gets pulled off course by a single day's mood.",
   "channels":[("#after-close","Daily P&L attribution, sector breakdown, the CIO daily read"),("#research","Watchlist updates, earnings review, entry and exit eligibility"),("#risk","Timing status, near-exit monitoring, stress signals")],
   "agents":[
     ("@earnings","Filings & disclosure review","Reads the day's disclosures and filings, raises event flags, and judges whether a name still qualifies — signals only, no automated trading."),
     ("@sentiment","Options sentiment","Refreshes options sentiment daily (implied volatility, put-call ratio, crowding) as an observation-layer signal."),
     ("@attribution","Daily P&L attribution","After the close, breaks the day's P&L down by sector and name to surface the main contributors and detractors."),
     ("@daily-read","CIO daily read","Weaves attribution, sentiment, and risk into a single human-readable daily read, pointing out the status lines that matter most."),
     ("@risk-timing","Timing & exit monitoring","Watches market timing status and near-exit signals on holdings, triggers mechanical stop-loss and take-profit, and leaves a full audit trail."),
   ],
   "briefing":"This is the working channel for a systematic equity fund. Rules:\n· Separate the observation layer from production actions — research and signals are observation; only mechanical stop-loss and take-profit plus my (the CIO's) sign-off are production actions.\n· No single day's move changes the mechanical rules; overheated reversals and rising sentiment all go to the observation layer first.\n· After every close, produce: attribution, then the daily read, then risk status. Each week, produce production candidates for me to sign off before entry.",
   "workflow":[
     ("Post-close attribution","After the close, @attribution computes the day's P&L breakdown by sector and name."),
     ("Information layer","@earnings and @sentiment each refresh the day's disclosure flags and sentiment metrics."),
     ("Weave the daily read","@daily-read pulls those three streams into a CIO daily read and points out the status lines to watch."),
     ("Watch the risk lines","@risk-timing updates timing status and near-exit monitoring; when a mechanical rule fires, it executes and logs it."),
     ("You make the call","You read the daily read and decide; entries come only from the weekly production candidates plus your sign-off."),
   ],
   "jobs":[("Daily post-close attribution","After every close, produce P&L attribution plus the daily read automatically."),
           ("Daily sentiment and flags","Refresh options sentiment and disclosure flags daily into the observation layer."),
           ("Weekly production candidates","Each week, surface candidate names awaiting the CIO's sign-off to enter.")],
   "followups":["Add an event-flag Agent to watch for insider selling, regulatory inquiries, and unusual disclosures.",
                "Add a stress-test Agent that runs scenarios like a five-percent drawdown against the portfolio.",
                "File the daily read automatically into a searchable research library."],
   "tips":["Keep observation and action separate — most research should stay in the observation layer, so a day's noise never triggers a trade.",
           "Let the models execute the mechanical discipline with a full audit trail; people only sign off on the weekly candidates and the key calls.",
           "Sensitive real holdings and figures don't need to sit in channel titles; share them within a restricted scope as needed."],
  },
  "platform":{
   "sub":"A fund needs its own portfolio-management platform — health, compliance, rebalancing, provenance, all of it — but it has no traditional engineering team.",
   "meta":[("Setup","1 lead + 5 Agents"),("Starting channels","#platform · #data-contract · #compliance"),("Ramp-up","A few days"),("Integration","Strategy-engine API")],
   "want":"Have a crew of Agents build and run the portfolio-management platform together: first lock down the data contract, then build the pages and components, run them past the compliance lines, deploy, and finally verify the live site item by item. Everything follows one design system, and risk is shown without jarring red-up-green-down coloring.",
   "channels":[("#platform","Pages, components, deployment, and release"),("#data-contract","Schema fields, contract checks, drift prevention"),("#compliance","Compliance lines and the gate before connecting real data")],
   "agents":[
     ("@frontend","Pages & components","Builds health cards, compliance lights, rebalancing tables, and source-provenance bands per the design system."),
     ("@contract","Data-contract gatekeeper","Defines and validates the schema, and errors at load time the moment the contract drifts."),
     ("@compliance","Compliance review","Watches the compliance lines: demo data must be labeled, past performance carries disclaimers, and risk colors avoid red-green."),
     ("@release","Release verification","After each deploy, verifies the live build against expectations item by item, using scripts and screenshots."),
     ("@design","Design-system alignment","Keeps components, colors, and copy on the shared design system instead of hand-coded values."),
   ],
   "briefing":"We're building and running a portfolio-management platform. Rules:\n· Everything starts from the data contract — lock the schema first, then wire up the frontend.\n· Don't show risk with red-up-green-down; use the design system's semantic colors (cypress green, muted gold, muted red).\n· Before connecting real holdings, the gate must pass: demo data off and permission lines in place.\n· Verify every release on the live site item by item, not by eyeballing it.",
   "workflow":[
     ("Lock the contract","@contract pins down the fields and schema for this version and adds the checks."),
     ("Build","@frontend builds the pages and components per the design system, wired to the contract's data."),
     ("Compliance review","@compliance runs the lines: demo-data labels, disclaimers, compliant risk colors."),
     ("Deploy","Ship the changes with a traceable version and commit history."),
     ("Verify live","@release verifies the live site item by item and fixes anything that's off."),
   ],
   "jobs":[("Contract checks","Run contract checks before and after each build to prevent schema drift."),
           ("Smoke tests","Auto-smoke the critical paths: auth gate, theming, and APIs all pass."),
           ("Release verification","After each deploy, verify the live version number and key metric distributions.")],
   "followups":["Turn the must-pass checklist before connecting real data into a fixed gate that runs automatically on every release.",
                "Add export to the rebalancing table, with source annotations, to make manual review easier.",
                "Distill the design-system components into a reusable library so new pages just snap together."],
   "tips":["Contract first: failing at load time the moment the schema drifts beats discovering it after release.",
           "Show risk in semantic colors, not red-up-green-down — that's a brand line.",
           "Always pass the gate before connecting real data: demo data off, permissions tightened by default."],
  },
  "comic":{
   "sub":"Turning a script into a serialized comic — dozens of pages per chapter, with characters that stay consistent across spreads — is more than one person can draw.",
   "meta":[("Setup","1 lead artist + 4 Agents"),("Starting channels","#script · #panels · #render"),("Ramp-up","Half a day"),("Output","Multi-chapter run · ~28 pages each")],
   "want":"One person sets the direction and the script, and the Agent team turns it into a serialized comic: read the script and lay out panels, lock character consistency, render in parallel, proof, and publish. About 28 pages per chapter, with characters keeping the same face across spreads.",
   "channels":[("#script","Script, chapter pacing, and key beats"),("#panels","Page-by-page visual beats and character staging"),("#render","Parallel rendering, consistency proofing, publishing")],
   "agents":[
     ("@panels","Paneling","Reads the script, sets each page's visual beats and character entrances, and writes the panel sheet."),
     ("@character","Character consistency","Manages character profiles and consistency; well-known characters are summoned by name, original characters get their profiles locked."),
     ("@render-a","Parallel rendering (forward)","Renders front to back, following the panel sheet."),
     ("@render-b","Parallel rendering (reverse)","Renders back to front, in parallel with A, meeting in the middle."),
     ("@publish","Packaging & publishing","Packages the finished pages, publishes by chapter, and notifies only after every page checks out."),
   ],
   "briefing":"We're turning a script into a serialized comic. Rules:\n· About 28 pages per chapter; produce the panel sheet before rendering.\n· Consistency first: summon well-known characters by name without forcing constraints; lock profiles for original characters.\n· The two rendering Agents work forward and reverse in parallel, then proof consistency together at the end.\n· Publish the full chapter and notify me only once every link is reachable.",
   "workflow":[
     ("Read the script","@panels reads this chapter's script, picking up from the last chapter's ending."),
     ("Lay out panels","Write a panel sheet of about 28 pages: visual beats plus character staging."),
     ("Render in parallel","@render-a goes forward and @render-b goes reverse, working at the same time."),
     ("Proof consistency","@character proofs faces and outfits for cross-spread consistency, re-rendering where needed."),
     ("Publish","@publish packages and ships, verifies every page is reachable, and notifies the lead artist."),
   ],
   "jobs":[("Panel sheet per chapter","Produce a panel sheet at the start of every new chapter."),
           ("Parallel rendering","Render about 28 pages per chapter on two parallel tracks."),
           ("Publish verification","After each chapter ships, verify every page is reachable and old versions are cleared.")],
   "followups":["Turn the publishing flow into a single command, reusable by swapping the chapter parameters.",
                "Keep a character profile card per chapter, and decide how to lock each new character as it appears.",
                "Make cross-spread consistency proofing a fixed checklist item."],
   "tips":["Summoning well-known characters by name is often more accurate than forcing constraints.",
           "Lock original characters' profiles and reuse them across spreads, so you don't get a new face on every page.",
           "Running forward and reverse in parallel compresses a chapter's render time to the minimum."],
  },
  "app":{
   "sub":"A founder wants to build and run an app — product, backend, servers, and store-release issues all need handling — but there's no dedicated team.",
   "meta":[("Setup","1 founder + 4 Agents"),("Starting channels","#product · #backend · #infra"),("Ramp-up","Same day"),("Scope","Frontend · Backend · Infrastructure")],
   "want":"Hand the end-to-end delivery of a consumer AI-recognition app to a team of Agents: product and frontend, backend, server migration and networking, third-party login, photo processing, the upload path, and dependency fixes. You raise issues whenever they come up, and the team locates the cause, fixes it, verifies end to end, and wraps up.",
   "channels":[("#product","Product experience, frontend logic, release issues"),("#backend","APIs, data, dependencies, and services"),("#infra","Server migration, networking, deployment, and operations")],
   "agents":[
     ("@product","Product & frontend","Watches frontend logic and release-experience issues, locating and fixing them."),
     ("@backend","Backend & APIs","Handles APIs, data, and server-side dependencies."),
     ("@infra","Migration & operations","Server migration, networking, deployment, origin-pull, and bandwidth issues."),
     ("@verify","End-to-end verification","After each fix, runs the flow end to end to confirm the issue is really gone."),
   ],
   "briefing":"We're building and running a consumer app end to end. Rules:\n· I'll report symptoms in the channel any time (which step, what error); you find the root cause, make the smallest change, and verify end to end.\n· For migration issues, check dependencies, networking, and origin-pull together — don't just patch the surface.\n· No fix is done until it passes one real-device or end-to-end verification.",
   "workflow":[
     ("Report the symptom","You describe the issue in the channel: which step, what you're seeing."),
     ("Find the root cause","The relevant Agent checks logs and reproduces it to find the cause (often a missing dependency, networking, or the upload path after migration)."),
     ("Smallest change","Propose the minimal fix to avoid breaking something else."),
     ("Verify end to end","@verify runs the full flow, including login and upload, to confirm it's fixed."),
     ("Wrap up","Close the task, report back in the channel, and note the lesson."),
   ],
   "jobs":[("Health checks","Regularly verify each service is up and the critical paths work."),
           ("Migration verification","After a migration, verify dependencies, networking, and origin-pull item by item."),
           ("Issue closure","Track every reported issue through to a passing end-to-end verification before closing it.")],
   "followups":["Write the common troubleshooting steps into a reusable checklist.",
                "Add monitoring on the critical paths so issues surface on their own instead of users finding them first.",
                "Turn the manual release and compliance steps into a step-by-step guide."],
   "tips":["Pull origin traffic over HTTPS; don't use plaintext with an unregistered host, or you'll get an injected interstitial.",
           "Right after a migration, check dependencies first: one missing library breaks the whole path.",
           "Every fix needs one end-to-end verification — don't stop at it should be fine."],
  },
  "sales":{
   "sub":"Frontline sales meet customers every day, but recordings, notes, customer needs, and follow-up scripts are scattered, so follow-ups slip.",
   "meta":[("Setup","Sales team + a support Agent"),("Starting channels","#visits · #follow-ups · #playbooks"),("Ramp-up","Same day"),("Stage","Rolling out gradually")],
   "want":"Turn customer conversations into something you can follow up on: sales drops a visit recording into the channel, and Agents transcribe it, distill what the customer needs, assemble the talking points and service scripts, and lay out the follow-ups. Let the frontline start with the small win of turning meetings into notes, then bring sales and support into Agent collaboration step by step.",
   "channels":[("#visits","Visit recordings, transcribed notes, customer needs"),("#follow-ups","Follow-up items, owners, next steps"),("#playbooks","Talking points and service scripts")],
   "agents":[
     ("@transcribe","Recording transcription","Turns visit recordings into structured written notes."),
     ("@needs","Needs analysis","Distills the customer's real needs and concerns from the notes."),
     ("@follow-up","Follow-up orchestration","Turns each need into a follow-up item with an owner and a due date."),
     ("@playbook","Playbook curation","Organizes talking points and service scripts by scenario for the frontline to reuse."),
   ],
   "briefing":"We're turning customer conversations into actionable follow-ups. Rules:\n· Start with the lightest step: turn visit recordings into notes plus a needs list.\n· Every need becomes a follow-up item with an owner and a next step.\n· Curate playbooks by scenario so they're reusable, and roll them out to more frontline colleagues over time.",
   "workflow":[
     ("Drop the recording","Sales posts the visit recording or link into #visits."),
     ("Transcribe","@transcribe turns it into structured notes."),
     ("Distill the needs","@needs lays out the customer's needs and concerns."),
     ("Lay out follow-ups","@follow-up turns them into items with owners and due dates."),
     ("Curate playbooks","@playbook saves the talking points and scripts that work into #playbooks."),
   ],
   "jobs":[("Notes per visit","After every customer visit, auto-transcribe and produce a needs list."),
           ("Weekly follow-up roundup","Each week, round up open follow-ups and remind the owners."),
           ("Playbook upkeep","Keep adding effective scripts to the library.")],
   "followups":["Tag needs by category to see clearly what customers care about most.",
                "Add reminders to follow-ups so the owner gets an @ mention when one comes due.",
                "Turn frequent questions into standard responses the support team can use directly."],
   "tips":["Start with the lightest step (recordings to notes) so the frontline gets an early win before you expand.",
           "Every need has to become a follow-up item with an owner, or it might as well not be recorded.",
           "Share sensitive customer information within a restricted scope as needed, not everywhere."],
  },
  "content":{
   "sub":"Hundreds of course and meeting notes need to become published articles — deduplicated, merged, redacted, categorized, and managed in one place — which is more than people can handle by hand.",
   "meta":[("Setup","1 editor + an editor-in-chief Agent + writer/platform Agents"),("Starting channels","#topics · #writing · #platform"),("Ramp-up","Half a day"),("Output","Hundreds of sources → 300+ finished pieces")],
   "want":"A content team rewrites hundreds of course and meeting notes into published articles in bulk: an editor-in-chief Agent coordinates the work, gatekeeps quality, and deduplicates; writer Agents draft in parallel; and a separate Agent builds a content-management platform to browse, edit, move by status, and publish it all in one place.",
   "channels":[("#topics","Source list, assignments, dedup boundaries"),("#writing","Parallel drafting, batch review, series merging"),("#platform","Content-platform development and upkeep")],
   "agents":[
     ("@editor","Coordination & gatekeeping","Assigns work, reviews drafts in batches, deduplicates, decides what to drop, and does the final roundup."),
     ("@writer-a","Bulk drafting","Drafts to the format: hook headline, intro, body, insight, sources — facts taken only from the source."),
     ("@writer-b","Bulk drafting","Works in parallel with A on a separate batch of sources to avoid overlap."),
     ("@platform","Content-platform build","Builds the article library in-house: browse, filter, inline edit, search, export, and status flow."),
   ],
   "briefing":"We're rewriting hundreds of notes into published articles in bulk and managing them in one place. Rules:\n· Filter first (drop weak ones, same-session duplicates, closed-door sensitive), then write; self-check the real word count after drafting.\n· Merge course series into coherent pieces — merge, don't stitch.\n· Drafts with undisclosed business figures get redacted and hidden by default.\n· Run the writing and platform tracks in parallel: writers produce drafts while the platform stands up centralized management.",
   "workflow":[
     ("Sort the sources","@editor batches the source list and sets dedup boundaries and assignments."),
     ("Write in parallel","@writer-a and @writer-b each take a batch and draft in parallel, posting to the thread by batch."),
     ("Review and merge","@editor reviews by batch, merges course series into coherent pieces, and isolates and redacts sensitive drafts."),
     ("Build the platform","@platform stands up the content-management platform in parallel: browse, edit, search, status."),
     ("Onto the platform","After a global dedup, import into the platform to browse, search, and publish by status."),
   ],
   "jobs":[("Bulk rewriting","Keep rewriting new sources into drafts, delivered in batches of 20."),
           ("Dedup and merge","Run a global dedup periodically and merge series into coherent pieces."),
           ("Platform upkeep","Keep the article library updated with new drafts and the status flow accurate.")],
   "followups":["Tag by topic, speaker, and status to build a searchable index.",
                "Give sensitive drafts a separate, admin-only view.",
                "Move the publishing schedule into the platform too — pick the first release and plan the calendar."],
   "tips":["Filter before you write: pulling out weak drafts, same-session duplicates, and closed-door sensitive material upfront saves most of the rework.",
           "Merging a series means merge, not stitch — rebuild it into a coherent piece rather than splicing fragments.",
           "Drafts with undisclosed figures are always redacted and hidden by default, then decided case by case."],
  },
 },
}


def build_detail(lang, slug):
    t = T[lang]
    c = next(x for x in CASES[lang] if x[4] == slug)
    d = DETAILS[lang][slug]
    ind, title, _desc, _tags, _ = c
    other = "en" if lang == "zh" else "zh"
    toggle = url(other, f"case-{slug}.html")

    meta = "".join(f'<div class="m"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in d["meta"])
    chan_desc = "".join(f'<div class="dstep chan"><div class="hh">{n}</div><p>{p}</p></div>' for n, p in d["channels"])
    agents = "".join(f"""<div class="agent"><div><div class="h">{h}</div><div class="r">{r}</div><div class="d">{ds}</div></div></div>""" for h, r, ds in d["agents"])
    wf = "".join(f'<div class="dstep"><div class="num">{i+1:02d}</div><div><h3>{ti}</h3><p>{p}</p></div></div>' for i, (ti, p) in enumerate(d["workflow"]))
    jobs = "".join(f'<div class="dstep"><div class="num">↻</div><div><h3>{ti}</h3><p>{p}</p></div></div>' for ti, p in d["jobs"])
    fus = "".join(f'<div class="tip">{x}</div>' for x in d["followups"])
    tips = "".join(f'<div class="tip">{x}</div>' for x in d["tips"])
    related = [x[4] for x in CASES[lang] if x[4] != slug][:3]
    rel = "".join(case_card(lang, *next(y for y in CASES[lang] if y[4] == s)) for s in related)

    D = [head(lang, f"{title}{t['d_title_suffix']}",
              f"{t['d_desc_prefix']}{title}. {d['sub']}",
              f'<!-- @dsCard group="{"Syfo 官网" if lang=="zh" else "Syfo Website"}" title="{t["d_card_prefix"]}{ind}" -->',
              toggle)]
    D.append(nav(lang, f"case-{slug}.html", "cases"))
    D.append(f"""<div class="wrap"><div class="crumb"><a href="{url(lang, "cases.html")}">{t["d_back"]}</a></div>
 <section class="dhero"><div class="ind">{ind}</div>
   <h1>{title}</h1><p class="sub">{d['sub']}</p>
   <div class="dmeta">{meta}</div>
 </section>
 <section class="dsec"><div class="lab">{t["d_lab_want"]}</div><h2>{t["d_h2_want"]}</h2>
   <div class="body">{d['want']}</div></section>
 <section class="dsec"><div class="lab">{t["d_lab_chan"]}</div><h2>{t["d_h2_chan"]}</h2>
   <div class="dsteps">{chan_desc}</div></section>
 <section class="dsec"><div class="lab">{t["d_lab_agents"]}</div><h2>{t["d_h2_agents"]}</h2>
   <div class="agents">{agents}</div></section>
 <section class="dsec"><div class="lab">{t["d_lab_brief"]}</div><h2>{t["d_h2_brief"]}</h2>
   <div class="brief-box">{d['briefing']}</div></section>
 <section class="dsec"><div class="lab">{t["d_lab_wf"]}</div><h2>{t["d_h2_wf"]}</h2>
   <div class="dsteps">{wf}</div></section>
 <section class="dsec"><div class="lab">{t["d_lab_jobs"]}</div><h2>{t["d_h2_jobs"]}</h2>
   <div class="dsteps">{jobs}</div></section>
 <section class="dsec"><div class="lab">{t["d_lab_fu"]}</div><h2>{t["d_h2_fu"]}</h2>
   <div class="tips">{fus}</div></section>
 <section class="dsec"><div class="lab">{t["d_lab_tips"]}</div><h2>{t["d_h2_tips"]}</h2>
   <div class="tips">{tips}</div></section>
</div>
<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">{t["d_close_eyebrow"]}</span>
 <h2>{t["d_close_h2"]}</h2>
 <div class="cta"><a class="btn btn-primary" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="{url(lang, "cases.html")}">{t["d_close_cta2"]}</a></div></div></section>
<div class="band" style="background:var(--bg-sunken);border-top:1px solid var(--border-1)"><section><div class="wrap">
 <div class="lab" style="font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)">{t["d_related"]}</div>
 <div class="related">{rel}</div>
</div></section></div>""")
    D.append(footer(lang))
    write(lang, f"case-{slug}.html", D)


# ── 载入 ja / es 翻译 (由 i18n/<lang>.json 提供，zh/en 保持内联) ──
for _lg in ("ja", "es", "vi"):
    _d = json.load(open(os.path.join(HERE, "i18n", f"{_lg}.json"), encoding="utf-8"))
    T[_lg] = _d["T"]; CASES[_lg] = _d["CASES"]; SCENES[_lg] = _d["SCENES"]
    STEPS[_lg] = _d["STEPS"]; RELAY[_lg] = _d["RELAY"]
    HOW_STEPS[_lg] = _d["HOW_STEPS"]; DETAILS[_lg] = _d["DETAILS"]


# ════════════════════════════════════════════ build
for _d in DIRS.values():
    os.makedirs(_d, exist_ok=True)
for lang in LANGS:
    build_home(lang)
    build_cases(lang)
    build_how(lang)
    for slug in [c[4] for c in CASES[lang]]:
        build_detail(lang, slug)

print("wrote " + " + ".join(PREFIX[l] for l in LANGS) + ": index.html + cases.html + how.html + 6 case detail pages each")
