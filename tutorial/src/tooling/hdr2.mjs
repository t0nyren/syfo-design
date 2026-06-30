import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const CH='019f17fa-da4c-73ec-a064-d65ffb247645';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
// list top-bar buttons with bounding box y<70
const info = await p.$$eval('button', es=>es.map(e=>{const r=e.getBoundingClientRect();return {al:e.getAttribute('aria-label'), tx:e.innerText.trim().slice(0,12), x:Math.round(r.x), y:Math.round(r.y)};}).filter(o=>o.y<70 && o.x>600));
console.log(JSON.stringify(info,null,1));
await b.close();
