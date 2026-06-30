import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const target = process.argv[2]||'English'; // 'English' or '简体中文'
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto('https://app.syfo.ai/s/reorc/settings/account',{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
// find the language control. Try native select first
const selects = await p.$$('select');
console.log('native selects:', selects.length);
let done=false;
for(const s of selects){ const opts=await s.$$eval('option',os=>os.map(o=>o.text)); 
  if(opts.some(o=>/简体中文|English|中文/.test(o))){ 
    console.log('lang options:', opts);
    await s.selectOption({label: target}).catch(async()=>{ await s.selectOption({label: target==='English'?'English':'简体中文'}); });
    done=true; break; } }
if(!done){
  // custom: click the element showing current language then pick
  console.log('no native lang select; dumping settings tail');
  console.log((await p.innerText('body')).replace(/\n{2,}/g,'\n').slice(0,600));
}
await p.screenshot({path:'./shots/lang-before-save.png'});
await b.close();
console.log('done part1, native?',done);
