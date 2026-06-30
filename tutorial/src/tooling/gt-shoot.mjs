import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const JOBS=JSON.parse(process.argv[2]); // [[path,name,action],...]
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
await ctx.addCookies([
  {name:'googtrans',value:'/zh-CN/en',domain:'app.syfo.ai',path:'/'},
  {name:'googtrans',value:'/zh-CN/en',domain:'.app.syfo.ai',path:'/'},
]);
const p = await ctx.newPage();
async function gt(){
  await p.evaluate(()=>{ if(!document.getElementById('gte')){const d=document.createElement('div');d.id='gte';d.style.cssText='position:fixed;left:-9999px';document.body.appendChild(d);}
    window.googleTranslateElementInit=function(){ new google.translate.TranslateElement({pageLanguage:'zh-CN',includedLanguages:'en',autoDisplay:false},'gte'); }; });
  await p.addScriptTag({url:'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit'}).catch(()=>{});
  await p.waitForTimeout(5500);
  // hide banner + reset body offset
  await p.addStyleTag({content:'.goog-te-banner-frame,.skiptranslate{display:none!important;visibility:hidden!important} body{top:0!important;position:static!important}'}).catch(()=>{});
  await p.evaluate(()=>{document.body.style.top='0px';});
  await p.waitForTimeout(800);
}
for(const [path,name,action] of JOBS){
  try{
    await p.goto('https://app.syfo.ai'+path,{waitUntil:'networkidle',timeout:50000});
    await p.waitForTimeout(3000);
    if(action==='search'){ await p.keyboard.press('Meta+k'); await p.waitForTimeout(900); await p.keyboard.type('noise',{delay:50}); await p.waitForTimeout(1200); }
    if(action==='thread'){ const r=p.locator('text=/\\d+ repl/i').first(); if(await r.count()){await r.click();await p.waitForTimeout(2200);} }
    await gt();
    await p.screenshot({path:`./shots-en/${name}.png`});
    console.log('OK',name);
  }catch(e){ console.log('ERR',name,e.message.slice(0,60)); }
}
await b.close();
