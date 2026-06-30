import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const b = await chromium.launch();
const ctx = await b.newContext({ viewport:{width:1240,height:860}, deviceScaleFactor:1.4 });
const p = await ctx.newPage();
await p.goto('https://syfo-guide.secondlife.today/',{waitUntil:'networkidle',timeout:40000});
await p.waitForTimeout(2500);
await p.screenshot({path:'/tmp/live-top.png'});
await b.close(); console.log('ok');
