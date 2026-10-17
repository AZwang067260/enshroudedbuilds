const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1200,height:630}});
await p.goto('file://' + __dirname + '/og.html'); await p.evaluate(() => document.fonts.ready);
await p.screenshot({path: process.argv[2]}); await b.close(); })();
