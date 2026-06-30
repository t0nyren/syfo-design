import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/inbox`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2500);
await p.click('[aria-label="新建频道"]',{force:true});
await p.waitForTimeout(1800);
await p.fill('input[placeholder="my-channel"]','tutorial-demo');
// description
const ta = await p.$('textarea'); if(ta) await ta.fill('Syfo 教程示例频道：演示新建项目、派发任务、Agent 协作与产出。');
// select 公开
await p.click('text=公开');
await p.waitForTimeout(500);
await p.screenshot({path:'./shots/15-new-channel-filled.png'});
await p.click('button:has-text("创建")');
await p.waitForTimeout(4000);
console.log('URL:', p.url());
console.log('TITLE:', await p.title());
await p.screenshot({path:'./shots/16-channel-created.png'});
console.log((await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,400));
await b.close();
