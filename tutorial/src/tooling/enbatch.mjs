import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SHOTS = JSON.parse(process.argv[2]);
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
for(const [path,name,wait=3200] of SHOTS){
  try{ await p.goto('https://app.syfo.ai'+path,{waitUntil:'networkidle',timeout:50000}); await p.waitForTimeout(wait);
    await p.screenshot({path:`./shots-en/${name}.png`});
    const t=(await p.innerText('body')).replace(/\n{2,}/g,' ').slice(0,140);
    console.log(`OK ${name} :: ${t}`);
  }catch(e){ console.log(`ERR ${name}: ${e.message}`); }
}
await b.close();
