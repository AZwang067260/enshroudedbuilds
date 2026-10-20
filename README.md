# enshroudedbuilds.org

A static Enshrouded Builds site: plain HTML + Tailwind CSS (compiled) + shadcn/ui-style components (CSS variable theme, Card / Badge / Button / Tabs / Accordion / Table).

## Structure

```
src/layout.py           Shared <head> (SEO meta, OG, JSON-LD), header, footer and UI components
src/content_builds.py   Data and copy for each class build (edit build content here)
src/build.py            Generator: home, builds hub, 9 class pages, 1.0 pages, tier list, skill tree, skill planner, sitemap and robots
src/skills_data.py      1.0 skill list (ranks, costs, effects) and build presets for the skill planner
src/planner.py          The /skill-planner/ page (interactive tree + static skill list)
src/planner.js          Skill tree planner code (GPL-3.0-or-later)
src/tree_data.py        Tree graph and build presets from the vendored game export
src/vendor/enshrouded-skill-tree/  GPL-3.0 tree data from rossicler/enshrouded-skill-tree (see its README)
src/art.py              Original SVG build illustrations (no game assets); per-build share images in public/og/
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

## Licenses

The skill planner (`src/planner.js`, `src/tree_data.py`, `src/vendor/enshrouded-skill-tree/` and the generated `public/assets/planner/`) is licensed under the GNU GPL v3.0 or later, because it uses tree data from [rossicler/enshrouded-skill-tree](https://github.com/rossicler/enshrouded-skill-tree). Enshrouded and its game text are property of Keen Games GmbH.
