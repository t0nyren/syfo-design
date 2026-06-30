import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const target = process.argv[2]||'English';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto('https://app.syfo.ai/s/reorc/settings/account',{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
// open dropdown (current value text)
const cur = target==='English' ? '简体中文' : 'English';
await p.getByText(cur,{exact:true}).first().click();
await p.waitForTimeout(800);
// pick target option
await p.getByText(target,{exact:true}).last().click();
await p.waitForTimeout(600);
// click the language Save button: the 保存 button nearest the language select.
// There are two 保存 (display name + language). Click the one in the language card.
// Strategy: the language select is inside a card; find 保存 button with x near 1735 and y>600
const saves = await p.$$('button');
let clicked=false;
for(const s of saves){ const tx=(await s.innerText()).trim(); if(tx==='保存'||tx==='Save'){ const box=await s.boundingBox(); if(box && box.y>560){ await s.click(); clicked=true; break; } } }
console.log('save clicked:', clicked);
await p.waitForTimeout(4000);
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,160).replace(/\n/g,' ');
console.log('after save UI:', t);
await b.close();
