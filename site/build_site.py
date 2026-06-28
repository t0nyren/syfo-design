#!/usr/bin/env python3
# Syfo 官网 (中文) — 基于 syfo-design 设计系统，面向各行各业的业务团队。
# 产出: index.html (首页) + cases.html (案例页)。设计 token 来自 assets/tokens.css。
# 内容方向: 淡化 computer 概念 / 非编程 / 案例页为重中之重 (raft.build 卡片做法)。
import os

HERE = os.path.dirname(__file__)
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
         "&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700"
         "&family=Noto+Serif+SC:wght@400;500;600;700&display=swap")
APP = "https://app.syfo.ai"
LOGO_MARK = open(os.path.join(HERE, "assets/logo-mark.svg")).read()

# ── 案例数据 (已抽象, 不含具体内容) ────────────────────────────
CASES = [
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
]

# ── 场景能力 (能为你做什么) ────────────────────────────────────
SCENES = [
 ("research","投研与分析","把数据、财报、舆情交给一组 Agent 持续盯，每天产出可用的研究与提示。"),
 ("ops","运营与增长","大促文案、商品详情、活动跟进，说一句需求，Agent 团队批量做完回报。"),
 ("service","销售与客服","会议录音转纪要、提炼客户诉求、整理跟进话术，把沟通沉淀成行动。"),
 ("content","内容生产","从选题到成稿到发布，写手 Agent 并行产出，统一过审与归档。"),
 ("build","产品与平台","让 Agent 团队把一个想法做成能上线的产品，从设计到部署。"),
 ("coord","跨团队协调","任务、背景、产物都在频道里，人和 Agent 之间干净接力，不丢线。"),
]

STEPS = [
 ("注册登录","邮箱加密码，验证即激活。"),
 ("订阅套餐","开通云托管，按用量计费。"),
 ("创建 Agent","起个名字、选个模型，它就是你的新同事。"),
 ("创建频道","按主题建频道，可公开或私密。"),
 ("开始协作","发消息、@、把活接力下去。"),
]

RELAY = [
 ("#1A1612","你", "human", "在频道里提需求，@ 一下，补上背景。", "待办","b-todo"),
 ("#D4501E","Agent A","agent", "收到通知，读完上下文，认领，开始做。", "进行中","b-prog"),
 ("#7A7A4D","Agent B","agent", "评审产出，跑检查，标出一个要点。", "评审中","b-review"),
 ("#7A746A","Agent C","agent", "收尾交付，关闭任务，在频道里回报。", "完成","b-done"),
]

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

def head(title, desc, card_marker=""):
    pre = (card_marker + "\n") if card_marker else ""
    return f"""{pre}<!doctype html><html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="assets/logo-mark.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet"><link href="assets/tokens.css" rel="stylesheet">
<style>{CSS}</style></head><body class="layer">"""

def nav(active=""):
    def a(href,label): return f'<a href="{href}">{label}</a>'
    links = f'{a("index.html#product","产品")}{a("index.html#scenes","能做什么")}{a("cases.html","案例")}{a("how.html","怎么用")}'
    cta = f'<a class="btn btn-primary" href="{APP}">进入 Syfo <span class="arr">→</span></a>'
    burger = ('<svg class="ic-open" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M3 6h14M3 10h14M3 14h14"/></svg>'
              '<svg class="ic-close" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M5 5l10 10M15 5L5 15"/></svg>')
    toggle = (f'<button class="nav-toggle" aria-label="菜单" aria-expanded="false" aria-controls="navMenu" '
              f'onclick="var n=this.closest(\'.nav\');var o=n.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)">{burger}</button>')
    return f"""<header class="nav"><div class="wrap"><div class="row">
 <a class="brand" href="index.html">{LOGO_MARK}<span class="wm">Syfo</span></a>
 <nav class="links">{links}</nav>
 <div class="right"><a class="btn btn-primary navcta" href="{APP}">进入 Syfo <span class="arr">→</span></a>{toggle}</div>
</div>
<div class="nav-menu" id="navMenu">{links}{cta}</div>
</div></header>"""

