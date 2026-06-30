import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const SHOTS = JSON.parse(process.argv[2]); // [[path,name,wait?],...]
const b = await chromium.launch();
const ctx = await b.newContext({ storageState: './.state.json', locale:'zh-CN', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
for (const [path,name,wait=3000] of SHOTS){
  try{
    await p.goto('https://app.syfo.ai'+path,{waitUntil:'networkidle',timeout:50000});
    await p.waitForTimeout(wait);
    await p.screenshot({ path:`./shots/${name}.png` });
    const txt=(await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,300).replace(/\n/g,' ');
    console.log(`OK ${name} :: ${p.url()} :: ${txt}`);
  }catch(e){ console.log(`ERR ${name}: ${e.message}`); }
}
await b.close();
