"""The /skill-planner/ page: a static, crawlable list of every 1.0 skill, enhanced with a point-budget planner in JS."""
import json

from layout import UPDATED_HUMAN, badge, e
from skills_data import TREE, flat, preset

PLANNER_FAQ = [
    ("How many skill points do you get in Enshrouded 1.0?", "212 at level 50 if you explore everything: 2 points for every level from 2 to 50 (98), 1 point for each of the 60 Shroud Roots and 3 points for each of the 18 Elixir Wells (114 together)."),
    ("How many points does it take to fill the whole skill tree?", "About 675 points, according to community planners built from the 1.0 game files. A level 50 character can afford roughly a third of the tree, so every build has to choose."),
    ("Does this planner check skill tree connections?", "Not yet. It checks your point budget, ranks and attributes. In the game you can only take a skill that connects to one you already own, so plan your path through the tree as well. Our build guides list the order that works."),
    ("Is this the same skill tree as the game?", "It lists all 178 skills and 231 nodes of the 1.0 tree with their ranks and point costs, taken from community data exported from the game files (Steam build 1267041) and checked against other 1.0 sources. Values marked as disputed differ between sources, so check the in-game tooltip."),
    ("Can I share my build?", "Yes. Every change updates the page address. Use the Copy link button and send it to a friend: the link opens the planner with your exact build, level and exploration settings."),
]

BUILD_NAMES = [("wizard", "Wizard / Mage"), ("battlemage", "Battlemage"), ("necromancer", "Necromancer / Summoner"), ("healer", "Healer"),
               ("warrior", "Warrior"), ("tank", "Tank"), ("barbarian", "Barbarian"), ("ranger", "Ranger"), ("assassin", "Assassin")]