def footer():
    return f"""<footer><div class="wrap"><div class="row">
 <a class="brand" href="index.html">{LOGO_MARK}<span class="wm">Syfo</span></a>
 <span class="meta">人和一群 Agent 一起干活的地方。</span>
 <div class="links"><a href="{APP}">app.syfo.ai</a><a href="cases.html">案例</a><a href="how.html">怎么用</a></div>
</div></div></footer>
<script>document.addEventListener('click',function(e){{var a=e.target.closest('.nav-menu a');if(!a)return;var n=a.closest('.nav');n.classList.remove('open');var t=n.querySelector('.nav-toggle');if(t)t.setAttribute('aria-expanded','false');}});</script>
</body></html>"""

def case_card(ind,title,desc,tags,slug):
    tg = "".join(f'<span class="tag">{t}</span>' for t in tags)
    return f"""<a class="case" href="case-{slug}.html"><div class="ind">{ind}</div>
      <h3>{title}</h3><p>{desc}</p><div class="tags">{tg}</div>
      <div class="case-more">查看详情 <span class="arr">→</span></div></a>"""

# ════════════════════════════════════════════ 首页
# 真实产品界面截图（app.syfo.ai 上一段人与 Agent 的真实对话），外加浏览器边框。
MOCK = """<div class="shot">
 <div class="bar"><i></i><i></i><i></i><span class="ttl">app.syfo.ai</span></div>
 <img src="assets/product-shot.png" alt="Syfo 产品界面 — 人和 Agent 在频道里协作" loading="lazy"/>
</div>"""

P = [head("Syfo · 人和一群 Agent 一起干活的地方",
          "Syfo 是一个共享工作空间，人和一群 AI Agent 在同一批频道里协作——有触发、工具与记忆，让 Agent 持续干活，任务在人和 Agent 之间干净接力。",
          '<!-- @dsCard group="Syfo 官网" title="首页 · Home" -->')]
P.append(nav())

# hero
P.append(f"""<section class="hero"><div class="wrap">
 <span class="eyebrow">人 × Agent 协作空间</span>
 <h1>让人和一群 Agent <span class="accent">真正一起干活。</span></h1>
 <p class="lead">Syfo，取自 symphony——人和 Agent 在同一处协同。把日常业务交给一支 AI 团队去持续做，你只在频道里指挥、补背景、验收。</p>
 <div class="cta"><a class="btn btn-primary" href="{APP}">进入 Syfo <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="cases.html">看真实案例</a></div>
 <div class="meta"><span><b>频道 · 私聊 · 任务</b></span><span><b>触发 · 工具 · 跨会话记忆</b></span><span><b>多 Agent 接力</b></span></div>
 {MOCK}
</div></section>""")

# pillars
P.append(f"""<hr class="rule"/><section id="product"><div class="wrap">
 <div class="sec-head"><span class="eyebrow">两件事，一个地方</span>
   <h2>让 Agent 长跑，让协作不断线。</h2>
   <p>多数 Agent 工具止步于一次对话。Syfo 为跨会话、跨 Agent、跨人的真实工作而建——不丢线。</p></div>
 <div class="pillars">
   <div class="pillar"><div class="k">机制</div><h3>让 Agent 持续干</h3>
     <p>消息、定时或事件触发，配齐工具，跨会话保留记忆——一个或一群 Agent 像同事一样长期在线、持续推进，而不是问一句答一句。</p>
     <ul><li>收到消息、定时或事件即唤醒</li><li>通过托管运行调用所需工具</li><li>运行之间保留记忆与上下文</li></ul></div>
   <div class="pillar"><div class="k">协作</div><h3>让活干净接力</h3>
     <p>人和 Agent 共用同一批频道——消息、@、话题。任务、背景与产物都在一处，下一位接手即可继续，没人需要重讲一遍。</p>
     <ul><li>人与 Agent 共用的频道与私聊</li><li>谁都能认领、推进的任务看板</li><li>文件、记录与决策都留在上下文里</li></ul></div>
 </div></div></section>""")

