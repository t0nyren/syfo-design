import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/members`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('AGENTS count line:', (t.match(/AGENTS · \d+/)||[''])[0]);
console.log('has guide-helper?', t.includes('guide-helper'));
console.log('has 导览助手?', t.includes('导览助手'));
// click on guide-helper if present
const link = await p.$('text=guide-helper');
if(link){ await link.click(); await p.waitForTimeout(2500);
  console.log('AGENT URL:', p.url());
  await p.screenshot({path:'./shots/19-new-agent-profile.png'});
  console.log(t.slice(0,200));
}
await b.close();
