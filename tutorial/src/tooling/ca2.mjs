import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/members`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await (await p.$('text=创建 Agent')).click();
await p.waitForTimeout(2000);
// select Syfo Cloud card then next
await p.click('text=Syfo Cloud');
await p.waitForTimeout(500);
await p.click('text=下一步');
await p.waitForTimeout(2500);
await p.screenshot({path:'./shots/13-create-agent-step2.png'});
console.log('=== STEP2 ===');
console.log((await p.innerText('[role=dialog]').catch(()=>p.innerText('body'))).replace(/\n{2,}/g,'\n').slice(0,1400));
await b.close();
