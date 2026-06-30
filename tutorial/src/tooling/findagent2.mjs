import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/members`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
// type in search box to filter
const sb = await p.$('input[placeholder="搜索成员"]');
if(sb){ await sb.fill('guide'); await p.waitForTimeout(1500); }
await p.screenshot({path:'./shots/19-agent-search.png'});
// click first result row containing guide-helper
const row = await p.$('text=guide-helper');
if(row){ await row.click(); await p.waitForTimeout(2500); console.log('URL after click:', p.url()); 
  await p.screenshot({path:'./shots/19-new-agent-profile.png'}); }
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
const idx=t.indexOf('guide-helper'); console.log(t.slice(Math.max(0,idx-40), idx+500));
await b.close();
