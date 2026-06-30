import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto('https://app.syfo.ai/s/minilu2008/inbox', { waitUntil:'networkidle', timeout:50000 });
await p.waitForTimeout(2500);
const el = await p.$('[aria-label="Mini-PC on Syfo"]');
if(!el){ console.log('not found, dumping rail buttons'); 
  const bs = await p.$$eval('button,a', e=>e.map(x=>x.getAttribute('aria-label')).filter(Boolean)); console.log(bs); await b.close(); process.exit(0);}
await el.click();
await p.waitForTimeout(4000);
console.log('URL after click:', p.url());
console.log('TITLE:', await p.title());
const txt = (await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,1400);
console.log('BODY:\n'+txt);
await p.screenshot({ path:'./shots/mpc-inbox.png' });
await b.close();
