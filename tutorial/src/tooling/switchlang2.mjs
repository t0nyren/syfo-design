import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const target = process.argv[2]||'English';
const cur = target==='English' ? '简体中文' : 'English';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto('https://app.syfo.ai/s/reorc/settings/account',{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
// open + select
await p.getByText(cur,{exact:true}).first().click(); await p.waitForTimeout(700);
await p.getByText(target,{exact:true}).last().click(); await p.waitForTimeout(600);
// find language select y
const langY = await p.getByText(target,{exact:true}).first().evaluate(el=>el.getBoundingClientRect().y).catch(()=>700);
// pick the 保存/Save button with y closest to langY
const btns = await p.$$('button');
let best=null,bestd=1e9;
for(const s of btns){ const tx=(await s.innerText()).trim(); if(tx==='保存'||tx==='Save'){ const box=await s.boundingBox(); if(box){ const d=Math.abs(box.y-langY); if(d<bestd){bestd=d;best=s;} } } }
if(best){ await best.click(); console.log('clicked save (dy='+bestd.toFixed(0)+')'); }
await p.waitForTimeout(4500);
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,120).replace(/\n/g,' ');
console.log('UI now:', t);
await b.close();