JS = r"""
(function(){
  var D = window.EB_PLANNER, n = D.skills.length, r = new Array(n).fill(0);
  var $ = function(s){ return document.querySelector(s); }, all = function(s){ return document.querySelectorAll(s); };
  var lv = $('#pl-level'), ro = $('#pl-roots'), we = $('#pl-wells'), fl = $('#pl-flame'), sel = $('#pl-preset');
  var B36 = '0123456789abcdefghijklmnopqrstuvwxyz';
  function budget(){ return 2 * (Math.min(50, Math.max(1, +lv.value || 1)) - 1) + Math.min(60, +ro.value || 0) + 3 * Math.min(18, +we.value || 0); }
  function spent(){ var s = 0; for (var i = 0; i < n; i++) s += r[i] * D.skills[i][2]; return s; }
  function render(){
    var b = budget(), s = spent(), left = b - s, at = {str:0, dex:0, int:0, con:0, spi:0, end:0}, half = Math.floor((+fl.value || 0) / 2);
    for (var i = 0; i < n; i++) {
      var k = D.skills[i], row = document.getElementById('sk-' + i);
      row.querySelector('[data-rank]').textContent = r[i] + '/' + k[1];
      row.classList.toggle('bg-primary/10', r[i] > 0);
      row.querySelector('[data-plus]').disabled = r[i] >= k[1] || k[2] > left;
      row.querySelector('[data-minus]').disabled = r[i] === 0;
      if (!r[i]) continue;
      var f = k[3];
      if (f.indexOf('attr:ranger') === 0) { at.dex += r[i]; at.end += r[i]; }
      else if (f.indexOf('attr:') === 0) at[f.slice(5, 8)] += r[i];
      else if (f.indexOf('flame:') === 0) at[f.slice(6, 9)] += half;
    }
    $('#pl-budget').textContent = b; $('#pl-spent').textContent = s;
    $('#pl-m-budget').textContent = b; $('#pl-m-spent').textContent = s; $('#pl-m-left').textContent = left;
    $('#pl-m-left').classList.toggle('text-destructive', left < 0);
    var l = $('#pl-left'); l.textContent = left; l.classList.toggle('text-destructive', left < 0);
    $('#pl-over').hidden = left >= 0;
    $('#pl-bar').style.width = Math.min(100, b ? s / b * 100 : 0) + '%';
    var stats = [['Strength', at.str, '+' + at.str * 5 + '% melee damage'], ['Dexterity', at.dex, '+' + at.dex * 5 + '% bow &amp; dagger damage'],
      ['Intelligence', at.int, '+' + at.int * 5 + '% magic damage'], ['Constitution', at.con, '+' + at.con * 50 + ' max health'],
      ['Spirit', at.spi, '+' + at.spi * 20 + ' max mana'], ['Endurance', at.end, '+' + at.end * 10 + ' max stamina']];
    $('#pl-attrs').innerHTML = stats.map(function(x){ return '<li class="flex justify-between gap-2"><span>' + x[0] + ' <strong>+' + x[1] + '</strong></span><span class="text-muted-foreground">' + x[2] + '</span></li>'; }).join('');
    all('[data-group]').forEach(function(g){
      var ids = g.getAttribute('data-ids').split(','), c = 0;
      ids.forEach(function(i){ c += r[+i] * D.skills[+i][2]; });
      g.querySelector('[data-gspent]').textContent = c ? c + ' pts' : '';
    });
    var code = r.map(function(x){ return B36[x]; }).join('').replace(/0+$/, '');
    history.replaceState(null, '', '#s=' + code + '&l=' + lv.value + '&r=' + ro.value + '&w=' + we.value + '&f=' + fl.value + (sel.value ? '&b=' + sel.value : ''));
  }
  function load(p){ r.fill(0); Object.keys(p).forEach(function(k){ r[+k] = p[k]; }); }
  function fromHash(){
    var h = {}; location.hash.slice(1).split('&').forEach(function(kv){ var a = kv.split('='); if (a[0]) h[a[0]] = decodeURIComponent(a[1] || ''); });
    ['l','r','w','f'].forEach(function(k, j){ if (h[k] !== undefined) [lv, ro, we, fl][j].value = h[k]; });
    if (h.b && D.presets[h.b]) sel.value = h.b;
    if (h.s !== undefined) { r.fill(0); for (var i = 0; i < h.s.length && i < n; i++) r[i] = Math.min(D.skills[i][1], Math.max(0, B36.indexOf(h.s[i]))); }
    else if (h.b && D.presets[h.b]) load(D.presets[h.b]);
  }
  document.addEventListener('click', function(ev){
    var b = ev.target.closest('[data-plus],[data-minus]'); if (!b) return;
    var i = +b.closest('[data-i]').getAttribute('data-i');
    if (b.hasAttribute('data-plus')) { if (r[i] < D.skills[i][1]) r[i]++; } else if (r[i] > 0) r[i]--;
    render();
  });
  [lv, ro, we, fl].forEach(function(x){ x.addEventListener('input', render); });
  sel.addEventListener('change', function(){ if (sel.value) { load(D.presets[sel.value]); lv.value = 50; ro.value = 60; we.value = 18; } render(); });
  $('#pl-reset').addEventListener('click', function(){ r.fill(0); sel.value = ''; render(); });
  $('#pl-copy').addEventListener('click', function(){
    var t = $('#pl-copy'), done = function(){ t.textContent = 'Link copied'; setTimeout(function(){ t.textContent = 'Copy link'; }, 1600); };
    try { navigator.clipboard.writeText(location.href).then(done, done); } catch (e) { done(); }
  });
  $('#pl-search').addEventListener('input', function(){
    var q = this.value.trim().toLowerCase();
    all('[data-i]').forEach(function(row){ row.hidden = q && row.getAttribute('data-name').indexOf(q) < 0; });
    all('[data-group]').forEach(function(g){ g.hidden = q && !g.querySelector('[data-i]:not([hidden])'); });
  });
  all('[data-pl-js]').forEach(function(x){ x.hidden = false; });
  fromHash(); render();
})();
"""


