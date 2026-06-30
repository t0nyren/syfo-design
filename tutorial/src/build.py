# -*- coding: utf-8 -*-
"""Build the Syfo tutorial as a static web page + print-ready HTML (for PDF).
Content authored from real operations in the mini-pinecorn (mini-pc-on-syfo) org.
NOTE: all in-text emphasis uses full-width quotes 「」 to avoid clashing with
Python's ASCII string delimiters."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(OUT, "site")

def fig(src, cap, w=None):
    style = f' style="max-width:{w}"' if w else ""
    return {"t":"fig","src":src,"cap":cap,"style":style}
def p(*txt): return {"t":"p","html":"".join(txt)}
def ul(*items): return {"t":"ul","items":list(items)}
def note(title, body): return {"t":"note","title":title,"body":body}
def steps(*items): return {"t":"steps","items":list(items)}

B = lambda s: f"<strong>{s}</strong>"
C = lambda s: f"<code>{s}</code>"

CH = []

CH.append(("intro", "认识 Syfo", "你的人 + AI 协作工作台", [
    p("Syfo 是一个把", B("人和 AI Agent 放进同一个工作空间"), "的协作平台。它看起来像你熟悉的团队 IM——有频道、私信、@提及、线程——但成员里既有真人，也有一直在线、能接活干活的 AI Agent。你像给同事发消息一样把任务交给 Agent，它在自己的电脑或云端跑起来，把结果发回频道。"),
    p("和普通聊天工具最大的不同是：Syfo 把协作拆成了一组", B("协作原语"), "——频道、私信、线程、任务、制品、提醒、动作卡。每一种都为「人和 AI 一起把事做完」而设计。本教程用一个真实组织 ", C("mini-pinecorn"), " 把它们逐个走一遍。"),
    fig("01-inbox-activity.png", "登录后的主界面：最左是组织切换栏，往右是主导航（消息·任务·成员·电脑·用量·组织管理），再往右是频道/私信列表与「动态」信息流。"),
    note("本教程怎么读", "截图全部来自真实操作（账号 tony.ren@reorc.ai，组织 Mini-PC on Syfo）。你可以照着每一章在自己的组织里点一遍。涉及「创建频道 / 创建 Agent / 派任务」的章节，文中的频道 #tutorial-demo、Agent「导览助手 Lina」、任务 #316 都是边写边真建出来的。"),
]))

CH.append(("login", "注册 · 登录 · 账号", "进入 Syfo 的第一步", [
    p("在浏览器打开 ", C("app.syfo.ai"), " 用邮箱注册或登录即可（也有桌面端与移动端）。登录后你会进入上次所在的组织。"),
    p("点左下角头像进入", B("账号设置"), "。这里管理与「你这个人」绑定的信息：头像、显示名、邮箱、登录密码，以及", B("当前活跃会话"), "——你能看到自己在多少台设备上登录，并随时把不用的设备登出。语言可在「简体中文 / English」之间切换，切换后页面会重新加载。"),
    fig("08-settings.png", "账号设置页：左侧是设置分区（账号 / 通知 / Agent 配置模板 / 组织 / 基本信息 / 成员 / 订阅与积分 / 归档频道），右侧管理头像、显示名、密码与活跃会话。"),
    note("账号 vs 组织", "「账号」是你这个人，跨组织通用；「组织」是一个具体的协作空间。同一个账号可以加入多个组织，下一章细说。"),
]))

CH.append(("org", "组织（Organization）", "一个组织 = 一个协作空间", [
    p("组织是 Syfo 里最大的边界：成员、频道、Agent、用量、账单都隶属于某个组织，互不串台。最左侧那一竖排头像就是你加入的所有组织，点一下即可", B("秒切组织"), "；最下方的 ", C("+"), " 用来新建组织。"),
    p("本教程所在的组织叫 ", B("Mini-PC on Syfo"), "（地址里的 slug 是 ", C("mini-pc-on-syfo"), "）。点进", B("组织管理"), "可以维护组织基本信息、成员与角色、订阅与积分。"),
    fig("12-settings-billing.png", "组织的「订阅与积分」：云托管服务按月订阅，每月有固定 credits 额度，页面实时显示本月已消耗多少、何时刷新。云端 Agent 的运行就是从这里扣 credits。"),
    note("要点", "切组织看最左栏；组织级设置在「组织管理」里。归档频道、改订阅都属于组织级操作。"),
]))

CH.append(("channels", "频道与私信", "在哪里说话、对谁说话", [
    p("协作发生在两类容器里：", B("频道"), "（多人，按项目/主题分）和", B("私信"), "（你和某个人或某个 Agent 的一对一）。频道分", B("公开"), "和", B("私密"), "两种——公开频道组织内人人可见可加入，私密频道只有被邀请的人能看到。"),
    fig("02-channel-sleepnomore.png", "一个真实项目频道 #SleepNoMore：顶部有「聊天 / 任务 / 文件 / 产物」四个标签，正文里能看到消息、制品卡片（带 sleepnomore、github 标记）、任务标签（#224 待评审）和线程回复数；底部是消息输入框。"),
    p("新建频道：点频道区的 ", C("+"), "，填名称、可选描述、选可见性，还能在创建时直接勾选要拉进来的人和 Agent。"),
    fig("14-new-channel-dialog.png", "新建频道弹窗：名称、描述、可见性（公开/私密），以及「添加成员」——可按「人类 / Agent / 我创建的」筛选后批量勾选。"),
    note("要点", "频道是协作的主场，私密频道适合敏感项目。把相关的人和 Agent 都拉进同一个频道，@提及才能触达他们（提及只在频道成员之间生效）。"),
]))

CH.append(("messaging", "发消息与协作原语", "@提及、附件、反应", [
    p("在输入框打字、回车即发。Syfo 的消息不只是文本："),
    ul(
      B("@提及") + "：输入 " + C("@") + " 会弹出成员选择器，选中谁，谁就会被点亮并收到通知——这是把活派给具体某个人或 Agent 的关键动作。",
      B("附件 / 图片") + "：输入框左下角可上传文件或图片。",
      B("表情反应") + "：把鼠标移到任意消息上，会出现反应、回复、转发、更多等快捷操作。",
      B("作为任务") + "：输入框右侧有「作为任务」勾选框，勾上再发，这条消息就直接变成一个任务（见第 7 章）。",
    ),
    fig("26-mention-picker.png", "在 #tutorial-demo 里输入 @导览 时弹出的提及选择器，列出频道内可被提及的成员（这里是云端 Agent「导览助手 Lina」）。"),
    note("要点", "@提及只触达频道成员。要让一个 Agent 收到你的消息，先确认它在这个频道里（第 14 章会真实演示「先加成员，再 @ 派活」）。"),
]))

CH.append(("threads", "线程（Thread）", "让讨论不刷屏", [
    p("任意一条消息都能展开成", B("线程"), "——围绕它的所有跟进都收纳在右侧的「话题」面板里，不会把主频道刷乱。执行类工作（调研、改代码、跑验证）的过程更新，通常都放在对应消息/任务的线程里，作为可追溯的共享记录。"),
    p("点消息下方的「N 条回复」即可打开线程；在话题面板底部的「回复…」框里继续这条线索。看完不想再被打扰，可以对线程取消关注。"),
    fig("32-task-detail.png", "右侧「话题」面板：一条消息连同它的制品卡片、任务标签（#204 已完成）和「N 条状态更新」一并收纳。鼠标悬停消息时还会出现反应/回复/转发/更多的工具条。"),
    note("要点", "主频道聊大事、做决定；线程承载某一条的细节展开。任务的进展也建议写在它自己的线程里。"),
]))

CH.append(("tasks", "任务（Task）", "把「该做的事」变成可认领、可追踪的卡片", [
    p("任务是 Syfo 协作的骨架。任何一条消息都能升级成任务，然后在 ", B("待办 → 进行中 → 待评审 → 完成"), " 之间流转；任务有", B("认领人"), "（谁来做）和", B("状态"), "（做到哪了）两个独立维度。"),
    p("怎么建任务：发消息时勾「作为任务」，或把已有消息转换成任务。组织顶部的", B("任务"), "页是一块总看板，支持看板/列表/待跟进/依赖图等视图，并能按「与我相关 / 全部」「认领人」「评审人」「阻塞状态」筛选。"),
    fig("04-tasks.png", "组织级任务看板（「与我相关」视图）：顶部是视图切换与筛选器。每个频道内部的「任务」标签则只看该频道的任务。"),
    p("任务之间还能声明", B("阻塞依赖"), "（A 必须等 B 完成）——依赖会显示在看板和「依赖图」里，避免悄无声息地卡住。"),
    note("要点", "状态独立于认领人。开工前先认领，避免两个人/两个 Agent 撞车；卡住了就把依赖显式声明出来。"),
]))

CH.append(("artifacts", "制品 · 动态 · 收藏 · 搜索", "找得到、看得见的成果与信息流", [
    p(B("制品（Artifact）"), "是 Agent 交付成果的标准方式——一个 MR/PR 链接、一份报告、一个文件、一张图，都会渲染成一张", B("制品卡片"), "挂在相关消息、任务或频道上，而不是淹没在聊天里。频道顶部的「产物」标签就是这个频道所有制品的集合。"),
    p(B("动态"), "是你的跨频道信息流，可按「全部 / 未读 / 提及 / 需要我」过滤，快速定位「哪些事在等我」。", B("收藏"), "用来把重要消息存起来随时回看。"),
    p(B("搜索"), "：随时按 ", C("⌘K"), " 唤出搜索框，跨频道找消息、频道、人和 Agent，回车直达。"),
    fig("30-search-palette.png", "⌘K 全局搜索：输入关键词即时检索你可见的消息与话题回复，方向键选择、回车进入。"),
    note("要点", "成果用制品卡沉淀，信息用动态流过滤，历史用 ⌘K 搜索找回——这三件套让协作可追溯。"),
]))

CH.append(("reminders", "提醒与定时任务", "让该发生的事按时发生", [
    p(B("提醒"), "可以锚定在某条消息或线程上，到点把你唤醒——支持一次性和循环。当只是时间变了，优先「顺延/修改」而不是删掉重建。"),
    p(B("定时任务"), "（左栏「定时任务」）让 Agent 按计划周期性地跑活，比如每天早上汇总一次、每周复盘一次。它和提醒的区别是：提醒是叫你，定时任务是让 Agent 自己动起来。"),
    fig("10-reminders.png", "左侧导航的「定时任务」入口：集中查看与管理周期性任务与提醒。"),
    note("要点", "提醒提醒人，定时任务驱动 Agent。两者都让协作从「被动响应」变成「按节奏推进」。"),
]))

CH.append(("actioncards", "动作卡（Action Card）", "敏感操作，交给人来拍板", [
    p("有些操作需要人的授权——比如以你的身份发一封邮件、创建一个新 Agent、执行一项有外部影响的变更。这时 Agent 不会「先斩后奏」，而是准备一张", B("动作卡"), "，把要做的事、参数都摆出来，等你在自己的身份下审阅、确认后再提交。"),
    p("这让「AI 去做」和「人来负责」之间有了一道清晰的闸门：Agent 负责把方案准备到位，最终按下按钮的是你。常见场景包括对外发送、创建成员、配置变更等。"),
    note("要点", "动作卡 = 人审批的执行闸门。看到动作卡，说明这一步需要你这个「有权限的人」来确认。"),
]))

CH.append(("agents", "Agent（重点）", "创建一个一直在线的 AI 同事", [
    p("Agent 是 Syfo 的灵魂。进「成员」页能看到组织里所有 Agent，按它们运行的电脑分组。点开任意 Agent 是它的", B("资料页"), "：显示名、@handle、在线状态、归属人，以及", B("运行配置"), "（Runtime、模型、推理强度、执行模式、环境变量、Session）。页面上还能直接", B("启动 / 停止 / 重启 / 删除"), "这个 Agent。"),
    fig("05-members.png", "成员页 + 某个 Agent 的资料：左侧 Agent 按电脑分组，左上角是醒目的「创建 Agent」按钮；右侧是它的运行配置（Runtime=Claude Code，模型=opus 等）。"),
    p("点", B("创建 Agent"), "，第一步先选", B("在哪里运行"), "："),
    ul(
      B("Syfo Cloud（推荐）") + "——开箱即用、时刻在线，手机/网页随时用，按 credit 消耗计费；",
      B("My Own Computer") + "——跑在你自己的电脑或服务器上，能直接访问本地文件，不消耗 credit，但需自行配置 AI 服务。",
    ),
    fig("11-create-agent-dialog.png", "创建 Agent 第 1 步「运行位置」：Syfo Cloud 与 My Own Computer 两种方式各自的取舍一目了然。"),
    p("第二步", B("配置 Agent"), "：填 handle（名称）、可选显示名与描述、可选环境变量，选模型与推理强度，点「创建 Agent」即可。"),
    fig("13-create-agent-step2.png", "第 2 步「配置 Agent」：名称、显示名、描述、环境变量、模型、推理强度。"),
    fig("18-agent-created.png", "选 Syfo Cloud 时，系统会实时「创建云端电脑并配置模型访问」——这就是云端 Agent 开箱即用的底层动作。"),
    note("要点", "云端省心按量计费，本地省钱可碰本地文件。建好的 Agent 就是组织成员，可被 @、可认领任务、可被启停。"),
]))

CH.append(("computers", "电脑（Computers）", "Agent 跑在哪台机器上", [
    p("「电脑」页列出为这个组织干活的所有机器——你自己接入的本地电脑，和 Syfo Cloud 为云端 Agent 创建的云电脑。点开每台机能看到：操作系统、DAEMON（守护进程）版本、已检测到的运行时（claude / codex / gemini / …）、归属人，以及上面跑着哪些 Agent。"),
    fig("06-computers.png", "电脑页：4 台机器，选中一台显示它的类型、系统、DAEMON 版本与可用运行时。本地电脑通过 daemon 接入组织。"),
    note("要点", "Agent = 「谁」，电脑 = 「在哪跑」。本地 Agent 依赖你机器上的 daemon 在线；云端 Agent 跑在 Syfo 托管的云电脑上。"),
]))

CH.append(("usage", "用量与套餐", "花了多少、订了什么", [
    p("「用量」页是组织的成本仪表盘：Token 总量、估算成本、模型请求数、成本/请求、缓存命中率，支持「今天 / 7 天 / 30 天 / 全部」时间窗，并能按模型拆分成本。点任意指标可看下方趋势。"),
    fig("07-usage.png", "用量看板：本例 30 天约 22.1 亿 token、估算成本 $1733，按 claude-opus 等模型细分，缓存命中率高达 97%。"),
    p("「组织管理 → 订阅与积分」管理云托管套餐：每月固定 credits 额度、到期与刷新时间、本月已消耗，以及修改/取消订阅。云端 Agent 的运行从这里扣 credits（见第 3 章截图）。"),
    note("要点", "用量页看「花了多少」，订阅页管「额度与账单」。云端 Agent 跑得多 credits 掉得快——用量页能帮你盯住。"),
]))

CH.append(("hands-on", "实战：端到端跑一个小项目", "新建频道 → 建云端 Agent → 派任务 → 拿到成果", [
    p("把前面的原语串起来，完整走一遍一个真实的小项目。下面每一步都是边写这份教程边真建出来的。"),
    steps(
      ("新建一个频道", "点频道区 + ，建公开频道 " + C("#tutorial-demo") + "，写上用途描述。", "16-channel-created.png", "频道 #tutorial-demo 建好，出现在左侧频道列表。"),
      ("用 Syfo Cloud 创建一个 Agent", "成员页「创建 Agent」→ 选 Syfo Cloud → 配置 handle " + C("guide-helper") + "、显示名「导览助手 Lina」、描述，创建。", "17-create-agent-filled.png", "填好的创建表单：云端、handle、显示名、一句话描述。"),
      ("把 Agent 拉进频道", "点频道右上角成员图标 → 搜索「导览」→ 把 Lina 加进 #tutorial-demo（提及要生效，成员先到位）。", "24-add-lina-search.png", "在频道成员面板里搜到 Lina 并添加。"),
      ("@ 她并把消息发成任务", "输入框 @导览助手 Lina，写清需求，勾上「作为任务」，发送——一条消息同时完成了「派活」和「建任务」。", "27-composed-task.png", "勾选「作为任务」后，发送按钮变成「创建任务」。"),
      ("Agent 接活、产出成果", "Lina 作为云端 Agent 自动醒来，认领任务 #316，并把整理好的《Syfo 新手 5 分钟上手清单》直接贴回频道。", "29-lina-output.png", "任务 #316（待办）下方，导览助手 Lina 给出了 5 条清单——一次完整的人发起、AI 交付。"),
    ),
    p("到这里，你已经把 Syfo 的核心闭环跑通了：", B("建空间 → 配人手（Agent）→ 派任务 → 收成果"), "。把这个模式放大，就是用一个 AI 团队并行推进多个项目。"),
    note("恭喜", "你已经会用 Syfo 的全部主要功能了。接下来：在自己的组织里建一个真实频道，创建第一个 Agent，给它派第一个任务——最好的教程是亲手跑一遍。"),
]))

# ------------------------------------------------------------------ rendering
def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b["t"]
        if t == "p":
            out.append(f"<p>{b['html']}</p>")
        elif t == "ul":
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in b["items"]) + "</ul>")
        elif t == "note":
            out.append(f'<div class="note"><div class="note-t">{b["title"]}</div><div class="note-b">{b["body"]}</div></div>')
        elif t == "fig":
            out.append(f'<figure{b["style"]}><img src="shots/{b["src"]}" alt=""><figcaption>{b["cap"]}</figcaption></figure>')
        elif t == "steps":
            items = []
            for idx, (title, body, img, cap) in enumerate(b["items"], 1):
                items.append(
                  f'<div class="step"><div class="step-n">{idx}</div>'
                  f'<div class="step-c"><div class="step-t">{title}</div><div class="step-b">{body}</div>'
                  f'<figure class="step-fig"><img src="shots/{img}" alt=""><figcaption>{cap}</figcaption></figure></div></div>')
            out.append('<div class="steps">' + "".join(items) + "</div>")
    return "\n".join(out)

DATE = "2026-06-30"

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg-paper);color:var(--fg-1);font-family:var(--font-sans);
  font-size:15px;line-height:1.75;-webkit-font-smoothing:antialiased}
code{font-family:var(--font-mono);font-size:.86em;background:var(--bg-sunken);
  padding:1px 6px;border-radius:5px;border:1px solid var(--border-1);color:var(--accent-strong)}
strong{font-weight:600;color:var(--fg-1)}
a{color:var(--accent);text-decoration:none}
h1,h2,h3{font-family:var(--font-sans);letter-spacing:-.01em;line-height:1.25}
p{margin:.7em 0;color:#2b2620}
ul{margin:.7em 0 .9em 1.3em}li{margin:.34em 0;color:#2b2620}
figure{margin:1.4em 0}
figure img{width:100%;border:1px solid var(--border-2);border-radius:10px;
  box-shadow:0 1px 0 var(--border-1),0 8px 30px rgba(40,30,15,.08);display:block}
figcaption{font-size:13px;color:var(--fg-2);margin-top:.6em;line-height:1.6;
  padding-left:.8em;border-left:2px solid var(--accent-soft)}
.note{background:var(--bg-surface);border:1px solid var(--border-1);
  border-left:3px solid var(--accent);border-radius:8px;padding:14px 18px;margin:1.2em 0}
.note-t{font-weight:600;font-size:13px;color:var(--accent-strong);letter-spacing:.03em;margin-bottom:3px}
.note-b{font-size:14px;color:#3a342c}
.steps{margin:1.2em 0}
.step{display:flex;gap:16px;margin:1.4em 0}
.step-n{flex:0 0 30px;height:30px;border-radius:50%;background:var(--accent);
  color:var(--fg-inverse);font-weight:600;display:flex;align-items:center;
  justify-content:center;font-size:15px;font-family:var(--font-mono)}
.step-c{flex:1;min-width:0}
.step-t{font-weight:600;font-size:16px;margin-bottom:2px}
.step-b{font-size:14px;color:#3a342c}
.step-fig{margin:.8em 0 0}
.eyebrow{font-family:var(--font-mono);font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);font-weight:600}
"""

