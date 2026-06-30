import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/members`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
const links = await p.$$eval('a[href*="/agents/"]', as=>as.map(a=>({t:a.innerText.trim().split('\n').join(' '), h:a.getAttribute('href')})));
const g = links.filter(l=>/guide|导览|Lina/i.test(l.t));
console.log('matches:', JSON.stringify(g,null,1));
if(g[0]){ await p.goto('https://app.syfo.ai'+g[0].h,{waitUntil:'networkidle',timeout:50000}); await p.waitForTimeout(2500);
  await p.screenshot({path:'./shots/19-new-agent-profile.png'});
  console.log('AGENT URL:', p.url());
  const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
  // print profile region
  const idx=t.indexOf('导览助手'); console.log(t.slice(idx, idx+600));
}
await b.close();