def planner_page(builds_lookup):
    skills = flat()
    index = {s[2]: i for i, s in enumerate(skills)}
    presets = {}
    for slug, _ in BUILD_NAMES:
        picks, _spent = preset(slug)
        presets[slug] = {index[name]: rank for name, rank in picks.items()}
    data = {"skills": [[s[2], s[3], s[4], s[6]] for s in skills], "presets": presets}

    btn = ('class="inline-flex h-7 w-7 items-center justify-center rounded-md border bg-background text-sm font-semibold '
           'hover:bg-accent disabled:cursor-not-allowed disabled:opacity-40"')
    sections, i = "", 0
    for area, groups in TREE:
        sections += f'<h2 id="{area.lower()}" class="mb-3 mt-10 text-2xl font-bold">{e(area)} skills</h2>'
        for group, sks in groups:
            ids = list(range(i, i + len(sks)))
            rows = ""
            for name, ranks, cost, effect, flags in sks:
                tags = (badge("New in 1.0", "primary") if "new" in flags else "") + (badge("Disputed", "outline") if "disputed" in flags else "")
                cost_txt = f"{cost} pt" if ranks == 1 else f"{cost} pt × {ranks}"
                rows += (f'<tr id="sk-{i}" data-i="{i}" data-name="{e(name.lower())}" class="border-t align-top transition-colors">'
                         f'<td class="px-3 py-2"><div class="flex flex-wrap items-center gap-1.5 font-medium">{e(name)}{tags}</div>'
                         f'<div class="mt-0.5 text-xs text-muted-foreground md:hidden">{e(effect)}</div></td>'
                         f'<td class="hidden px-3 py-2 text-sm text-muted-foreground md:table-cell">{e(effect)}</td>'
                         f'<td class="whitespace-nowrap px-3 py-2 text-sm">{cost_txt}</td>'
                         f'<td class="whitespace-nowrap px-3 py-2"><div class="flex items-center justify-end gap-1.5" data-pl-js hidden>'
                         f'<button type="button" data-minus {btn} aria-label="Remove a rank of {e(name)}">−</button>'
                         f'<span data-rank class="w-10 text-center text-sm tabular-nums">0/{ranks}</span>'
                         f'<button type="button" data-plus {btn} aria-label="Add a rank of {e(name)}">+</button></div></td></tr>')
                i += 1
            sections += (f'<section data-group data-ids="{",".join(map(str, ids))}" class="mb-6 overflow-hidden rounded-lg border bg-card">'
                         f'<div class="flex items-center justify-between border-b bg-muted/50 px-3 py-2"><h3 class="text-base font-semibold">{e(group)}'
                         f'<span class="ml-2 text-xs font-normal text-muted-foreground">{e(area)} · {len(sks)} skills</span></h3>'
                         f'<span data-gspent class="text-xs font-semibold text-primary"></span></div>'
                         f'<div class="overflow-x-auto"><table class="w-full text-left"><thead class="sr-only"><tr><th>Skill</th><th>Effect at max rank</th><th>Cost</th><th>Ranks</th></tr></thead>'
                         f'<tbody>{rows}</tbody></table></div></section>')

    options = "".join(f'<option value="{s}">{e(n)} build</option>' for s, n in BUILD_NAMES)
    field = "h-9 w-full rounded-md border bg-background px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    controls = f'''
<div id="pl-top" class="scroll-mt-20 space-y-4 rounded-lg border bg-card p-4 shadow-sm">
  <div class="grid grid-cols-2 gap-3">
    <label class="text-xs font-medium">Level (1–50)<input id="pl-level" type="number" min="1" max="50" value="50" class="mt-1 {field}"></label>
    <label class="text-xs font-medium">Flame level<input id="pl-flame" type="number" min="0" max="20" value="10" class="mt-1 {field}"></label>
    <label class="text-xs font-medium">Shroud Roots (0–60)<input id="pl-roots" type="number" min="0" max="60" value="60" class="mt-1 {field}"></label>
    <label class="text-xs font-medium">Elixir Wells (0–18)<input id="pl-wells" type="number" min="0" max="18" value="18" class="mt-1 {field}"></label>
  </div>
  <label class="block text-xs font-medium">Load a build<select id="pl-preset" class="mt-1 {field}"><option value="">Empty tree</option>{options}</select></label>
  <div>
    <div class="flex items-baseline justify-between text-sm"><span>Points spent</span><span><strong id="pl-spent">0</strong> / <span id="pl-budget">212</span></span></div>
    <div class="mt-2 h-2 overflow-hidden rounded-full bg-secondary"><div id="pl-bar" class="h-full bg-primary transition-all" style="width:0"></div></div>
    <p class="mt-2 text-sm">Points left: <strong id="pl-left">212</strong></p>
    <p id="pl-over" hidden class="mt-1 text-xs font-medium text-destructive">Over budget: raise your level or exploration, or remove ranks.</p>
  </div>
  <div><p class="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Attributes from the tree</p><ul id="pl-attrs" class="space-y-1 text-sm"></ul></div>
  <div class="flex gap-2"><button id="pl-copy" type="button" class="inline-flex h-9 flex-1 items-center justify-center rounded-md bg-primary px-3 text-sm font-medium text-primary-foreground hover:bg-primary/90">Copy link</button>
  <button id="pl-reset" type="button" class="inline-flex h-9 items-center justify-center rounded-md border px-3 text-sm font-medium hover:bg-accent">Reset</button></div>
