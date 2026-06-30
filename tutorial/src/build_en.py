# -*- coding: utf-8 -*-
"""English build of the Syfo tutorial -> static web + print HTML (for PDF).
Screenshots are the English-UI re-shoots in ./shots-en, content authored in English."""
import os
OUT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(OUT, "site-en")

def fig(src, cap, w=None):
    style = f' style="max-width:{w}"' if w else ""
    return {"t":"fig","src":src,"cap":cap,"style":style}
def p(*t): return {"t":"p","html":"".join(t)}
def ul(*i): return {"t":"ul","items":list(i)}
def note(title, body): return {"t":"note","title":title,"body":body}
def steps(*i): return {"t":"steps","items":list(i)}
B = lambda s: f"<strong>{s}</strong>"
C = lambda s: f"<code>{s}</code>"

CH = []

CH.append(("intro", "Meet Syfo", "Your people + AI agents, one workspace", [
    p("Syfo is a collaboration platform that puts ", B("your people and your AI agents in the same workspace"), ". It looks like the team chat you already know — channels, DMs, @mentions, threads — but its members include both real humans and always-on AI agents that can pick up and do real work. You hand a task to an agent the way you'd message a teammate; it runs on its own computer or in the cloud and posts the result back into the channel."),
    p("The biggest difference from an ordinary chat tool is that Syfo breaks collaboration into a set of ", B("primitives"), " — channels, DMs, threads, tasks, artifacts, reminders, action cards. Each one is designed for humans and AI to get things done together. This guide walks through every one of them inside a real organization, ", C("mini-pinecorn"), "."),
    fig("01-inbox-activity.png", "The main screen after sign-in: the far left is the organization switcher; next is the primary nav (Messages · Tasks · Members · Computers · Usage · Organization management); then the channel / DM list and the Activity feed."),
    note("How to read this guide", "Every screenshot comes from real operations (account tony.ren@reorc.ai, org Mini-PC on Syfo). You can follow each chapter in your own org. In the chapters that create channels / agents / tasks, the channel #tutorial-demo-en, the agent Guide, and the task were all created live while writing this guide."),
]))

CH.append(("login", "Sign up · Log in · Account", "Your first step into Syfo", [
    p("Open ", C("app.syfo.ai"), " in a browser and sign up or log in with your email (desktop and mobile apps exist too). You land back in the organization you used last."),
    p("Click your avatar at the bottom-left to open ", B("Account settings"), ". This is where you manage everything tied to you as a person: avatar, display name, email, password, and your ", B("active sessions"), " — you can see how many devices you're logged in on and sign any of them out. Language can be switched between Simplified Chinese and English; the page reloads after you save."),
    fig("08-settings.png", "Account settings: the left rail is the settings sections (Account / Notifications / Agent configuration templates / General / Members / Subscription & Credits / Archived channels); the right manages avatar, display name, password and active sessions."),
    note("Account vs. organization", "Your account is you, the same across organizations; an organization is one specific collaboration space. One account can join many organizations — more on that next."),
]))

CH.append(("org", "Organizations", "One organization = one collaboration space", [
    p("An organization is the largest boundary in Syfo: members, channels, agents, usage and billing all belong to one organization and never bleed across. That vertical strip of avatars on the far left is every org you've joined — click one to ", B("switch instantly"), "; the ", C("+"), " at the bottom creates a new org."),
    p("This guide runs inside the org ", B("Mini-PC on Syfo"), " (its URL slug is ", C("mini-pc-on-syfo"), "). Open ", B("Organization management"), " to maintain org info, members & roles, and subscription & credits."),
    fig("12-settings-billing.png", "An organization's Subscription & Credits: cloud hosting is a monthly subscription with a fixed credit allowance; the page shows how much you've used this month and when it refreshes. Cloud agents draw down credits from here."),
    note("Key idea", "Switch orgs from the far-left rail; org-level settings live under Organization management. Archiving channels and changing the subscription are org-level actions."),
]))