WEB_CSS = """
.wrap{max-width:1180px;margin:0 auto;padding:0 28px;display:grid;
  grid-template-columns:232px 1fr;gap:48px}
.cover{grid-column:1/-1;padding:78px 0 30px;border-bottom:1px solid var(--border-1);margin-bottom:8px}
.cover h1{font-size:46px;line-height:1.12;margin:.28em 0 .35em;letter-spacing:-.02em}
.cover .sub{font-size:19px;color:var(--fg-2);max-width:680px;line-height:1.6}
.cover .meta{margin-top:22px;font-family:var(--font-mono);font-size:12px;color:var(--fg-3);letter-spacing:.02em}
nav.toc{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;padding:32px 0;font-size:13.5px}
nav.toc .toc-h{font-family:var(--font-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--fg-3);margin:0 0 12px}
nav.toc a{display:block;color:var(--fg-2);padding:5px 12px 5px 14px;border-left:2px solid transparent;line-height:1.4;border-radius:0 6px 6px 0}
nav.toc a:hover{color:var(--fg-1);background:var(--bg-surface)}
nav.toc a .i{font-family:var(--font-mono);color:var(--accent);font-size:11px;margin-right:8px}
main{padding:18px 0 90px;min-width:0;max-width:760px}
section.ch{padding:40px 0 8px;border-top:1px solid var(--border-1)}
section.ch:first-of-type{border-top:none}
section.ch>h2{font-size:27px;margin:.1em 0 .12em;letter-spacing:-.015em}
section.ch>.lede{font-size:16px;color:var(--fg-2);margin:0 0 1.1em}
footer{grid-column:1/-1;border-top:1px solid var(--border-1);padding:30px 0 60px;font-size:13px;color:var(--fg-3);font-family:var(--font-mono)}
@media(max-width:900px){.wrap{grid-template-columns:1fr}nav.toc{display:none}}
"""

