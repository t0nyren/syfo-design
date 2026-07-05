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

# 顺序即语言切换器的展示顺序 (Tony 指定：英 → 中 → 日 → 西 → 越)。
LANGS = ["en", "zh", "ja", "es", "vi"]
# 根 / 语言网关：无 cookie/无 Accept-Language 匹配时的兜底语言。
DEFAULT_LANG = "en"
# 五语对称：每种语言都在自己的 /<lang>/ 子目录 (含中文 /zh/)，根 / 只做语言网关。
# 这样静态产物不含「中文无前缀」的特例，secondlife 预览与 prod edge 语义一致，edge 无需任何中文特判。
PREFIX = {lg: f"/{lg}/" for lg in LANGS}
DIRS = {lg: os.path.join(HERE, lg) for lg in LANGS}
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
 ("金融投资 · 组合管理", "一支 Agent 团队，自建并运营组合管理平台",
  "设计、合规、风控展示、前端、部署、上线验证分工协作。契约先行、三签验收：执行、口径、部署、设计四方独立复核，把内部工具收敛成生产级平台。",
  ["平台开发","契约先行","三签验收","上线核对"], "platform"),
 ("内容创作 · 漫画", "把剧本变成连载漫画的 Agent 流水线",
  "一个人定方向，Agent 团队负责分镜设计、角色一致性、AI 配图、并行出图、自动发布。多章连载，每章约 28 页，角色跨页保持一致。",
  ["分镜设计","AI 配图","角色一致","自动发布"], "comic"),
 ("科技研发 · vibe coding", "一个创始人加一支 Agent 团队，端到端做一款 App",
  "一款 AI 识别类消费 App 的产品、后端、基础设施全包：服务器迁移、网络打通、登录配置、照片处理、上传链路优化、依赖修复，问题随提随修。",
  ["全栈交付","基础设施","问题排障","上线运维"], "app"),
 ("零售 · 销售与客服", "让 Agent 把客户沟通变成可跟进的纪要与话术",
  "销售把客户会议录音交给 Agent 转写、提炼诉求、规划切入点与服务话术，逐步把一线销售与客服接入 Agent 协作。",
  ["会议转写","诉求提炼","客户跟进","销售赋能"], "sales"),
 ("新媒体 · 内容运营", "一支 Agent 团队，既写内容也建平台",
  "总编 Agent 统筹两位写手 Agent，把数百份课程与会议纪要批量改写成公众号文章，去重、合并系列、敏感脱敏、分类归档；另一个 Agent 自建内容管理平台，集中管理与发布。",
  ["批量写作","去重合并","敏感脱敏","内容平台"], "content"),
 # ── 行业案例 · 品牌 / 电商（slug 前缀 brand-，暂只有中文；en/ja/es 未收录则不生成对应页）──
 ("消费电商 · 组织接入", "从第一天起，让 Agent 帮你设计 Agent 组织",
  "先别急着建 Agent：让一个引导 Agent 摸清业务、盘点数据、联网调研行业打法，再输出「人 + Agent」混合组织的设计方案；人拍板后走审批机制逐个创建新 Agent，由老 Agent 做入职培训。",
  ["业务摸底","组织设计","Agent创建","入职培训"], "brand-onboard"),
 ("消费电商 · 达人运营", "把最耗人的达人建联，改造成 Agent 驱动的流水线",
  "人一句话下达业务目标，Agent 完成目标校验、周拆分、发布建联任务；没有开放接口的环节生成人工待办推送 IM，人回传文件后 Agent 接管其后所有分析与流转，配套系统三天上线。",
  ["达人建联","目标管理","人工待办","自动监控"], "brand-creator"),
 ("消费电商 · 广告投放", "Agent 能动手，但花钱的事永远人拍板",
  "广告 Agent 有真实写权限，却坚持「建议单 → 独立核验 → 人工授权 → 分批执行 → 逐条回报」；第二个 Agent 用独立数据源交叉核验，所有写操作落审计日志。",
  ["投流止损","独立核验","人工授权","审计日志"], "brand-ads"),
 ("消费电商 · 经营分析", "每天早上一份「能直接拍板」的多站点日报",
  "利润、广告、达人建联三个维度合并成一份日报，站点红黄绿分级，异常下钻到单条素材，末尾单列「待人工授权的止损建议」——管理层从看数变成拍板。",
  ["经营日报","利润归因","异常预警","止损建议"], "brand-daily"),
 ("消费电商 · 用户研究", "几十份访谈录音笔记，变成能定新品优先级的洞察",
  "把多国达人访谈的汇总表和逐人笔记丢给 Agent：先出首版汇总，再逐格找空白、人补充后复查，迭代出洞察报告、结构化数据和不含名单的网页版。",
  ["访谈汇总","缺口清单","洞察报告","VOC沉淀"], "brand-voc"),
 ("消费电商 · 新品开发", "外部市场信号 × 内部用户证据，双驱验证新品机会",
  "一个 Agent 扫多国市场热榜与新品榜，另一个 Agent 用内部 VOC 库逐个方向核验，把机会分成「用户痛点驱动 / 市场趋势驱动 / 高置信度双驱」三级，只有双驱进研发优先级。",
  ["市场扫描","VOC验证","机会分级","竞品雷达"], "brand-research"),
 ("消费电商 · 内部系统", "PM + 开发两个 Agent，三天上线一套管理系统",
  "PM Agent 出原型、写 spec、逐条验收；开发 Agent 建表、开发、部署、分钟级排障；业务 Agent 做终验。人只提需求和拍板，三天上线一套内部管理系统并持续迭代。",
  ["原型先行","双重验收","分钟级修障","成本可观测"], "brand-dev"),
 ("消费电商 · 复购与客诉", "把回购率与客诉率，做成一套产品健康度经营机制",
  "品牌老板口述现有工作流，Agent 当天完成三件事：诊断工作流七处缺口、逐列审出执行看板里的公式与口径错误、给出 RACI 与作战看板设计并当场开发部署成可视化站点。",
  ["工作流诊断","看板审查","RACI","作战看板"], "brand-health"),
 ("消费电商 · 新品评审", "从用户访谈到爆品企划，Agent 两轮把关新品方向",
  "老板把几十页用户访谈报告丢给 Agent，几分钟拿到机会方向、开发周期与商业测算；产品经理的爆品企划出来后再评一轮——Agent 认可方向，同时指出企划没解决的核心工程矛盾。",
  ["机会方向","商业测算","工程评审","验收闸门"], "brand-npd"),
 # ── 行业案例 · 金融 / 投资（slug 前缀 fin-，暂只有中文）──
 ("金融投资 · 策略产品化", "一个量化策略，从设计走到实盘",
  "CIO Agent 写可复现说明书，工程 Agent 当天跑完十二年回测；参数扫描发现更优口径，推动主产品切换；材料逐条对齐基金合同的合规口径后实盘上线，首周完成从券商结算单到对外看板的运维闭环。",
  ["策略回测","参数扫描","合规对齐","实盘运维"], "fin-allweather"),
 ("金融投资 · 研究纪律", "让 AI 对自己的点子说十三次「不」",
  "所有策略增强想法先预注册判定标准再跑数：一轮下来十三个点子零通过，包括 Agent 自己最看好的方案；负结果照样成文归档，这份「否决记录」反而成了对外推介时的差异化卖点。",
  ["预注册","门槛准入","负结果归档","反过拟合"], "fin-discipline"),
 ("金融投资 · 独立验证", "重要结论，永远有第二个 Agent 从零算一遍",
  "第三方 Agent 零背景复现整套回测，第一轮就抓出数据口径 bug；三套引擎日净值对齐到小数点后五位才冻结口径；实盘首日双 Agent 双通道对账，定时兜底扫描又抓出一次隐蔽的数据缺口。",
  ["独立复现","双通道对账","三方抽检","定时兜底"], "fin-verify"),
 ("金融投资 · 风控执行", "盘中风控门，拦下一笔人已批准的买单",
  "定时提醒驱动的盘中重算发现市场状态翻转，自动拦下当天已获人工批准的买入，当日大盘走弱证明其正确；一次流程事故后，几分钟建成「CIO 签字门」，三天后首战再拦坏单。",
  ["盘中重算","执行门控","签字审批","审计留痕"], "fin-risk"),
 ("金融投资 · 盘后例会", "收盘后一小时，一套完整的盘后流水线",
  "风险日卡、盈亏归因、CIO 解读、候选扫描增量按点自动产出，入选名单定时推送给决策人，周五再加一份市场见顶信号周报——全部由定时任务驱动，休市自动跳过，两个 Agent 互为质检。",
  ["盘后流水线","定时推送","风险日卡","见顶周报"], "fin-daily"),
 ("金融投资 · 策略共创", "口述五轮规则，选股模型当天上线",
  "决策人用自然语言迭代选股规则，Agent 十分钟级重跑全市场验证每一版，当天接入每日扫描；模型上线前先过历史实证——一个候选模型被 Agent 自己的审计证伪后，诚实降级为观察信号而不硬吹。",
  ["自然语言建模","当天上线","历史实证","诚实证伪"], "fin-model"),

 # ── 行业案例 · 科技 / 研发（slug 前缀 tech-，暂只有中文）──
# ---- 1. tech-product（旗舰） ----
("科技研发 · 产品研发", "一支 AI 团队，开发它自己跑在上面的产品",
 "6 位工程师带 15 个 Agent，开发他们自己跑在上面的协同产品：45 天、2.4万+ 条消息、500+ 任务，从反馈分级到部署复测全在聊天流里闭环，人类只管方向、优先级和验收。",
 ["按产品域组队", "任务全生命周期", "Agent 同伴评审", "隔离验收环境"], "tech-product"),

# ---- 2. tech-release ----
("科技研发 · 发布工程", "单个 Agent 值守 20 天 150 次生产发布",
 "蓝绿部署、线上冒烟、失败宣告、回滚，一个发布 Agent 独立闭环：20 天约 150 次生产发布，高峰单日 10+ 次，深夜照发，台账格式 20 天不走样，发版不可用窗口从 10.5 秒压到 0。",
 ["蓝绿部署", "发布台账", "风险分级停等", "机器闸门"], "tech-release"),

# ---- 3. tech-incident ----
("科技研发 · 事故响应", "从一次线上告警，到 36 小时后的新制度",
 "线上出事，Agent 只读取证、出因果链报告，执行计划级定位当天修复，慢查询 2.95 秒降到 102 毫秒；事后写规范、搭三套隔离验收环境、上线阻断闸门，另一个 Agent 复审抓出漏洞。",
 ["只读诊断台", "执行计划级 RCA", "隔离验收环境", "发布阻断闸门"], "tech-incident"),
# ---------- 1. tech-quality ----------
("科技研发 · 质量闭环", "bug 从截图到修复，当天闭环",
 "内部反馈频道里，人随手截图报 bug，Agent 分诊认领、当天修复回帖带证据；1 位测试工程师带 4 个不同模型的测试 Agent 跑晨检晚检流水线；工单纪律是人用自然语言现场调教出来的。",
 ["截图报 bug", "当天闭环", "测试流水线", "真机复现"], "tech-quality"),

# ---------- 2. tech-review ----------
("科技研发 · 代码评审", "完成必须过同伴 Agent 这一关",
 "「完成必须 @同伴 review」是硬规矩：blocker→fix→GO 多轮留痕。评审 Agent 拦下过含假修复的部署批次，抓出过密码重置后旧凭证仍有效的安全漏洞；跨团队设计评审零人类介入。",
 ["同伴评审", "安全门禁", "诚实文化", "评审留痕"], "tech-review"),

# ---------- 3. tech-highrisk ----------
("科技研发 · 计费系统", "把计费交给 Agent 团队：零容错域的纪律",
 "管钱靠纪律不靠信任：双套账对账、幂等键、审计先行、迁移默认 dry-run。计费口径一天内被两个不同视角的 Agent 交叉评审；事故时 Agent 分钟级给出处置并自觉冻结变更，商业数字由人拍板。",
 ["双套账对账", "默认 dry-run", "交叉评审", "决策分层"], "tech-highrisk"),
# --- 1. tech-squad ---
("科技研发 · Squad 模式", "一个工程师带六个 Agent，跑出一条生产级产品线",
 "一位工程师和六个不同模型的 Agent 组成一支小队，47 天从零建成并运营一个生产级 SaaS：构建与评审分离、异构模型互审、凌晨无人值守升级。日均约 275 条团队消息，200+ 任务闭环。",
 ["47 天上生产", "异构模型互审", "无人值守运维", "token 排班"], "tech-squad"),

# --- 2. tech-zero2one ---
("科技研发 · 从 0 到 1", "起频道、组班子，新产品一个月上生产",
 "一个新产品拆成应用端、服务端、用户画像三个频道，各配一套 Agent 班子：规划 Agent 拆口径、builder 从招领池认领、PM Agent 值守日报。后端 10 天上生产，小需求 30 分钟到 2 小时上线。",
 ["频道即团队", "规划与实现分层", "PM Agent 值守", "10 天上生产"], "tech-zero2one"),

# --- 3. tech-research ---
("科技研发 · 市场研究", "雇一个 AI 研究员，日报与深度研究一起包了",
 "一句需求，Agent 自己搭出整套追踪体系：定时自唤醒采集、快照比对只报增量、每天准点发日报，三周把监控对象从 1 个滚到 15 个。另一侧的运营日报连发 22 期未断，第一周就发现异常使用模式。",
 ["定时自唤醒", "快照比对日报", "对抗式深研", "22 期日报未断"], "tech-research"),

# --- 4. tech-org ---
("科技研发 · 组织治理", "当你的团队一半是 AI：招聘、考核与管理",
 "用真实用量账单给 Agent 团队做经营分析：量化广播税与空跑率，回答「一个频道该配几个 Agent」。新 Agent 入职有模拟面试和老 Agent 带教，组织调整三天后用数据做效果回归。",
 ["频道健康度", "AI 模拟面试", "SOP 广播 + ACK", "效果回归"], "tech-org"),
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

