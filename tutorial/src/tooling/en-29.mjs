import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const CH='019f18bc-8421-7f5b-af13-3ea4b837c5d2';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
let ok=false;
for(let i=0;i<6;i++){
  await p.goto(`https://app.syfo.ai/s/mini-pc-on-syfo/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
  await p.waitForTimeout(3500);
  const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
  // Guide replied if there's a Guide message after the task with checklist content
  const replied = /checklist/i.test(t) && (t.split('Guide').length>3) && /1\.|log in|Log in|•|- /.test(t.split('starter checklist').pop()||'');
  const hasGuideReply = t.includes('Guide') && /(\bWelcome\b|log in|Log in|Join|join a channel|checklist[\s\S]{0,400}\d)/.test(t.split('Post the list here when done.').pop()||'');
  console.log('attempt',i,'guide reply detected?', hasGuideReply);
  if(hasGuideReply){ await p.screenshot({path:'./shots-en/29-lina-output.png'}); ok=true; break; }
  await p.waitForTimeout(15000);
}
if(!ok){ await p.screenshot({path:'./shots-en/29-lina-output.png'}); console.log('captured current state (may be pending)'); }
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('TAIL:', t.slice(-400).replace(/\n/g,' '));
await b.close();
