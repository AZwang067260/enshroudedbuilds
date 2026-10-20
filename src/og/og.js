// Usage: node og.js out.png                      -> renders og.html
//        node og.js page.html out.png [...pairs]  -> renders each page.html to out.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const args = process.argv.slice(2);
  const jobs = args.length === 1 ? [[path.join(__dirname, 'og.html'), args[0]]] : [];
  for (let i = 0; i + 1 < args.length && args.length > 1; i += 2) jobs.push([path.resolve(args[i]), args[i + 1]]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [src, out] of jobs) {
    await p.goto('file://' + src); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: out });
  }
  await b.close();
})();
