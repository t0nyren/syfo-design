import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const CH='019f17fa-da4c-73ec-a064-d65ffb247645';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.mouse.click(1306, 20);
await p.waitForTimeout(1200);
await p.fill('input[placeholder="搜索人或 Agent…"]','导览');
await p.waitForTimeout(1500);
await p.screenshot({path:'./shots/24-add-lina-search.png'});
// click the add (person+) button on the Lina row
const row = p.locator('text=导览助手 Lina').first();
await row.waitFor({timeout:5000}).catch(()=>{});
// the add button is the last button in that row
const addBtn = p.locator('div:has-text("导览助手 Lina") >> button').last();
await addBtn.click().catch(async()=>{ await p.mouse.click(1290,725); });
await p.waitForTimeout(2000);
await p.screenshot({path:'./shots/25-lina-added.png'});
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
console.log('member count area:', t.slice(t.indexOf('成员'), t.indexOf('成员')+60));
console.log('has 导览 in 当前成员?', t.includes('导览助手'));
await b.close();
