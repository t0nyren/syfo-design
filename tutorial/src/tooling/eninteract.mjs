import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const SNM='019e72d2-2f66-751a-a01c-6df8e5e1b2fd';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
// billing
await p.goto(`https://app.syfo.ai/s/${SLUG}/settings/account`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.getByText(/Subscription|Credits|Billing/i).first().click().catch(e=>console.log('billing nav err',e.message));
await p.waitForTimeout(2500);
await p.screenshot({path:'./shots-en/12-settings-billing.png'});
console.log('billing:',(await p.innerText('body')).replace(/\n{2,}/g,' ').slice(0,200));
// search palette
await p.goto(`https://app.syfo.ai/s/${SLUG}/inbox`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.keyboard.press('Meta+k'); await p.waitForTimeout(1000);
await p.keyboard.type('noise',{delay:50}); await p.waitForTimeout(1500);
await p.screenshot({path:'./shots-en/30-search-palette.png'});
await p.keyboard.press('Escape'); await p.waitForTimeout(400);
// thread (32)
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${SNM}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
const rep = p.locator('text=/\\d+ repl/i').first();
if(await rep.count()){ await rep.click(); await p.waitForTimeout(2500); await p.screenshot({path:'./shots-en/32-task-detail.png'}); console.log('thread ok'); }
else { console.log('no reply link; trying 条回复'); const r2=p.locator('text=/repl|回复/').first(); if(await r2.count()){await r2.click();await p.waitForTimeout(2500);await p.screenshot({path:'./shots-en/32-task-detail.png'});} }
await b.close();
