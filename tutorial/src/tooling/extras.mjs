import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const SNM='019e72d2-2f66-751a-a01c-6df8e5e1b2fd';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
// 1) ⌘K search palette
await p.goto(`https://app.syfo.ai/s/${SLUG}/inbox`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.keyboard.press('Meta+k'); await p.waitForTimeout(1000);
await p.keyboard.type('noise', {delay:50}); await p.waitForTimeout(1500);
await p.screenshot({path:'./shots/30-search-palette.png'});
console.log('search tail:', (await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(-200));
await p.keyboard.press('Escape'); await p.waitForTimeout(500);
// 2) thread view in SleepNoMore — click a "N 条回复"
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${SNM}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
const rep = p.locator('text=/\\d+ 条回复/').first();
if(await rep.count()){ await rep.click(); await p.waitForTimeout(2500); await p.screenshot({path:'./shots/31-thread-view.png'}); console.log('thread opened'); }
else console.log('no reply link');
// 3) task detail — click a 任务 # tag
const tt = p.locator('text=/任务 #\\d+/').first();
if(await tt.count()){ await tt.click(); await p.waitForTimeout(2500); await p.screenshot({path:'./shots/32-task-detail.png'}); console.log('task detail opened'); }
else console.log('no task tag');
await b.close();
