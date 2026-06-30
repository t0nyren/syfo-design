import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto('https://app.syfo.ai/s/minilu2008/inbox', { waitUntil:'networkidle', timeout:50000 });
await p.waitForTimeout(3000);
// collect all anchor hrefs that look like org links /s/<slug>
const links = await p.$$eval('a[href*="/s/"]', as => [...new Set(as.map(a=>a.getAttribute('href')))]);
console.log('ORG/LINKS:', JSON.stringify(links, null, 1));
// also dump aria-labels/titles in left rail
const labels = await p.$$eval('[aria-label],[title]', els => els.map(e=>e.getAttribute('aria-label')||e.getAttribute('title')).filter(Boolean).slice(0,60));
console.log('LABELS:', JSON.stringify([...new Set(labels)]));
await b.close();
