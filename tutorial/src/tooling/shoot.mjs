// usage: node shoot.mjs <urlPath> <outName> [waitMs]
import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const [,, urlPath='/', out='out', wait='3000'] = process.argv;
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
const url = urlPath.startsWith('http') ? urlPath : 'https://app.syfo.ai'+urlPath;
await p.goto(url, { waitUntil:'networkidle', timeout:50000 });
await p.waitForTimeout(parseInt(wait));
console.log('URL:', p.url());
console.log('TITLE:', await p.title());
const txt = (await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,1200);
console.log('BODY:\n'+txt);
await p.screenshot({ path:`./shots/${out}.png`, fullPage:false });
await b.close();