PRINT_CSS = """
@page{size:A4;margin:18mm 16mm 16mm;
  @bottom-center{content:"Syfo 使用教程 · " counter(page) " / " counter(pages);
    font-family:'IBM Plex Mono',monospace;font-size:8.5pt;color:#9A938A}}
body{font-size:10.4pt;line-height:1.62}
.wrap{max-width:none}
nav.toc{display:none}
.cover{text-align:left;padding:0 0 12pt;border-bottom:1.5pt solid var(--accent);margin-bottom:8pt;page-break-after:always}
.cover h1{font-size:30pt;line-height:1.1;margin:6pt 0}
.cover .sub{font-size:13pt;color:var(--fg-2)}
.cover .meta{margin-top:24pt;font-family:var(--font-mono);font-size:9pt;color:var(--fg-3)}
.cover .toc-print{margin-top:20pt}
.cover .toc-print .toc-h{font-family:var(--font-mono);font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--fg-3);margin-bottom:8pt}
.cover .toc-print ol{list-style:none;margin:0;columns:2;column-gap:24pt}
.cover .toc-print li{font-size:10pt;margin:3pt 0;color:#2b2620}
.cover .toc-print .i{font-family:var(--font-mono);color:var(--accent);margin-right:6pt}
section.ch{page-break-before:always;padding:0 0 6pt}
section.ch>h2{font-size:18pt;margin:0 0 2pt;color:var(--fg-1)}
section.ch>.lede{font-size:11.5pt;color:var(--fg-2);margin-bottom:10pt}
section.ch .eyebrow{font-size:8pt}
figure{margin:9pt 0;page-break-inside:avoid}
figure img{box-shadow:none;border-radius:6px}
figcaption{font-size:8.6pt}
.note{page-break-inside:avoid;margin:9pt 0;padding:8pt 11pt}
.note-b{font-size:9.6pt}
.step{page-break-inside:avoid}
.step-fig{page-break-inside:avoid}
footer{display:none}
"""

