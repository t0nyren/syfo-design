import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const CH='019f17fa-da4c-73ec-a064-d65ffb247645';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
// the main content header is the top bar of chat area; find buttons within it (right side)
const main = await p.$('main') || p;
// click the "更多" button in channel header
await p.click('button[aria-label="更多"]').catch(e=>console.log('no 更多 aria',e.message));
await p.waitForTimeout(1200);
await p.screenshot({path:'./shots/22-channel-more-menu.png'});
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('MENU tail:', t.slice(-400));
await b.close();
