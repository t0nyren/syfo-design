import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='reorc';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/members`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
await (await p.$('text=创建 Agent')).click(); await p.waitForTimeout(1600);
await p.click('text=My Own Computer'); await p.waitForTimeout(600);
await p.locator('text=选择电脑').first().click(); await p.waitForTimeout(800);
await p.locator('text=breeze-cobra-99').last().click(); await p.waitForTimeout(700);
await p.click('text=下一步'); await p.waitForTimeout(1600);
await p.fill('input[placeholder="marketing-expert"]','Bill-Bain');
// click model combobox
await p.locator('text=使用运行时默认模型').first().click();
await p.waitForTimeout(900);
await p.screenshot({path:'./shots/bb-model-options.png'});
const t=(await p.innerText('body')).replace(/\n{2,}/g,'\n');
// print near 'opus'
const idx=t.toLowerCase().indexOf('opus');
console.log('around opus:', t.slice(Math.max(0,idx-200), idx+200));
await b.close();
