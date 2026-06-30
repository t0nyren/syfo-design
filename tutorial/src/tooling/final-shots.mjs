import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
// billing/订阅与积分
await p.goto(`https://app.syfo.ai/s/${SLUG}/settings/account`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.click('text=订阅与积分').catch(()=>{});
await p.waitForTimeout(2500);
await p.screenshot({path:'./shots/12-settings-billing.png'});
console.log('BILLING:', (await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,600));
// tasks 全部 board
await p.goto(`https://app.syfo.ai/s/${SLUG}/tasks`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.click('text=全部').catch(()=>{});
await p.waitForTimeout(2000);
await p.screenshot({path:'./shots/04b-tasks-all.png'});
console.log('TASKS:', (await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(300,700));
await b.close();