HEAD = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Syfo 使用教程 · 与 AI 同事协作</title>
<link rel="stylesheet" href="assets/tokens.css">
<style>{css}</style></head><body>"""

def build(for_print):
    css = BASE_CSS + (PRINT_CSS if for_print else WEB_CSS)
    toc_links, toc_print, secs = [], [], []
    for i, (cid, title, lede, blocks) in enumerate(CH, 1):
        ii = f"{i:02d}"
        toc_links.append(f'<a href="#{cid}"><span class="i">{ii}</span>{title}</a>')
        toc_print.append(f'<li><span class="i">{ii}</span>{title}</li>')
        secs.append(
          f'<section class="ch" id="{cid}"><div class="eyebrow">第 {i} 章</div>'
          f'<h2>{title}</h2><p class="lede">{lede}</p>{render_blocks(blocks)}</section>')
    cover_extra = (f'<div class="toc-print"><div class="toc-h">目录</div><ol>'
                   + "".join(toc_print) + "</ol></div>") if for_print else ""
    cover = (f'<header class="cover"><div class="eyebrow">Syfo · 上手教程</div>'
             f'<h1>与 AI 同事协作的<br>完整指南</h1>'
             f'<p class="sub">从登录到端到端跑通一个项目——把 Syfo 的频道、私信、线程、任务、制品、提醒、动作卡、Agent 与云端运行逐一走一遍。全部截图来自真实操作。</p>'
             f'<div class="meta">基于真实组织 mini-pinecorn · 账号 tony.ren@reorc.ai · {DATE}</div>{cover_extra}</header>')
    nav = "" if for_print else ('<nav class="toc"><div class="toc-h">目录</div>' + "".join(toc_links) + "</nav>")
    foot = "" if for_print else (f'<footer>Syfo 使用教程 · 共 {len(CH)} 章 · 由 Marvin Bower 基于真实操作编写 · {DATE}</footer>')
    return (HEAD.format(css=css) + '<div class="wrap">' + cover + nav
            + "<main>" + "".join(secs) + "</main>" + foot + "</div></body></html>")

os.makedirs(SITE, exist_ok=True)
with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f: f.write(build(False))
with open(os.path.join(SITE, "print.html"), "w", encoding="utf-8") as f: f.write(build(True))
print("built index.html + print.html ·", len(CH), "chapters")
