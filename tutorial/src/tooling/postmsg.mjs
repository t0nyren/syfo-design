import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const CH='019f17fa-da4c-73ec-a064-d65ffb247645';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
// focus composer
const comp = p.locator('[placeholder="发送到 #tutorial-demo"], [contenteditable=true]').first();
await comp.click();
await p.waitForTimeout(500);
await p.keyboard.type('@导览', {delay:60});
await p.waitForTimeout(1500);
await p.screenshot({path:'./shots/26-mention-picker.png'});
// select first suggestion
await p.keyboard.press('Enter');
await p.waitForTimeout(600);
await p.keyboard.type(' 帮我整理一份《Syfo 新手 5 分钟上手清单》：用 5 条要点说明新用户进入 Syfo 后应依次做什么（登录 → 加入频道 → 发消息/@他人 → 建任务 → 认识 Agent）。每条一句话、中文。整理好后直接贴在本频道。', {delay:5});
await p.waitForTimeout(500);
// check 作为任务
await p.click('text=作为任务').catch(()=>{});
await p.waitForTimeout(400);
await p.screenshot({path:'./shots/27-composed-task.png'});
await b.close();
