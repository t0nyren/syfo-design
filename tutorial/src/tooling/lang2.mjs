import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto('https://app.syfo.ai/s/reorc/settings/account',{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
// scroll to 语言
await p.getByText('语言',{exact:true}).first().scrollIntoViewIfNeeded().catch(()=>{});
await p.waitForTimeout(500);
// the control showing 简体中文
const ctl = p.getByText('简体中文',{exact:true}).first();
await ctl.scrollIntoViewIfNeeded().catch(()=>{});
await p.screenshot({path:'./shots/lang-area.png'});
await ctl.click();
await p.waitForTimeout(900);
await p.screenshot({path:'./shots/lang-open.png'});
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
const i=t.indexOf('简体中文'); console.log('after open:', t.slice(i-20,i+120).replace(/\n/g,' '));
await b.close();
