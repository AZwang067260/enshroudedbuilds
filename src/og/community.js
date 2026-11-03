// Usage: node community.js <public dir> <jobs.json> <out dir>
// Opens each community build in the built planner (files served from <public dir> through request routing),
// names it and saves the planner's own "save as image" card.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [root, jobsFile, outDir] = process.argv.slice(2);
const jobs = JSON.parse(fs.readFileSync(jobsFile));
const ORIGIN = 'https://enshroudedbuilds.org';
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png' };
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {};
  const b = await chromium.launch(proxy);
  fs.mkdirSync(outDir, { recursive: true });
  for (const [slug, name, code] of jobs) {
    const ctx = await b.newContext({ acceptDownloads: true, ignoreHTTPSErrors: true });
    await ctx.route(/googletagmanager|googlesyndication|google-analytics/, r => r.abort());
    await ctx.route(ORIGIN + '/**', r => {
      let f = path.join(root, decodeURIComponent(new URL(r.request().url()).pathname));
      if (f.endsWith(path.sep)) f = path.join(f, 'index.html');
      if (!fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
      r.fulfill({ status: 200, contentType: types[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) });
    });
    const p = await ctx.newPage();
    await p.goto(`${ORIGIN}/skill-planner/#c=${code}`); await p.waitForTimeout(400);
    await p.evaluate(n => { document.querySelector('#pl-name').value = n; }, name);
    const [dl] = await Promise.all([p.waitForEvent('download'), p.evaluate(() => document.querySelector('#pl-image').click())]);
    await dl.saveAs(path.join(outDir, slug + '.png'));
    await ctx.close();
  }
  await b.close();
})();