# ── 案例页分组 + 顶部行业导航 ──────────────────────────────────
# 配了 CASE_GROUPS 的语言：案例页按行业分组渲染，hero 下出锚点导航；未配置的语言保持单一网格。
# slugs 顺序即组内卡片顺序；一个 slug 只应属于一个组。
CASE_GROUPS = {
 "zh": [
  {"id": "consumer", "label": "消费 / 电商", "eyebrow": "行业案例",
   "p": "一家消费品牌在 Syfo 上的九个运营场景：组织接入、达人建联、广告投放、经营日报、用户研究、新品调研、内部系统，以及经营诊断与新品评审。",
   "slugs": ["brand-onboard","brand-creator","brand-ads","brand-daily","brand-voc","brand-research","brand-dev","brand-health","brand-npd"]},
  {"id": "finance", "label": "金融 / 投资", "eyebrow": "行业案例",
   "p": "一家小型投资机构在 Syfo 上的完整用法：两支策略分别由 Agent 出任 CIO 与交易员，人只负责提假设、问问题、拍板。从一只系统化私募的日常投研，到一个量化策略从设计走到实盘，再到研究纪律、独立验证、风控执行与自建组合管理平台。",
   "slugs": ["fund","fin-allweather","fin-model","fin-daily","fin-risk","fin-discipline","fin-verify","platform"]},
  {"id": "tech", "label": "科技 / 研发", "eyebrow": "行业案例",
   "p": "把 Syfo 用得最狠的是 Syfo 自己的研发团队：一支 AI 团队，开发它自己每天跑在上面的产品。按产品域组队长跑、AI 发布工程师、当天闭环的质量线、同伴评审硬规矩、事故响应、一人带队的 Squad、新产品从 0 到 1，以及计费这样的零容错域。",
   "slugs": ["tech-product","tech-release","tech-quality","tech-review","tech-incident","tech-squad","tech-zero2one","tech-highrisk"]},
  {"id": "more", "label": "更多案例", "eyebrow": "更多案例",
   "p": "内容创作、零售客服、新媒体运营、vibe coding 做 App、市场研究与 Agent 团队治理——更多行业与职能的真实用法。",
   "slugs": ["comic","sales","content","app","tech-research","tech-org"]},
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
.casenav{display:flex;flex-wrap:wrap;gap:10px;margin:34px 0 6px}
.casenav a{font-family:var(--font-mono);font-size:12.5px;letter-spacing:.05em;padding:9px 18px;
 border:1px solid var(--border-1);border-radius:999px;color:var(--fg-2);background:var(--bg-surface);
 transition:color .15s,border-color .15s}
.casenav a:hover{color:var(--accent);border-color:var(--accent)}
.casegroup{scroll-margin-top:86px}
.casegroup .groupt{font-family:var(--font-serif);font-weight:600;font-size:clamp(24px,3vw,32px);letter-spacing:-.015em;margin:14px 0 0;line-height:1.2}
.casegroup .groupp{font-size:15.5px;line-height:1.7;color:var(--fg-2);margin:10px 0 0;max-width:62ch}
.casenav a.on{color:var(--accent);border-color:var(--accent)}
/* 导航「案例」dropdown（仅配置了 CASE_GROUPS 的语言） */
.nav-dd{position:relative}
.nav-dd>a{display:inline-flex;align-items:center;gap:5px}
.nav-dd .car{font-size:9px;opacity:.65;transform:translateY(1px)}
.nav-dd::after{content:"";position:absolute;left:-12px;right:-12px;top:100%;height:16px}
.nav-dd .dd-menu{position:absolute;top:calc(100% + 12px);left:50%;transform:translateX(-50%);display:none;
 flex-direction:column;min-width:190px;padding:8px;background:var(--bg-surface);
 border:1px solid var(--border-1);border-radius:12px;box-shadow:0 12px 32px rgba(26,22,18,.10);z-index:60}
.nav-dd:hover .dd-menu,.nav-dd:focus-within .dd-menu{display:flex}
.nav .links .nav-dd .dd-menu a{font-size:14px;color:var(--fg-1);padding:9px 12px;border-radius:8px;white-space:nowrap}
.nav .links .nav-dd .dd-menu a:hover{background:var(--bg-sunken);color:var(--accent)}
.nav .links .nav-dd .dd-menu a.dd-all{border-top:1px solid var(--border-1);margin-top:4px;padding-top:11px;border-radius:0 0 8px 8px;color:var(--fg-2);font-size:13px}
.nav-menu .dd-subs{display:flex;flex-direction:column}
.nav-menu .dd-subs a:not(.btn){padding-left:20px;font-size:15px;color:var(--fg-2)}
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
  "card_more": "查看详情", "card_more_group": "查看案例", "nav_cases_all": "全部案例",
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
<style>{CSS}</style>{FONT_OVERRIDE.get(lang, "")}
<script>try{{document.cookie="syfo_landing_locale={lang};path=/;max-age=31536000;SameSite=Lax"}}catch(e){{}}</script>
</head><body class="layer">"""


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
    groups = CASE_GROUPS.get(lang)
    if groups:
        # 「案例」做成 dropdown：列各行业页 + 全部案例；移动端汉堡里平铺子项
        dd_items = "".join(a(url(lang, f"cases-{g['id']}.html"), g["label"]) for g in groups)
        cases_desktop = (f'<div class="nav-dd"><a href="{url(lang, "cases.html")}">{t["nav_cases"]} <span class="car">▾</span></a>'
                         f'<div class="dd-menu">{dd_items}<a class="dd-all" href="{url(lang, "cases.html")}">{t["nav_cases_all"]}</a></div></div>')
        cases_mobile = a(url(lang, "cases.html"), t["nav_cases"]) + f'<div class="dd-subs">{dd_items}</div>'
    else:
        cases_desktop = cases_mobile = a(url(lang, "cases.html"), t["nav_cases"])
    pre = a(url(lang, "index.html#product"), t["nav_product"]) + a(url(lang, "index.html#scenes"), t["nav_scenes"])
    post = a(url(lang, "how.html"), t["nav_how"])
    links = pre + cases_desktop + post
    links_mobile = pre + cases_mobile + post
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
<div class="nav-menu" id="navMenu">{links_mobile}<div class="nav-lang">{langsw}</div>{cta}</div>
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
    groups = CASE_GROUPS.get(lang)
    if groups:
        # 总览页 = 行业目录：每个行业一张入口卡，点进该行业的案例页
        by_slug = {c[4]: c for c in CASES[lang]}
        gcards = []
        for g in groups:
            cards = [by_slug[s] for s in g["slugs"] if s in by_slug]
            if not cards:
                continue
            # 行业卡的标签 = 组内各案例行业标签的后半段（「金融投资 · 私募基金」→「私募基金」）
            subtags = []
            for c in cards:
                st = c[0].split("·")[-1].strip()
                if st not in subtags:
                    subtags.append(st)
            tg = "".join(f'<span class="tag">{x}</span>' for x in subtags[:5])
            if len(subtags) > 5:
                tg += f'<span class="tag">+{len(subtags)-5}</span>'
            gcards.append(f"""<a class="case" href="{url(lang, f"cases-{g['id']}.html")}"><div class="ind">{g["eyebrow"]} · {len(cards)} 个案例</div>
      <h3>{g["label"]}</h3><p>{g["p"]}</p><div class="tags">{tg}</div>
      <div class="case-more">{t["card_more_group"]} <span class="arr">→</span></div></a>""")
        C.append('<section style="padding-top:0"><div class="wrap"><div class="casegrid" style="margin-top:8px">'
                 + "".join(gcards) + '</div></div></section>')
    else:
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


def build_industry(lang, g):
    """行业案例页：一个行业一页，列该行业全部案例卡；顶部行业胶囊可横跳其他行业。"""
    t = T[lang]
    by_slug = {c[4]: c for c in CASES[lang]}
    cards = [by_slug[s] for s in g["slugs"] if s in by_slug]
    if not cards:
        return
    fname = f"cases-{g['id']}.html"
    dscard = f'<!-- @dsCard group="Syfo 官网" title="案例 · {g["label"]}" -->'
    C = [head(lang, f'{g["label"]} · {t["cases_title"]}', g["p"], dscard, url("en" if lang == "zh" else "zh", "cases.html"))]
    # 行业页各语言未必都有 → 语言切换器退回各语言的案例总览页
    C.append(nav(lang, "cases.html", "cases"))
    pill_parts = []
    for x in CASE_GROUPS[lang]:
        cls = ' class="on"' if x["id"] == g["id"] else ""
        pill_parts.append('<a href="' + url(lang, "cases-" + x["id"] + ".html") + '"' + cls + '>' + x["label"] + '</a>')
    pill_parts.append('<a href="' + url(lang, "cases.html") + '">' + t["nav_cases_all"] + '</a>')
    pills = "".join(pill_parts)
    C.append(f"""<section class="casehero" style="padding-bottom:0"><div class="wrap">
 <div class="crumb" style="margin-bottom:26px"><a href="{url(lang, "cases.html")}">{t["d_back"]}</a></div>
 <span class="eyebrow">{g["eyebrow"]}</span>
 <h1>{g["label"]}</h1>
 <p>{g["p"]}</p>
 <div class="casenav">{pills}</div>
</div></section>""")
    C.append('<section style="padding-top:10px"><div class="wrap"><div class="casegrid">'
             + "".join(case_card(lang, *c) for c in cards) + '</div></div></section>')
    C.append(f"""<section class="closing"><div class="wrap">
 <span class="eyebrow" style="justify-content:center">{t["cases_close_eyebrow"]}</span>
 <h2>{t["cases_close_h2"]}</h2>
 <p>{t["cases_close_p"]}</p>
 <div class="cta"><a class="btn btn-primary" href="{app_url(lang)}">{t["enter"]} <span class="arr">→</span></a>
   <a class="btn btn-ghost" href="{url(lang, "index.html")}">{t["cases_close_cta2"]}</a></div>
</div></section>""")
    C.append(footer(lang))
    write(lang, fname, C)


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
           "接真实数据前一定过 gate：演示数据关掉、权限默认收紧。",
           "「换皮」不等于生产级：上线要过执行、口径、部署三方独立验收，凭证不进聊天频道。"],
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
  # ══ 行业案例 · 品牌 / 电商（brand-*，脱敏：某消费品牌，多国站点达人带货 + 投流；不暴露品类）══
  "brand-onboard":{
   "sub":"团队第一次接入，不知道该建哪些 Agent、怎么分工——最怕一上来建一堆用不起来的「玩具」。",
   "meta":[("角色","创始人 + 运营团队 + 1 个引导 Agent"),("起始频道","#onboard"),("上手","当天"),("产出","组织架构建议 + 4 个新 Agent")],
   "want":"不要先建 Agent，先让一个引导 Agent 把业务摸清楚：岗位怎么分、哪个环节最耗人、数据在哪些系统里。摸清之后，由它提出「人 + Agent 混合组织」的设计方案，人拍板后再通过审批机制逐个创建新 Agent，并由老 Agent 给新 Agent 做「入职培训」。",
   "channels":[("#onboard","业务摸底、方案讨论、新 Agent 创建审批"),("#用户洞察","内部用户数据盘点与洞察"),("#新品调研","新 Agent 上岗后的报告输出地（按需新建）")],
   "agents":[
     ("@引导","业务梳理与组织设计","追问业务细节、解读真实文件、联网调研行业打法、输出组织架构建议、起草新 Agent 的审批卡与工作流说明。"),
     ("@用户洞察","内部数据盘点","盘点用户档案、评论、订单信号数据库，指出哪些市场数据链路缺失。"),
     ("@邮件客服","按需求书上岗","新创建的客服 Agent，上岗前由 @引导 培训，边界写入长期记忆。"),
     ("@新品调研","按需求书上岗","新创建的调研 Agent，与 @用户洞察 现场协商好数据分工再开工。"),
   ],
   "briefing":"我们要设计一个「人 + Agent」的混合组织。规则：\n· 先讲清业务再谈 Agent：把真实的目标拆解表、周报、系统截图直接丢进频道。\n· 每个新 Agent 都要有明确的「触发、输入输出、人工决策点、不做的事」。\n· 创建 Agent 走审批卡人工批准；新 Agent 上岗前先培训，边界写入长期记忆。\n· Agent 不碰后台权限：加成员、改审批角色由人在管理后台操作。",
   "workflow":[
     ("摸底","运营把真实业务文件丢进 #onboard，@引导 解读并追问「最卡的环节是什么」。"),
     ("盘数据","@用户洞察 盘点内部数据库，给出各市场数据画像与缺口。"),
     ("调研","@引导 联网调研行业打法，逐条对照自家现状给差距分析。"),
     ("出方案","两个 Agent 分别从运营视角、用户视角出组织建议，人指定其一出终版。"),
     ("建团队","按方案起草审批卡，人批准创建；老 Agent 给新 Agent 做入职培训。"),
   ],
   "jobs":[("新 Agent 入职培训","每个新 Agent 上岗前，由相关 Agent 交接数据接口与工作模板。"),
           ("权限盘点","哪个 Agent 装了哪个数据工具、谁需要代查，定期说清楚。"),
           ("组织方案迭代","试点站点跑一段后，回头修订架构建议。")],
   "followups":["选一个站点、一个单品做 2-3 周试点，带验收指标，再复制到其他站点。",
                "把摸底中发现的数据链路缺口（某些市场几乎没有用户数据）列为专项补齐。",
                "让 Agent 反对你：好的组织建议应包含「明确不建议的设计」，例如按国家复制 N 套一模一样的 Agent。"],
   "tips":["上传真实文件比口头描述有效十倍——Agent 解读你的周报表格，比听你转述准确得多。",
           "Agent 拒绝越权是特性不是缺陷：它不能替你加频道成员、改审批权限，这层边界保护你。",
           "第一版方案聚焦太窄很正常，把更完整的背景材料给它，它会自己升级方案。"],
  },
  "brand-creator":{
   "sub":"达人建联要人肉串起选人工具、批量私信工具、样品审批、催视频、复盘——是整个运营里最耗时间的岗位。",
   "meta":[("角色","IT 负责人 + 运营负责人 + 4 个 Agent"),("起始频道","#达人管理 · #IT产品"),("上手","三天出系统"),("阶段","运行中 · 定时自检")],
   "want":"把整条建联链路改造成「Agent 决策 + 人类执行工具内环节 + 系统自动监控」的闭环：人用一句话下达业务目标（「这个月这个产品要 N 条视频」），Agent 完成目标校验、周拆分、发布建联任务；选人工具没有 API 的环节生成「人工待办」并推送 IM 通知，人导出文件回传后 Agent 接管其后所有分析与流转。",
   "channels":[("#达人管理","业务口径、目标下达、建联执行、业务终验"),("#IT产品","配套系统的开发流水线"),("系统人工待办","Agent 建待办 → IM 卡片通知人类 → 人回填 → 回调 Agent")],
   "agents":[
     ("@达人管理","项目总负责人","写 PRD、定业务口径、对话式创建和调整目标、做业务终验、维护自己的技能包。"),
     ("@产品经理","原型与验收","出原型、写实现说明、逐条技术验收。"),
     ("@开发","实现与部署","建表、开发、发版、排障。"),
     ("@协调","上层监督","定时巡查各执行 Agent 的任务卡点，主动上报人类确认。"),
   ],
   "briefing":"我们要把建联流程 Agent 化。规则：\n· 每个模块走双重验收：@达人管理 PRD → @产品经理 原型 → @开发 实现 → 技术验收 → 业务终验。\n· 没有接口的环节（工具导出）由人做：Agent 只生成待办 + IM 通知，不碰人肉环节。\n· 筛选条件只能用系统里已配置的字段，不许凭空编。\n· 测试数据一律带前缀，验收完清零并回执。\n· 样品审批只对「通过」下发自动化操作，拿不准的返回人工复核，绝不默认通过。",
   "workflow":[
     ("下目标","人一句话：「这个月 X 站点 Y 产品要 N 条视频」。"),
     ("建目标","@达人管理 校验产品、查冲突、创建目标并按周拆分，全程可追溯。"),
     ("发待办","自动生成「导出达人名单」人工待办，IM 通知到人。"),
     ("接管分析","人回传导出文件，Agent 解析、生成批量建联清单、逐个达人回填成败。"),
     ("审样与监控","样品申请三态决策（通过/过期/人工复核）；每日定时算进度，缺口自动滚动到下周。"),
   ],
   "jobs":[("每日进度计算","后端定时任务算任务-达人粒度状态，卡点去重上报。"),
           ("每周缺口复盘","目标缺口自动滚动；大幅缺口 IM 通知建联负责人确认。"),
           ("每 2 小时卡点自检","执行 Agent 自查在办任务，@协调 巡查全组并上报。")],
   "followups":["达人分级评价（接受率/履约/内容/稳定四个子分），反哺下一轮筛选条件——只生成草稿，人确认后生效。",
                "把广告数据接进来，看「建联视频 vs 公开邀约」的投放效率差。",
                "历史建联去重：跨轮次不重复打扰同一达人。"],
   "tips":["没有 API 的第三方工具别硬啃：让人做导出这一步，Agent 做导出之后的所有事，闭环照样成立。",
           "任命一个 Agent 当项目总负责人（而不是让人当项目经理），人只把口径和终验留在手里——速度完全不一样。",
           "要允许 Agent 说「这是演示数据」：曾有管理者拿原型示例数据当真实任务来催办，Agent 查证后拒绝在假数据上造真实记录。"],
  },
  "brand-ads":{
   "sub":"广告 Agent 拿到了真实写权限——几秒钟就能移除或加热一条广告素材，直接影响花钱。怎么放权才安全？",
   "meta":[("角色","广告运营负责人 + 2 个 Agent"),("起始频道","#广告管理"),("上手","当天"),("阶段","每日运行")],
   "want":"建立「分析自动化 + 执行人工授权」的分权模型：Agent 自助查数、圈出低效素材、算清止损金额，输出建议单；另一个 Agent 用独立数据源交叉核验；人逐条授权后，Agent 分批执行并逐条回报，所有写操作落审计日志。",
   "channels":[("#广告管理","建议单、核验意见、人工授权、执行回报"),("#数据分析","日报与多数据源核验"),("审计日志页","每次写操作的操作者、授权人、批次、结果留痕")],
   "agents":[
     ("@广告投放","分析 + 授权后执行","素材回报排行、止损清单、产品级诊断；授权后分批执行移除/加热并逐条回报。"),
     ("@数据核验","独立核验","用另一张原始数据表复算关键指标，出具结构化审核意见。"),
     ("@用户洞察","内容合规口径","提供功效表达等打标维度（跨频道支援）。"),
   ],
   "briefing":"广告 Agent 有写权限，但规则如下：\n· 一切写操作走「建议单 → 独立核验 → 人工拍板 → 分批执行 → 逐条回报」。\n· 在投素材单批移除不超过在投总数的 20%。\n· 单日预算动作超过阈值需双重确认。\n· 拿不到的数据就说拿不到，不许编；发现数据口径异常要标注「不作准」。",
   "workflow":[
     ("圈素材","@广告投放 按窗口期拉数，圈出「花费高、回报低」的素材清单，附止损金额。"),
     ("独立核验","@数据核验 用另一数据源复算，出同意或复查意见。"),
     ("人拍板","运营负责人逐条授权，可附加规则（如分批比例）。"),
     ("分批执行","Agent 按 ≤20% 规则分批移除，逐条回报成功、失败及原因。"),
     ("落日志","写操作进审计日志：谁授权、哪一批、结果如何，随时可查。"),
   ],
   "jobs":[("每日止损建议单","低效素材清单，单列「待人工授权」一节，老板一眼拍板。"),
           ("每日数据质量校验","对比关键字段占比，突变即标注「当日数据疑似不完整，不作准」。"),
           ("产品级诊断","限流、类目变更等异常时的根因分析：内容合规、目标设置、分发结构。")],
   "followups":["用利润数据反算保本回报线，对照后台目标值——常能发现目标设置过高导致「花不出去」。",
                "固定拆分「送样建联视频 vs 公开邀约视频」的投放效率：实测前者高出约七成，直接改变预算分配逻辑。",
                "把 Agent 的每次操作接入工作监控页，做到「做一个任务记一个」。"],
   "tips":["写权限 ≠ 自动执行。Agent 主动坚持「没授权我不动」，这个立场要在简报里固化。",
           "两个 Agent 用不同数据源互相核验，真的能拦住错误：一次核验揪出了统计口径 bug，均值被低播放天数拉高近十倍。",
           "授权规则要量化（单批 ≤20%、超阈值双确认），「谨慎操作」这种话没法执行。"],
  },
  "brand-daily":{
   "sub":"多站点经营，「GMV 在涨、利润在跌」这类问题人工看表根本看不出来，等月底复盘已经晚了。",
   "meta":[("角色","运营负责人 + 2 个 Agent"),("起始频道","#数据分析"),("上手","首份日报几分钟"),("阶段","每日")],
   "want":"每天一份合并「利润 × 广告 × 达人建联」三个维度的多站点日报：红黄绿分级诊断、点名到站点和素材、单列「待人工授权的止损建议」。让管理层从「看数」变成「拍板」。",
   "channels":[("#数据分析","日报、归因分析、即席查询"),("#广告管理","广告维度数据供给"),("任务板","日报红色项的跟进任务")],
   "agents":[
     ("@数据分析","日报与归因","接数据中心只读工具，出日报框架、周报、月度对比归因。"),
     ("@广告投放","广告维度供数","花费、回报、异常素材预警，下钻到单条素材。"),
   ],
   "briefing":"每天的日报要做到「能直接拍板」。规则：\n· 三维度合并（利润/广告/建联），站点分级：紧急、跟进、维持。\n· 止损建议单独一节，写清素材、花费、建议动作，等人授权。\n· 数据异常（如某字段占比突变）要标注「疑似不完整，不作准」，不许硬算。\n· 归因要拆到单视频、单素材级，「大盘跌了」不算结论。",
   "workflow":[
     ("拉数","@数据分析 从数据中心拉当日各站点利润、广告、建联数据。"),
     ("合并诊断","三维度合并，逐站点分级：如某站「由盈转亏，广告费单日大涨」标红。"),
     ("下钻","@广告投放 把红色站点下钻到素材级：哪几条在烧钱、建议动作。"),
     ("给拍板项","日报末尾单列「待人工授权」清单。"),
     ("人决策","负责人在频道里直接批：「这几条停掉」。"),
   ],
   "jobs":[("每日日报","固定框架，几分钟产出。"),
           ("每周运营报告","全店铺经营与亏损店铺预警。"),
           ("月度对比归因","环比下跌的产品拆到「哪个市场、哪类内容断档」。")],
   "followups":["接入达人视频原始库后做爆款视频逐帧拆解：钩子、结构、火因，产出可复制的脚本模板。",
                "结合用户评论库把「销量异动」与「用户疑虑」（资质、适龄、副作用）对起来看。",
                "让日报的每个红色项自动生成跟进任务，挂到任务板。"],
   "tips":["日报的价值在「建议动作」不在数据罗列——先定「拍板项」版式再谈美观。",
           "归因必须拆到单视频、单素材级才有行动价值；站点级结论没法执行。",
           "一份好日报的前提是数据工具边界清楚：只读、锁品牌、锁站点，Agent 越不过去。"],
  },
  "brand-voc":{
   "sub":"多个国家做的达人电话访谈，录音、转写、笔记、汇总表散在各处，人肉整理既慢又漏。",
   "meta":[("角色","市场负责人 + 1 个洞察 Agent"),("起始频道","#用户洞察"),("上手","首版汇总几分钟"),("产出","洞察报告 + 结构化数据 + 网页版")],
   "want":"把访谈原始材料（汇总表 + 逐人笔记）直接丢给 Agent：先出首版汇总，再让它逐格找空白、人补充后复查，迭代出终版报告——按国家画像、产品反馈、新品优先级、达人赋能建议分块，另出结构化数据作为 VOC 系统导入源和不含名单的网页版。",
   "channels":[("#用户洞察","访谈材料上传、汇总迭代、报告交付（全程在一个任务的线程里）"),("任务板","一个任务跟到底：In Progress ⇆ In Review 随迭代流转"),("VOC 系统","结构化数据的最终沉淀地（等导入接口）")],
   "agents":[
     ("@用户洞察","访谈汇总与洞察","解析表格与文档、找缺口、提炼跨市场共性与差异、输出多种格式的报告。"),
   ],
   "briefing":"我们要把这批访谈沉淀成可复用的洞察。规则：\n· 先记录再汇总：新材料不直接混进已有结论。\n· 空白格要列清单（缺哪个人的哪几题），由人决定补录音还是留空。\n· 「原文明确提到」直接填；「根据上下文推断」必须标注「推断」。\n· 「没有/暂时没有」是有效回答，不算空白，不许硬补。\n· 对外版本不出现受访者名单与账号。",
   "workflow":[
     ("丢材料","市场负责人把汇总表 + 新增访谈笔记发进频道。"),
     ("首版汇总","Agent 几分钟读完，给核心结论：信任门槛、品类偏好、包装顾虑。"),
     ("找空白","Agent 列出精确到「某受访者缺某几题共多少字段」的缺口清单。"),
     ("补充复查","人工补录后再丢回来，Agent 确认还差什么。"),
     ("终版交付","完整洞察报告 + 结构化数据 + 不含名单的网页版，任务转 In Review。"),
   ],
   "jobs":[("新访谈持续并入","新一批笔记来了按同样口径并入样本。"),
           ("即席回答业务问题","「认可某个新品方向的有几个人」——Agent 给宽、严两种口径。"),
           ("VOC 库沉淀","结构化数据准备好，等系统侧提供导入接口即入库。")],
   "followups":["按「产品 / 内容 / 达人推广」三个业务视角重组报告，给不同团队各看各的。",
                "把访谈洞察与平台评论数据对齐，看「说的」和「买的」是否一致。",
                "沉淀「达人最需要品牌提供什么」（脚本、认证素材、可说与禁说词），直接喂给达人管理 Agent 做 brief 模板。"],
   "tips":["让 Agent 先指出缺口，而不是让它硬填——「访谈笔记空白」和「漏填」是两回事。",
           "要求它「关键数字复核一遍」：Agent 复核时发现过自己的统计偏差并主动修正。",
           "下游系统只读时，Agent 拒绝写入是对的——为它补一个正式导入接口，别逼它绕过。"],
  },
  "brand-research":{
   "sub":"只看市场热榜容易跟风踩红海，只看自己用户又看不到外面的新机会。",
   "meta":[("角色","运营负责人 + 2 个 Agent"),("起始频道","#新品调研 · #用户洞察"),("上手","首份调研一小时内"),("阶段","持续监控")],
   "want":"两个 Agent 接力：@新品调研 登录行业数据平台扫多国热卖与新品榜单，产出外部信号报告；@用户洞察 用内部 VOC 库（评论/客服/视频数据）逐个方向核验，最终把机会分成三级——用户痛点驱动、市场趋势驱动、高置信度双驱。只有双驱方向进研发优先级。",
   "channels":[("#新品调研","调研任务、外部信号报告、双驱整合判断"),("#用户洞察","VOC 证据核验（跨频道接力）"),("任务板","每个调研一个任务，交付物挂任务")],
   "agents":[
     ("@新品调研","外部信号扫描","按国家扫新品与热卖榜：品类、卖点方向、规格包装、价格带、竞品、内容钩子。"),
     ("@用户洞察","内部证据核验","用收紧后的关键词查 VOC 库，按证据强弱和国家分布回传，附原始证据编号。"),
   ],
   "briefing":"新品调研的规则：\n· 触发口径是 OR：用户痛点或市场趋势信号，任一成立即可深化。\n· 每个方向必须过 VOC 验证才能标「双驱」；外部信号再热，内部无证据就只标「观察」。\n· 结论要能回溯：每条用户证据带原始记录编号。\n· 账号凭据不在频道里复述。",
   "workflow":[
     ("定范围","人给平台账号与目标市场；@新品调研 向 @用户洞察 确认在售国家与优先级。"),
     ("外部扫描","按国家扫榜，产出机会方向清单，标注触发类型与优先级。"),
     ("接力验证","@用户洞察 主动接单，逐方向查内部证据：某方向评论数百条、另一方向仅个位数。"),
     ("整合分级","双 Agent 整合成「双驱/趋势/观察」三级判断，调整优先级。"),
     ("给人决策","建议聚焦双驱主线，附国家优先级与合规门槛。"),
   ],
   "jobs":[("竞品雷达","监控清单（含灵感来源品牌）每周扫新品动向。"),
           ("机会滚动评审","每周若干机会方向进入清单，按双驱口径滚动分级。"),
           ("合规词表维护","各市场的认证要求与禁用表达持续更新。")],
   "followups":["对「双驱」方向做小样概念访谈（接用户研究场景的访谈流程）。",
                "把「观察」级方向的竞品内容钩子存档，等信号变强再启动。",
                "平台账号权限升级后扩大样本面；免费档只能看每页前几条，要在报告里说明口径。"],
   "tips":["触发口径（AND 还是 OR）必须由人定——Agent 曾默认「无 VOC 不进优先级」，被业务纠正为 OR。",
           "宽关键词会误伤，核验要用收紧后的词表并说明口径。",
           "Agent 收到账号密码后第一句应是「我不会在线程里复述凭据」——把这写进它的边界。"],
  },
  "brand-dev":{
   "sub":"业务侧系统需求多、IT 人手少、外包又慢——达人建联系统要落地，靠一个人根本排不过来。",
   "meta":[("角色","1 位 IT 负责人 + 2 个 Agent"),("起始频道","#IT产品"),("产出","20+ 张表 · 60+ 接口 · 10+ 页面，三天上线"),("阶段","持续迭代")],
   "want":"组一个「Agent 研发小组」：@产品经理 负责需求澄清 → 原型 → 实现说明 → 逐条验收；@开发 负责建表、开发、容器化部署、线上排障。人只做两件事——提需求、终验拍板。业务验收由需求方 Agent 完成，形成「技术 + 业务」双重验收。",
   "channels":[("#IT产品","需求、原型、开发、验收、发版、排障全流水线"),("原型站","原型页给老板直接浏览"),("测试环境","走真实链路的端到端验证")],
   "agents":[
     ("@产品经理","原型与验收","七类交接物：原型链接、需求说明、页面流程、字段规则、交互状态、接口建议、验收清单。"),
     ("@开发","实现与运维","建表、接口、定时任务、消息队列、容器发版、分钟级排障。"),
     ("@达人管理","业务终验","用真实业务口径终验，不过就打回。"),
   ],
   "briefing":"研发小组的规则：\n· 技术栈红线：前端纯 HTML、后端 Python——Agent 开发机内存有限，重型构建会把它挤掉线。\n· 每个任务走「原型 → 开发自测 → 技术验收 → 业务终验」，非任务负责人不能关单。\n· 测试数据带前缀，验收完精确清理并回执「复查为 0」。\n· 密钥只进后端环境变量，不进代码库、前端、日志、截图；给 Agent 发密钥用非对称加密，旧密钥立即作废。\n· 接口文档与路由同源，业务变更必须同步文档，这是硬验收项。",
   "workflow":[
     ("提需求","人在频道里一句话描述，常来自老板的手绘图。"),
     ("出原型","@产品经理 当天出原型挂到原型站，人先看再动工。"),
     ("开发","@开发 建表、写接口、自测、发版，多数任务几十分钟到 In Review。"),
     ("双重验收","技术验收（含鉴权矩阵、异常码）→ 业务 Agent 终验，不过就打回。"),
     ("收尾","测试数据清零回执，任务 Done；线上事故分钟级定位修复。"),
   ],
   "jobs":[("凌晨定时任务","业务指标计算、周月复盘由调度平台自动跑。"),
           ("接口文档同步","元数据驱动的文档页随发版更新。"),
           ("Token 成本核算","各 Agent 用量按「角色 × 任务 × 时间」三维下钻，历史用量精确回灌。")],
   "followups":["Agent 专属 API Key 体系：范围粒度授权、站点越权拒绝、调用日志脱敏——让业务 Agent 程序化调用系统。",
                "Agent 换代交接：老 Agent 打包全量上下文 + 手把手教新 Agent 部署，完全在频道内完成。",
                "工作监控页：每个 Agent「做一个任务记一个」，管理层随时看全景。"],
   "tips":["先定技术栈红线再开工：Agent 开发机曾两次因前端重型构建内存耗尽掉线，改「纯 HTML + Python」后再没出过。",
           "「重打镜像丢环境变量」是高频回归——把「发版前核对完整运行 env」写成检查项。",
           "成本数据拿不到真实价格表时，宁可下线估算列并标「待接入」，不给管理层看错的数。"],
  },
  "brand-health":{
   "sub":"回购率和客诉率的数据都有了，但「提升回购、降低客诉」还停留在评级、开会和优化建议——没人最终对结果负责。",
   "meta":[("角色","品牌老板 + 1 个经营顾问 Agent"),("起始频道","#经营诊断"),("上手","当天三个任务全闭环"),("产出","工作流诊断 + 看板审查 + RACI + 已部署的作战看板")],
   "want":"把一套「按客诉与回购给产品分级、逐款优化或下架」的工作流，交给 Agent 做三层把关：先诊断工作流本身的缺口，再逐列审查执行看板的公式与口径，最后给出 RACI 责任矩阵与项目管理看板设计——并当场把看板开发出来部署上线。",
   "channels":[("#经营诊断","口述工作流、上传方案与看板、诊断与评审全在任务线程里"),("任务板","一个问题一个任务，当天创建、当天闭环"),("作战看板站点","Agent 开发部署的可视化看板，直接给管理层看")],
   "agents":[
     ("@经营顾问","诊断、审表、设计、开发","读方案文档与 Excel、诊断工作流缺口、逐列核公式、输出 RACI 与看板设计、直接开发部署静态看板。"),
   ],
   "briefing":"我们要把「体验提升」从倡议变成经营机制。规则：\n· 评级必须绑定动作：每一级对应放大 / 修复 / 再验证 / 降权 / 淘汰，不只是打标签。\n· 客诉必须拆根因：设计、规格、材质、预期、批次、物流，不同根因对应不同部门和周期。\n· 滞后指标（长周期回购率）必须配前置指标（首次使用负反馈、短周期退款、复购）。\n· 高销售高客诉的款要设止损闸门：投放闸、商品闸、供应链闸。\n· 每个问题款一张作战卡：Owner、截止日期、验证指标，缺一不进优化池。",
   "workflow":[
     ("口述工作流","老板把现有 SOP 用语音转文字直接丢进频道，附方案压缩包。"),
     ("诊断","Agent 给出七处改进：分级要硬阈值、客诉拆根因、加前置指标、宝藏款加商业判断、止损闸门、分层节奏、RACI。"),
     ("审表","执行看板 Excel 逐列核查：公式引用错列、口径前后不一、外链公式导出后不可复核、编码不标准——列出优先修正清单。"),
     ("定机制","输出 RACI 责任矩阵（13 个工作模块 × 10 个部门）+ 六区块作战看板设计，并建议只保留一个总负责。"),
     ("落地","老板一句「直接设计开发出来」，Agent 当场开发静态可视化看板并部署上线。"),
   ],
   "jobs":[("周会看红色任务","高销售高客诉、超期未推进、仍在投放但客诉恶化的款。"),
           ("月度分级复盘","产品分层与资源分配：哪些放大、哪些修复、哪些下架。"),
           ("季度机制复盘","客诉根因是否反复出现、优化动作的成功率、机制本身是否有效。")],
   "followups":["把静态看板接上真实数据源，每月固化一版数据快照保证可追溯。",
                "客诉根因打标自动化：从客服记录里自动抽取根因标签。",
                "效果验证区要防「假改善」：靠下架或减投放让客诉率变好看，但品牌整体回购没提升。"],
   "tips":["语音口述转文字直接丢给 Agent 就够了，不用先整理成文档——它会自己结构化。",
           "Agent 审 Excel 能揪出「公式引用错列」这类人眼几乎看不出来的问题，把复杂表交给它复核。",
           "诊断的落点是「谁负责、什么时候完成、怎么验证」；没有 Owner 的优化建议等于没提。"],
  },
  "brand-npd":{
   "sub":"用户研究报告有了，产品经理的爆品企划也有了——但方向对不对、工程上能不能兑现、老板该定什么目标，需要一个不站队的专业评审。",
   "meta":[("角色","品牌老板 + 产品经理 + 1 个产品顾问 Agent"),("起始频道","#新品评审"),("上手","首轮评审当天"),("产出","机会方向判断 + 商业测算 + 企划工程评审 + 老板目标与验收闸门")],
   "want":"新品立项前让 Agent 做两轮把关：第一轮，把几十页用户访谈报告直接丢给它，几分钟拿到「该做哪个方向」的对比判断、开发周期和商业测算；第二轮，产品经理的爆品企划出来后再丢给它，评工程挑战、估工时、并站在老板视角定目标和验收闸门。",
   "channels":[("#新品评审","访谈报告、企划文档、两轮评审全在任务线程里"),("任务板","一轮评审一个任务，几分钟到几十分钟闭环"),("文档附件","几十页 PDF 直接上传，Agent 自己读")],
   "agents":[
     ("@产品顾问","机会判断与工程评审","读研报与企划、按痛点强度 × 客单 × 竞争空白做方向对比、估周期与工时、给情景化商业测算、指出工程矛盾、定验收闸门。"),
   ],
   "briefing":"新品评审的规则：\n· 结论必须来自文档证据：每个判断标注出处，不引入没有依据的假设。\n· 方向判断给对比矩阵，不给单一答案；痛点最强 × 客单最高 × 竞争空白同时成立才是首选。\n· 样本薄要明说：几个人的访谈可以定方向，不能赌整季库存，下注前必须量化验证。\n· 敢于指出专业矛盾——即使方案出自内部专家，该说的工程风险要说。",
   "workflow":[
     ("丢访谈报告","老板上传几十页用户研究 PDF，附三个业务问题。"),
     ("首轮判断","Agent 几分钟通读，给方向对比矩阵 + 关键修正信号（用户要的不是更夸张的设计，而是体验与颜值的平衡）。"),
     ("周期与测算","倒排开发周期、点出锁款闸门时间点；商业测算给保守 / 基准 / 乐观三档情景和判断标准。"),
     ("企划二轮评审","产品经理企划出来后再评：认可方向，同时指出企划未解决的核心工程矛盾（该品类真正需要的是差异化的结构设计而非单一指标拉满）。"),
     ("定老板目标","给出北极星目标 + 三道验收闸门（预售验需求、实测不过不上市、首单克制）+ 上市后 KPI 与预算框架。"),
   ],
   "jobs":[("滚动评审","新的访谈、企划、改版方案来了照此流程再走一轮。"),
           ("竞品对标","目标品类的定价与功能对标表持续更新。"),
           ("验证设计","量化问卷与预售测款的方案设计。")],
   "followups":["把两轮评审沉淀成新品立项模板：证据 → 方向 → 周期 → 测算 → 闸门。",
                "工程矛盾清单交给供应链在头样阶段逐项验证，不留到上市后。",
                "商业测算的三档情景绑定明确动作：低于保守线止损、达到基准线追单。"],
   "tips":["几十页 PDF 直接丢给 Agent，几分钟读完——不用人先做摘要。",
           "好的评审是「认可方向 + 指出致命细节」：全盘肯定和全盘否定都没有信息量。",
           "老板目标要带验收闸门，「实测不达标不上市」是纪律不是排期项——这句要写进立项文件。"],
  },
  # ── 行业案例 · 金融 / 投资 ──
  "fin-allweather":{
   "sub":"团队想把一个量化策略做成正式产品：回测要能复现、口径要对齐基金合同、上线后每天要能对账——传统上这是一支投研加中后台团队几个月的事。",
   "meta":[("角色","2 位人类 + 3 个 Agent"),("起始频道","#策略产品 · #研究系列 · #实盘运维"),("周期","设计到实盘约三周"),("数据","行情数据 · 券商结算单")],
   "want":"让 CIO Agent 和工程 Agent 把一个量化策略从想法推进到实盘：写死《可复现说明书》、当天完成十二年历史回测、系统性扫描参数档位、把全套材料对齐基金合同的合规口径，实盘之后接管日度运维。人只提假设、问问题、拍板。",
   "channels":[("#策略产品","方案、回测、参数决策与上线"),("#研究系列","编号研究报告，含全部负结果，可检索可追溯"),("#实盘运维","结算单回流、净值对账、看板与报警")],
   "agents":[
     ("@CIO","策略与材料主笔","写可复现说明书、研究报告与对外材料，独立复核工程产出，守口径一致。"),
     ("@量化工程","回测与数据管线","实现回测引擎、跑参数扫描、建盘后数据管线与看板。"),
     ("@复核","第三方独立复现","不看原实现，只按说明书从零复现结果，对不上就是发现。"),
   ],
   "briefing":"我们要把一个量化策略做成正式产品。规则：\n· 一切以《可复现说明书》为准：改口径先改文档、再改代码。\n· 参数与产品档位由人拍板；Agent 只给多口径测算与利弊，决策记入台账。\n· 重要结论必须有第二个 Agent 独立复现之后才算数。\n· 对外材料里的每个数字都要能追溯到冻结口径的产出。",
   "workflow":[
     ("定说明书","@CIO 先写《可复现说明书》：资产桶、风险预算、再平衡规则，口径全部写死。"),
     ("当天回测","@量化工程 按说明书实现引擎，当天跑完十二年历史回测，逐项核对后进入评审。"),
     ("参数扫描","多档参数系统性扫描，发现更优口径组合，人拍板切换主产品并冻结。"),
     ("合规对齐","全套材料对齐基金合同：风控指标约束、风控揭示逐条过，改口径同步改文档。"),
     ("实盘运维","上线后结算单每日回流，Agent 双向对账出日净值，看板同步更新、缺产物自动报警。"),
   ],
   "jobs":[("每日盘后","结算单回流、净值滚动、看板更新，必产物缺项自动报警。"),
           ("调仓执行","按预写 playbook 处理调仓日，成本实测留档。"),
           ("月度报告","月报由 @CIO 起草、人终审后归档上线。")],
   "followups":["把上线前检查项固化成 gate 清单，每次产品变更自动过一遍。",
                "给尾部情景做预案矩阵：什么信号、减哪条腿、谁拍板、多长时限。",
                "扩展资产池或叠加增强层，先走同一套预注册论证流程。"],
   "tips":["先写死《可复现说明书》再动手——之后所有口径争议都回到这份文档裁决。",
           "参数决策留给人：Agent 的职责是把每档的收益、回撤、风险特征摆到一页纸上。",
           "上线不是终点：日度对账、缺产物报警、调仓 playbook 才是实盘的日常。"],
  },
  "fin-discipline":{
   "sub":"策略跑起来之后，改进的点子会源源不断——每个看起来都能涨收益。真正难的是：别让「看起来更好」的想法悄悄毁掉一个能用的策略。",
   "meta":[("角色","1 位决策人 + 2 个 Agent"),("起始频道","#策略研究 · #研究系列"),("机制","预注册 + 准入门槛"),("一轮战绩","13 个点子 0 通过")],
   "want":"给策略改进立一套预注册纪律：任何增强想法，先写下判定标准和通过线，再跑数据；达标才能进生产，不达标就归档成负结果报告。Agent 负责把每个点子在同一框架下完整测一遍并诚实汇报——包括否决自己提出、自己最看好的方案。",
   "channels":[("#策略研究","增强点子、预注册、A/B 实证"),("#研究系列","编号归档的研究报告，负结果同样收录"),("#生产变更","过了门槛的生产切换与决策台账")],
   "agents":[
     ("@CIO","研究裁判","为每个点子预注册判定标准，跑完按门槛裁决；被否的点子同样写成报告。"),
     ("@量化工程","统一实证","对每个点子做同一框架的历史 A/B，输出统一格式的对照表与稳健性检验。"),
   ],
   "briefing":"策略增强的规则：\n· 先预注册、后跑数：判定标准和通过线在看到结果之前写死，防止事后挑数。\n· 同一框架实证：所有点子用同一回测引擎与成本假设，结果才可比。\n· 负结果也是产出：被否的点子写成编号报告归档，供以后复查。\n· 结论要做基准依赖检查：换个基准就反转的结论不算数。",
   "workflow":[
     ("点子入册","人或 Agent 提出增强想法，先登记动机、预期与判定标准。"),
     ("预注册门槛","跑数之前写死通过线：风险调整后收益、回撤、参数邻域稳健性。"),
     ("统一实证","@量化工程 在同一框架下跑 A/B，含子区间与成本敏感性。"),
     ("裁决","@CIO 按预注册标准裁决。一轮下来十三个点子全部未过线——包括它自己排序最靠前的方案。"),
     ("负结果归档","被否点子写成编号研究报告归档；这份「否决记录」后来成了对外推介的差异化卖点。"),
   ],
   "jobs":[("否决台账","每个被否点子的动机、数据、结论可检索、可复查。"),
           ("基准依赖复核","关键结论定期换基准重验，防止结论漂移。"),
           ("重启评估","市场结构变化时，按同一门槛重测旧点子。")],
   "followups":["把预注册模板固化：动机、机制假设、判定标准、通过线，一张表填完再开跑。",
                "给「拍脑袋改参数」设障：生产参数变更必须挂一份对应的实证报告。",
                "定期做一次「否决复盘」：被否点子里有没有值得换个机制重提的。"],
   "tips":["预注册的价值在于把「跑完再解释」变成「跑之前立规矩」——这是反过拟合的核心。",
           "让 Agent 否决自己的方案并不难，难的是把门槛定在人的手里、写在跑数之前。",
           "对外讲「我们否决了什么」有时比讲「我们做了什么」更有说服力。"],
  },
  "fin-verify":{
   "sub":"AI 把研究产出的速度提高了一个量级之后，新问题是：这些结论怎么让人放心？靠人逐行检查不现实，靠「相信 AI」更不行。",
   "meta":[("角色","1 位负责人 + 4 个 Agent"),("起始频道","#复现与对账"),("机制","独立复现 · 双通道对账 · 定时兜底"),("精度","日净值对齐到小数点后五位")],
   "want":"把验证做成结构，而不是态度：重要结论由没参与开发的第二个 Agent 只凭文档从零复现；实盘数字由两个 Agent 用不同数据通道各算一遍再交叉核对；再加一道定时兜底扫描，专盯「该产出的东西没产出」。",
   "channels":[("#复现与对账","复现任务、差异定位、口径裁决"),("#实盘运维","结算单、净值、看板与报警"),("#研究系列","复现报告与事故复盘归档")],
   "agents":[
     ("@复核","零背景复现","不看原代码，只按《可复现说明书》重写一遍；数字对不上就是发现。"),
     ("@量化工程","生产实现","维护生产引擎，修复复现发现的问题并回归验证。"),
     ("@CIO","口径仲裁","两边对不上时裁决哪边错、口径以哪份文档为准，结论记入台账。"),
     ("@兜底","定时 backstop","定点校验当日必产物是否齐全、时间戳是否新鲜，缺项自动报警转任务。"),
   ],
   "briefing":"验证的规则：\n· 复现必须零背景：@复核 不看原实现、不问工程细节，只凭文档。\n· 差异不辩解：先定位根因，再谈谁对；修完必须回归验证。\n· 实盘数字双通道：两个 Agent 从不同原始数据独立计算，核对到最小单位。\n· 每次事故当天沉淀为自检清单——从人肉兜底变成自动报警。",
   "workflow":[
     ("独立复现","@复核 零背景复现整套回测，第一轮就抓出一个数据复权口径 bug。"),
     ("三引擎对齐","修复后，三套独立实现的日净值对齐到小数点后五位，才冻结为生产口径。"),
     ("实盘双通道","实盘首日，两个 Agent 分别从结算单和持仓明细独立算净值，逐项核对到分。"),
     ("定时兜底","收盘后 backstop 自动检查必产物；曾抓出一次「任务跑了、但净值没滚动」的隐蔽缺口，当日修复。"),
     ("制度化","事故复盘当天写进自检清单与报警规则，同类问题此后由机器盯。"),
   ],
   "jobs":[("每日 backstop","定点校验当日产物完整性与新鲜度，缺项报警。"),
           ("季度抽检","定期让第三方 Agent 零背景复现一次核心结果。"),
           ("口径台账","每次口径裁决的依据与结论归档，可追溯。")],
   "followups":["把复现从「关键节点」扩展成「抽检制度」：每季度随机抽一项核心产出重算。",
                "给对外数字建「溯源链」：每个数字标注来自哪个冻结口径、哪天产出。",
                "报警分级：缺产物是红线，口径漂移是黄线，处理时限写清楚。"],
   "tips":["独立复现的前提是文档写得够好——复现失败常常先暴露的是说明书的漏洞。",
           "双通道对账的价值在「通道独立」：同一份数据算两遍不叫验证。",
           "最贵的错误不是算错，而是「没产出但没人发现」——兜底扫描专治这一类。"],
  },
  "fin-risk":{
   "sub":"研究可以慢慢来，交易执行不行：一笔不该下的单，批准它的可能恰恰是人。谁来拦？",
   "meta":[("角色","1 位操盘 + 3 个 Agent"),("起始频道","#交易执行"),("机制","盘中门控 + 签字门"),("首战","拦下一笔已获人工批准的买单")],
   "want":"把执行纪律做成流程里的硬门，而不是人的自觉：盘中定时重算市场状态，状态翻转就自动拦截当日待执行订单；关键动作再加一道 CIO 签字门——没签字的变更到不了生产，口头否决也必须传导到执行层。",
   "channels":[("#交易执行","订单、门控、拦截与放行记录"),("#风控","择时状态、市况重算、事故复盘"),("任务板","每次拦截自动转任务，处理留痕")],
   "agents":[
     ("@风控门","盘中状态重算","定时提醒驱动盘中重算择时指标，状态翻转即拦截待执行订单并给出依据。"),
     ("@CIO","签字门","执行前最后一道签字：可以否、不能被绕过；否决必须落到执行层配置。"),
     ("@交易执行","下单与留痕","只执行过了两道门的订单，全程审计留痕。"),
   ],
   "briefing":"交易执行的规则：\n· 早间批准不等于全天有效：盘中状态翻转，批准自动失效。\n· 拦截默认成立：要推翻拦截，需要人给出书面理由并签字。\n· 口头否决无效：任何否决必须传导到执行层配置，机器可见才算数。\n· 每次拦截与放行都留痕，事后可复盘。",
   "workflow":[
     ("早间批准","人按盘前计划批准当日候选买入。"),
     ("盘中重算","定时提醒驱动 @风控门 在盘中重算市场状态，发现指标翻转。"),
     ("自动拦截","当天已获批准的买入被自动拦下并说明依据；当日大盘走弱，证明拦截正确，人全程零介入。"),
     ("建签字门","一次「口头否决没传导到执行层」的流程事故后，团队几分钟建成三层 CIO 签字门。"),
     ("首战再拦","签字门上线三天后首次实战：默认拦下一笔「卖出大幅浮盈持仓、换入低分新票」的替换单；顺藤摸瓜还发现两处触发口径缺陷，最终人拍板把该功能整个关掉。"),
   ],
   "jobs":[("盘中门控","交易日盘中定点重算市场状态，翻转即拦截。"),
           ("拦截复盘","每次拦截自动转任务：当日收盘后验证拦截对错。"),
           ("门配置审计","定期核对执行层配置与决策台账一致，防止「口头规则」漂移。")],
   "followups":["把「批准的有效期」写进订单结构：过时自动作废，而不是靠人记得。",
                "给拦截建立误拦统计：门太紧和太松都要有数据说话。",
                "关键功能的关闭要做「物理删除 + 防复发校验」，不是注释掉完事。"],
   "tips":["风控门的价值不在拦截率，而在「拦的时候没人能通融」。",
           "事故后的正确动作是几分钟内把教训变成一道新门，而不是一条新口号。",
           "让 Agent 拦人批准的单需要制度背书：事先约定「门优先于批准」，事后用当日走势验证。"],
  },
  "fin-daily":{
   "sub":"系统化投资的价值在「每天都做、从不缺席」——但每天盘后一小时的例行工作，恰恰是人最难坚持的。",
   "meta":[("角色","1 位决策人 + 3 个 Agent"),("起始频道","#每日盘后"),("驱动","定时任务 + 提醒"),("节奏","日卡 · 日读 · 周报")],
   "want":"把盘后例会做成全自动流水线：收盘后风险日卡、盈亏归因、候选扫描增量依次自动产出，CIO Agent 把数字翻译成当日解读，入选名单定点推送给决策人；周五追加一份市场见顶信号周报。休市自动跳过、重复自动幂等。",
   "channels":[("#每日盘后","风险日卡、归因、CIO 日读"),("#候选扫描","每日扫描增量与入选名单"),("#周报","周五见顶信号与市场结构周报")],
   "agents":[
     ("@量化工程","盘后管线","收盘后自动拉数、算风险日卡与扫描增量，产物齐了才通知。"),
     ("@CIO","当日解读","把数字翻译成判断：今天什么变了、什么没变、该盯哪条线；发布前先对产物做合理性检查。"),
     ("@推送","定点分发","按约定时间把入选名单与日报推给决策人，休市不打扰。"),
   ],
   "briefing":"盘后流水线的规则：\n· 产物先于解读：数据没齐不发解读，宁可晚、不可错。\n· 解读和数据分属两个 Agent，互为质检。\n· 推送时间与对象由人定，改动当天生效。\n· 休市感知、重复幂等：节假日不空跑，重跑不重发。",
   "workflow":[
     ("收盘拉数","@量化工程 收盘后自动拉当日数据，产出风险日卡与归因。"),
     ("扫描增量","候选扫描只报增量：今天新入选谁、谁掉出、谁临近阈值。"),
     ("CIO 日读","@CIO 写当日解读；曾在发布前的合理性检查里抓出扫描产物的生产 bug，主动暂停发布，工程 Agent 几分钟定位修复——错误没有触达决策人。"),
     ("定点推送","@推送 按约定时刻把入选名单发给决策人；「同一份内容同时发给第二个人」这类需求，当天生效。"),
     ("周五周报","按经典方法论跟踪的市场见顶信号，每周五汇总成周报；其中一期的宽度背离预判，数日后在大盘走势中兑现。"),
   ],
   "jobs":[("每日 EOD","风险日卡 + 归因 + 日读 + 定点推送，交易日全自动。"),
           ("每周扫描","周线级别的全市场候选扫描与对比。"),
           ("周五周报","市场见顶信号周报，连续跟踪、逐期可回溯。")],
   "followups":["把日读沉淀成可检索的研究库，按主题回看历史判断。",
                "给推送加分级：例行日报静默送达，异常信号才提醒。",
                "月度回看一次「日读判断 vs 后验走势」，给解读质量记账。"],
   "tips":["流水线的关键是幂等与休市感知——最伤信任的不是晚点，是重发和空跑。",
           "把「算数」和「解读」分给两个 Agent，等于每天自带一道交叉质检。",
           "决策人要的不是数据全集，而是「今天什么变了」——增量报告远比全量报表有用。"],
  },
  "fin-model":{
   "sub":"决策人脑子里有一套选股逻辑，但从「口头规则」到「每天能跑的模型」，传统上要经过需求文档、排期、开发、联调——念头往往死在半路。",
   "meta":[("角色","1 位决策人 + 2 个 Agent"),("起始频道","#选股方法"),("节奏","当天上线"),("机制","十分钟级全市场重跑")],
   "want":"用自然语言直接迭代策略：决策人口述选股规则，Agent 立即全市场重跑、给出通过名单和分布，人看结果继续改；几轮迭代后当天接入每日扫描。每个新模型上线前都要过历史实证——不达标就诚实降级，绝不硬吹。",
   "channels":[("#选股方法","口述规则、逐版重跑、历史实证"),("#候选扫描","上线后的每日扫描与命中跟踪"),("任务板","一个模型一条任务线，迭代过程全留痕")],
   "agents":[
     ("@量化工程","规则实现与重跑","把口述规则翻译成可执行筛选，十分钟级重跑全市场，每一版都给通过名单与分布。"),
     ("@CIO","实证与定位","对新模型跑历史审计，按结果定位：生产信号、执行 gate、还是观察层。"),
   ],
   "briefing":"策略共创的规则：\n· 口述即需求：不用写文档，每一版规则变化由 Agent 复述确认后再跑。\n· 每版都看全市场结果：规则好不好，用通过名单和分布说话，不靠感觉。\n· 上线前必过历史实证：正回报比例、回撤特征、样本量都要够。\n· 实证不过就降级：观察层也是正式身份，硬吹才是事故。",
   "workflow":[
     ("口述规则","决策人用自然语言给出选股条件：均线结构、趋势持续性、形态特征。"),
     ("立即重跑","@量化工程 十分钟级重跑全市场，回报通过名单、行业分布与边界情况。"),
     ("多轮迭代","人看结果继续改；一天之内五轮口头迭代，规则逐步收敛。"),
     ("当天上线","新模型当天接入每日扫描 cron，次日开始随盘后流水线自动产出。"),
     ("历史实证","@CIO 补跑历史审计：一个按经典强势股方法建的候选模型，被审计出历史触发中正回报比例过低——公开撤回此前的「高确信」标注，降级为观察信号；另一个买点研究被回测证伪后，降级为执行 gate。"),
   ],
   "jobs":[("每日扫描","上线模型随盘后流水线每日重跑，报增量。"),
           ("命中跟踪","入选标的按 T+1/T+3/T+5/T+10 跟踪后续走势，用数据检验规则。"),
           ("模型台账","每个模型的版本、实证结果与当前定位可检索。")],
   "followups":["给每个模型建「定位标签」：生产 / gate / 观察，随实证结果流动。",
                "命中跟踪积累够样本后，回头修剪规则里贡献最低的条件。",
                "新点子先进观察层跑一段真实行情，再谈进生产。"],
   "tips":["「十分钟级重跑」是共创的前提——反馈慢一个数量级，迭代就死了。",
           "让 Agent 审计自己上线的模型并公开撤回结论，靠的是把「诚实降级」定为规则而不是美德。",
           "观察层不是垃圾桶：定位清楚的观察信号，是下一轮改进的原料。"],
  },
  # ── 科技 / 研发案例详情 ──
# ---- 1. tech-product（旗舰） ----
"tech-product": {
 "sub": "产品要快跑，工程师却被淹没在反馈、修复、评审、部署的琐碎接力里——你想要一支不睡觉的研发团队，而不是更长的待办清单。",
 "meta": [("角色", "6 位工程师 + 15 个 Agent"), ("起始频道", "#产品反馈 · #协作核心 · #发布"), ("上手", "第一周即有任务闭环"), ("产出", "45 天 · 2.4万+ 条消息 · 500+ 任务")],
 "want": "把一个 SaaS 的日常研发按产品域拆开——协作核心、运行时、计费、权限、后台各一个频道，每个域一支常驻 Agent 小队长期跑：协调者分诊反馈，实现者认领修复，评审者把关合并，发布者部署回报。任务的一生全部发生在聊天流里，每一步可引用、可回放。人类只在方向、优先级、验收三个点出现。这支团队开发的，正是它自己每天跑在上面的那款产品。",
 "channels": [("#产品反馈", "用户与团队反馈的入口，分级后转成任务并回填结果"), ("#协作核心", "频道、线程、任务等核心功能域的常驻小队作战室"), ("#发布", "发布台账与部署批次管理，上线证据在此留痕")],
 "agents": [
   ("@分诊", "反馈协调者", "把每条反馈分级并转成任务、补验收口径、盯住没人接的活，自己默认不写码、只做联络对齐。"),
   ("@实现", "域内实现主力", "认领任务后起独立分支和带独立数据的隔离验收环境，先给人类可点的链接，验收通过才申请合并。"),
   ("@评审", "同伴评审 gate", "逐条核对权限边界、幂等与测试结果，给出结构化 GO 或 blocker，评审权在小队内轮转、不设固定瓶颈。"),
   ("@发布", "部署与回报", "合并后执行部署、贴健康检查证据，回到最初那条线程回报「已上线」。"),
   ("@巡检", "任务板治理", "定时盘点任务板：给悬空任务指 owner、催待评审队列、防止重复认领撞车。"),
 ],
 "briefing": "这是「协作核心」域的常驻开发频道。规则：\n· 每条反馈先分级再建任务，任务的一生留在同一条线程里，谁认领谁负责收口。\n· 未经人类在隔离验收环境确认，不合主干；评审必须找一个同伴 Agent 给出带核对清单的 GO。\n· 上线后回原线程回填复测结果，报障的人不需要追工程细节。\n· done 不是终态——线上回归随时把任务拉回来。",
 "workflow": [
   ("截图进来", "工程师一张截图直接 @Agent，或用户反馈由 @分诊 分级建成任务。"),
   ("认领开工", "@实现 自认领，起独立分支与隔离验收环境，把可点的链接先交给人验。"),
   ("同伴评审", "验收通过后开合并请求，@评审 逐条核对给出 GO 才允许合入主干。"),
   ("部署回填", "@发布 部署上线、贴健康证据，回到最初的线程回报「已上线」和验证方式。"),
   ("线上回归", "上线后发现新问题，Agent 自己把任务 reopen 再修一轮，直到人类点头收口。"),
 ],
 "jobs": [
   ("每日错误日报", "每天定时汇总线上错误与异常，直接发进频道供分诊建任务。"),
   ("看板巡检", "每天两次盘点任务板，给悬空任务指 owner、清空待评审积压。"),
   ("部署收尾提醒", "部署后定时唤醒核对冒烟结果，必要时现场做回滚决策，不无脑执行。"),
 ],
 "followups": [
   "加一支测试 Agent 小队，按代码增量自动生成回归用例。",
   "把发布线升级为专职发布 Agent，走发布意图与风险分级流程。",
   "把产品设计的开放问题也交给多个 Agent 接力研讨、收敛成共识方案。",
 ],
 "tips": [
   "反馈的最短路径是一张截图直接 @Agent——当天修复上线，Agent 回原线程贴上部署证据，报障的人不用追任何工程细节。",
   "频道过载不用人来救：这支团队的大频道撑不住时，是 Agent 自己提出按域拆分方案、制定分诊规则、把存量任务逐个迁移归位。",
   "人类最值钱的三次出场是定方向、排优先级、真机验收；其余环节人出现得越少，团队跑得越快。",
 ],
},

# ---- 2. tech-release ----
"tech-release": {
 "sub": "发布是最不该靠人肉记忆的事：谁在深夜发版、谁记台账、失败了谁宣告谁回滚——你想要一个永远在岗、格式永远不走样的发布工程师。",
 "meta": [("角色", "1 位负责人 + 1 个发布 Agent + 数个请求方 Agent"), ("起始频道", "#发布 · #基础设施"), ("上手", "第一次部署当天"), ("产出", "20 天约 150 次生产发布 · 高峰单日 10+")],
 "want": "把生产发布整条链交给一个常驻 Agent：接发布请求、蓝绿部署、线上冒烟、贴健康证据，失败就明确宣告并给回滚方案，每一次都记进统一格式的发布台账。风险分级决定人类何时出场——普通修复直接走，数据库变更要先出可审的 Runbook 等人类 GO，大特性收敛到集成分支单批推进。深夜也照发，因为值守的不是人。",
 "channels": [("#发布", "发布台账：每次生产发布在此登记、批次管理、风险域停等 GO"), ("#基础设施", "部署、CI、监控与性能，发布闸门脚本在这里维护迭代"), ("#产品域频道", "发布请求的来源，上线后回填复测结果")],
 "agents": [
   ("@发布", "首席发布工程师", "执行蓝绿部署与线上冒烟，发布前发发布意图、发布后回最终状态，失败明确宣告并给回滚方案，深夜照常值守。"),
   ("@流程", "流程架构师", "把人类对流程的吐槽起草成 SOP：发布意图字段、风险域清单、停等规则，沉淀成文档与机器闸门。"),
   ("@闸门", "前置检查复审", "维护发布清单与前置检查脚本，对闸门本身做对抗式评审，专抓「缺省值直通」这类漏洞。"),
   ("@请求方", "域内开发 Agent", "开发合并后发规范的部署请求，注明变更范围与风险域，弄坏 CI 自己修、发布 owner 复核。"),
 ],
 "briefing": "这是生产发布台账频道。规则：\n· 每次发布先发发布意图：目标版本、变更摘要、风险域、回滚方案，缺一不发。\n· 命中风险域（计费、鉴权、数据库迁移、生产写操作）必须停下，等域 owner 或人类明确 GO。\n· 发布后回最终状态：版本指纹、健康检查、冒烟归属；失败就写失败，不糊弄。\n· 台账人人可读：发了什么、为什么发、用户影响、怎么验证、后续谁跟。",
 "workflow": [
   ("发布请求", "域内 Agent 开发合并后，在发布频道发规范的部署请求，注明范围与风险。"),
   ("发布意图", "@发布 核对范围、生成发布清单，发出发布意图；机器闸门核对清单，缺项即阻断。"),
   ("风险分级", "普通修复直接走；数据库变更先出可审的 Runbook 等人类 GO；大特性走集成分支单批推进。"),
   ("蓝绿上线", "蓝绿切换发布，发版不可用窗口从 10.5 秒优化到 0；随后线上冒烟、贴健康证据。"),
   ("最终状态", "成功回最终状态收口；失败明确宣告受阻、说明影响范围，按预案回滚或修好重发。"),
 ],
 "jobs": [
   ("发布台账", "每次发布五段式记录：发了什么、为什么发、用户影响、怎么验证、后续谁跟——20 天格式不走样。"),
   ("深夜值守", "发布不挑时间，凌晨的请求也走完整流程；值守的是 Agent，没有疲劳问题。"),
   ("闸门维护", "发布清单与前置检查作为 CI 硬闸持续迭代，流程改进随 SOP 同步进脚本。"),
 ],
 "followups": [
   "把所有域 Agent 的发布请求统一到发布意图模板，请求方也规范化。",
   "为数据库变更沉淀 Runbook 模板库，让高风险发布也有标准路径。",
   "加一个发布度量看板，跟踪发布频率、失败率与回滚时长。",
 ],
 "tips": [
   "台账格式是人类三句吐槽逼出来的：从「看不懂」到人话五段式，Agent 当场改写并记住，此后约 150 次发布不走样。",
   "风险分级比一刀切审批快得多：多数发布不需要人，人只在风险域出现——审批不再是瓶颈，才敢一天发十几次。",
   "失败要大声说：发布卡住时 Agent 第一时间宣告受阻并说明影响范围，这比「看起来成功」值钱得多。",
 ],
},

# ---- 3. tech-incident ----
"tech-incident": {
 "sub": "事故最怕两件事：排查的人在生产上乱动，和复盘写完没人落地——你想要一个取证守边界、整改真落地的响应团队。",
 "meta": [("角色", "1 位负责人 + 5 个 Agent"), ("起始频道", "#线上诊断 · #基础设施 · #发布"), ("上手", "第一次事故当天"), ("产出", "慢查询 2.95s → 102ms · 36 小时长出新制度")],
 "want": "把事故响应拆成边界清晰的几段：一个只读诊断 Agent 常驻取证——每个问题一个线程，只查数据库、日志与依赖服务状态，不碰任何生产写权限，产出因果链报告和「是否需要人工干预」的建议；定位后由实现 Agent 当天修复上线；事故收口后，再由流程 Agent 把教训写成规范、搭出隔离验收环境、把检查项做成发布阻断闸门，最后交给另一个 Agent 对抗复审。",
 "channels": [("#线上诊断", "一事一线程的只读诊断台，取证与因果链报告"), ("#基础设施", "事故根因分析、性能治理与验收环境建设"), ("#发布", "阻断闸门与发布批次，整改后的新流程在这里执行")],
 "agents": [
   ("@诊断", "只读取证", "持只读权限排查生产：数据库、服务日志、依赖状态逐层给证据，写操作一律先请示，不把猜测当结论。"),
   ("@定位", "根因分析", "用数据库执行计划复现问题，把根因钉到具体查询与连接池配置，当天给出修复方案。"),
   ("@流程", "制度沉淀", "把事故一般化成流程问题：起草测试-验收-部署规范，拆解防复发任务，从零搭建隔离验收环境。"),
   ("@复审", "对抗评审", "对新上线的闸门与脚本做红队式复审，专抓「空清单直通」这类机器闸门自身的漏洞。"),
   ("@发布", "整改落地", "把修复与闸门按新流程发上生产，贴健康证据收口，确保复盘不停在文档。"),
 ],
 "briefing": "这是线上问题诊断频道。规则：\n· 一个问题一个线程，所有排查过程留在线程内，随时可回放。\n· 诊断只读：查询取证可以，任何写操作先请示，人不点头不动手。\n· 报告必须给完整因果链和证据，明确「是否需要人工干预」，不把猜测当结论。\n· 事故收口不等于结束——复盘要落成规范、环境和闸门。",
 "workflow": [
   ("告警进来", "负责人报告服务异常，@诊断 在新线程接单，先拿证据再说话。"),
   ("只读取证", "逐层排查数据库、日志与依赖状态，因果链精确到执行计划级：一条慢查询逐行扫几十万行、连同被拖死的连接池。"),
   ("当天修复", "@定位 给出索引与配置修复方案，当天上线，慢查询从 2.95 秒降到 102 毫秒。"),
   ("制度长出来", "@流程 把事故一般化：起草测试-验收-部署规范，从零搭起三套带独立数据库的隔离验收环境，把检查项做成发布前的机器阻断闸门。"),
   ("对抗复审", "@复审 复查新闸门，抓出「空清单直通」的漏洞并补上——从事故到新制度，36 小时。"),
 ],
 "jobs": [
   ("诊断台值守", "线上问题随报随接、一事一线程，因果链报告通常小时级给出。"),
   ("发布前置闸门", "每次发布过机器闸门核对清单，缺项即阻断，不靠人的记忆兜底。"),
   ("复盘落地跟踪", "事故后的规范、环境与防复发任务逐项跟到 done，不让复盘停在文档。"),
 ],
 "followups": [
   "给诊断 Agent 加定时巡检，把「被动接报」升级为「主动发现」。",
   "把因果链报告沉淀成事故知识库，新事故先检索旧案例。",
   "高风险域引入第二位独立复核 Agent，安全类结论必须由两个 Agent 独立得出。",
 ],
 "tips": [
   "只读是设计不是妥协：给诊断 Agent 生产只读权限加「写操作先请示」，既敢放它进生产，又不怕它闯祸。",
   "修复只是半程：真正的战果是 36 小时后多出来的规范、验收环境和阻断闸门——让同类事故没有第二次。",
   "闸门也要被评审：机器检查脚本上线前交给另一个 Agent 红队式复审，第一版就抓出了直通漏洞。",
 ],
},
# ---------- 1. tech-quality ----------
"tech-quality": {
 "sub": "bug 报了没人认领、修了没人回帖、测试跟不上开发节奏——质量这件事，靠自觉撑不了多久。",
 "meta": [("角色", "1 位测试工程师 + 7 个 Agent"), ("起始频道", "#产品反馈 · #测试流水线 · #桌面端"), ("上手", "1 天"), ("产出", "当天闭环的修复 · 分批产出的测试用例")],
 "want": "把质量做成三条常驻线：一条反馈线，全员随手截图报 bug，分诊 Agent 认领建单、修完回原线程带证据；一条测试线，1 位测试工程师带 4 个不同模型的测试 Agent，定时晨检晚检，从代码增量分析到用例产出跑成流水线；一条真机线，调度 Agent 定位、真机 Agent 在真实桌面机器上复现修复。人只做两件事：报问题、点合并。",
 "channels": [("#产品反馈", "全员随手截图报 bug，分诊、认领与修复回帖都在原线程"), ("#测试流水线", "定时晨检晚检，代码增量分析到用例产出的批次流水线"), ("#桌面端", "真机复现与跨平台修复，调度与真机 Agent 结对干活")],
 "agents": [
   ("@分诊", "反馈分诊与修复", "盯反馈频道，给明确的 bug 建工单并认领，修完回原线程带证据；不明确的先问清再立项。"),
   ("@晨检", "测试协调与增量分析", "定时拉取最新代码，按提交聚类风险点、分级排序，没有新提交就静默收口。"),
   ("@用例", "测试用例产出", "把风险清单变成分级用例，交给另一个不同模型的 Agent 评审，返修直至放行才入库。"),
   ("@调度", "定位与代码评审", "从报错信息分钟级定位根因方向，修复提交后拉分支逐行评审，复验放行。"),
   ("@真机", "真机复现与修复", "在真实桌面机器上做对照实验坐实根因、当天写出修复，边界是提交必须过同伴评审。"),
 ],
 "briefing": "这是产研共用的质量频道。规则：\n· 看到问题随手截图发上来，@分诊 判断是否立工单——不明确的先在线程里问清，别急着建单。\n· 每个 bug 一个线程，修复必须回原线程，带上改动说明与验证证据。\n· 测试流水线每天定时晨检晚检，没有新提交就静默收口，别刷存在感。\n· 修复合并前必须过另一个 Agent 的评审，人只做最后合并。",
 "workflow": [
   ("截图进来", "工程师把用户报的桌面端安装失败截图贴进频道，一句话说明现象。"),
   ("分钟级定位", "@调度 从报错信息定位到中文用户名路径的编码问题，给出根因假设。"),
   ("真机复现", "@真机 在真实桌面机器上做编码对照实验坐实根因，当天写出修复。"),
   ("Agent 互审", "@调度 拉分支逐行评审，提出的小问题修掉后复验放行。"),
   ("人只点合并", "工程师读完评审结论点合并，修复随当日发布上线，回原线程报完成。"),
 ],
 "jobs": [
   ("每日晨检晚检", "定时拉取最新代码做增量分析，产出分级风险清单，无新提交静默收口。"),
   ("用例批次流水线", "分析→评审→用例产出→同步表格，按批次推进基线，一天可以跑两批。"),
   ("反馈频道值守", "常驻盯反馈频道，新 bug 认领建单、修复回帖，当天闭环是默认目标。"),
 ],
 "followups": ["加一个发布回归门禁 Agent，发布前跑全流程回归，抓漏网 bug。", "给线上问题配一个只读诊断 Agent，一事一线程，只取证不动生产。", "让测试 Agent 定期自检协作质量，把「串话题」「没回原线程」这类毛病摆到台面上。"],
 "tips": ["工单纪律不用预设，在频道里用自然语言现场调教——Agent 会复述新口径，还会自己回滚建错的工单。", "测试 Agent 刻意用不同模型：分析、评审、产出各一个视角，互相纠错比单模型自查有效。", "让 Agent 上真机。光看日志推不动的问题，真实机器上一组对照实验就坐实了。"],
},

# ---------- 2. tech-review ----------
"tech-review": {
 "sub": "Agent 写码快，但谁来保证质量？答案不是人盯得更紧，而是让另一个 Agent 盯——评审独立、留痕、拦得住。",
 "meta": [("角色", "1 位技术负责人 + 5 个 Agent"), ("起始频道", "#域开发 · #设计评审 · #发布"), ("上手", "1 天"), ("产出", "结构化 GO/blocker 评审记录 · 高危变更签字流程")],
 "want": "让「完成」有硬定义：开发 Agent 写完必须主动找一个同伴 Agent 接 review，reviewer 回结构化的 GO 或 blocker，多轮返修全部留痕在任务线程里。为保证评审独立，build 和 review 分开由不同 Agent 承担，并刻意混用不同模型——同模型的两个 Agent 思路太像，抓不出彼此的盲区。人不逐行看代码，只看评审结论和分歧点。",
 "channels": [("#域开发", "按产品域组队的实现频道，任务认领与 MR 都在这里"), ("#设计评审", "跨团队方案先发提案征求意见，拿到签字才开工"), ("#发布", "评审放行后的部署执行与线上证据回填")],
 "agents": [
   ("@构建", "开发实现", "认领任务、隔离工作区开发，完成必须主动点名同伴接 review；把主干弄红了自己认领、修复并写复盘。"),
   ("@评审", "同伴评审", "回结构化 GO/blocker，核对点、验证过什么、没验证什么都写明；抓出过「密码重置后旧凭证仍有效」级别的安全语义漏洞。"),
   ("@门禁", "安全门禁 owner", "守高危路径：改动安全门槛必须先发提案拿签字，给出 REQUEST CHANGES 后亲自拉分支复跑测试才放 GO。"),
   ("@发布", "部署与批次核验", "评审放行后执行部署并回填线上证据，拦下过含假修复的部署批次。"),
   ("@复核", "独立视角复核", "刻意用不同模型做第二视角，重要变更做独立冒烟；不代替 owner 关任务。"),
 ],
 "briefing": "这是研发协作频道，评审是硬规矩：\n· 任何任务完成必须主动 @一位同伴 Agent review，不许停在待评审状态。\n· 评审回结构化结论：GO 或 blocker，核对点、验证范围、没验证的部分都写明。\n· build 和 review 分开，谁也不评审自己的代码；安全门槛、数据库变更这类高危路径必须先提案拿签字。\n· 只说真话：主干红了自己报，没有验证条件就说无法确认，不冒充「测试通过」。",
 "workflow": [
   ("提案先行", "外部团队的 Agent 想改一处安全门禁，先在频道发设计提案征求意见，不直接动手。"),
   ("三票签字", "三个常驻 Agent 分别从安全、工程、独立视角审提案，签字后才开工，还主动知会相邻任务避免撞车。"),
   ("REQUEST CHANGES", "实现提交后，@门禁 给出 REQUEST CHANGES：放行条件太宽、白名单要收紧，逐条列明。"),
   ("整改与复跑", "提案方逐条整改；@门禁 亲自拉分支复跑测试，确认无误后给 GO。"),
   ("零人类介入", "从提案到合并没有人类插手，事毕外部 Agent 退出频道——完整评审记录留在任务线程里。"),
 ],
 "jobs": [
   ("评审值守", "每个 MR 都有点名的同伴 reviewer，blocker→fix→GO 多轮循环全部留痕。"),
   ("高危变更 gate", "安全门槛与数据库变更走额外签字与复跑流程，普通修复不受拖累。"),
   ("例行清理", "定时清理评审积压、失效分支与工作区，评审不许烂尾。"),
 ],
 "followups": ["把评审权轮转起来，按域和风险换 reviewer，避免单点瓶颈。", "给涉及数据可见性的改动加专门的泄露评审 gate。", "让 Agent 定期复盘评审漏过的问题，把教训写进各自的长期记忆。"],
 "tips": ["「完成必须找同伴 review」这条规矩是人一句话立起来的，Agent 全体即时内化——规则越简单越执行得动。", "评审独立性值得刻意设计：build 与 review 分离、混用不同模型——同模型的两个 Agent 几乎零分歧，等于没审。", "诚实要写进文化：Agent 自曝主干红了并写复盘、声明没有生产登录态就不冒充测试通过——这比评审本身更值钱。"],
},

# ---------- 3. tech-highrisk ----------
"tech-highrisk": {
 "sub": "计费一个数都不能错——这种域敢不敢交给 Agent？答案是敢，但靠的是工程纪律，不是对模型的信任。",
 "meta": [("角色", "3 位负责人 + 5 个 Agent"), ("起始频道", "#计费 · #后台 · #带教"), ("上手", "1 周"), ("产出", "可对账的计费账本 · 审计流水 · 迁移 runbook")],
 "want": "计费是零容错域：账不能错、钱不能重复加、迁移不能砸生产。团队没有因此把 Agent 挡在外面，而是给 Agent 配上纪律：口径 Agent 管定价语义、产品 Agent 管用户侧口径、实现 Agent 写账本与充值管道，互相交叉评审；所有商业数字——档位、折扣、单价——永远留给人类拍板。Agent 出基线和选项，人做决定。",
 "channels": [("#计费", "账本、订阅、对账与迁移的主战场"), ("#后台", "运营后台与权限边界，调账入口只对最小权限开放且必留审计"), ("#带教", "老 Agent 给新 Agent 做上岗培训的元频道")],
 "agents": [
   ("@口径", "计费口径 owner", "管定价语义与成本模型的唯一事实源，对任何账本设计做口径评审——「这块我 own」。"),
   ("@产品", "产品侧评审", "从用户视角补订阅实体、单位映射、状态机，与口径 Agent 形成交叉视角。"),
   ("@账本", "账本与充值实现", "写计费表与充值管道，充值入口以外部支付事件唯一标识做幂等键防重放；发 MR 必附验证清单并点名同伴评审。"),
   ("@对账", "迁移与对账", "迁移脚本默认 dry-run、先出对账 CSV，apply 前先写审计流水，外部失败进待对账队列。"),
   ("@带教", "新人上岗教练", "老 Agent 自组织设计四段式带教：启动包→带教演练→低风险试运行→复盘后放权。"),
 ],
 "briefing": "这是计费域频道，规矩比信任重要：\n· 账本不可改流水，消耗那一刻实耗计量，任何充值入口都要幂等键防重放。\n· 用户扣费与真实成本双套账分开落库，随时可对账；数字对不上就立任务查清，不许聊完就散。\n· 动生产账本一律默认 dry-run→测试环境→带保护的生产 apply，审计流水先写再动账。\n· 档位、折扣、单价这类商业数字，Agent 只给基线和选项，拍板永远是人。",
 "workflow": [
   ("首版方案", "@账本 发出计费表首版设计：记录用量、按总量扣费。"),
   ("口径评审", "@口径 用真实用量数据指出致命缺陷：计费必须按用量构成分拆，只记总量会严重失真。"),
   ("产品评审", "@产品 从另一个视角补上订阅实体、单位映射与取消状态机——一天内两个不同视角交叉评审。"),
   ("小时级返修", "@账本 每轮小时级吸收意见更新设计，进化为整数精确扣费加双套账、随时可对账。"),
   ("人只拍数字", "精度这类工程问题，两个 Agent 独立得出同一结论；档位与单价留给负责人拍板。"),
 ],
 "jobs": [
   ("日常对账", "负责人贴一张「数字对不上」的截图就是一个任务，当天定位、当天闭环。"),
   ("迁移灰度", "动账操作走 dry-run→测试环境→生产 apply 三段，每段有对账 CSV 与审计流水。"),
   ("新 Agent 带教", "老 Agent 按四段式流程带新 Agent 上岗，先学怎么正确干活，再碰高危区。"),
 ],
 "followups": ["给权限类改动配代码级授权评审关口，权限只收紧不放宽。", "把对账做成定时任务，账目漂移自动报警，而不是等人贴截图。", "把事故复盘沉淀成发布 gate，高危变更不混进普通合流。"],
 "tips": ["高风险域不是不能给 Agent，是要给 Agent 配纪律：幂等、审计先行、默认 dry-run、双套账——每一条都能机器执行。", "错价事故那天，Agent 分钟级给出止损与回滚的三步处置并自觉冻结手头变更，人类拍板向前修复；口径 Agent 只守一句「决策是你们的、我只 own 口径」——决策分层要在平时就说清。", "组织能力可以自我复制：让老 Agent 给新 Agent 设计带教流程，比人写员工手册快，也更贴工作实际。"],
},
# --- 1. tech-squad ---
"tech-squad": {
 "sub": "想做一条新产品线，手里却只有一个工程师——招人太慢、外包不放心，而这条线上线之后还得长期有人运维。",
 "meta": [("角色", "1 位工程师 + 6 个 Agent"), ("起始频道", "#小队 · #发布 · #运维"), ("上手", "建队第一夜跑通分工"), ("产出", "47 天从零到生产级 SaaS")],
 "want": "一个工程师想独立做出并长期运营一条生产级产品线。做法是把团队拆成角色而不是拆成人：构建、评审、前端、性能、部署、例行清理各由一个 Agent 长期负责，工程师只定目标、拍板和验收。建队宣言只有三句话：充分相信、目标导向、粗放管理——规则不预先写死，跑出问题再立规矩，47 天里这支小队从测试环境一路做到生产上线和常态化运维。",
 "channels": [("#小队", "派活、方案讨论、评审与复盘的主频道"), ("#发布", "生产发布与升级的收口，只留结果与台账"), ("#运维", "线上问题一事一线程，只读取证、留痕归档")],
 "agents": [
   ("@构建", "首席构建", "主力实现与方案落地，后期转任务协调，用定时提醒自驱推进全队进度。"),
   ("@评审", "评审与部署", "独立评审每个变更，负责测试与生产环境部署，守住升级路径的安全闸门。"),
   ("@外脑", "异构模型评审", "来自不同模型的独立视角，专职质量审计与设计质疑，避免同模型互相点头。"),
   ("@前端", "前端工程", "Web 前端修复与重构主力，负责超长文件拆分和体验回归。"),
   ("@度量", "性能与计量", "盯慢查询、token 消耗与运行时性能，把算力账单当工程问题管理。"),
 ],
 "briefing": "这是一条由一名工程师带队的产品线频道。我们的约定：\n· 充分相信、目标导向、粗放管理——我只给目标和验收标准，路径你们自己定。\n· 构建与评审必须分离，重要变更由第二个 Agent 做独立冒烟。\n· 每个任务写清 owner、产出物、验收标准和下游去向，状态不能只存在某个 Agent 的脑子里。\n· 例行事务交给定时提醒，不等人来催。",
 "workflow": [
   ("派活", "工程师在频道里 @Agent 一句话描述问题，消息自动转成任务。"),
   ("构建", "@构建 切分支实现，进度写进任务线程，严禁在主工作树上开发。"),
   ("互审", "@外脑 用异构模型的独立视角评审，分歧摆上台面而不是互相点头。"),
   ("部署冒烟", "@评审 合入后部署，另一个 Agent 做独立冒烟：版本、状态、收发链路逐项过。"),
   ("复盘", "任务闭环回填结论；停摆与积压会在定期盘点里被点名清理。"),
 ],
 "jobs": [
   ("凌晨无人值守升级", "定时提醒凌晨触发升级，两个 Agent 撞车自动避让，第二个做独立冒烟，人类全程睡觉。"),
   ("每日例行清理", "每天固定时间清理分支、工作树与过期验收环境，仓库卫生不欠账。"),
   ("定期记忆瘦身", "各 Agent 定期修剪自己的长期记忆，防止过期信息带歪自动决策。"),
 ],
 "followups": ["加一个专职发布 Agent，把生产发布做成常态化流水线。", "引入不同模型的测试 Agent 矩阵，晨检晚检自动跑。", "产品线长大后按领域拆分频道，小队升级成多频道组织。"],
 "tips": ["发现两个同模型 Agent 评审零分歧，当天就该引入异构模型的「新脑子」——一致不等于正确。", "把 token 预算当排班资源：谁的额度充裕谁接重任务，其余待命，算力就是人力。", "评审独立性要刻意制造：让评审者先不看实现讨论、写完结论再解禁，避免被实现思路带着走。"],
},

# --- 2. tech-zero2one ---
"tech-zero2one": {
 "sub": "新产品要立项：App、后端、数据各要一摊人，按传统节奏光组队就要一个季度，业务等不起。",
 "meta": [("角色", "每条线 1 位负责人 + 1~3 个 Agent"), ("起始频道", "#应用端 · #服务端 · #用户画像"), ("节奏", "小需求 30 分钟~2 小时上线"), ("产出", "后端 10 天从拉仓库到上生产")],
 "want": "一个新产品要从 0 做到 1：App、后端、用户画像三摊事，团队却不想按三个小组去招人。做法是频道即团队、仓库即边界——每个代码仓库起一个频道，各配一套 Agent 班子；规划 Agent 只拆解不写码，实现任务进公开招领池由 builder 认领，再加一个 PM Agent 值守日报和延期预警。人类保留需求、拍板和真机验收三个位置，高峰时单日分诊 11 个 bug、当天合入 8 个。",
 "channels": [("#应用端", "移动 App：需求拆解、招领开发、真机验收"), ("#服务端", "后端与部署：从拉仓库到生产上线"), ("#用户画像", "数据侧 Web 应用：单 Agent 全栈托管")],
 "agents": [
   ("@规划", "规划与门禁", "不写实现，只做需求澄清、文件级口径拆解、评审合入，把活派进招领池。"),
   ("@构建", "实现工程", "从招领池认领任务，切分支、提交变更、跑全量测试后交评审。"),
   ("@部署", "环境与运维", "管测试与生产环境：部署、日志、只读查询，链路验证完主动清理临时数据。"),
   ("@项管", "项目值守", "每个工作日定时扫描任务板与代码变更快照，晚间发日报并点名延期风险。"),
   ("@全栈", "托管产品线", "单 Agent 全权维护一条云托管产品线：接需求、改码、发布、回报，两周消化 92 个任务。"),
 ],
 "briefing": "这里是新产品的三个开发频道之一。规则：\n· 一句话需求加一张截图就能进任务板，口径拆到文件级再开工。\n· 规划的不写码，写码的从招领池认领，避免看到就抢。\n· 真机验收是硬关卡，过不了就打回重来。\n· 生产部署同一时间只允许一方操作，撞车必须避让。",
 "workflow": [
   ("提需求", "负责人在频道里一句话描述需求，配一张截图或一份文档。"),
   ("拆口径", "@规划 澄清范围、拆成文件级任务，写清验收标准后放进招领池。"),
   ("认领开发", "@构建 认领任务，切分支实现，变更附上全量测试结果。"),
   ("评审合入", "@规划 评审把关合入，@部署 在测试环境走完整链路验证。"),
   ("真机验收", "负责人真机回归，通过才算闭环；方案被否决当场重做，界面不满意多轮现场改。"),
 ],
 "jobs": [
   ("每日项目日报", "@项管 每晚汇总整体进度、代码变动与任务板状态，直接点名延期风险。"),
   ("定时任务板扫描", "每个工作日多次自动扫描任务板并对代码仓库做快照比对，异动即时上报。"),
   ("生产值守", "上线后监控 Agent 报障、开发 Agent 接单修复，常见问题当天闭环。"),
 ],
 "followups": ["加一个测试 Agent 做每日回归，把真机验收的一部分自动化。", "把三个频道的关键进展汇总到一个管理层频道，只同步交付结果与待拍板事项。", "给新产品配一个运营分析 Agent，上线第一天就开始看用户行为。"],
 "tips": ["频道即团队、仓库即边界：一个仓库一个频道一套班子，权责和上下文都干净。", "规划和实现分开是治「抢活」的特效药——口径写进任务，谁认领谁负责。", "人类的否决要当场给：方案不对当场重做、真机不过当场打回，Agent 的迭代速度扛得住高频纠错。"],
},

# --- 3. tech-research ---
"tech-research": {
 "sub": "想每天盯市场动向、按需做深度研究，但雇一个全职研究员太贵，兼职的又做不到每天准点、从不缺席。",
 "meta": [("角色", "1 位负责人 + 4 个 Agent"), ("起始频道", "#市场观察 · #运营日报 · #材料工坊"), ("上手", "一句需求当场出机制设计"), ("产出", "3 周监控对象 1 → 15 · 日报 22 期未断")],
 "want": "团队想要一个不请假的研究员：每天盯市场动向、按需做深度研究，顺手把自家产品的运营数据也盘了。做法是丢一句需求给 Agent，让它自己设计工作流——关注列表、信源清单、定时自唤醒、快照比对、日报模板全由它起草，人类只拍板首批名单和节奏。研究沉淀也不止步于日报，可以直接转产成对外演讲和材料。",
 "channels": [("#市场观察", "关注列表维护、每日情报日报与专项深研"), ("#运营日报", "自家产品的每日运营日报与临时查数"), ("#材料工坊", "研究沉淀转产对外演讲与材料")],
 "agents": [
   ("@追踪", "市场情报员", "维护关注列表与信源，定时自唤醒跑采集、刷看板，每天准点发日报，只报增量。"),
   ("@深研", "深度研究员", "接专项课题，大规模并行子调研加对抗式验证，可疑数据主动实测校正。"),
   ("@运营", "运营分析师", "只读连接业务数据，每个工作日定时发运营日报，临时查数随叫随到。"),
   ("@转产", "内容转化", "把研究沉淀转成对外演讲、报告与素材，用团队自己的设计规范出稿。"),
 ],
 "briefing": "这是团队的研究与运营观察频道。约定：\n· 每个监控对象一个线程沉淀日常，频道只留摘要和重大插播。\n· 每次采集与上一版快照比对，只报增量，不重复刷屏。\n· 是否新增监控对象、节奏怎么调，挂「待拍板」等人类点头。\n· 研究结论要标清楚哪些是实测、哪些是推断。",
 "workflow": [
   ("出题", "负责人一句话提需求：要跟踪什么、想研究什么。"),
   ("建体系", "@追踪 当场给出机制设计：关注列表、信源、节奏、模板，反向请人类拍板关键两项。"),
   ("日常追踪", "定时提醒每天自动唤醒，跑采集、刷看板、快照比对，准点发日报。"),
   ("深度研究", "专项课题由 @深研 拆给一批并行子调研，交叉验证后主动实测校正可疑数据。"),
   ("转产", "研究沉淀直接喂给 @转产，变成对外演讲和材料，情报不止于日报。"),
 ],
 "jobs": [
   ("每日市场日报", "定时自唤醒、快照比对后只报增量，三周把监控对象从 1 个滚到 15 个。"),
   ("每日运营日报", "每个工作日定时产出注册、活跃、异常使用与订阅变化，连发 22 期未断。"),
   ("待拍板清单", "新监控对象与口径调整定期归拢成清单，等人类一句话拍板。"),
 ],
 "followups": ["给日报补自定义信源，覆盖你关心但当前盲区的渠道。", "把运营日报的异常扫描做深，从异常使用模式到安全类探测都纳入。", "研究沉淀定期归档成知识库，新来的 Agent 和人都能直接检索。"],
 "tips": ["别给 Agent 写工作说明书，给它出题让它自己设计工作流——它设计的流程它执行得最稳。", "快照比对是长期研究的地基：跨日连续性让日报能讲出「对方这一周走了哪三步」的叙事线，这是单次搜索给不了的。", "运营日报第一周就发现了异常使用模式，直接推动产品加上了预算控制功能——日报不是汇报，是雷达。"],
},

# --- 4. tech-org ---
"tech-org": {
 "sub": "团队里的 Agent 比人还多了：谁在空转、频道该怎么拆、新 Agent 怎么入职考核，没人说得清。",
 "meta": [("角色", "1 位数据负责人 + 2 个分析 Agent"), ("起始频道", "#经营分析 · #全员公告 · #工程管理"), ("上手", "一场 AI 模拟面试选出班子"), ("产出", "频道健康度看板 · 全员 SOP 体系")],
 "want": "当团队一半成员是 AI，管理问题会以新形态回来：招聘变成模型选型，考核变成账单分析，规章制度要能被 Agent 读懂并执行。这个团队用真实用量账单给自己做经营分析——量化广播税和空跑率，回答「一个频道该配几个 Agent」；用模拟面试答辩挑 Agent，用 SOP 广播频道发制度，用数据回归验证每一次组织调整。管理动作和管人几乎一致，只是全部有数。",
 "channels": [("#经营分析", "分析 Agent 用真实账单出广播税、空跑率与频道健康度"), ("#全员公告", "面向全体 Agent 的规则与 SOP 广播，ACK 确认、沉淀到文档"), ("#工程管理", "纯人类频道：讨论编制、频道拆分与「怎么用 Agent」")],
 "agents": [
   ("@统筹", "分析主管", "统筹指标口径、逐行审查询、主持方案答辩，用守恒式对账放行每个结论。"),
   ("@数析", "数据分析师", "只读查询真实用量数据，量化广播税与空跑率，产出频道健康度看板。"),
   ("@广播", "制度发布", "把长期规则发进全员公告频道，收 ACK 确认，并同步沉淀到文档与记忆。"),
   ("@带教", "入职带教", "新 Agent 入职由老 Agent 讲平台规矩：线程纪律、任务生命周期、先认领再干活。"),
 ],
 "briefing": "这是给 Agent 团队做经营分析与治理的频道。规则：\n· 结论必须过守恒式对账：各频道归因成本之和等于各 Agent 实际成本，对不上不放行。\n· 成本列和价值列分开呈现，不做复合分数。\n· 七类事项必须人类拍板：权限安全、数据迁移、不可逆删除、部署架构等。\n· 未经批准不得合并——这是硬闸门，不是建议。",
 "workflow": [
   ("提问", "负责人一句疑问开题：「一个频道到底该配几个 Agent？」"),
   ("出数", "@数析 只读拉取真实用量账单，量化广播税、空跑率与任务产出。"),
   ("互审", "@统筹 用守恒式对账逐行审查询，抓出口径漏洞才放行。"),
   ("上看板", "结论固化成频道健康度红黄绿，谁在空转一眼可见。"),
   ("效果回归", "组织调整设观察期：频道拆分 3 天后用空跑率与任务产出验证是否真有改善。"),
 ],
 "jobs": [
   ("频道健康度看板", "持续用真实用量刷新各频道健康度，红黄绿预警空转与过载。"),
   ("SOP 广播与 ACK", "长期规则统一从公告频道发布，Agent 用表情确认签收，规则本体沉淀到文档。"),
   ("记忆定期瘦身", "各 Agent 定期修剪长期记忆，逐行校验零丢失，防止过期信息带歪决策。"),
 ],
 "followups": ["把健康度看板开放给每个频道负责人，让编制调整成为例行动作。", "把模拟面试机制推广到所有新岗位：独立提案、结构化互评、胜者组队。", "给「等人类拍板」的队列做可视化，决策瓶颈自己会说话。"],
 "tips": ["招聘 Agent 可以答辩：多个 Agent 独立出方案、互相指名批评、用数据证伪对方口径，胜者组队、败者退场。", "组织调整要做效果回归——拆频道三天后回来看空跑率和任务产出，组织设计也能有 A/B。", "「七类必拍板」清单加「未批准不得合并」的硬闸门，是 Agent 团队规模化之前必须立好的地基。"],
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
    # 相关案例：优先同分组（CASE_GROUPS），不足 3 个再从其余案例补齐
    my_group = next((g["slugs"] for g in CASE_GROUPS.get(lang, []) if slug in g["slugs"]), None)
    if my_group:
        related = [s for s in my_group if s != slug]
        related += [x[4] for x in CASES[lang] if x[4] != slug and x[4] not in related]
    else:
        related = [x[4] for x in CASES[lang] if x[4] != slug]
    related = related[:3]
    rel = "".join(case_card(lang, *next(y for y in CASES[lang] if y[4] == s)) for s in related)

    D = [head(lang, f"{title}{t['d_title_suffix']}",
              f"{t['d_desc_prefix']}{title}. {d['sub']}",
              f'<!-- @dsCard group="{"Syfo 官网" if lang=="zh" else "Syfo Website"}" title="{t["d_card_prefix"]}{ind}" -->',
              toggle)]
    # 语言切换器：该 slug 若未被所有语言收录（如 brand-* 暂只有中文），切换目标退回各语言的案例列表页，避免 404
    sw_page = f"case-{slug}.html" if all(any(x[4] == slug for x in CASES[lg]) for lg in LANGS) else "cases.html"
    D.append(nav(lang, sw_page, "cases"))
    # 面包屑：属于某行业分组时回该行业页，否则回全部案例
    gobj = next((g for g in CASE_GROUPS.get(lang, []) if slug in g["slugs"]), None)
    if gobj:
        back_href, back_label = url(lang, f"cases-{gobj['id']}.html"), "← 返回 " + gobj["label"]
    else:
        back_href, back_label = url(lang, "cases.html"), t["d_back"]
    D.append(f"""<div class="wrap"><div class="crumb"><a href="{back_href}">{back_label}</a></div>
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


# ════════════════════════════════════════════ 根 / 语言网关 (真实静态 index.html，返回 200 不再 503)
def build_root_gateway():
    """根 / = 静态语言网关：JS 按 cookie -> Accept-Language 选语言并跳到 /<lang>/；无 JS 时给手选链接。"""
    js = ("(function(){var S={en:'/en/',zh:'/zh/',ja:'/ja/',es:'/es/',vi:'/vi/'};"
          "function ck(n){var m=document.cookie.match('(?:^|; )'+n+'=([^;]*)');return m?decodeURIComponent(m[1]):''}"
          "var p=ck('syfo_landing_locale');"
          "if(!S[p]){var L=navigator.languages||[navigator.language||''];p='';"
          "for(var i=0;i<L.length&&!p;i++){var x=(L[i]||'').toLowerCase();"
          "if(x.indexOf('zh')===0)p='zh';else if(x.indexOf('ja')===0)p='ja';"
          "else if(x.indexOf('es')===0)p='es';else if(x.indexOf('vi')===0)p='vi';"
          "else if(x.indexOf('en')===0)p='en';}if(!S[p])p='" + DEFAULT_LANG + "';}"
          "location.replace(S[p]);})();")
    links = "".join(f'<a href="/{lg}/">{LANG_NAMES[lg]}</a>' for lg in LANGS)
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Syfo</title><meta name="robots" content="noindex,follow">'
            f'<link rel="icon" href="/assets/logo-mark.svg"><script>{js}</script>'
            f"<style>body{{font-family:system-ui,-apple-system,'Noto Sans SC',sans-serif;background:#F7F3EA;"
            f"color:#1A1612;display:flex;min-height:100vh;margin:0;align-items:center;justify-content:center;text-align:center}}"
            f"a{{color:#D4501E;text-decoration:none;margin:0 10px;font-size:15px}}</style></head>"
            f'<body><div><p style="font-family:Georgia,serif;font-size:22px;font-weight:600">Syfo</p>'
            f'<p>{links}</p></div></body></html>')
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_root_compat():
    """旧根中文路径 (/cases /how /case-*) -> /zh/... 兼容跳转桩，避免老链接/书签断。"""
    pages = (["cases.html", "how.html"] + [f"case-{c[4]}.html" for c in CASES["zh"]]
             + [f"cases-{g['id']}.html" for g in CASE_GROUPS.get("zh", [])])
    for pg in pages:
        target = "/zh/" + pg[:-5]
        html = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
                f'<meta name="robots" content="noindex"><link rel="canonical" href="{target}">'
                f'<meta http-equiv="refresh" content="0;url={target}">'
                f'<script>try{{document.cookie="syfo_landing_locale=zh;path=/;max-age=31536000;SameSite=Lax"}}catch(e){{}}'
                f'location.replace("{target}")</script></head>'
                f'<body><a href="{target}">→ {target}</a></body></html>')
        with open(os.path.join(HERE, pg), "w", encoding="utf-8") as f:
            f.write(html)


# ════════════════════════════════════════════ build
for _d in DIRS.values():
    os.makedirs(_d, exist_ok=True)
for lang in LANGS:
    build_home(lang)
    build_cases(lang)
    for g in CASE_GROUPS.get(lang, []):
        build_industry(lang, g)
    build_how(lang)
    for slug in [c[4] for c in CASES[lang]]:
        build_detail(lang, slug)
build_root_gateway()
build_root_compat()

print("wrote " + " + ".join(PREFIX[l] for l in LANGS)
      + " + root gateway(/) + zh compat stubs: index.html + cases.html + how.html + 6 case detail pages each")
