import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
const go=async(path,w=3000)=>{await p.goto('https://app.syfo.ai'+path,{waitUntil:'networkidle',timeout:50000});await p.waitForTimeout(w);};

// 1) Create Agent dialog
await go(`/s/${SLUG}/members`);
const btn = await p.$('text=创建 Agent');
if(btn){ await btn.click(); await p.waitForTimeout(2500);
  await p.screenshot({path:'./shots/11-create-agent-dialog.png'});
  const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
  // grab the dialog text region
  console.log('=== CREATE AGENT DIALOG TEXT ===');
  console.log(t.slice(0, 1500));
  // close
  await p.keyboard.press('Escape');
}
// 2) Billing settings
await go(`/s/${SLUG}/settings/billing`,2500).catch(()=>{});
await p.screenshot({path:'./shots/12-settings-billing.png'});
console.log('=== BILLING URL ===', p.url());
console.log((await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,500));
await b.close();
