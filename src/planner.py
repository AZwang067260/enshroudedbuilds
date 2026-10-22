"""The /skill-planner/ page: an interactive skill tree (src/planner.js) plus a static, crawlable list of every 1.0 skill."""
import json

from layout import UPDATED_HUMAN, badge, e
from skills_data import TREE
from tree_data import BIOMES, BUILD_ID, NODES, PROGRESSION, RAW, STAGES, build_preset, our_name, skill_cost

AREA_COLORS = {"Mage": "#60a5fa", "Warrior": "#f87171", "Ranger": "#4ade80", "Core": "#fbbf24"}

PLANNER_FAQ = [
    ("How many skill points do you get in Enshrouded 1.0?", "212 at level 50 if you explore everything: 2 points for every level from 2 to 50 (98), plus 114 from exploration, 1 for each Shroud Root and 3 for each Elixir Well, spread over the seven biomes."),
    ("How many points does it take to fill the whole skill tree?", "675 points. A level 50 character can afford roughly a third of the tree, so every build has to choose."),
    ("Is there an Enshrouded skill calculator or build planner?", "Yes, this page. The Enshrouded skill planner works as a skill calculator and build planner in one: it adds up the points your build costs, compares them with your budget for your level and explored biomes, and shows the attributes you end up with."),
    ("Does this planner follow the real skill tree connections?", "Yes. The tree uses the node positions and links exported from the Enshrouded 1.0 game files: 231 nodes and 291 links. You can only learn a skill that connects to one you already have, starting from the entry nodes around the center, exactly like in the game. Refunding a skill also refunds anything that would lose its connection."),
    ("Is this the same skill tree as the game?", f"Yes. The data comes from the 1.0 game files (Steam build {BUILD_ID}), including the in-game skill text you see in the details panel. Keen Games can still change values in hotfixes, so the in-game tooltip always wins."),
    ("Can I share my build?", "Yes. Every change updates the page address. Use Copy build link and send it to a friend: the link opens the planner with your exact build, level, flame level and explored biomes."),
    ("What does the Flame level do?", "Every Flame level after the first adds 1 point to each attribute, and Flame nodes like Thick Skin or Exalted add 1 more point of their attribute for every 2 Flame levels."),
]

BUILD_NAMES = [("wizard", "Wizard / Mage"), ("battlemage", "Battlemage"), ("necromancer", "Necromancer / Summoner"), ("healer", "Healer"),
               ("warrior", "Warrior"), ("tank", "Tank"), ("barbarian", "Barbarian"), ("ranger", "Ranger"), ("assassin", "Assassin")]

STYLE = """
#tree-svg{touch-action:none;cursor:grab;user-select:none}
#tree-svg:active{cursor:grabbing}
.tr-core{fill:none;stroke:hsl(var(--border));stroke-width:2;stroke-dasharray:4 6}
.tr-link{stroke:hsl(var(--muted-foreground)/.28);stroke-width:2}
.tr-link.tr-on{stroke:#fb923c;stroke-width:3.5}
.tr-node{cursor:pointer}
.tr-hit{fill:transparent}
.tr-dot{fill:hsl(var(--card));stroke:var(--c);stroke-width:2;opacity:.45}
.tr-ini{font:600 9px Inter,sans-serif;fill:hsl(var(--muted-foreground));pointer-events:none}
.tr-rank{font:600 9px Inter,sans-serif;fill:hsl(var(--muted-foreground));pointer-events:none}
.tr-label{font:700 30px Cinzel,serif;letter-spacing:.12em;opacity:.55;pointer-events:none}
[data-state=open] .tr-dot{opacity:1;stroke-width:3;filter:drop-shadow(0 0 6px var(--c))}
[data-state=open] .tr-ini{fill:hsl(var(--foreground))}
[data-state=on] .tr-dot,[data-state=max] .tr-dot{fill:var(--c);opacity:1;stroke:#fff;stroke-width:2}
[data-state=on] .tr-ini,[data-state=max] .tr-ini{fill:#111}
[data-state=on] .tr-rank,[data-state=max] .tr-rank{fill:hsl(var(--foreground))}
[data-state=max] .tr-dot{stroke:#fde68a;stroke-width:3}
.tr-focus .tr-dot{stroke:#fff;stroke-width:4;opacity:1}
.tr-searching .tr-node{opacity:.25}
.tr-searching .tr-node.tr-hitq{opacity:1}
.tr-hitq .tr-dot{filter:drop-shadow(0 0 10px #facc15);stroke:#facc15;opacity:1}
.tr-btn{display:inline-flex;height:1.9rem;width:1.9rem;align-items:center;justify-content:center;border-radius:.4rem;border:1px solid hsl(var(--border));font-weight:700;background:hsl(var(--background))}
.tr-btn:hover{background:hsl(var(--accent))}
"""


