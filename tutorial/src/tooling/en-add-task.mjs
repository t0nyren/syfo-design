import pkg from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.js';
const { chromium } = pkg;
const SLUG='mini-pc-on-syfo';
const CH='019f18bc-8421-7f5b-af13-3ea4b837c5d2';
const b = await chromium.launch();
const ctx = await b.newContext({ storageState:'./.state.json', locale:'en-US', viewport:{width:1440,height:900}, deviceScaleFactor:2 });
const p = await ctx.newPage();
await p.goto(`https://app.syfo.ai/s/${SLUG}/channel/${CH}`,{waitUntil:'networkidle',timeout:50000});
await p.waitForTimeout(2800);
// find header member button
const info = await p.$$eval('button', es=>es.map(e=>{const r=e.getBoundingClientRect();return {al:e.getAttribute('aria-label'),x:Math.round(r.x),y:Math.round(r.y)};}).filter(o=>o.y<70&&o.x>600&&o.al));
console.log('hdr btns:', JSON.stringify(info));
const mb = info.find(o=>/member|agent|people/i.test(o.al));
await p.mouse.click(mb.x+10, mb.y+12); await p.waitForTimeout(1400);
// search input placeholder English
const sp = await p.$('input[placeholder*="Search" i]');
await sp.fill('Guide'); await p.waitForTimeout(1400);
await p.screenshot({path:'./shots-en/24-add-lina-search.png'});
const rowBtn = p.locator('xpath=//*[contains(text(),"Guide")]/ancestor::*[self::div or self::li][1]//button').last();
await rowBtn.click({timeout:5000});
await p.waitForTimeout(2000);
// close popover
await p.keyboard.press('Escape'); await p.waitForTimeout(800);
// composer
const comp = p.locator('[placeholder*="tutorial-demo-en"], [contenteditable=true]').first();
await comp.click(); await p.waitForTimeout(400);
await p.keyboard.type('@Guide',{delay:60}); await p.waitForTimeout(1400);
await p.screenshot({path:'./shots-en/26-mention-picker.png'});
await p.keyboard.press('Enter'); await p.waitForTimeout(500);
await p.keyboard.type(' Please put together a "Syfo 5-minute starter checklist": 5 bullet points on what a new user should do first after joining Syfo (log in → join a channel → post & @mention → create a task → meet the Agents). One sentence each, in English. Post the list here when done.',{delay:3});
await p.waitForTimeout(400);
// check "as task"
await p.getByText(/as task/i).first().click().catch(e=>console.log('as task err',e.message));
await p.waitForTimeout(400);
await p.screenshot({path:'./shots-en/27-composed-task.png'});
// send
await p.getByRole('button',{name:/Create task|Send/i}).last().click().catch(async()=>{await p.keyboard.press('Enter');});
await p.waitForTimeout(3500);
const t=(await p.innerText('body')).replace(/\n{2,}/g,' ');
console.log('posted starter checklist?', t.includes('starter checklist'));
console.log('task#:', (t.match(/Task #\d+|#\d+/)||[''])[0]);
await b.close();
