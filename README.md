# enshroudedbuilds.org

A static Enshrouded Builds site: plain HTML + Tailwind CSS (compiled) + shadcn/ui-style components (CSS variable theme, Card / Badge / Button / Tabs / Accordion / Table).

## Structure

```
src/layout.py           Shared <head> (SEO meta, OG, JSON-LD), header, footer and UI components
src/content_builds.py   Data and copy for each class build (edit build content here)
src/build.py            Generator: home, builds hub, 9 class pages, 1.0 page, tier list, skill tree page, sitemap and robots
src/input.css           Tailwind entry file + shadcn theme variables (light/dark)
tailwind.config.js      Tailwind config (shadcn color tokens)
public/                 Generated output. Deploy this directory.
```

## Usage

```bash
npm install
npm run build    # generate public/ and compile public/assets/styles.css
npm run serve    # local preview at http://localhost:3000
```

Deploy `public/` to Cloudflare Pages, Netlify, Vercel or GitHub Pages (use `public/404.html` as the 404 page).

## Before launch

- Submit `https://enshroudedbuilds.org/sitemap.xml` in Google Search Console
- After each Enshrouded patch, update the copy in `content_builds.py` and the `UPDATED` / `UPDATED_HUMAN` dates in `src/layout.py`, then rebuild

## Share image

`public/og-image.png` (1200×630) is rendered from `src/og/og.html` with Playwright during `npm run build`, using local copies of the Cinzel and Inter fonts. To change the image, edit that HTML file and rebuild. If Playwright isn't installed, run `npm i -D playwright` first.
