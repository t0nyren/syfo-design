import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='reorc';
const CH='019f070a-2ab0-72ab-a2ea-6c83dab3e261';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
console.log('channel title bar present:', (await p.innerText('body')).includes('syfo-orientation'));
// open member popover via header member button (aria-label 成员, has count text)
const memBtns = await p.$$('button[aria-label="成员"]');
// pick the header one (top, x>600)
let clicked=false;
for(const mb of memBtns){ const box=await mb.boundingBox(); if(box && box.y<70 && box.x>600){ await mb.click(); clicked=true; break; } }
if(!clicked && memBtns.length) await memBtns[memBtns.length-1].click();
await p.waitForTimeout(1500);
await p.fill('input[placeholder="搜索人或 Agent…"]','Bill').catch(e=>console.log('no search input',e.message));
await p.waitForTimeout(1500);
await p.screenshot({path:'./shots/bb-add-search.png'});
const rowBtn = p.locator('xpath=//*[contains(text(),"Bill Bain")]/ancestor::*[self::div or self::li][1]//button').last();
console.log('Bill rows:', await p.locator('xpath=//*[contains(text(),"Bill Bain")]').count());
await rowBtn.click({timeout:5000}).catch(e=>console.log('add click err',e.message));
await p.waitForTimeout(2500);
await p.screenshot({path:'./shots/bb-added.png'});
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('member count:', (t.match(/\d+ 个成员/)||[''])[0]);
console.log('added msg present:', t.includes('Bill Bain') );
await b.close();