def type_key_by_name():
    return {our_name(k): k for k in RAW["types"]}


TIERS = [("S", "Strongest picks for 1.0"), ("A", "Strong with the right playstyle or group"), ("B", "Situational, high skill")]


def stage_picks(slug):
    """Per stage: what the preset adds over the previous stage, as (skills [(name, rank, max)], attribute counts {attr: n})."""
    out, prev_skills, prev_attrs = [], {}, {}
    for label, budget, _ in STAGES:
        skills, attrs = {}, {}
        for nid, rank in build_preset(slug, budget)[0].items():
            name = our_name(NODES[nid]["type"])
            if name.endswith(" node"):
                attrs[name[:-5]] = attrs.get(name[:-5], 0) + 1
            else:
                skills[name] = max(skills.get(name, 0), rank)
        new_skills = [(n, r, skill_cost(n)[1]) for n, r in skills.items() if r > prev_skills.get(n, 0)]
        new_attrs = {a: c - prev_attrs.get(a, 0) for a, c in attrs.items() if c > prev_attrs.get(a, 0)}
        out.append((label, budget, new_skills, new_attrs))
        prev_skills, prev_attrs = skills, attrs
    return out


def build_ranking(builds_lookup):
    """Tiered list of our builds; each card loads its stage presets into the planner above and links to the full guide."""
    btn = "inline-flex h-8 items-center justify-center rounded-md border px-2.5 text-xs font-medium hover:bg-accent data-[on]:border-primary data-[on]:bg-primary data-[on]:text-primary-foreground"
    html = ""
    for tier, blurb in TIERS:
        cards = ""
        for slug, _ in BUILD_NAMES:
            b = builds_lookup[slug]
            if b["tier"] != tier:
                continue
            stages = stage_picks(slug)
            loads = "".join(
                f'<a href="#b={slug}&amp;s={i if i < 3 else 0}" data-load="{slug}" data-stage="{i if i < 3 else 0}" class="{btn}">Lv {label.split(" ")[1]}</a>'
                for i, (label, _, _, _) in enumerate(stages, 1))
            steps = ""
            for label, budget, skills, attrs in stages:
                items = ", ".join(f"{e(n)}" + (f" {r}/{m}" if m > 1 else "") for n, r, m in skills)
                extra = ", ".join(f"+{c} {e(a)}" for a, c in attrs.items())
                steps += (f'<li><p class="font-medium">{label} <span class="text-muted-foreground">({budget} points)</span></p>'
                          f'<p class="text-muted-foreground">{items or "Ranks only"}{"; attributes: " + extra if extra else ""}</p></li>')
            cards += f'''<div class="flex flex-col rounded-lg border bg-card p-4 shadow-sm">
  <div class="flex items-center justify-between gap-2"><h4 class="text-base font-semibold">{e(b["short"])} build</h4><span class="text-xs text-muted-foreground">{e(b["difficulty"])}</span></div>
  <p class="mt-1 text-xs text-muted-foreground">{e(b["role"])} · {e(b["weapon"])}</p>
  <p class="mt-3 text-xs font-medium">Load into the planner:</p>
  <div class="mt-1.5 flex flex-wrap gap-1.5">{loads}</div>
  <details class="mt-3 text-xs"><summary class="cursor-pointer font-medium text-primary">What to take at each level</summary><ol class="mt-2 space-y-2">{steps}</ol></details>
  <a href="/builds/{slug}/" class="mt-auto pt-3 text-sm font-medium text-primary hover:underline">Full {e(b["short"])} guide: gear, spells and skill order →</a>
</div>'''
        html += (f'<h3 class="mb-3 mt-8 flex items-center gap-2 text-xl font-bold">{badge(tier + "-Tier", "primary" if tier == "S" else "outline")}'
                 f'<span class="text-sm font-normal text-muted-foreground">{blurb}</span></h3><div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{cards}</div>')
    return f'''<section id="best-builds" class="container scroll-mt-16 py-8" aria-labelledby="best-builds-h">
<h2 id="best-builds-h" class="text-2xl font-bold md:text-3xl">Best Enshrouded 1.0 builds: load any build by level</h2>
<p class="mt-2 max-w-3xl text-muted-foreground">Our nine 1.0 builds, ranked by tier. Pick a level range to load that stage of the build into the planner above, with the matching level and explored biomes. Open <em>What to take at each level</em> to see which skills each stage adds, and the full guide for gear, spells and playstyle. Rankings explained in the <a href="/tier-list/" class="text-primary hover:underline">tier list</a>.</p>
{html}
</section>'''


