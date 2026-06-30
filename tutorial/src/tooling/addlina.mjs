import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const CH='019f17fa-da4c-73ec-a064-d65ffb247645';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.mouse.click(1306, 20); // header member button
await p.waitForTimeout(1500);
await p.screenshot({path:'./shots/23-member-popover.png'});
const t1=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('POPOVER tail:', t1.slice(-350));
await b.close();
