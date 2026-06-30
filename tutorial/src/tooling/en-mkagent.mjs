import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/members`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(3000);
await p.getByRole('button',{name:/Create agent/i}).first().click();
await p.waitForTimeout(1800);
await p.screenshot({path:'./shots-en/11-create-agent-dialog.png'});  // location step
await p.getByText('Syfo Cloud').click(); await p.waitForTimeout(500);
await p.getByText(/^Next$/).click(); await p.waitForTimeout(1800);
await p.screenshot({path:'./shots-en/13-create-agent-step2.png'});  // config step
await p.fill('input[placeholder="marketing-expert"]','guide-en');
await p.fill('input[placeholder="Research Agent"]','Guide');
const ta=await p.$('textarea'); if(ta) await ta.fill('Syfo tutorial demo cloud agent: shows how a cloud agent takes a task, does a small research, and posts a deliverable.');
await p.waitForTimeout(400);
await p.screenshot({path:'./shots-en/17-create-agent-filled.png'});  // filled
await p.getByRole('button',{name:'Create Agent'}).last().click();
await p.waitForTimeout(2500);
await p.screenshot({path:'./shots-en/18-agent-created.png'});  // progress
await p.waitForTimeout(6000);
const t=(await p.innerText('body')).replace(/\n{2,}/g,' ');
console.log('has Guide?', t.includes('Guide')||t.includes('guide-en'));
console.log('URL:',p.url());
await b.close();