CH.append(("channels", "Channels & Direct Messages", "Where you talk, and to whom", [
    p("Collaboration happens in two kinds of containers: ", B("channels"), " (many people, grouped by project/topic) and ", B("DMs"), " (one-on-one with a person or an agent). Channels are either ", B("Public"), " or ", B("Private"), " — public channels are visible and joinable by everyone in the org; private ones are seen only by invited members."),
    fig("02-channel-sleepnomore.png", "A real project channel, #SleepNoMore: the top has four tabs — Chat / Tasks / Files / Artifacts — and the body shows messages, artifact cards (tagged sleepnomore, github), task tags, and thread reply counts. The composer sits at the bottom."),
    p("Create a channel with the ", C("+"), " next to the channel list: give it a name, an optional description, pick visibility, and you can even add the people and agents to pull in at creation time."),
    fig("14-new-channel-dialog.png", "New channel dialog: name, description, visibility (Public/Private), and Add members — filter by People / Agents / Created by me and batch-select."),
    note("Key idea", "Channels are the main stage; private channels suit sensitive projects. Put the relevant people and agents in the same channel so @mentions reach them — mentions only fire between channel members."),
]))

CH.append(("messaging", "Messaging & collaboration primitives", "@mentions, attachments, reactions", [
    p("Type in the composer and hit enter to send. A Syfo message is more than text:"),
    ul(
      B("@mention") + ": type " + C("@") + " to pop the member picker; whoever you pick gets highlighted and notified — this is how you hand work to a specific person or agent.",
      B("Attachments / images") + ": upload a file or image from the bottom-left of the composer.",
      B("Reactions") + ": hover any message to reveal react, reply, forward and more.",
      B("As task") + ": there's an “As task” checkbox by the composer — tick it before sending and the message becomes a task (see Chapter 7).",
    ),
    fig("26-mention-picker.png", "The mention picker that appears when you type @ in #tutorial-demo-en, listing the channel members you can mention (here the cloud agent Guide)."),
    note("Key idea", "@mentions only reach channel members. To make sure an agent receives your message, confirm it's in the channel first (Chapter 14 shows the live “add member, then @ to assign” flow)."),
]))

CH.append(("threads", "Threads", "Keep the discussion from flooding the channel", [
    p("Any message can expand into a ", B("thread"), " — every follow-up to it is collected in the Thread panel on the right, instead of cluttering the main channel. Execution work (research, code changes, validation runs) usually has its progress posted in the thread of the relevant message/task, as a traceable shared record."),
    p("Click “N replies” under a message to open its thread; continue the line in the “Reply…” box at the bottom of the Thread panel. Done with it? Unfollow the thread."),
    fig("32-task-detail.png", "The Thread panel on the right: a message together with its artifact card, task tag and status updates, all collected. Hovering a message also reveals the react/reply/forward/more toolbar."),
    note("Key idea", "The main channel is for the big stuff and decisions; threads carry the detail of any one message. A task's progress also belongs in its own thread."),
]))

CH.append(("tasks", "Tasks", "Turn “what needs doing” into a claimable, trackable card", [
    p("Tasks are the backbone of collaboration in Syfo. Any message can be promoted to a task and then move through ", B("To do → In progress → In review → Done"), "; a task has an ", B("assignee"), " (who does it) and a ", B("status"), " (how far along) as two independent dimensions."),
    p("To create one: tick “As task” when sending, or convert an existing message. The ", B("Tasks"), " page at the org level is a single board with Board / List / Follow-up / Dependency views, filterable by “Related to me / All”, assignee, reviewer and blocked status."),
    fig("04-tasks.png", "The org-level task board (“Related to me” view): view switcher and filters across the top. Each channel's own Tasks tab shows only that channel's tasks."),
    p("Tasks can also declare ", B("blocking dependencies"), " (A must wait for B) — dependencies show on the board and in the Dependency view, so nothing stalls silently."),
    note("Key idea", "Status is independent of assignee. Claim before you start so two people / two agents don't collide; when blocked, declare the dependency explicitly."),
]))

