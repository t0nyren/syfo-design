import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/inbox`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2800);
// find new-channel button by aria-label containing channel
const btn = await p.$('[aria-label="New channel"]');
console.log('btn aria:', btn? await btn.getAttribute('aria-label'):'none');
await btn.click({force:true});
await p.waitForTimeout(1800);
await p.fill('input[placeholder="my-channel"]','tutorial-demo-en');
const ta=await p.$('textarea'); if(ta) await ta.fill('Syfo tutorial demo channel: new project, task assignment, agent collaboration & deliverables.');
// select Public
await p.getByText(/Public/i).first().click().catch(()=>{});
await p.waitForTimeout(400);
await p.screenshot({path:'./shots-en/14-new-channel-dialog.png'});
await p.locator('button').filter({hasText:/^Create$/}).last().click().catch(async()=>{ await p.getByRole('button',{name:'Create'}).last().click(); });
await p.waitForTimeout(4500);
console.log('URL:',p.url());
await p.screenshot({path:'./shots-en/16-channel-created.png'});
const t=(await p.innerText('body')).replace(/\n{2,}/g,' ');
console.log('has tutorial-demo-en?', t.includes('tutorial-demo-en'));
console.log('CHID:', p.url().split('/channel/')[1]||'');
await b.close();