</div>'''

    guide_links = " · ".join(f'<a href="/builds/{s}/">{e(builds_lookup[s]["short"])}</a>' for s, _ in BUILD_NAMES)
    body = f'''
<div class="hero-glow border-b"><div class="container py-10 md:py-12">{{crumbs}}
<div class="flex flex-wrap gap-2">{badge("Free tool", "primary")}{badge("Enshrouded 1.0", "outline")}{badge("178 skills · 231 nodes", "outline")}{badge("Updated " + UPDATED_HUMAN, "outline")}</div>
<h1 class="mt-4 max-w-4xl text-3xl font-bold tracking-tight md:text-5xl">Enshrouded 1.0 Skill Planner</h1>
<p class="mt-4 max-w-3xl text-lg text-muted-foreground">Plan your Enshrouded build before you spend a single point. Pick ranks for all 178 skills of the 1.0 skill tree, see how many of your 212 points are left, check your attribute bonuses and share the build with one link.</p>
<noscript><p class="mt-3 text-sm text-destructive">The planner needs JavaScript. The full skill list below works without it.</p></noscript>
</div></div>
<div class="container grid gap-8 py-8 lg:grid-cols-[1fr_320px]">
  <aside class="lg:order-2"><div class="lg:sticky lg:top-20" data-pl-js hidden>{controls}</div></aside>
  <div class="min-w-0 lg:order-1">
    <div class="sticky top-16 z-10 -mx-1 mb-4 bg-background/90 px-1 py-2 backdrop-blur" data-pl-js hidden>
      <input id="pl-search" type="search" placeholder="Search skills, e.g. Blink, Unity, Puncture" aria-label="Search skills" class="{field}">
    </div>
    <nav class="flex flex-wrap gap-2 text-sm" aria-label="Skill areas">{"".join(f'<a href="#{a.lower()}" class="rounded-md border px-3 py-1 hover:bg-accent">{a}</a>' for a, _ in TREE)}</nav>
    {sections}
  </div>
</div>
<div data-pl-js hidden class="fixed inset-x-0 bottom-0 z-30 border-t bg-background/95 px-4 py-2 text-sm backdrop-blur lg:hidden">
  <div class="flex items-center justify-between gap-3"><span>Spent <strong id="pl-m-spent">0</strong> / <span id="pl-m-budget">212</span></span><span>Left <strong id="pl-m-left">212</strong></span><a href="#pl-top" class="rounded-md border px-2 py-1 text-xs">Settings</a></div>
</div>
<div class="container"><article class="prose-eb mx-auto max-w-4xl">
<h2 id="how-to-use">How to use the Enshrouded skill planner</h2>
<ol class="my-4 list-decimal space-y-2 pl-5">
<li><strong>Set your progress.</strong> Enter your level and how many Shroud Roots and Elixir Wells you have cleared. The planner works out your point budget: 2 per level after level 1, 1 per Shroud Root and 3 per Elixir Well.</li>
<li><strong>Load a build or start empty.</strong> Each preset is the level 50 version of one of our guides: {guide_links}.</li>
<li><strong>Add and remove ranks</strong> with the + and − buttons. Point costs differ a lot: attribute nodes cost 1 point, big skills like Blink or Swift Blades cost 4, and Flame nodes cost 5.</li>
<li><strong>Watch your attributes.</strong> Attribute nodes, the Ranger node and the Flame nodes (Thick Skin, Barbarian, Exalted, Arcane Concentration, Graceful Stride, Endurance of the Flame) add to your stats. Flame nodes give +1 for every 2 Flame levels.</li>
<li><strong>Share it.</strong> The link updates with every click, so Copy link always shares your current plan.</li>
</ol>
<h2 id="points">Enshrouded 1.0 skill points explained</h2>
<p>The 1.0 skill tree has <strong>231 nodes</strong> and <strong>178 skills</strong> across the Core and the three class areas: Mage (Wizard, Healer, Battlemage, Trickster), Warrior (Tank, Warrior, Barbarian, Athlete) and Ranger (Ranger, Assassin, Beastmaster, Survivor). Filling every node would cost <strong>675 points</strong>, but a fully explored level 50 character has <strong>212</strong>. That is why every build has to commit to one area and borrow only the best skills from its neighbours. Read the <a href="/skill-tree/">skill tree guide</a> for how the areas fit together.</p>
{{faq}}
{{sources}}
</article></div>'''
    return body, data, JS
