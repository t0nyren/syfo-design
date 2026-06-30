import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='reorc';
const CH='019f070a-2ab0-72ab-a2ea-6c83dab3e261';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
const info = await p.$$eval('button', es=>es.map(e=>{const r=e.getBoundingClientRect();return {al:e.getAttribute('aria-label'),tx:e.innerText.trim().slice(0,6),x:Math.round(r.x),y:Math.round(r.y)};}).filter(o=>o.y<70&&o.x>600));
console.log('header btns:', JSON.stringify(info));
// click the member one (aria 成员)
const mb = info.find(o=>o.al==='成员');
if(mb){ await p.mouse.click(mb.x+10, mb.y+12); await p.waitForTimeout(1500); }
await p.screenshot({path:'./shots/bb-add-search.png'});
await p.fill('input[placeholder="搜索人或 Agent…"]','Bill').catch(e=>console.log('no input',e.message));
await p.waitForTimeout(1500);
await p.screenshot({path:'./shots/bb-add-search.png'});
const cnt = await p.locator('xpath=//*[contains(text(),"Bill Bain")]').count();
console.log('Bill rows:', cnt);
const rowBtn = p.locator('xpath=//*[contains(text(),"Bill Bain")]/ancestor::*[self::div or self::li][1]//button').last();
await rowBtn.click({timeout:5000}).catch(e=>console.log('click err',e.message));
await p.waitForTimeout(2500);
await p.screenshot({path:'./shots/bb-added.png'});
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('member count:', (t.match(/\d+ 个成员/)||[''])[0]);
await b.close();