def planner_page(builds_lookup):
    keys = type_key_by_name()
    field = "h-9 w-full rounded-md border bg-background px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    small_btn = "inline-flex h-9 w-9 items-center justify-center rounded-md border bg-background/90 text-lg font-semibold hover:bg-accent"

    options = "".join(f'<option value="{s}">{e(n)} build</option>' for s, n in BUILD_NAMES)
    biomes = "".join(f'<label class="flex items-center justify-between gap-2 py-0.5"><span class="flex items-center gap-2"><input type="checkbox" checked data-biome="{k}" data-points="{PROGRESSION["biomes"][k]["points"]}" class="h-4 w-4 accent-[hsl(var(--primary))]">{e(label)}</span><span class="text-muted-foreground">+{PROGRESSION["biomes"][k]["points"]}</span></label>' for k, label in BIOMES)
    legend = "".join(f'<span class="inline-flex items-center gap-1.5"><i class="inline-block h-2.5 w-2.5 rounded-full" style="background:{c}"></i>{a}</span>' for a, c in AREA_COLORS.items())
    controls = f'''
<div class="space-y-4 rounded-lg border bg-card p-4 shadow-sm">
  <label class="block text-xs font-medium">Load a build<select id="pl-preset" class="mt-1 {field}"><option value="">Empty tree</option>{options}</select></label>
  <div>
    <div class="flex items-baseline justify-between text-sm"><span>Points spent</span><span><strong id="pl-spent">0</strong> / <span id="pl-budget">212</span></span></div>
    <div class="mt-2 h-2 overflow-hidden rounded-full bg-secondary"><div id="pl-bar" class="h-full bg-primary transition-all" style="width:0"></div></div>
    <p class="mt-2 text-sm">Points left: <strong id="pl-left">212</strong></p>
    <p id="pl-over" hidden class="mt-1 text-xs font-medium text-destructive">Over budget: raise your level or explored biomes, or refund skills.</p>
    <p id="pl-areas" class="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs"></p>
  </div>
  <div class="grid grid-cols-2 gap-3">
    <label class="text-xs font-medium">Level (1–{PROGRESSION["leveling"]["playerLevelCap"]})<input id="pl-level" type="number" min="1" max="{PROGRESSION["leveling"]["playerLevelCap"]}" value="{PROGRESSION["leveling"]["playerLevelCap"]}" class="mt-1 {field}"></label>
    <label class="text-xs font-medium">Flame level (1–{PROGRESSION["flame"]["flameLevelCap"]})<input id="pl-flame" type="number" min="1" max="{PROGRESSION["flame"]["flameLevelCap"]}" value="{PROGRESSION["flame"]["flameLevelCap"]}" class="mt-1 {field}"></label>
  </div>
  <details class="rounded-md border px-3 py-2 text-sm"><summary class="flex items-center justify-between text-xs font-medium">Explored biomes (Shroud Roots &amp; Elixir Wells) <span class="text-muted-foreground">▾</span></summary><div class="mt-2 space-y-0.5">{biomes}</div></details>
  <div><p class="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Attributes</p><ul id="pl-attrs" class="space-y-1 text-sm"></ul></div>
  <label class="block text-xs font-medium">Build name for the image (optional)<input id="pl-name" type="text" maxlength="40" placeholder="e.g. Frost Necro" class="mt-1 {field}"></label>
  <div class="flex gap-2"><button id="pl-copy" type="button" class="inline-flex h-9 flex-1 items-center justify-center rounded-md bg-primary px-3 text-sm font-medium text-primary-foreground hover:bg-primary/90">Copy build link</button>
  <button id="pl-reset" type="button" class="inline-flex h-9 items-center justify-center rounded-md border px-3 text-sm font-medium hover:bg-accent">Reset</button></div>
  <button id="pl-image" type="button" class="inline-flex h-9 w-full items-center justify-center rounded-md border px-3 text-sm font-medium hover:bg-accent">Save as image</button>
</div>'''

    guide_links = " · ".join(f'<a href="/builds/{s}/">{e(builds_lookup[s]["short"])}</a>' for s, _ in BUILD_NAMES)
    body = f'''<style>{STYLE}</style>
<div class="hero-glow border-b"><div class="container py-8 md:py-10">{{crumbs}}
<div class="flex flex-wrap gap-2">{badge("Free tool", "primary")}{badge("Enshrouded 1.0", "outline")}{badge("231 nodes · 178 skills · 212 points", "outline")}{badge("Game build " + BUILD_ID, "outline")}</div>
<h1 class="mt-4 max-w-4xl text-3xl font-bold tracking-tight md:text-5xl">Enshrouded Skill Planner (1.0)</h1>
<p class="mt-3 max-w-3xl text-lg text-muted-foreground">This free <strong>Enshrouded skill planner</strong> shows the real 1.0 skill tree, with every node and link taken from the game files. Plan your build point by point, check your 212-point budget and share it with one link.</p>
<p class="mt-4"><a href="#best-builds" class="inline-flex h-9 items-center justify-center rounded-md border bg-background/60 px-4 text-sm font-medium hover:bg-accent">Load a top 1.0 build by level ↓</a></p>
</div></div>
<section id="planner" class="container scroll-mt-16 py-6" aria-label="Enshrouded skill tree planner">
  <noscript><p class="mb-4 rounded-md border p-3 text-sm">The skill planner needs JavaScript. The <a href="/skill-tree/#all-skills">full skill list</a> works without it.</p></noscript>
  <div class="grid gap-6 lg:grid-cols-[1fr_330px]" data-pl-js hidden>
    <div class="min-w-0">
      <div class="relative overflow-hidden rounded-xl border bg-card shadow-sm">
        <div class="absolute inset-x-3 top-3 z-10 flex gap-2">
          <input id="pl-search" type="search" placeholder="Search skills, e.g. Blink, Unity, Puncture" aria-label="Search skills" class="{field} max-w-xs bg-background/90">
          <div class="ml-auto flex gap-1.5"><button id="tr-zoom-out" type="button" class="{small_btn}" aria-label="Zoom out">−</button><button id="tr-fit" type="button" class="{small_btn} text-sm" aria-label="Fit tree">⌂</button><button id="tr-zoom-in" type="button" class="{small_btn}" aria-label="Zoom in">+</button></div>
        </div>
        <svg id="tree-svg" viewBox="-900 -900 1800 1800" class="block h-[68vh] min-h-[460px] w-full" role="img" aria-label="Enshrouded 1.0 skill tree"><g id="tree-view"></g></svg>
        <div class="absolute inset-x-3 bottom-3 flex flex-wrap items-center justify-between gap-2 text-xs text-muted-foreground"><span class="flex flex-wrap gap-3 rounded-md bg-background/80 px-2 py-1">{legend}</span><span class="rounded-md bg-background/80 px-2 py-1">Drag to pan · scroll or pinch to zoom · right-click to refund</span></div>
        <p id="pl-notice" hidden role="status" class="absolute left-1/2 top-16 z-10 -translate-x-1/2 rounded-md bg-foreground px-3 py-2 text-sm text-background shadow"></p>
      </div>
      <div id="pl-info" class="mt-4 rounded-lg border bg-card p-4" aria-live="polite"></div>
    </div>
    <aside>{controls}</aside>
  </div>
</section>
{build_ranking(builds_lookup)}
<div class="container"><article class="prose-eb mx-auto max-w-4xl">
<h2 id="about-planner">Enshrouded skill tree planner for the 1.0 release</h2>
<p>Enshrouded 1.0 reset every character's skill tree, so most players are re-planning their build right now. This <strong>Enshrouded skill tree planner</strong> lets you do that before you spend a single point in the game. It draws the full 1.0 tree, with 231 nodes covering 178 different skills, at the positions and with the links the game uses. Like in Enshrouded itself, you can only learn a skill that connects to one you already have.</p>
<p>Use the skill planner to test a new build, compare two paths to the same capstone, or check how many points a hybrid really costs. When you like the result, copy the build link and share it with your group.</p>
<h2 id="how-to-use">How to use the Enshrouded skill planner</h2>
<ol class="my-4 list-decimal space-y-2 pl-5">
<li><strong>Load a build or start empty.</strong> Each preset is the level 50 version of one of our guides, following real paths through the tree: {guide_links}.</li>
<li><strong>Start at the center.</strong> Glowing nodes are the ones you can learn now, starting from the entry nodes next to the center ring.</li>
<li><strong>Click to add a rank, right-click to refund.</strong> On phones, tap once to see a skill and tap again to add it; use the − button in the details panel to refund. Refunding a skill also refunds anything that would lose its connection.</li>
<li><strong>Set your level, Flame level and explored biomes.</strong> The planner adjusts your point budget and attributes to match.</li>
<li><strong>Share it.</strong> The address updates with every click, so Copy build link always shares your current plan. <em>Save as image</em> creates a picture of your tree, attributes and key skills to post on Reddit or Discord; give it a name first if you like.</li>
</ol>
<h2 id="skill-points">Enshrouded build calculator: skill points at every level</h2>
<p>The planner works as a <strong>skill point calculator</strong> too. You earn 2 skill points per level after level 1 (98 at level 50), 1 point for every Shroud Root and 3 for every Elixir Well. Exploration adds 114 points across the seven biomes, for <strong>212 skill points at level 50</strong> on a fully explored character. Filling the whole tree would cost 675 points, so every Enshrouded build has to commit to one area and borrow only the best skills from its neighbours. Untick the biomes you have not finished yet to see your real budget today.</p>
<h2 id="respec">Respec your build after the 1.0 reset</h2>
<p>Every existing character got a free skill tree reset when loading a save in 1.0. After that, you respec at the Flame Altar. Plan the new build in the skill planner first so you only respec once. The <a href="/skill-tree/#respec">skill tree guide</a> explains respec costs and rules, and lists every skill with its effect.</p>
{{faq}}
<h2 id="credits">Data and license</h2>
<p>The tree layout, links, costs and in-game skill text come from the open-source <a href="https://www.enshrouded-skill-tree.com/" rel="noopener" target="_blank">Enshrouded Skill Planner</a> project (<a href="https://github.com/rossicler/enshrouded-skill-tree" rel="noopener" target="_blank">rossicler/enshrouded-skill-tree</a>), exported from the Enshrouded 1.0 game files and licensed under the GNU GPL v3.0. Our planner code and the data files it loads are released under the same license, and their source is <a href="https://github.com/AZwang067260/enshroudedbuilds" rel="noopener" target="_blank">available on GitHub</a>. Enshrouded and its game text are property of Keen Games GmbH.</p>
{{sources}}
</article></div>'''
    return body