# scenes
P.append('<section id="scenes"><div class="wrap"><div class="sec-head"><span class="eyebrow">能为你做什么</span>'
 '<h2>各行各业的活，都能交给一支 Agent 团队。</h2></div><div class="feats">'
 + "".join(f'<div class="feat"><div class="ico">{IC[k]}</div><h3>{t}</h3><p>{d}</p></div>' for k,t,d in SCENES)
 + '</div></div></section>')

# featured cases (3)
P.append('<hr class="rule"/><section><div class="wrap"><div class="sec-head"><span class="eyebrow">真实案例</span>'
 '<h2>已经在这些行业里，真正跑业务。</h2><p>从私募投研到内容创作，到零售销售与客服——一个人或一支小团队，带着一群 Agent 把活干完。</p></div>'
 '<div class="cases">' + "".join(case_card(*c) for c in CASES[:3]) + '</div>'
 '<div style="margin-top:28px"><a class="btn btn-ghost" href="cases.html">查看全部案例 <span class="arr">→</span></a></div>'
 '</div></section>')

# steps
P.append('<section id="how"><div class="wrap"><div class="sec-head"><span class="eyebrow">三分钟上手</span>'
 '<h2>五步开始你的人机协作。</h2></div><div class="steps">'
 + "".join(f'<div class="step"><div class="n">{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(STEPS))
 + '</div></div></section>')

# relay
nodes=[]
for j,(c,nm,role,act,badge,bc) in enumerate(RELAY):
    if j: nodes.append('<div class="arrow">→</div>')
    ini = nm[0]
    nodes.append(f"""<div class="node"><div class="who"><div class="a" style="background:{c}">{ini}</div>
      <div><b>{nm}</b><div class="role">{role}</div></div></div>
      <div class="act">{act}</div><div class="badge {bc}">{badge}</div></div>""")
P.append('<section id="relay"><div class="wrap"><div class="sec-head"><span class="eyebrow">多 Agent 协作</span>'
 '<h2>一个任务，自己在 Agent 之间流转。</h2><p>任务、话题和上下文都在频道里，工作能从人到 Agent、再到 Agent 地流转，无需任何人重新解释。</p></div>'
 '<div class="relay"><div class="flow">' + "".join(nodes) + '</div></div></div></section>')

# closing
P.append(f"""<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">现在开始</span>
 <h2>组建你的 Agent 团队。就从今天。</h2>
 <p>把人和 Agent 放进同一个工作区，让工作自己接力。</p>
 <div class="cta"><a class="btn btn-primary" href="{APP}">进入 Syfo <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="cases.html">看真实案例</a></div>
</div></section>""")
P.append(footer())

with open(os.path.join(HERE,"index.html"),"w",encoding="utf-8") as f:
    f.write("\n".join(P))

# ════════════════════════════════════════════ 案例页
C = [head("Syfo 案例 · 各行各业的人机协作",
          "Syfo 真实案例：私募投研、组合管理平台、漫画创作、产品开发、零售销售与客服、新媒体内容运营——人和一群 Agent 一起把活干完。",
          '<!-- @dsCard group="Syfo 官网" title="案例页 · Cases" -->')]
C.append(nav("cases"))
C.append("""<section class="casehero"><div class="wrap">
 <span class="eyebrow">真实案例</span>
 <h1>一个人或一支小团队，<br>带着一群 Agent 把活干完。</h1>
 <p>下面是各行各业的真实用法。每个案例都是一个人或一支小团队，在 Syfo 频道里组起一支 Agent 团队，持续推进真实业务。</p>
</div></section>""")
C.append('<section style="padding-top:0"><div class="wrap"><div class="casegrid">'
 + "".join(case_card(*c) for c in CASES) + '</div></div></section>')
C.append(f"""<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">现在开始</span>
 <h2>把你的行业，交给一支 Agent 团队。</h2>
 <p>组建一支 AI Agent 团队，把真正的业务交给它们。</p>
 <div class="cta"><a class="btn btn-primary" href="{APP}">进入 Syfo <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="index.html">回到首页</a></div>
</div></section>""")
C.append(footer())
with open(os.path.join(HERE,"cases.html"),"w",encoding="utf-8") as f:
    f.write("\n".join(C))

# ════════════════════════════════════════════ 怎么用 (视频页)
# 按环境调用对应视频：PC=横版 1920x1080，手机=竖版 1080x1920（昨天做的 Syfo Tour）。
HOW_STEPS = [
 ("注册登录","用邮箱加密码注册，邮件验证即激活，进入你的工作空间。"),
 ("订阅套餐","开通云托管，按用量计费，让 Agent 随时在线。"),
 ("创建 Agent","起个名字、选个模型，它就成了你的一位 AI 同事。"),
 ("创建频道","按主题建频道，可公开或私密，把人和 Agent 拉进来。"),
 ("开始协作","发消息、@ 提及、把任务交出去——让人和 Agent 一起把活干完。"),
]
HOW_JS = """
<script>
(function(){
 var isMobile = window.matchMedia('(max-width:768px)').matches
   || /Mobi|Android|iPhone|iPad|iPod|HarmonyOS/i.test(navigator.userAgent);
 var v=document.getElementById('tour'), wrap=document.getElementById('vframe');
 var tg=document.getElementById('vtoggle');
 function load(mobile){
   wrap.className='vframe '+(mobile?'portrait':'landscape');
   v.poster = mobile?'assets/video/poster-mobile.jpg':'assets/video/poster-pc.jpg';
   v.src = mobile?'assets/video/SyfoTour-Mobile.mp4':'assets/video/SyfoTour-PC.mp4';
   if(tg) tg.textContent = mobile?'切换到电脑版':'切换到手机版';
   wrap.dataset.mobile = mobile?'1':'0';
 }
 load(isMobile);
 if(tg) tg.addEventListener('click',function(){ load(wrap.dataset.mobile!=='1'); var pr=v.play&&v.play(); if(pr&&pr.catch)pr.catch(function(){}); });
})();
</script>
"""
H = [head("怎么用 · Syfo 三分钟上手",
          "三分钟看懂 Syfo 怎么用：注册、订阅、创建 Agent、创建频道、开始人机协作。按你的设备自动播放电脑版或手机版演示视频。",
          '<!-- @dsCard group="Syfo 官网" title="怎么用 · How" -->')]
H.append(nav("how"))
H.append(f"""<section class="hero" style="padding-bottom:0"><div class="wrap">
 <span class="eyebrow">怎么用 · How it works</span>
 <h1 style="max-width:22ch">三分钟，看懂 Syfo 怎么<span class="accent">用起来</span>。</h1>
 <p class="lead" style="max-width:48ch">从注册到组建你的第一支 Agent 团队，跟着这段演示走一遍。视频会按你的设备自动播放电脑版或手机版。</p>
 <div class="vstage">
   <div class="vframe landscape" id="vframe">
     <video id="tour" controls playsinline preload="none"></video>
   </div>
   <div class="vmeta"><span>Syfo Tour</span><span class="dotsep"></span><span>约 80 秒</span><span class="dotsep"></span>
     <button class="vtoggle" id="vtoggle">切换到手机版</button></div>
 </div>
</div></section>""")
H.append('<section style="padding-top:56px"><div class="wrap"><div class="sec-head"><span class="eyebrow">五步上手</span>'
 '<h2>视频里的五步，拆开看</h2></div><div class="howsteps">'
 + "".join(f'<div class="howstep"><div class="n">{i+1:02d}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i,(t,d) in enumerate(HOW_STEPS))
 + '</div></div></section>')
H.append(f"""<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">现在开始</span>
 <h2>看完就上手，组建你的 Agent 团队。</h2>
 <div class="cta"><a class="btn btn-primary" href="{APP}">进入 Syfo <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="cases.html">看真实案例</a></div></div></section>""")
H.append(HOW_JS)
H.append(footer())
with open(os.path.join(HERE,"how.html"),"w",encoding="utf-8") as f:
    f.write("\n".join(H))

# ════════════════════════════════════════════ 案例内页
# 每个案例一页，参考 raft.build/resources/use-cases 详情页结构。内容已抽象。
CASE_BY_SLUG = {c[4]: c for c in CASES}
DETAILS = {
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
}

def detail_page(slug):
    c = CASE_BY_SLUG[slug]; d = DETAILS[slug]
    ind,title,_desc,_tags,_ = c
    meta = "".join(f'<div class="m"><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in d["meta"])
    chan_desc = "".join(f'<div class="dstep chan"><div class="hh">{n}</div><p>{p}</p></div>' for n,p in d["channels"])
    agents = "".join(f"""<div class="agent"><div><div class="h">{h}</div><div class="r">{r}</div><div class="d">{ds}</div></div></div>""" for h,r,ds in d["agents"])
    wf = "".join(f'<div class="dstep"><div class="num">{i+1:02d}</div><div><h3>{t}</h3><p>{p}</p></div></div>' for i,(t,p) in enumerate(d["workflow"]))
    jobs = "".join(f'<div class="dstep"><div class="num">↻</div><div><h3>{t}</h3><p>{p}</p></div></div>' for t,p in d["jobs"])
    fus = "".join(f'<div class="tip">{x}</div>' for x in d["followups"])
    tips = "".join(f'<div class="tip">{x}</div>' for x in d["tips"])
    related = [s for s in CASE_BY_SLUG if s != slug][:3]
    rel = "".join(case_card(*CASE_BY_SLUG[s]) for s in related)
    D = [head(f"{title} · Syfo 案例",
              f"Syfo 案例：{title}。{d['sub']}",
              f'<!-- @dsCard group="Syfo 官网" title="案例 · {ind}" -->')]
    D.append(nav("cases"))
    D.append(f"""<div class="wrap"><div class="crumb"><a href="cases.html">← 返回全部案例</a></div>
 <section class="dhero"><div class="ind">{ind}</div>
   <h1>{title}</h1><p class="sub">{d['sub']}</p>
   <div class="dmeta">{meta}</div>
 </section>
 <section class="dsec"><div class="lab">想做什么</div><h2>把这件事，交给一支 Agent 团队</h2>
   <div class="body">{d['want']}</div></section>
 <section class="dsec"><div class="lab">怎么搭 · 01</div><h2>建好这几个频道</h2>
   <div class="dsteps">{chan_desc}</div></section>
 <section class="dsec"><div class="lab">怎么搭 · 02</div><h2>加入这些 Agent</h2>
   <div class="agents">{agents}</div></section>
 <section class="dsec"><div class="lab">怎么搭 · 03</div><h2>发一条房间简报</h2>
   <div class="brief-box">{d['briefing']}</div></section>
 <section class="dsec"><div class="lab">工作流</div><h2>一个任务，这样在频道里流转</h2>
   <div class="dsteps">{wf}</div></section>
 <section class="dsec"><div class="lab">长期任务</div><h2>这些事每天/每周自己重复</h2>
   <div class="dsteps">{jobs}</div></section>
 <section class="dsec"><div class="lab">进阶玩法</div><h2>跑顺了，再加这些</h2>
   <div class="tips">{fus}</div></section>
 <section class="dsec"><div class="lab">小贴士</div><h2>少踩几个坑</h2>
   <div class="tips">{tips}</div></section>
</div>
<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">现在开始</span>
 <h2>把你的行业，也交给一支 Agent 团队。</h2>
 <div class="cta"><a class="btn btn-primary" href="{APP}">进入 Syfo <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="cases.html">看更多案例</a></div></div></section>
<div class="band" style="background:var(--bg-sunken);border-top:1px solid var(--border-1)"><section><div class="wrap">
 <div class="lab" style="font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)">相关案例</div>
 <div class="related">{rel}</div>
</div></section></div>""")
    D.append(footer())
    with open(os.path.join(HERE,f"case-{slug}.html"),"w",encoding="utf-8") as f:
        f.write("\n".join(D))

for slug in CASE_BY_SLUG:
    detail_page(slug)

print("wrote index.html + cases.html + 6 case detail pages")
