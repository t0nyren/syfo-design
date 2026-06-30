import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='reorc';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/members`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
await (await p.$('text=创建 Agent')).click();
await p.waitForTimeout(1800);
await p.click('text=My Own Computer');
await p.waitForTimeout(600);
// computer select
const sel = p.locator('text=选择电脑').first();
await sel.click();
await p.waitForTimeout(900);
await p.screenshot({path:'./shots/bb-computer-dropdown.png'});
// choose breeze-cobra-99 option
const opt = p.locator('text=breeze-cobra-99').last();
await opt.click({timeout:5000}).catch(e=>console.log('comp opt err',e.message));
await p.waitForTimeout(800);
await p.click('text=下一步');
await p.waitForTimeout(1800);
// step2 fields
await p.fill('input[placeholder="marketing-expert"]','Bill-Bain').catch(async()=>{
  const inputs=await p.$$('input'); if(inputs[0]) await inputs[0].fill('Bill-Bain'); });
await p.fill('input[placeholder="Research Agent"]','Bill Bain').catch(()=>{});
const ta=await p.$('textarea'); if(ta) await ta.fill('贝恩公司（Bain & Company）创始人 Bill Bain。');
await p.waitForTimeout(400);
await p.screenshot({path:'./shots/bb-step2-filled.png'});
// dump current model value + options by clicking model select
console.log('STEP2 text:', (await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,900));
await b.close();