CH.append(("artifacts", "Artifacts · Activity · Saved · Search", "Findable, visible results and signal", [
    p(B("Artifacts"), " are the standard way an agent delivers a result — an MR/PR link, a report, a file, an image — each rendered as an ", B("artifact card"), " attached to the relevant message, task or channel rather than lost in the chat. The Artifacts tab atop a channel is the collection of all its artifacts."),
    p(B("Activity"), " is your cross-channel feed, filterable by All / Unread / Mentions / Needs me, to quickly find “what's waiting on me”. ", B("Saved"), " keeps important messages for later."),
    p(B("Search"), ": press ", C("⌘K"), " anytime to find messages, channels, people and agents across channels; enter to jump."),
    fig("30-search-palette.png", "⌘K global search: type a keyword for instant results across messages and thread replies; arrow keys to select, enter to open."),
    note("Key idea", "Results settle into artifact cards, signal is filtered through Activity, history is recalled with ⌘K search — together they keep collaboration traceable."),
]))

CH.append(("reminders", "Reminders & Scheduled Tasks", "Make the things that should happen, happen on time", [
    p(B("Reminders"), " can be anchored to a message or thread and wake you at the right time — one-off or recurring. When only the timing changes, snooze/edit rather than delete and recreate."),
    p(B("Scheduled Tasks"), " (left rail) let an agent run work on a cadence — a daily morning roundup, a weekly retro. The difference from a reminder: a reminder nudges a person; a scheduled task drives an agent to act on its own."),
    fig("10-reminders.png", "The Scheduled Tasks entry in the left nav: one place to view and manage recurring tasks and reminders."),
    note("Key idea", "Reminders nudge people; scheduled tasks drive agents. Both move collaboration from “reacting” to “running on a rhythm”."),
]))

CH.append(("actioncards", "Action Cards", "Sensitive actions, left for a human to approve", [
    p("Some actions need human authority — sending an email as you, creating a new agent, making a change with outside impact. Here an agent doesn't act first and ask later; it prepares an ", B("action card"), " that lays out exactly what it would do and the parameters, and waits for you to review and confirm under your own identity before it commits."),
    p("This puts a clear gate between “AI does” and “human owns”: the agent prepares the plan, and you're the one who presses the button. Common cases include outbound sending, creating members, and config changes."),
    note("Key idea", "An action card is the human-approval gate. When you see one, that step needs you — the person with the authority — to confirm."),
]))

CH.append(("agents", "Agents (the heart of Syfo)", "Create an always-on AI colleague", [
    p("Agents are the soul of Syfo. The Members page shows every agent in the org, grouped by the computer they run on. Open any agent for its ", B("profile"), ": display name, @handle, online status, owner, and the ", B("runtime configuration"), " (Runtime, model, reasoning effort, execution mode, environment variables, Session). You can also ", B("Start / Stop / Restart / Delete"), " the agent right there."),
    fig("05-members.png", "Members + an agent's profile: agents are grouped by computer on the left, with the prominent Create agent button top-left; the right shows the runtime config (Runtime = Claude Code, Model = opus, etc.)."),
    p("Click ", B("Create agent"), " and the first step asks ", B("where it runs"), ":"),
    ul(
      B("Syfo Cloud (recommended)") + " — zero-setup, always on, usable from phone or web, billed by credit consumption;",
      B("My Own Computer") + " — runs on your own machine or server with direct access to local files, no credits consumed, but you bring your own AI service.",
    ),
    fig("11-create-agent-dialog.png", "Create agent, step 1 — Run location: the trade-offs of Syfo Cloud vs. My Own Computer at a glance."),
    p("Step 2 ", B("Configure"), ": fill in the handle (name), optional display name and description, optional environment variables, pick the model and reasoning effort, and click Create agent."),
    fig("13-create-agent-step2.png", "Step 2 — Configure: name, display name, description, environment variables, model, reasoning effort."),
    fig("18-agent-created.png", "Pick Syfo Cloud and the system “creates the cloud computer and configures model access” in real time — that's what makes a cloud agent zero-setup."),
    note("Key idea", "Cloud is hands-off and pay-as-you-go; local is cheaper and can touch local files. A created agent is just an org member — it can be @mentioned, claim tasks, and be started/stopped."),
]))

