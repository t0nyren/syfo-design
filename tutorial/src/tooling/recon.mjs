import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
const go = async(path)=>{ await p.goto('https://app.syfo.ai'+path,{waitUntil:'networkidle',timeout:50000}); await p.waitForTimeout(2500); };
await go(`/s/${SLUG}/inbox`);
// map channel + dm names to ids
const map = await p.evaluate(()=>{
  const out={channels:[],dms:[]};
  document.querySelectorAll('a[href*="/channel/"]').forEach(a=>{ const id=a.getAttribute('href').split('/channel/')[1]; out.channels.push({name:a.innerText.trim().split('\n')[0], id}); });
  document.querySelectorAll('a[href*="/dm/"]').forEach(a=>{ const id=a.getAttribute('href').split('/dm/')[1]; out.dms.push({name:a.innerText.trim().split('\n')[0], id}); });
  return out;
});
console.log(JSON.stringify(map,null,1));
await b.close();
