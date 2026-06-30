import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const CH='019f17fa-da4c-73ec-a064-d65ffb247645';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2800);
// dump header aria-labels/buttons
const btns = await p.$$eval('button,[role=button]', es=>es.map(e=>e.getAttribute('aria-label')||e.getAttribute('title')||e.innerText.trim().slice(0,20)).filter(Boolean));
console.log('BTNS:', JSON.stringify([...new Set(btns)].slice(0,40)));
await p.screenshot({path:'./shots/20-empty-channel.png'});
await b.close();