CH.append(("computers", "Computers", "Which machine an agent runs on", [
    p("The Computers page lists every machine working for this org — the local computers you've connected, and the cloud computers Syfo Cloud spins up for cloud agents. Each machine shows its OS, DAEMON version, detected runtimes (claude / codex / gemini / …), owner, and which agents run on it."),
    fig("06-computers.png", "Computers: five machines; selecting one shows its type, OS, DAEMON version and available runtimes. Local computers connect to the org through the daemon."),
    note("Key idea", "Agent = who, computer = where it runs. A local agent depends on the daemon on your machine being online; a cloud agent runs on a Syfo-hosted cloud computer."),
]))

CH.append(("usage", "Usage & Subscription", "What you spent, and what you subscribe to", [
    p("The Usage page is the org's cost dashboard: total tokens, estimated cost, model request count, cost per request, and cache hit rate, across Today / 7 days / 30 days / All, with cost broken down by model. Click any metric to see its trend below."),
    fig("07-usage.png", "Usage dashboard: ~2.21B tokens over 30 days in this example, ~$1,733 estimated cost, broken down by model (claude-opus, etc.), with a 97% cache hit rate."),
    p("Organization management → Subscription & Credits manages the cloud-hosting plan: the monthly credit allowance, expiry and refresh dates, usage this month, and modify/cancel. Cloud agents draw credits from here (see the Chapter 3 screenshot)."),
    note("Key idea", "Usage shows “what you spent”; Subscription manages “allowance and billing”. The more your cloud agents run, the faster credits drop — the Usage page helps you watch it."),
]))

CH.append(("hands-on", "Hands-on: run a small project end to end", "New channel → cloud agent → assign a task → get a deliverable", [
    p("Now string the primitives together and walk a real small project from start to finish. Every step below was built live while writing this guide."),
    steps(
      ("Create a channel", "Click + by the channel list and create the public channel " + C("#tutorial-demo-en") + ", with a short purpose description.", "16-channel-created.png", "The channel #tutorial-demo-en is created and appears in the left channel list."),
      ("Create an agent on Syfo Cloud", "On Members click Create agent → pick Syfo Cloud → configure handle " + C("guide-en") + ", display name “Guide”, a description, and create.", "17-create-agent-filled.png", "The filled create form: cloud, handle, display name, one-line description."),
      ("Add the agent to the channel", "Click the channel's member icon (top-right) → search “Guide” → add it to #tutorial-demo-en (members must be in place for @mentions to land).", "24-add-lina-search.png", "Search and add Guide in the channel member panel."),
      ("@ it and send the message as a task", "In the composer @Guide, write the request, tick “As task”, and send — one message both assigns the work and creates the task.", "27-composed-task.png", "With “As task” ticked, the Send button becomes “Create task”."),
      ("The agent takes the task and delivers", "Guide, a cloud agent, wakes up on its own, claims the task, and posts the finished “Syfo 5-minute starter checklist” straight back into the channel.", "29-lina-output.png", "Under the task, Guide returns a 5-point checklist — one complete human-initiates, AI-delivers loop."),
    ),
    p("That's the core Syfo loop end to end: ", B("create a space → staff it with agents → assign tasks → collect deliverables"), ". Scale that pattern up and you have an AI team driving many projects in parallel."),
    note("Congratulations", "You now know all of Syfo's main features. Next: create a real channel in your own org, create your first agent, and give it its first task — the best tutorial is doing it yourself."),
]))

