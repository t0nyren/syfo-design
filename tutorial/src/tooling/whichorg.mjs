import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
// open ReOrc org
await p.goto('https://app.syfo.ai/s/minilu2008/inbox',{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
const el = await p.$('[aria-label="ReOrc"]');
if(el){ await el.click(); await p.waitForTimeout(3500); }
console.log('ReOrc URL:', p.url());
const slug = p.url().split('/s/')[1].split('/')[0];
console.log('SLUG:', slug);
// channels containing orientation?
const chans = await p.$$eval('a[href*="/channel/"]', as=>[...new Set(as.map(a=>a.innerText.trim().split('\n')[0]))]);
console.log('has syfo-orientation channel?', chans.some(c=>/orientation|orient|引导/i.test(c)));
console.log('channels sample:', JSON.stringify(chans.slice(0,30)));
// computers
await p.goto(`https://app.syfo.ai/s/${slug}/computers`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
const body=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('has breeze-cobra-99?', body.includes('breeze-cobra-99'));
console.log('computers region:', body.slice(body.indexOf('电脑 ·'), body.indexOf('电脑 ·')+200));
await b.close();
