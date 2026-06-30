import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
// set googtrans cookie for the domain to force zh->en
await ctx.addCookies([
  {name:'googtrans',value:'/zh-CN/en',domain:'app.syfo.ai',path:'/'},
  {name:'googtrans',value:'/zh-CN/en',domain:'.app.syfo.ai',path:'/'},
]);
const p = await ctx.newPage();
await p.goto('https://app.syfo.ai/s/mini-pc-on-syfo/channel/019e72d2-2f66-751a-a01c-6df8e5e1b2fd',{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
// inject GT element
await p.evaluate(()=>{ if(!document.getElementById('gte')){const d=document.createElement('div');d.id='gte';d.style.position='fixed';d.style.left='-9999px';document.body.appendChild(d);}
  window.googleTranslateElementInit=function(){ new google.translate.TranslateElement({pageLanguage:'zh-CN',includedLanguages:'en',autoDisplay:false},'gte'); }; });
await p.addScriptTag({url:'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit'}).catch(e=>console.log('script err',e.message));
await p.waitForTimeout(6000);
const t=(await p.innerText('body')).replace(/\n{2,}/g,' ').slice(0,400);
console.log('after GT:', t);
await p.screenshot({path:'./shots-en/_gt-test.png'});
await b.close();