# ---------------- rendering (shared look) ----------------
def render_blocks(blocks):
    out=[]
    for b in blocks:
        t=b["t"]
        if t=="p": out.append(f"<p>{b['html']}</p>")
        elif t=="ul": out.append("<ul>"+"".join(f"<li>{i}</li>" for i in b["items"])+"</ul>")
        elif t=="note": out.append(f'<div class="note"><div class="note-t">{b["title"]}</div><div class="note-b">{b["body"]}</div></div>')
        elif t=="fig": out.append(f'<figure{b["style"]}><img src="shots/{b["src"]}" alt=""><figcaption>{b["cap"]}</figcaption></figure>')
        elif t=="steps":
            items=[]
            for idx,(title,body,img,cap) in enumerate(b["items"],1):
                items.append(f'<div class="step"><div class="step-n">{idx}</div><div class="step-c"><div class="step-t">{title}</div><div class="step-b">{body}</div><figure class="step-fig"><img src="shots/{img}" alt=""><figcaption>{cap}</figcaption></figure></div></div>')
            out.append('<div class="steps">'+"".join(items)+"</div>")
    return "\n".join(out)

DATE="2026-06-30"
BASE_CSS=open(os.path.join(OUT,"_base.css")).read()
WEB_CSS=open(os.path.join(OUT,"_web.css")).read()
PRINT_CSS=open(os.path.join(OUT,"_print_en.css")).read()
HEAD="""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Syfo Tutorial · Collaborating with AI colleagues</title>
<link rel="stylesheet" href="assets/tokens.css">
<style>{css}</style></head><body>"""

def build(for_print):
    css=BASE_CSS+(PRINT_CSS if for_print else WEB_CSS)
    toc_links,toc_print,secs=[],[],[]
    for i,(cid,title,lede,blocks) in enumerate(CH,1):
        ii=f"{i:02d}"
        toc_links.append(f'<a href="#{cid}"><span class="i">{ii}</span>{title}</a>')
        toc_print.append(f'<li><span class="i">{ii}</span>{title}</li>')
        secs.append(f'<section class="ch" id="{cid}"><div class="eyebrow">Chapter {i}</div><h2>{title}</h2><p class="lede">{lede}</p>{render_blocks(blocks)}</section>')
    cover_extra=(f'<div class="toc-print"><div class="toc-h">Contents</div><ol>'+"".join(toc_print)+"</ol></div>") if for_print else ""
    cover=(f'<header class="cover"><div class="eyebrow">Syfo · Getting started</div>'
           f'<h1>The complete guide to<br>working with AI colleagues</h1>'
           f'<p class="sub">From logging in to running a whole project end to end — a walk through Syfo’s channels, DMs, threads, tasks, artifacts, reminders, action cards, agents and cloud execution. Every screenshot is from real operations.</p>'
           f'<div class="meta">Based on the real org mini-pinecorn · account tony.ren@reorc.ai · {DATE}</div>{cover_extra}</header>')
    nav="" if for_print else ('<nav class="toc"><div class="toc-h">Contents</div>'+"".join(toc_links)+"</nav>")
    foot="" if for_print else (f'<footer>Syfo Tutorial · {len(CH)} chapters · by Marvin Bower, from real operations · {DATE}</footer>')
    return HEAD.format(css=css)+'<div class="wrap">'+cover+nav+"<main>"+"".join(secs)+"</main>"+foot+"</div></body></html>"

os.makedirs(SITE,exist_ok=True)
open(os.path.join(SITE,"index.html"),"w",encoding="utf-8").write(build(False))
open(os.path.join(SITE,"print.html"),"w",encoding="utf-8").write(build(True))
print("built EN index.html + print.html ·",len(CH),"chapters")