def client_payload():
    from tree_data import client_data
    return "/*! SPDX-License-Identifier: GPL-3.0-or-later. Data: rossicler/enshrouded-skill-tree, Enshrouded 1.0 game files. */\nwindow.EB_TREE=" + json.dumps(
        client_data(AREA_COLORS), separators=(",", ":"), ensure_ascii=False) + ";\n"


def skills_table():
    """Crawlable list of every 1.0 skill (shown on /skill-tree/), each linking to the skill in the planner."""
    keys = type_key_by_name()
    sections = ""
    for area, groups in TREE:
        sections += f'<h3 id="skills-{area.lower()}" class="mb-3 mt-8 text-xl font-bold">{e(area)} skills</h3>'
        for group, sks in groups:
            rows = ""
            for name, ranks, cost, effect, flags in sks:
                tags = (badge("New in 1.0", "primary") if "new" in flags else "") + (badge("Disputed", "outline") if "disputed" in flags else "")
                cost_txt = f"{cost} pt" if ranks == 1 else f"{cost} pt × {ranks}"
                find = (f'<a href="/skill-planner/#n={keys[name]}" class="whitespace-nowrap text-xs font-medium text-primary hover:underline">Open in planner</a>'
                        if name in keys else "")
                rows += (f'<tr class="border-t align-top"><td class="px-3 py-2"><div class="flex flex-wrap items-center gap-1.5 font-medium">{e(name)}{tags}</div>'
                         f'<div class="mt-0.5 text-xs text-muted-foreground md:hidden">{e(effect)}</div></td>'
                         f'<td class="hidden px-3 py-2 text-sm text-muted-foreground md:table-cell">{e(effect)}</td>'
                         f'<td class="whitespace-nowrap px-3 py-2 text-sm">{cost_txt}</td><td class="px-3 py-2 text-right">{find}</td></tr>')
            sections += (f'<section class="mb-5 overflow-hidden rounded-lg border bg-card">'
                         f'<div class="border-b bg-muted/50 px-3 py-2"><h4 class="text-base font-semibold">{e(group)}'
                         f'<span class="ml-2 text-xs font-normal text-muted-foreground">{e(area)} · {len(sks)} skills</span></h4></div>'
                         f'<div class="overflow-x-auto"><table class="w-full text-left"><thead class="sr-only"><tr><th>Skill</th><th>Effect at max rank</th><th>Cost</th><th>Tree</th></tr></thead>'
                         f'<tbody>{rows}</tbody></table></div></section>')

    return sections
