"""Static site generator for enshroudedbuilds.org. Run: python3 src/build.py  -> writes ./public"""
import datetime
import json
import os
import re
import shutil
import subprocess

from art import ART, alt_text, build_svg
from blog import POSTS
from content_builds import BUILDS
from planner import PLANNER_FAQ, client_payload, planner_page, skills_table
from skills_data import PRESETS
from tree_data import BIOMES, BUILD_ID, OUR, STAGES, build_preset, game_text, skill_cost, type_of
from layout import (CONTACT_EMAIL, GAME_VERSION, SITE, UPDATED, UPDATED_HUMAN, accordion, alert, badge, breadcrumb, button, card, e,
                    faq_schema, page, table)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
BY_SLUG = {b["slug"]: b for b in BUILDS}
TIER_ORDER = {"S": 0, "A": 1, "B": 2}
PAGES = []  # (path, priority) for the sitemap


def write(path, html, priority="0.8", lastmod=UPDATED):
    target = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)
    if path != "/404.html":
        PAGES.append((path, priority, lastmod))


def article_schema(path, headline, desc, image="/og-image.png"):
    return {"@type": "Article", "headline": headline, "description": desc, "inLanguage": "en", "image": SITE + image,
            "datePublished": "2026-10-16", "dateModified": UPDATED, "mainEntityOfPage": SITE + path,
            "author": {"@type": "Organization", "name": "Enshrouded Builds", "url": SITE + "/"}, "citation": citations(),
            "publisher": {"@type": "Organization", "name": "Enshrouded Builds", "url": SITE + "/"},
            "about": {"@type": "VideoGame", "name": "Enshrouded", "author": {"@type": "Organization", "name": "Keen Games"}}}


def tier_badge(t):
    return badge(f"{t}-Tier", "primary" if t == "S" else "shroud")


def art_src(b):
    return f"/assets/img/builds/{b['slug']}.svg"


def build_card(b):
    return f'''<a href="/builds/{b["slug"]}/" class="group block overflow-hidden rounded-lg border bg-card shadow-sm transition-all hover:-translate-y-0.5 hover:border-primary/60 hover:shadow-md">
  <img src="{art_src(b)}" alt="{e(alt_text(b["slug"], b["short"]))}" width="1200" height="630" loading="lazy" decoding="async" class="aspect-[40/21] w-full border-b object-cover">
  <div class="p-5"><div class="mb-3 flex items-center justify-between gap-2">{tier_badge(b["tier"])}<span class="text-xs text-muted-foreground">{e(b["difficulty"])}</span></div>
  <h3 class="text-lg font-semibold group-hover:text-primary">Enshrouded {e(b["short"])} Build</h3>
  <p class="mt-1 text-sm text-muted-foreground">{e(b["role"])} · {e(b["weapon"])}</p>
  <p class="mt-3 text-sm leading-relaxed text-foreground/80">{e(b["tagline"])}</p>
  <p class="mt-4 text-sm font-medium text-primary">Read the {e(b["short"])} build →</p></div>
</a>'''


HUBS = [
    ("/enshrouded-1-0-builds/", "Enshrouded 1.0 Builds", "Everything Update 1.0 changed, plus the skill tree reset re-spec checklist."),
    ("/enshrouded-1-0-patch-notes/", "Enshrouded 1.0 Patch Notes", "Every new skill, spell and change in Update 1.0."),
    ("/tier-list/", "Builds Tier List (1.0)", "Every Enshrouded build ranked for the 1.0 full release."),
    ("/skill-planner/", "Skill Planner (1.0)", "Plan your build on the real 1.0 skill tree (231 nodes) with a 212-point budget."),
    ("/skill-tree/", "Skill Tree Guide (1.0)", "All 12 archetypes, attributes, skill points and respecs."),
    ("/builds/", "All Enshrouded Builds", "Compare every class build by role, stats and difficulty."),
]


def hub_links(exclude=""):
    """Cards linking to the hub pages; the 1.0 builds page is highlighted as the main entry point."""
    out = ""
    for href, name, blurb in HUBS:
        if href == exclude:
            continue
        accent = "border-primary/60 bg-primary/5" if href == "/enshrouded-1-0-builds/" else "bg-card"
        out += (f'<a href="{href}" class="block rounded-lg border p-4 text-sm transition-colors hover:border-primary/60 {accent}">'
                f'<span class="font-semibold">{e(name)} →</span><br><span class="text-muted-foreground">{e(blurb)}</span></a>')
    return f'<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{out}</div>'


def all_builds_grid(exclude=""):
    """Compact links to every class build page."""
    items = "".join(
        f'<a href="/builds/{b["slug"]}/" class="flex items-center justify-between gap-2 rounded-lg border bg-card p-3 text-sm hover:border-primary/60">'
        f'<span class="font-medium">Enshrouded {e(b["short"])} Build</span>{tier_badge(b["tier"])}</a>'
        for b in sorted(BUILDS, key=lambda b: TIER_ORDER[b["tier"]]) if b["slug"] != exclude)
    return f'<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{items}</div>'


def section(id_, title, inner):
    return f'<section aria-labelledby="{id_}"><h2 id="{id_}">{title}</h2>{inner}</section>'


def paras(ps):
    return "".join(f"<p>{p}</p>" for p in ps)


def ul(items):
    return '<ul class="dots">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


OFFICIAL = [
    ("https://enshrouded.com/en-US/news/release-trailer-changelog-everything-you-need-to-wait-for-tomorrow", "Keen Games: Enshrouded 1.0 release changelog"),
    ("https://enshrouded.com/en-US/news/10-combat-changes-and-additions", "Keen Games: 1.0 combat changes and additions"),
    ("https://steamdb.info/patchnotes/25966634/", "SteamDB: hotfix 1.0.0.1 patch notes"),
    ("https://steamdb.info/patchnotes/25988036/", "SteamDB: hotfix 1.0.0.2 patch notes"),
    ("https://enshrouded.wiki.gg/wiki/1.0_Update", "Enshrouded Wiki: 1.0 Update"),
]


def sources(extra=()):
    """Sources block shown at the end of guide pages: official notes first, then community data used for numbers."""
    links = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{e(t)}</a></li>' for u, t in OFFICIAL + list(extra))
    return (f'<section aria-labelledby="sources" class="mt-12 rounded-lg border bg-card p-5 text-sm">'
            f'<h2 id="sources" class="!mt-0 !text-lg">Sources &amp; how we checked this guide</h2>'
            f'<p>Facts on this page were last checked on <strong>{UPDATED_HUMAN}</strong> against Enshrouded <strong>{GAME_VERSION}</strong>. '
            f'Patch facts come from Keen Games\' official posts. Skill ranks, point costs and percentages were checked against the in-game skill text exported from the 1.0 game files '
            f'(build 1267041) and cross-checked with two independent community sources. Item names were checked against the official Enshrouded Wiki. '
            f'Read our <a href="/about/#methodology">methodology</a>.</p><ul class="dots">{links}</ul></section>')


def citations():
    return [u for u, _ in OFFICIAL[:2]]


# ============================================================ BUILD PAGES

def build_page(b):
    path = f"/builds/{b['slug']}/"
    crumbs_html, crumbs_schema = breadcrumb([("/", "Home"), ("/builds/", "Enshrouded Builds"), (path, f"{b['short']} Build")])
    n = b["short"]
    toc = [("overview", f"{n} build overview"), ("why-1-0", "What changed in 1.0"), ("respec", "Re-spec after the 1.0 reset"), ("attributes", "Attribute priority"),
           ("skill-order", "Skill order (1–50)"), ("key-skills", "Key skills"), ("gear", "Best gear")]
    if b["spells"]:
        toc.append(("spells", "Spells & arrows"))
    toc += [("playstyle", "Playstyle & rotation"), ("pros-cons", "Pros & cons"), ("mistakes", "Common mistakes"),
            ("hybrids", "Hybrid builds"), ("faq", "FAQ")]
    toc_html = "".join(f'<li><a href="#{i}" class="block rounded px-2 py-1 hover:bg-accent hover:text-foreground">{t}</a></li>' for i, t in toc)

    quick = table(["Stat", "Value"], [
        ["Tier (1.0)", tier_badge(b["tier"])], ["Role", e(b["role"])], ["Difficulty", e(b["difficulty"])],
        ["Best for", e(b["best_for"])], ["Weapon", e(b["weapon"])], ["Armor", e(b["armor"])],
        ["Main attributes", e(b["primary"])], ["Skill tree", e(b["tree"])], ["Max level", "50 (gear up to 55)"]])

    order_rows, step = [], 0
    for label, skills in b["phases"]:
        for skill, why in skills:
            step += 1
            order_rows.append([str(step), e(label.replace("Levels ", "")), f"<strong>{e(skill)}</strong>", e(why)])
    order_table = table(["#", "Level", "Skill / node", "Why"], order_rows)

    # one-line answer for the hero: attributes, weapon and the named skills in order
    attr_words = r"^(Strength|Dexterity|Intelligence|Constitution|Endurance|Spirit)\b"
    key_order = [re.sub(r"\s*\(.*?\)", "", sk.replace("(archetype node)", "node")) for _, skills in b["phases"] for sk, _ in skills
                 if not re.search(r"nodes|Remaining|Spare|capstones", sk) and not re.search(attr_words, sk)]
    alias = f' (also called the {e(b["name"].split(" / ")[1].lower())} build)' if " / " in b["name"] else ""
    lead = (f'The best Enshrouded 1.0 {n.lower()} build{alias} puts points into {e(b["primary"].replace(", ", " and "))}, '
            f'uses {e(b["weapon"][0].lower() + b["weapon"][1:])} and follows this skill order to level 50: {" → ".join(e(k) for k in key_order[:7])}. '
            f'Rated {b["tier"]}-tier after the Update 1.0 skill tree reset (October 15, 2026).')

    # core skills: the build's preset skills (no attribute nodes), with in-game values and our notes
    notes = {}
    for k, v in b["key_skills"]:
        for part in re.split(r"\s*(?:&amp;|&)\s*", k):
            notes.setdefault(part.strip(), v)
    for _, skills in b["phases"]:
        for sk, why in skills:
            notes.setdefault(re.sub(r"\s*\(.*?\)", "", sk).strip(), why)
    core = [nm for nm in PRESETS[b["slug"]] if not nm.endswith(" node") and nm != "Double Jump" and type_of(nm)]
    core.sort(key=lambda nm: (0 if any(nm in k for k, _ in b["key_skills"]) else 1))
    core_rows = []
    for nm in core:
        c, ranks = skill_cost(nm)
        cost_txt = f"{c} pt" if ranks == 1 else f"{c} pt × {ranks}"
        o = OUR.get(nm)
        core_rows.append([f'<strong>{e(nm)}</strong><br><span class="text-xs text-muted-foreground">{e(o[1] if o else "")}</span>',
                          cost_txt, e(game_text(nm)), e(notes.get(nm, ""))])
    key = (f'<p>The skills this build depends on, with the in-game text at max rank from the 1.0 game files (build {BUILD_ID}) and why each one matters for the {n.lower()}:</p>'
           + table(["Skill", "Cost", "In-game effect (max rank)", f"Why it matters for the {n}"], core_rows))

    # level stages: planner presets that follow real paths through the tree
    stage_cards = ""
    for i, (label, budget, biomes) in enumerate(STAGES, 1):
        spent_i = build_preset(b["slug"], budget)[1]
        link = f'/skill-planner/#b={b["slug"]}' + (f"&s={i}" if i < len(STAGES) else "")
        stage_cards += (f'<a href="{link}" class="block rounded-lg border bg-card p-4 text-sm hover:border-primary/60">'
                        f'<span class="font-semibold">{label}</span><br><span class="text-muted-foreground">{spent_i} / {budget} points'
                        f' ({biomes} of 7 biomes explored)</span><br><span class="font-medium text-primary">Open this stage in the planner →</span></a>')
    stages = (f'<h3 id="stages">{n} build by level: points per stage</h3><p>Your budget grows with your level and the biomes you explore: 2 points per level plus the Shroud Roots and Elixir Wells of each finished biome. '
              f'Each card opens a planner preset for that stage that follows real paths through the 1.0 skill tree.</p>'
              f'<div class="my-5 grid gap-3 sm:grid-cols-3">{stage_cards}</div>')

    full_spent = build_preset(b["slug"])[1]
    quick_answer = (f'<div class="not-prose mb-8 rounded-lg border border-primary/40 bg-primary/5 p-5" id="quick-answer"><p class="text-xs font-semibold uppercase tracking-wide text-primary">Quick answer</p>'
             f'<p class="mt-2 leading-relaxed"><strong>{e(n)}: {b["tier"]}-tier</strong>, {e(b["difficulty"].lower())} difficulty, best for {e(b["best_for"].lower())}. '
             f'It scales with <strong>{e(b["primary"].replace(", ", " and "))}</strong> and uses {e(b["weapon"][0].lower() + b["weapon"][1:])}. '
             f'The level 50 planner preset spends <strong>{full_spent} of 212 points</strong>. '
             f'Core skills: {", ".join(e(x) for x in core[:5])}{f" (+{len(core) - 5} more)" if len(core) > 5 else ""}. '
             f'Main weakness: {e(b["cons"][0][0].lower() + b["cons"][0][1:])}.</p></div>')

    pros = card('<div class="p-5"><h3 class="!mt-0 text-base font-semibold text-emerald-500">Pros</h3>' + ul([e(p) for p in b["pros"]]) + "</div>")
    cons = card('<div class="p-5"><h3 class="!mt-0 text-base font-semibold text-destructive">Cons</h3>' + ul([e(c) for c in b["cons"]]) + "</div>")

    hyb = '<div class="my-5 grid gap-3 sm:grid-cols-3">' + "".join(
        f'<a href="/builds/{s}/" class="rounded-lg border bg-card p-4 text-sm hover:border-primary/60"><span class="font-semibold">{e(BY_SLUG[s]["short"])} build</span><br><span class="text-muted-foreground">{e(t)}</span></a>'
        for s, t in b["hybrids"]) + "</div>"

    first_skills = ", ".join(f"<strong>{e(s)}</strong>" for s, _ in b["phases"][0][1][:3])
    respec = (f'<h3 id="respec">How to re-spec the {n} after the 1.0 skill tree reset</h3><ol class="my-4 list-decimal space-y-2 pl-5">'
              f'<li>Stay in your base and open the skill tree. Every point was refunded when you first loaded your save in Update 1.0.</li>'
              f'<li>Take the opening nodes first: {first_skills}.</li>'
              f'<li>Put attribute points into <strong>{e(b["primary"])}</strong>, following the priority table below.</li>'
              f'<li>Follow the level 1–50 path in the <a href="#skill-order">skill order table</a> and stop where your current level runs out.</li>'
              f'<li>Re-check your hotbar and weapon swap ({e(b["weapon"])}) before leaving base.</li></ol>'
              f'<p>For the changes that affect every build, read our <a href="/enshrouded-1-0-builds/">Enshrouded 1.0 builds guide</a> and its full re-spec checklist, or the <a href="/enshrouded-1-0-patch-notes/">Enshrouded 1.0 patch notes</a> for every new skill and spell.</p>')
    related = (f'<p class="mb-4 text-muted-foreground">Every other Enshrouded 1.0 class build, rebuilt after the October 15, 2026 skill tree reset:</p>'
               + all_builds_grid(b["slug"])
               + '<h3 class="mb-4 mt-10 text-lg font-semibold">Enshrouded 1.0 guides</h3>' + hub_links())

    body = f'''
<div class="hero-glow border-b">
  <div class="container grid items-center gap-8 py-10 md:py-14 lg:grid-cols-[1fr_420px]">
    <div>
    {crumbs_html}
    <div class="flex flex-wrap gap-2">{tier_badge(b["tier"])}{badge("Enshrouded 1.0", "outline")}{badge(b["role"])}{badge("Updated " + UPDATED_HUMAN, "outline")}{badge("Checked against 1.0.0.2 · build " + BUILD_ID, "outline")}</div>
    <h1 class="mt-4 max-w-4xl text-3xl font-bold tracking-tight md:text-5xl">Enshrouded 1.0 {e(b["name"])} Build</h1>
    <p class="mt-4 max-w-3xl text-lg text-muted-foreground">{e(b["tagline"])}</p>
    <p class="mt-3 max-w-3xl leading-relaxed text-foreground/85">{lead}</p>
    <div class="mt-6 flex flex-wrap gap-3">{button("#skill-order", "Skill order 1–50")}{button("#gear", "Best gear", "outline")}{button(f"/skill-planner/#b={b['slug']}", "Open in skill planner", "outline")}</div>
    </div>
    <figure class="overflow-hidden rounded-xl border shadow-lg"><img src="{art_src(b)}" alt="{e(alt_text(b["slug"], b["short"]))}" width="1200" height="630" fetchpriority="high" decoding="async" class="aspect-[40/21] w-full object-cover"></figure>
  </div>
</div>
<div class="container grid gap-10 py-10 lg:grid-cols-[1fr_280px]">
  <article class="prose-eb min-w-0">
    {quick_answer}
    {section("overview", f"Enshrouded {n} build overview", paras(b["intro"]) + quick)}
    {section("why-1-0", f"What changed for the {n} in Enshrouded 1.0", paras(b["why"]) + alert("Update 1.0 skill tree reset", 'Every character\'s skill tree was reset when Enshrouded Update 1.0 launched on October 15, 2026, and all points were refunded. Re-spend your points before leaving your base. Your character level is kept. See all <a href="/enshrouded-1-0-builds/">Enshrouded 1.0 builds</a>.') + respec)}
    {section("attributes", f"{n} attribute priority", f"<p>Attribute points decide how your {n.lower()} build scales. Use this priority when you spend points on the skill tree. What each of the six attributes does is explained in our <a href=\"/skill-tree/\">Enshrouded skill tree guide</a>.</p>" + table(["Attribute", "Priority", "Why"], [[f"<strong>{e(a)}</strong>", e(p), e(w)] for a, p, w in b["attributes"]]))}
    {section("skill-order", f"Enshrouded 1.0 {n} Skills &amp; Skill Order (Level 1–50)", f"<p>This is the full {n.lower()} skill order for Enshrouded 1.0, from level 1 to the new level 50 cap. Take the skills from top to bottom and fill in attribute nodes as you path between them. Each row lists the level range where that skill fits.</p>" + order_table + stages + alert("Hotfixes", "Skill names, costs and values were checked against the 1.0 game files (hotfix 1.0.0.2). Keen Games may still adjust values in later hotfixes, so check the in-game tooltip before committing your points."))}
    {section("key-skills", f"Key {n} skills explained", key)}
    {section("gear", f"Best {n} gear: weapons, armor, accessories and food", f"<p>Gear matters as much as skills in Enshrouded. With the 1.0 gear cap raised to 55, always upgrade your main weapon first. Here is the {n.lower()} loadout to aim for:</p>" + table(["Slot", "Recommended", "Why"], [[f"<strong>{e(s)}</strong>", p, e(w)] for s, p, w in b["gear"]]))}
    {section("spells", "Best spells & arrows for this build", table(["Spell / arrow", "Use"], [[f"<strong>{e(s)}</strong>", e(u)] for s, u in b["spells"]])) if b["spells"] else ""}
    {section("playstyle", f"How to play the {n} build", '<ol class="my-4 list-decimal space-y-2 pl-5">' + "".join(f'<li class="leading-relaxed">{e(s)}</li>' for s in b["playstyle"]) + "</ol>")}
    {section("pros-cons", f"{n} build pros and cons", f'<div class="my-5 grid gap-4 sm:grid-cols-2">{pros}{cons}</div>')}
    {section("mistakes", f"Common {n.lower()} build mistakes", ul([e(m) for m in b["mistakes"]]))}
    {section("hybrids", f"{n} hybrid builds", f"<p>Enshrouded has no hard class lock, so the {n.lower()} blends well with other archetypes. These are the best hybrid directions:</p>" + hyb)}
    {section("faq", f"Enshrouded {n} build FAQ", accordion(b["faqs"]))}
    {sources()}
  </article>
  <aside class="hidden lg:block"><div class="sticky top-24 space-y-4">
    {card('<div class="p-4"><p class="mb-2 text-sm font-semibold">On this page</p><ul class="space-y-0.5 text-sm text-muted-foreground">' + toc_html + '</ul></div>')}
    {card(f'<div class="p-4 text-sm"><p class="font-semibold">Other Enshrouded builds</p><ul class="mt-2 space-y-1 text-muted-foreground">' + "".join(f'<li><a class="hover:text-foreground" href="/builds/{x["slug"]}/">{e(x["short"])} build</a></li>' for x in BUILDS if x["slug"] != b["slug"]) + '</ul></div>')}
  </div></aside>
</div>
<section class="container" aria-labelledby="more"><h2 id="more" class="mb-6 text-2xl font-bold">More Enshrouded 1.0 builds</h2>{related}</section>
'''
    og = f"/og/{b['slug']}.png"
    write(path, page(path=path, title=b["title"], description=b["desc"], keywords=b["keywords"], body=body, builds=BUILDS,
                     active="/builds/", og_image=og, og_alt=f"Enshrouded 1.0 {b['short']} build guide",
                     schemas=[article_schema(path, b["title"], b["desc"], og), crumbs_schema, faq_schema(b["faqs"])]), "0.9")


# ============================================================ HOME

HOME_FAQ = [
("What are the best Enshrouded builds in 1.0?", "The top Enshrouded 1.0 builds are the <a href='/builds/battlemage/'>Battlemage wand build</a> (best overall and best solo), the new <a href='/builds/necromancer/'>Necromancer summoner build</a>, the <a href='/builds/wizard/'>Wizard</a> (best area damage) and the <a href='/builds/barbarian/'>two-handed Barbarian</a> (highest physical DPS). The <a href='/builds/tank/'>Tank</a> and <a href='/builds/healer/'>Healer</a> are the most valuable picks in co-op."),
("Does Enshrouded have classes?", "No. Enshrouded uses one large skill tree with twelve archetypes: Warrior, Tank, Barbarian and Athlete; Wizard, Battlemage, Healer and Trickster; Ranger, Assassin, Beastmaster and Survivor. A \"class build\" is a path through these archetypes, and you can mix them freely."),
("When did Enshrouded 1.0 release?", "Enshrouded 1.0 launched on October 15, 2026 on PC (Steam) and PlayStation 5, ending Early Access. An Xbox version is expected in 2027."),
("Did Enshrouded 1.0 reset my skills?", "Yes. Every skill tree was reset at launch and all points were refunded. Your character level and items carry over, but you need to re-spend your points. Keen Games recommends doing this before leaving your base."),
("What is the max level in Enshrouded 1.0?", "The player level cap went up from 45 to 50, and gear now goes up to level 55."),
("What is the best Enshrouded build for beginners?", "The <a href='/builds/warrior/'>sword-and-shield Warrior</a>. It has strong self-healing through Battle Heal, needs no mana management, and teaches you blocking and parrying."),
("What is the best solo build in Enshrouded?", "The <a href='/builds/battlemage/'>Battlemage wand build</a> is the most reliable solo build in 1.0. The new <a href='/builds/necromancer/'>Necromancer</a> is a relaxed alternative, because summons absorb aggro for you."),
("Can I respec in Enshrouded?", "Yes. Enshrouded lets you reset skill points, and the 1.0 launch already reset everyone for free. Our <a href='/skill-tree/'>skill tree guide</a> explains how points and resets work."),
]


def home():
    path = "/"
    sorted_builds = sorted(BUILDS, key=lambda b: TIER_ORDER[b["tier"]])
    cards = '<div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">' + "".join(build_card(b) for b in sorted_builds) + "</div>"
    stats = "".join(
        card(f'<div class="p-5"><p class="text-3xl font-bold text-primary">{v}</p><p class="mt-1 text-sm text-muted-foreground">{l}</p></div>')
        for v, l in [("50", "New level cap in 1.0"), ("55", "Max gear level"), ("9", "New spells incl. summons"), ("12", "Skill tree archetypes")])
    picks = table(["Goal", "Best Enshrouded build", "Why"], [
        ["Best overall", '<a href="/builds/wizard/">Wizard</a>', "Highest area damage and strong new 1.0 spells"],
        ["Best solo", '<a href="/builds/battlemage/">Battlemage</a>', "Near-infinite mana with a shield for safety"],
        ["Best for beginners", '<a href="/builds/warrior/">Warrior</a>', "Self-healing, no mana, forgiving"],
        ["Best melee DPS", '<a href="/builds/barbarian/">Barbarian</a>', "Two-handed stuns and huge hits"],
        ["Best co-op tank", '<a href="/builds/tank/">Tank</a>', "Heavy armor scaling and aggro skills"],
        ["Best co-op support", '<a href="/builds/healer/">Healer</a>', "Keeps 16-player groups alive"],
        ["Best ranged physical", '<a href="/builds/ranger/">Ranger</a>', "New Eternal arrows and archer skills"],
        ["Best new 1.0 build", '<a href="/builds/necromancer/">Necromancer</a>', "Skeletons and totems were added in 1.0"],
        ["Best crit / mobility", '<a href="/builds/assassin/">Assassin</a>', "Daggers moved to the Assassin tree"],
    ])
    body = f'''
<section class="hero-glow border-b">
  <div class="container py-16 md:py-24">
    <div class="flex flex-wrap gap-2">{badge("Updated for Enshrouded 1.0", "primary")}{badge(UPDATED_HUMAN, "outline")}</div>
    <h1 class="mt-5 max-w-4xl font-display text-4xl font-bold leading-tight tracking-tight md:text-6xl">Enshrouded Builds: Best Class Builds for 1.0</h1>
    <p class="mt-5 max-w-2xl text-lg leading-relaxed text-muted-foreground">Every Enshrouded build, rebuilt for the 1.0 full release. Each class guide covers the skill tree path to level 50, attribute priorities, the best weapons, armor and spells, and how to play the build solo or in co-op. Then plan your own build on the real 1.0 skill tree with our free <a href="/skill-planner/" class="text-primary hover:underline">Enshrouded skill planner</a>.</p>
    <div class="mt-8 flex flex-wrap gap-3">{button("/builds/", "Browse all builds")}{button("/skill-planner/", "Open the skill planner", "outline")}{button("/enshrouded-1-0-builds/", "What changed in 1.0", "outline")}</div>
    <div class="mt-12 grid grid-cols-2 gap-4 md:grid-cols-4">{stats}</div>
  </div>
</section>

<section class="container py-16" aria-labelledby="builds">
  <div class="mb-8 max-w-3xl"><h2 id="builds" class="text-3xl font-bold tracking-tight">Best Enshrouded builds by class</h2>
  <p class="mt-3 text-muted-foreground">Pick a playstyle. Each page is a complete Enshrouded 1.0 build guide with a skill order, gear table and FAQ.</p></div>
  {cards}
</section>

<div class="container grid gap-10 pb-8 lg:grid-cols-[1fr_300px]">
<article class="prose-eb min-w-0">
  <h2 id="quick-picks">Quick picks: which Enshrouded build should you play?</h2>
  <p>Not sure where to start? This table matches each common goal with the strongest <strong>Enshrouded 1.0 build</strong> for it. Every link goes to a full guide.</p>
  {picks}

  <h2 id="about-enshrouded-builds">How builds work in Enshrouded</h2>
  <p>Enshrouded is a survival action RPG by Keen Games set in the Shroud-covered world of Embervale. It has no character classes in the traditional sense. Every Flameborn character uses the same large skill tree, and your build depends on where you spend your skill points, which attributes you raise, and which weapons, armor and spells you equip. When players search for <strong>Enshrouded builds</strong>, they usually want a proven path through that tree for a specific playstyle: a mage, a tank, an archer or a melee fighter.</p>
  <p>The skill tree has <strong>twelve archetypes</strong>, grouped into three combat areas. The <em>Warrior</em> area holds the Warrior, Tank, Barbarian and Athlete. The <em>Mage</em> area holds the Wizard, Battlemage, Healer and Trickster. The <em>Ranger</em> area holds the Ranger, Assassin, Beastmaster and Survivor. Each archetype has its own passive bonuses and active skills, and the strongest builds usually go deep into one or two neighboring archetypes instead of spreading points thin. Our <a href="/skill-tree/">Enshrouded skill tree guide</a> explains each archetype in detail.</p>
  <p>Attributes are the second layer of every build. <strong>Strength</strong> scales melee damage, <strong>Dexterity</strong> scales bows and daggers, <strong>Intelligence</strong> scales staves, wands and spells, <strong>Constitution</strong> adds about 50 health per point, <strong>Spirit</strong> adds about 20 mana per point, and <strong>Endurance</strong> controls stamina for dodging, blocking and gliding. A good build picks one damage attribute and backs it up with the right mix of defensive stats.</p>

  <h2 id="enshrouded-1-0">Enshrouded 1.0 builds: what changed in the full release</h2>
  <p>Enshrouded left Early Access with the <strong>1.0 release on October 15, 2026</strong>. This is the biggest balance change the game has had, and it is why so many players are searching for updated <strong>Enshrouded 1.0 builds</strong>. The headline changes for builds are:</p>
  <ul class="dots">
    <li><strong>Full skill tree reset</strong> for every character. Points are refunded and your level is kept.</li>
    <li><strong>Level cap raised from 45 to 50</strong>, and gear now goes up to <strong>level 55</strong>.</li>
    <li><strong>Eight new skills</strong>: five for mages (Advanced Necromancy, Totem Mastery, Aerial Wand Attack, Wand Evasion Attack, Blast and Cast) and three for archers (Puncture, Barrage, Survival Instinct).</li>
    <li><strong>Nine new spells</strong>, including summons: Mana Drain, Entangle, Pillar of Flames, Blizzard, Ball Lightning, Summon Fire/Ice/Shock Totem and Summon Hollow Skeleton.</li>
    <li><strong>22 Eternal spells and new Eternal arrows</strong> that can be upgraded and don't use up spell charges or ammo (Eternal arrows cost mana instead).</li>
    <li><strong>Dagger skills moved</strong> from the Warrior tree to the Assassin tree, and many existing skills got cheaper or stronger.</li>
  </ul>
  <p>Every guide on this site has been rewritten for these changes. For the full list with what each new skill and spell does, read the <a href="/enshrouded-1-0-patch-notes/">Enshrouded 1.0 patch notes</a>. For the full breakdown, and a checklist for re-spending your points after the reset, read our <a href="/enshrouded-1-0-builds/">Enshrouded 1.0 builds guide</a>.</p>

  <h2 id="choose">How to choose the right Enshrouded build</h2>
  <h3>Solo or co-op?</h3>
  <p>Enshrouded supports up to 16 players on one server, and some builds are much better in groups. The <a href="/builds/healer/">Healer</a> and the aggro-focused <a href="/builds/tank/">Tank</a> are most useful with friends. Solo players should look at the <a href="/builds/battlemage/">Battlemage</a>, the <a href="/builds/warrior/">Warrior</a> or the new <a href="/builds/necromancer/">Necromancer</a>, because each one has its own sustain or aggro control.</p>
  <h3>Melee, ranged or magic?</h3>
  <p>If you like being in the middle of a fight, go <a href="/builds/barbarian/">Barbarian</a> for damage or <a href="/builds/warrior/">Warrior</a> for safety. If you like to stay at range, choose between the <a href="/builds/ranger/">Ranger</a> for physical bow damage and the <a href="/builds/wizard/">Wizard</a> for elemental magic. If you want burst and mobility, the <a href="/builds/assassin/">Assassin</a> is the most demanding build and has the highest skill ceiling.</p>
  <h3>How much do you want to manage?</h3>
  <p>Mage builds have to manage mana, swap between wand and staff, and position carefully. Melee builds only track stamina. If you are new to Enshrouded, start with a Warrior and respec later. Skill points can be reset, and the 1.0 reset already gives everyone a fresh start.</p>

  <h2 id="tier-list-summary">Enshrouded builds tier list (1.0)</h2>
  <p>Our current ranking puts the <strong>Battlemage, Necromancer, Wizard and Barbarian in S-tier</strong>, the Tank, Warrior, Healer and Ranger in A-tier, and the Assassin in B-tier. Every build on this site can clear the full 1.0 game, so the tiers show how efficient and forgiving each build is, not whether it is viable. See the full <a href="/tier-list/">Enshrouded builds tier list</a> for the reasoning.</p>

  <h2 id="faq">Enshrouded builds FAQ</h2>
  {accordion(HOME_FAQ)}
</article>
<aside class="hidden lg:block"><div class="sticky top-24 space-y-4">
  {card('<div class="p-5"><p class="font-semibold">Start here</p><p class="mt-2 text-sm text-muted-foreground">Just reset by the 1.0 patch? Follow our re-spec checklist before you leave your base.</p><div class="mt-4">' + button("/enshrouded-1-0-builds/", "1.0 re-spec checklist") + '</div></div>')}
  {card('<div class="p-5"><p class="font-semibold">Top 3 builds right now</p><ol class="mt-3 list-decimal space-y-1 pl-5 text-sm"><li><a class="hover:text-primary" href="/builds/wizard/">Wizard</a></li><li><a class="hover:text-primary" href="/builds/battlemage/">Battlemage</a></li><li><a class="hover:text-primary" href="/builds/barbarian/">Barbarian</a></li></ol></div>')}
</div></aside>
</div>
'''
    title = "Enshrouded Builds 1.0: Best Builds & Skill Planner"
    desc = "The best Enshrouded 1.0 builds for every class with skill order to level 50 and gear, plus a free skill planner with the real 1.0 skill tree."
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, og_type="website",
                     keywords="enshrouded builds, enshrouded 1.0 builds, best enshrouded builds, enshrouded class builds, enshrouded skill tree",
                     schemas=[{"@type": "WebPage", "name": title, "url": SITE + "/", "description": desc, "dateModified": UPDATED},
                              {"@type": "ItemList", "name": "Enshrouded Builds", "itemListElement": [
                                  {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/builds/{b['slug']}/", "name": f"Enshrouded {b['short']} Build"}
                                  for i, b in enumerate(sorted_builds)]},
                              faq_schema(HOME_FAQ)]), "1.0")


# ============================================================ SKILL PLANNER

def skill_planner():
    path = "/skill-planner/"
    ch, cs = breadcrumb([("/", "Home"), ("/skill-tree/", "Skill Tree Guide"), (path, "Skill Planner")])
    body = planner_page(BY_SLUG)
    body = (body.replace("{crumbs}", ch).replace("{faq}", '<h2 id="faq">Skill planner FAQ</h2>' + accordion(PLANNER_FAQ))
            .replace("{sources}", sources([("https://github.com/rossicler/enshrouded-skill-tree", "rossicler/enshrouded-skill-tree: tree data from the 1.0 game files (GPL-3.0)")])))
    # planner data and code are GPL-3.0-or-later (see src/vendor/enshrouded-skill-tree)
    assets = os.path.join(OUT, "assets", "planner")
    os.makedirs(assets, exist_ok=True)
    with open(os.path.join(assets, "tree-data.js"), "w", encoding="utf-8") as f:
        f.write(client_payload())
    shutil.copy(os.path.join(ROOT, "src", "planner.js"), os.path.join(assets, "planner.js"))
    shutil.copy(os.path.join(ROOT, "src", "vendor", "enshrouded-skill-tree", "LICENSE"), os.path.join(assets, "LICENSE.txt"))
    body += '<script src="/assets/planner/tree-data.js" defer></script><script src="/assets/planner/planner.js" defer></script>'
    title = "Enshrouded Skill Planner (1.0): Skill Tree Calculator"
    desc = "Free Enshrouded skill planner and skill tree calculator for 1.0: the real tree from the game files, a 212-point budget, attributes and shareable builds."
    app = {"@type": "WebApplication", "name": "Enshrouded 1.0 Skill Planner", "url": SITE + path, "applicationCategory": "GameApplication",
           "operatingSystem": "Any (web browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": desc,
           "about": {"@type": "VideoGame", "name": "Enshrouded"}, "license": "https://www.gnu.org/licenses/gpl-3.0.html"}
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, active=path,
                     keywords="enshrouded skill planner, enshrouded skill tree planner, enshrouded skill calculator, enshrouded build planner, enshrouded 1.0 skill tree",
                     schemas=[app, cs, faq_schema(PLANNER_FAQ)]), "0.9")


# ============================================================ BUILDS HUB

def builds_hub():
    path = "/builds/"
    ch, cs = breadcrumb([("/", "Home"), (path, "Enshrouded Builds")])
    groups = [("Mage builds", ["wizard", "battlemage", "necromancer", "healer"]),
              ("Melee builds", ["barbarian", "warrior", "tank"]),
              ("Ranged & crit builds", ["ranger", "assassin"])]
    out = ""
    for g, slugs in groups:
        out += f'<h2 class="mb-5 mt-12 text-2xl font-bold">{g}</h2><div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">' + "".join(build_card(BY_SLUG[s]) for s in slugs) + "</div>"
    compare = table(["Build", "Tier", "Role", "Main stats", "Difficulty", "Best for"], [
        [f'<a class="font-medium text-primary hover:underline" href="/builds/{b["slug"]}/">{e(b["short"])}</a>', tier_badge(b["tier"]), e(b["role"]),
         e(b["primary"]), e(b["difficulty"]), e(b["best_for"])] for b in sorted(BUILDS, key=lambda b: TIER_ORDER[b["tier"]])])
    body = f'''
<div class="hero-glow border-b"><div class="container py-12">{ch}
<h1 class="text-3xl font-bold tracking-tight md:text-5xl">All Enshrouded 1.0 Builds</h1>
<p class="mt-4 max-w-3xl text-lg text-muted-foreground">Every Enshrouded class build in one place: mage, melee, ranged and support. All guides have been rewritten after the 1.0 skill tree reset, with skill paths to the new level 50 cap.</p></div></div>
<div class="container py-10">
<div class="prose-eb max-w-4xl"><h2 class="!mt-0">Enshrouded builds compared</h2><p>This table compares every <strong>Enshrouded build</strong> by role, main attributes and difficulty. Choose by playstyle first, then open the full guide for the skill order and gear.</p>{compare}</div>
{out}
<div class="prose-eb mt-16 max-w-4xl">
<h2>Choosing between Enshrouded builds</h2>
<p>Because Enshrouded has no locked classes, every build here is a starting point, not a cage. Most players settle on one main archetype and borrow a few nodes from a neighboring one. A Warrior might take Tank armor scaling, a Wizard might add Battlemage wand sustain, and a Ranger might take Assassin crits. Each build page ends with a <em>Hybrid builds</em> section that shows which combinations work well.</p>
<p>If you are coming back after Update 1.0 (October 15, 2026), remember that your skill points were refunded. It is the best time to try something new, since you have to re-spend everything anyway. Our <a href="/enshrouded-1-0-builds/">Enshrouded 1.0 builds guide</a> covers every change and the re-spec checklist.</p>
</div>
<section class="mt-12" aria-labelledby="guides"><h2 id="guides" class="mb-4 text-2xl font-bold">More Enshrouded 1.0 guides</h2>{hub_links(path)}</section></div>'''
    title = "All Enshrouded 1.0 Builds: Mage, Melee, Ranged & Support"
    desc = "Compare every Enshrouded 1.0 build: Wizard, Battlemage, Necromancer, Healer, Barbarian, Warrior, Tank, Ranger and Assassin by tier, stats and difficulty."
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, active=path,
                     keywords="enshrouded builds, enshrouded class builds, all enshrouded builds, enshrouded 1.0 builds",
                     schemas=[cs, {"@type": "CollectionPage", "name": title, "url": SITE + path, "description": desc}]), "0.9")


# ============================================================ 1.0 PAGE

ONE_FAQ = [
("When was Enshrouded 1.0 released?", "October 15, 2026, on Steam (PC) and PlayStation 5. The Xbox version is planned for 2027."),
("Do I lose my character in Enshrouded 1.0?", "No. Existing saves carry over. Only the skill tree is reset, and all points are refunded."),
("What is the best build after the 1.0 update?", "For most players, the <a href='/builds/battlemage/'>Battlemage</a>, which nearly every 1.0 guide ranks first, or the new <a href='/builds/necromancer/'>Necromancer</a>. For pure area damage, the <a href='/builds/wizard/'>Wizard</a>. For melee, the <a href='/builds/barbarian/'>Barbarian</a>. See our <a href='/tier-list/'>tier list</a>."),
("What new spells are in Enshrouded 1.0?", "Mana Drain, Entangle, Pillar of Flames, Blizzard, Ball Lightning, Summon Fire Totem, Summon Ice Totem, Summon Shock Totem and Summon Hollow Skeleton."),
("Is there crossplay in Enshrouded 1.0?", "There is no crossplay at launch."),
]


# what 1.0 changed for each build, from Keen Games' 1.0 changelog and combat post
CLASS_10 = {
    "wizard": "The 1.0 spell pass is aimed at you: Pillar of Flames, Blizzard and Ball Lightning add area damage, every spell now has an upgradeable Eternal version, and <strong>Blast and Cast</strong> gives your next staff attack 50% more base damage after a wand crit.",
    "battlemage": "Wands now have a piercing <strong>heavy attack</strong> from the start, plus two new active skills, <strong>Wand Evasion Attack</strong> and <strong>Aerial Wand Attack</strong>. Anvils in enemy camps now also repair your ward or shield.",
    "necromancer": "A real build for the first time: four summon spells (three totems and Hollow Skeletons) plus <strong>Advanced Necromancy</strong> and <strong>Totem Mastery</strong> to keep more of them out. Companions from Gems of Necromancy now lose health out of combat, so the spells carry the build.",
    "healer": "Every healing spell now has an Eternal version you can upgrade at the crafting survivors, so you no longer run out of charges in long fights. The new Ice Totem gives a support player a way to slow enemies chasing the group.",
    "warrior": "The dagger skills left the Warrior area, so the path to one-handed and shield skills is cleaner. Heavy melee attacks now hit several enemies, and stamina now recovers while you block.",
    "tank": "Stamina now recovers while blocking, blocking follows your camera direction for faster reactions, and anvils in enemy camps repair shields. Heavy melee attacks also hit several enemies, which helps a slow tank clear packs.",
    "barbarian": "Heavy melee attacks now hit several enemies standing close together, which is a direct buff to two-handed play, and the attack range of two-handed axes was fixed.",
    "ranger": "Three new archer skills (<strong>Puncture</strong>, <strong>Barrage</strong>, <strong>Survival Instinct</strong>) and upgradeable Eternal Ember and Voltaic arrows that use mana instead of ammo. Arrow costs and effects were rebalanced too.",
    "assassin": "All dagger skills moved into the Assassin group, so the whole build now lives in the Ranger area. Revelwood and Nomad Highlands got craftable dagger armor sets, and dagger sets now upgrade melee crit chance instead of sneak attack damage.",
}


def class_summaries():
    out = []
    for b in sorted(BUILDS, key=lambda b: TIER_ORDER[b["tier"]]):
        core = [k for k in PRESETS[b["slug"]] if not k.endswith(" node")][:4]
        spent = build_preset(b["slug"])[1]
        out.append(f'''<h3 id="{b["slug"]}-1-0">{e(b["short"])} in 1.0 ({b["tier"]}-tier, {e(b["difficulty"])})</h3>
<p>{CLASS_10[b["slug"]]}</p>
<p><strong>Plays as:</strong> {e(b["role"])}, {e(b["weapon"])}. <strong>Attributes:</strong> {e(b["primary"])}. <strong>Core skills:</strong> {", ".join(e(c) for c in core)}. Our level 50 preset spends {spent} of 212 points. <a href="/builds/{b["slug"]}/">Read the full {e(b["short"])} build →</a></p>''')
    return "\n".join(out)


def leveling_route():
    biome_names = [label for _, label in BIOMES]
    tips = [
        "Take your weapon's specialization and the first damage nodes of your main archetype, plus two or three Constitution nodes. Clear every Shroud Root and Elixir Well in Springlands and Revelwood: they are worth more than half of your points at this stage.",
        "Buy the build-defining skills (the ones in each guide's core skills table) and max their ranks. Add the utility you actually use, such as Double Jump or Inner Fires, and keep clearing Roots and Wells as you reach new biomes.",
        "Finish capstones and max ranks, then reach into one neighbouring archetype for defense or sustain. Flame nodes such as Thick Skin or Exalted get stronger with every Flame level, so they are good late picks.",
    ]
    rows = []
    for (label, budget, nb), tip in zip(STAGES, tips):
        level = int(label.split("–")[1])
        levels = 2 * (level - 1)
        rows.append([f"<strong>{label}</strong>", f"{budget} ({levels} from levels, {budget - levels} from {', '.join(biome_names[:nb]) if nb < 7 else 'all 7 biomes'})", tip])
    return table(["Stage", "Skill points by the end", "What to spend them on"], rows)


def one_point_oh():
    path = "/enshrouded-1-0-builds/"
    ch, cs = breadcrumb([("/", "Home"), (path, "Enshrouded 1.0 Builds")])
    changes = table(["Change", "Before 1.0", "In 1.0", "Builds affected"], [
        ["Level cap", "45", "<strong>50</strong>", "All"],
        ["Gear level", "Lower cap", "<strong>Up to 55</strong>", "All"],
        ["Skill tree", "Your old spend", "<strong>Full reset, points refunded</strong>", "All"],
        ["Mage skills", "-", "Advanced Necromancy, Totem Mastery, Aerial Wand Attack, Wand Evasion Attack, Blast and Cast", '<a href="/builds/wizard/">Wizard</a>, <a href="/builds/battlemage/">Battlemage</a>, <a href="/builds/necromancer/">Necromancer</a>'],
        ["Archer skills", "-", "Puncture, Barrage, Survival Instinct", '<a href="/builds/ranger/">Ranger</a>, <a href="/builds/assassin/">Assassin</a>'],
        ["Spells", "-", "9 new spells incl. 4 summons", "Mage builds"],
        ["Eternal gear", "-", "22 Eternal spells (tier 7, upgradeable) and upgradeable Eternal arrows", "Mage, Ranger"],
        ["Daggers", "Warrior tree", "<strong>Assassin tree</strong>", '<a href="/builds/assassin/">Assassin</a>, <a href="/builds/warrior/">Warrior</a>'],
    ])
    checklist = [
        "<strong>Don't leave your base</strong> with unspent points. Keen Games itself recommends this.",
        "Decide on <strong>one main archetype</strong> and, at most, one hybrid neighbor.",
        "Spend attribute points on your <strong>damage stat first</strong>, then on Constitution.",
        "Re-check your <strong>hotbar, spells and weapon swaps</strong>. Old setups may not match your new skills.",
        "Mages: slot at least one new 1.0 spell and plan which <strong>Eternal spell</strong> to upgrade.",
        "Archers: switch to <strong>Eternal arrows</strong> and upgrade the type you use most.",
        "Dagger users: look for your dagger skills in the <strong>Assassin tree</strong> now.",
        "Farm gear toward the new <strong>level 55</strong> tier. Weapon level is your biggest damage increase.",
    ]
    body = f'''
<div class="hero-glow border-b"><div class="container py-12">{ch}
<div class="flex flex-wrap gap-2">{badge("Update 1.0 · Released Oct 15, 2026", "primary")}{badge("PC & PS5", "outline")}{badge("Updated " + UPDATED_HUMAN, "outline")}</div>
<h1 class="mt-4 text-3xl font-bold tracking-tight md:text-5xl">Enshrouded 1.0 Builds: Best Builds for Update 1.0 (October 15, 2026)</h1>
<p class="mt-4 max-w-3xl text-lg text-muted-foreground">Enshrouded Update 1.0 launched on October 15, 2026 and reset every skill tree. Here are the best Enshrouded 1.0 builds for every class, what changed in the update, and how to re-spec your points.</p>
<div class="mt-6 flex flex-wrap gap-3">{button("#best", "Best 1.0 builds")}{button("#checklist", "Re-spec checklist", "outline")}</div></div></div>
<div class="container py-10"><article class="prose-eb mx-auto max-w-4xl">
<h2 class="!mt-0" id="overview">Enshrouded 1.0 at a glance</h2>
<p><strong>Enshrouded Update 1.0</strong>, the full release, launched on <strong>October 15, 2026</strong> for PC and PlayStation 5, ending more than two and a half years of Early Access. For build-focused players this release changes everything: <strong>every skill tree was reset</strong>, the level cap went from 45 to 50, gear now goes up to level 55, and the game added eight new skills, nine new spells and upgradeable Eternal gear. Every older guide is now outdated, which is why demand for <strong>Enshrouded 1.0 builds</strong> is rising so fast.</p>
<h2 id="best-build">What is the best build in Enshrouded 1.0?</h2>
<p>The best build in Enshrouded 1.0 depends on how you play, but these builds lead the Update 1.0 meta:</p>
<ul class="dots">
<li><strong>Best overall and best solo:</strong> the <a href="/builds/battlemage/">Battlemage wand build</a>, ranked first by most 1.0 guides. Unity and Arcane Deflection keep mana nearly infinite, and a ward or shield covers mistakes.</li>
<li><strong>Best area damage:</strong> the <a href="/builds/wizard/">Wizard build</a>. The new 1.0 spells (Pillar of Flames, Blizzard, Ball Lightning) and Blast and Cast make it the strongest pure caster.</li>
<li><strong>Best melee:</strong> the <a href="/builds/barbarian/">Barbarian build</a>. Two-handed stuns give it the highest physical damage.</li>
<li><strong>Best new 1.0 build:</strong> the <a href="/builds/necromancer/">Necromancer (summoner) build</a>, built on Advanced Necromancy and Totem Mastery.</li>
</ul>
<p>See the full ranking in the <a href="/tier-list/">Enshrouded 1.0 builds tier list</a>.</p>
<h2 id="changes">What changed for builds in Update 1.0</h2>
<p>The table below covers the build-relevant changes. For every new skill and spell with what it does, see the <a href="/enshrouded-1-0-patch-notes/">Enshrouded 1.0 patch notes</a>.</p>
{changes}
<h2 id="checklist">1.0 re-spec checklist</h2>
<p>Your points were refunded when you first loaded your save in 1.0. Follow this checklist before you go back into the Shroud:</p>
<ol class="my-4 list-decimal space-y-2 pl-5">{"".join(f"<li>{c}</li>" for c in checklist)}</ol>
<h2 id="mage">1.0 changes for mage builds</h2>
<p>Mages got the biggest share of new content. Five new skills and nine spells give casters options they never had in Early Access. <strong>Blast and Cast</strong> links the wand and staff: after a wand critical hit, your next staff attack within 10 seconds gets a 50% base damage bonus. <strong>Aerial Wand Attack</strong> and <strong>Wand Evasion Attack</strong> reward mobile, wand-heavy play, and <strong>Advanced Necromancy</strong> and <strong>Totem Mastery</strong> enable a full summoner archetype for the first time. Read the <a href="/builds/wizard/">Wizard</a>, <a href="/builds/battlemage/">Battlemage</a> and <a href="/builds/necromancer/">Necromancer</a> guides for details.</p>
<h2 id="ranged">1.0 changes for archer and assassin builds</h2>
<p>Archers got three new skills: <strong>Puncture</strong> (more ranged piercing damage), <strong>Barrage</strong> (bow hits can restore durability) and <strong>Survival Instinct</strong> (killing Shroud enemies with a bow or dagger extends your Shroud time). The new upgradeable <strong>Eternal arrows</strong> (the Eternal Ember fire line unlocks at levels 15, 28 and 45, plus a shock line) cost mana instead of ammo and remove most of the arrow grind. Dagger skills moved to the Assassin tree, which makes dagger builds much more focused. See the <a href="/builds/ranger/">Ranger</a> and <a href="/builds/assassin/">Assassin</a> guides.</p>
<h2 id="melee">1.0 changes for melee builds</h2>
<p>Melee builds got fewer new skills but benefit from lower skill costs and buffs to existing nodes, plus the higher level and gear caps. Warriors no longer need to step around dagger nodes, Tanks get more value from top-tier heavy armor, and Barbarians reach their two-handed damage spikes earlier. See the <a href="/builds/warrior/">Warrior</a>, <a href="/builds/tank/">Tank</a> and <a href="/builds/barbarian/">Barbarian</a> guides.</p>
<h2 id="best">Best Enshrouded 1.0 builds</h2>
<p>Every class guide below was rewritten for Update 1.0, with a level 1–50 skill path and a re-spec section for the October 15 skill tree reset. Start with the S-tier builds if you want the strongest picks.</p>
<div class="not-prose my-6 grid gap-5 sm:grid-cols-2">{"".join(build_card(b) for b in sorted(BUILDS, key=lambda b: TIER_ORDER[b["tier"]]))}</div>
<p>Want the ranking at a glance? See the <a href="/tier-list/">Enshrouded builds tier list</a>, or learn how each archetype works in the <a href="/skill-tree/">skill tree guide</a>.</p>
<h2 id="by-class">Every Enshrouded 1.0 build by class: what changed</h2>
<p>A short summary of each build after the update: what 1.0 changed for it, the attributes and core skills it uses, and how many points our planner preset spends. Each one links to the full guide with the level 1–50 skill order and gear.</p>
{class_summaries()}
<h2 id="leveling">Enshrouded 1.0 leveling route: level 1 to 50</h2>
<p>Every build follows the same three stages. Skill points come from levels (2 per level after level 1) and from exploration (1 per Shroud Root, 3 per Elixir Well), so the budget below assumes you clear the biomes that match your level. Each class guide has a stage card for every row that opens the matching preset in the <a href="/skill-planner/">skill planner</a>.</p>
{leveling_route()}
<p>The exact skill order for your class is in its guide, and the reasons behind these budgets are in <a href="/blog/enshrouded-1-0-skill-tree-changes/">what changed in the 1.0 skill tree</a>.</p>
<h2 id="mistakes">Common Enshrouded 1.0 build mistakes</h2>
<ul class="dots">
<li><strong>Leaving the base with refunded points.</strong> The 1.0 reset gave every point back. A character with an empty tree is much weaker than the one you remember.</li>
<li><strong>Rebuying your Early Access build point for point.</strong> Many skills changed cost, effect or position in 1.0, and the dagger skills moved to the Assassin group. Plan the new tree from scratch.</li>
<li><strong>Spreading points over the whole tree.</strong> A full tree costs 675 points and you get 212. Commit to one main archetype and one neighbour.</li>
<li><strong>Skipping Shroud Roots and Elixir Wells.</strong> They give 114 of your 212 points. Grinding levels alone leaves you far behind.</li>
<li><strong>Stacking Shroud time bonuses.</strong> 1.0 reduced how well Shroud time extensions stack. Hourglass capsules are now common and also drop from large Fell enemies, so pick those up instead.</li>
<li><strong>Leaving Eternal spells and arrows at their base level.</strong> They can now be upgraded at the crafting survivors, like weapons.</li>
<li><strong>Not upgrading your weapon.</strong> Gear now goes to level 55, and weapon level is still the biggest damage increase in the game.</li>
</ul>
{alert("Hotfixes ahead", "Enshrouded 1.0 is only a few days old. Keen Games' notes don't list exact skill values, so ours come from the in-game skill text (see <a href='/blog/enshrouded-1-0-new-skills/'>every new skill's ranks and costs</a>). We will update these guides when balance patches arrive.")}
<h2 id="faq">Enshrouded 1.0 FAQ</h2>
{accordion(ONE_FAQ)}
{sources()}
</article></div>'''
    title = "Enshrouded 1.0 Builds: Best Build for Every Class"
    desc = "Best Enshrouded 1.0 builds for every class after Update 1.0 (Oct 15, 2026): skill tree reset, level 50 cap, new skills and spells, re-spec checklist."
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, active=path,
                     keywords="enshrouded 1.0 builds, enshrouded 1.0 best build, enshrouded update 1.0, enshrouded 1.0, enshrouded skill tree reset, enshrouded 1.0 best build, enshrouded full release",
                     schemas=[article_schema(path, title, desc), cs, faq_schema(ONE_FAQ)]), "1.0")


# ============================================================ 1.0 PATCH NOTES

PATCH_FAQ = [
("When were the Enshrouded 1.0 patch notes released?", "Update 1.0 went live on October 15, 2026 on PC (Steam) and PlayStation 5, ending Early Access. The Xbox version is planned for 2027."),
("What are the new skills in Enshrouded 1.0?", "Eight new skills: five for mages (Advanced Necromancy, Totem Mastery, Aerial Wand Attack, Wand Evasion Attack, Blast and Cast) and three for archers (Puncture, Barrage, Survival Instinct)."),
("What are the new spells in Enshrouded 1.0?", "Nine new spells: Mana Drain, Entangle, Pillar of Flames, Blizzard, Ball Lightning, Summon Fire Totem, Summon Ice Totem, Summon Shock Totem and Summon Hollow Skeleton."),
("Did Enshrouded 1.0 reset my skill tree?", "Yes. Every character's skill tree was reset and all skill points were refunded the first time you load your save in 1.0. Your level, items and base are kept."),
("What is the new level cap in Enshrouded 1.0?", "The player level cap went up from 45 to 50, and gear now goes up to level 55. A level 50 character has 212 skill points in total."),
("Does Enshrouded 1.0 have crossplay?", "No, there is no crossplay at launch."),
]


def patch_notes():
    path = "/enshrouded-1-0-patch-notes/"
    ch, cs = breadcrumb([("/", "Home"), (path, "Enshrouded 1.0 Patch Notes")])
    skills = table(["New skill", "Tree", "What it does", "Best for"], [
        ["<strong>Advanced Necromancy</strong>", "Mage", "+1 summoned Hollow ally per rank (3 ranks).", '<a href="/builds/necromancer/">Necromancer</a>'],
        ["<strong>Totem Mastery</strong>", "Mage", "+1 active totem per rank (3 ranks).", '<a href="/builds/necromancer/">Necromancer</a>'],
        ["<strong>Aerial Wand Attack</strong>", "Mage", "Hold the use-item key during a jump: the shot deals +50% weapon damage in a small blast (25 stamina).", '<a href="/builds/battlemage/">Battlemage</a>'],
        ["<strong>Wand Evasion Attack</strong>", "Mage", "Dodging fires a piercing wand disc for +50% weapon damage (costs 50 mana).", '<a href="/builds/battlemage/">Battlemage</a>'],
        ["<strong>Blast and Cast</strong>", "Mage", "After a wand critical hit, your next staff attack within 10 seconds deals 50% more base damage.", '<a href="/builds/wizard/">Wizard</a>'],
        ["<strong>Puncture</strong>", "Archer", "+10% ranged piercing damage per rank (30% at rank 3).", '<a href="/builds/ranger/">Ranger</a>'],
        ["<strong>Barrage</strong>", "Archer", "Bow hits have a 15% chance per rank to restore 1 durability (45% at rank 3).", '<a href="/builds/ranger/">Ranger</a>'],
        ["<strong>Survival Instinct</strong>", "Archer", "Killing Shroud enemies with a bow or dagger restores 3 seconds of Shroud time per rank (9 s at rank 3).", '<a href="/builds/assassin/">Assassin</a>, <a href="/builds/ranger/">Ranger</a>'],
    ])
    spells = table(["New spell", "Type", "Use"], [
        ["<strong>Pillar of Flames</strong>", "Fire damage", "Area damage on groups"],
        ["<strong>Blizzard</strong>", "Frost damage", "Large area that slows enemies"],
        ["<strong>Ball Lightning</strong>", "Shock damage", "Mobile damage that chases targets"],
        ["<strong>Mana Drain</strong>", "Utility", "Mana sustain in long fights"],
        ["<strong>Entangle</strong>", "Control", "Roots enemies in place"],
        ["<strong>Summon Fire Totem</strong>", "Summon", "Stationary fire damage"],
        ["<strong>Summon Ice Totem</strong>", "Summon", "Slows enemies near it"],
        ["<strong>Summon Shock Totem</strong>", "Summon", "Stationary shock damage"],
        ["<strong>Summon Hollow Skeleton</strong>", "Summon", "Minion that fights and draws aggro"],
    ])
    glance = table(["Change", "Before 1.0", "In Update 1.0"], [
        ["Release", "Early Access", "<strong>Full release, October 15, 2026</strong> (PC & PS5)"],
        ["Skill tree", "Your old spend", "<strong>Full reset, all points refunded</strong>"],
        ["Level cap", "45", "<strong>50</strong>"],
        ["Gear level", "Lower cap", "<strong>Up to 55</strong>"],
        ["Skill points", "-", "<strong>212 at level 50</strong>: 98 from levels, 60 from Shroud Roots, 54 from Elixir Wells"],
        ["Wands", "Light attack only", "<strong>New heavy attack</strong> that pierces and can interrupt weaker enemies"],
        ["New skills", "-", "<strong>8</strong> (5 mage, 3 archer)"],
        ["New spells", "-", "<strong>9</strong> (4 of them summons)"],
        ["Eternal gear", "-", "<strong>22 tier-7 Eternal spells</strong> and <strong>upgradeable Eternal arrows</strong>"],
        ["Dagger skills", "Warrior tree", "<strong>Assassin tree</strong>"],
        ["Saves", "-", "Carry over (only the skill tree resets)"],
        ["Crossplay", "-", "Not at launch"],
    ])
    hotfixes = table(["Hotfix", "Date", "Build-relevant changes"], [
        ["<strong>1.0.0.1</strong>", "October 15, 2026", "Crash and lighting fixes. The <strong>Fire Wisp</strong> scroll is now fixed at level 27; before, its damage scaled with player level and was far too strong in the endgame."],
        ["<strong>1.0.0.2</strong>", "October 16, 2026", "Fixed locked world settings, grey fog on Nvidia GPUs and crashes. Corrupted characters are skipped during migration. No balance changes."],
    ])
    body = f'''
<div class="hero-glow border-b"><div class="container py-12">{ch}
<div class="flex flex-wrap gap-2">{badge("Update 1.0 · October 15, 2026", "primary")}{badge("PC & PS5", "outline")}{badge("Updated " + UPDATED_HUMAN, "outline")}</div>
<h1 class="mt-4 text-3xl font-bold tracking-tight md:text-5xl">Enshrouded 1.0 Patch Notes: Every New Skill, Spell &amp; Change</h1>
<p class="mt-4 max-w-3xl text-lg text-muted-foreground">Enshrouded Update 1.0 launched on October 15, 2026. Here is every change that matters for your character: the skill tree reset, the level 50 cap, gear 55, 8 new skills, 9 new spells, Eternal gear and the dagger move.</p>
<div class="mt-6 flex flex-wrap gap-3">{button("#new-skills", "New skills")}{button("#new-spells", "New spells", "outline")}{button("/enshrouded-1-0-builds/", "Best 1.0 builds", "outline")}</div></div></div>
<div class="container py-10"><article class="prose-eb mx-auto max-w-4xl">
<h2 class="!mt-0" id="overview">Enshrouded 1.0 update at a glance</h2>
<p><strong>Enshrouded Update 1.0</strong> is the full release of Keen Games' survival action RPG. It went live on <strong>October 15, 2026</strong> on PC (Steam) and PlayStation 5 after more than two and a half years of Early Access, and an Xbox version is planned for 2027. This page summarizes the character, combat and progression changes from the 1.0 patch notes.</p>
{glance}
{alert("Unofficial summary", "This is a player-focused summary of the 1.0 changes that affect skills, spells and builds. It is not the full official changelog. For every fix and balance number, check Keen Games' official patch notes on Steam.")}

<h2 id="skill-tree-reset">Skill tree reset in 1.0</h2>
<p>The biggest change for existing characters: <strong>every skill tree was reset</strong>. All skill points are refunded the first time you load your save in Update 1.0. Your character level, items and bases stay. Keen Games' own advice is to re-spend your points <strong>before leaving your base</strong>. Many existing skills also got lower costs or stronger effects, so old builds are worth re-planning instead of rebuilding point for point.</p>
<p>Not sure how to spend them? Our <a href="/enshrouded-1-0-builds/">Enshrouded 1.0 builds guide</a> has a re-spec checklist, and every class guide has a level 1–50 skill order.</p>

<h2 id="level-cap">Level cap 50 and gear level 55</h2>
<p>The player level cap rose from <strong>45 to 50</strong>, which means more skill points for every build: <strong>212 in total at level 50</strong> according to community planners built from the game files: <strong>98</strong> from levels (2 per level after level 1), <strong>60</strong> from Shroud Roots (1 each) and <strong>54</strong> from Elixir Wells (3 each). You only reach 212 if you explore every biome. Gear now goes up to <strong>level 55</strong>, so the top weapons and armor sets of Early Access are no longer the best in the game. Upgrading your main weapon to the new tier is the biggest damage increase after the update.</p>

<h2 id="new-skills">New skills in Enshrouded 1.0</h2>
<p>Update 1.0 adds <strong>eight new combat skills</strong>: five for mages and three for archers (a ninth new skill, Airborne Architect, is a building skill). Values below were checked against the in-game skill text in the 1.0 game files.</p>
{skills}

<h2 id="new-spells">New spells in Enshrouded 1.0</h2>
<p>Mages get <strong>nine new spells</strong>, including four summons. The summons and the new Advanced Necromancy and Totem Mastery skills make a full <a href="/builds/necromancer/">necromancer (summoner) build</a> possible for the first time.</p>
{spells}

<h2 id="eternal">Eternal spells and Eternal arrows</h2>
<p>1.0 adds <strong>Eternal</strong> versions of spells: 22 tier-7 Eternal spells that cast without using up spell charges and can be upgraded with perks. Archers get upgradeable <strong>Eternal arrows</strong> (an Eternal Ember fire line unlocks at levels 15, 28 and 45, plus a shock line) that cost mana instead of arrows, which removes most of the arrow crafting grind. See the <a href="/builds/wizard/">Wizard</a> and <a href="/builds/ranger/">Ranger</a> guides for which ones to upgrade first.</p>

<h2 id="wands">Wand heavy attack and combat changes</h2>
<p>Keen Games' official combat post confirms that <strong>wands now have a heavy attack</strong> that pierces through enemies and can interrupt weaker foes. Lock-on targeting was improved, wands can now hit explosive barrels, and <strong>melee heavy attacks now hit multiple enemies</strong>. Mana costs and cast times of spells were rebalanced as well.</p>

<h2 id="hotfixes">Enshrouded 1.0 hotfixes (1.0.0.1 and 1.0.0.2)</h2>
{hotfixes}
<h2 id="daggers">Dagger skills moved to the Assassin tree</h2>
<p>Dagger skills moved from the Warrior tree to the <strong>Assassin tree</strong>. Dagger players can now focus their points in one area, and Warriors no longer path around dagger nodes. Read the updated <a href="/builds/assassin/">Assassin build</a> and <a href="/builds/warrior/">Warrior build</a>.</p>

<h2 id="what-next">What to do after updating to 1.0</h2>
<ol class="my-4 list-decimal space-y-2 pl-5">
<li>Load your save and stay in your base. Your skill points have been refunded.</li>
<li>Pick a build from the <a href="/tier-list/">Enshrouded 1.0 tier list</a> and follow its skill order.</li>
<li>Slot at least one new spell or Eternal arrow if you play a mage or archer.</li>
<li>Farm toward the new level 55 gear tier.</li>
</ol>
<h2 id="builds">Enshrouded 1.0 builds for every class</h2>
<div class="not-prose my-6">{all_builds_grid()}</div>

<h2 id="faq">Enshrouded 1.0 patch notes FAQ</h2>
{accordion(PATCH_FAQ)}
{sources()}
</article>
<section class="mx-auto mt-12 max-w-5xl" aria-labelledby="guides"><h2 id="guides" class="mb-4 text-2xl font-bold">More Enshrouded 1.0 guides</h2>{hub_links(path)}</section></div>'''
    title = "Enshrouded 1.0 Patch Notes: New Skills, Spells & Changes"
    desc = "Enshrouded 1.0 patch notes (Oct 15, 2026): skill tree reset, level 50 cap, gear 55, 8 new skills, 9 new spells, Eternal arrows and the dagger move."
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, active=path,
                     keywords="enshrouded 1.0 patch notes, enshrouded 1.0 update, enshrouded 1.0 new skills, enshrouded 1.0 new spells, enshrouded update 1.0",
                     schemas=[article_schema(path, title, desc), cs, faq_schema(PATCH_FAQ)]), "1.0")


# ============================================================ TIER LIST

def tier_list():
    path = "/tier-list/"
    ch, cs = breadcrumb([("/", "Home"), (path, "Enshrouded Builds Tier List")])
    reasons = {
        "wizard": "Best area damage in the game. New 1.0 spells add crowd control.",
        "battlemage": "Near-infinite mana, ward or shield safety. Best solo build.",
        "barbarian": "Highest physical DPS; stuns double as defense.",
        "tank": "Essential in co-op and nearly unkillable. Slower solo.",
        "warrior": "Most forgiving build with strong self-sustain.",
        "healer": "Top value in groups, weak alone.",
        "ranger": "Eternal arrows and new skills; aim-dependent.",
        "assassin": "Biggest opener in the game (Sneak Attack +900%), but fragile and hard to play.",
        "necromancer": "New in 1.0. Summons tank for you; strongest new archetype.",
    }
    rows = ""
    for t in ["S", "A", "B"]:
        rank = ["battlemage", "necromancer", "wizard", "barbarian", "warrior", "ranger", "tank", "healer", "assassin"]
        bs = sorted((b for b in BUILDS if b["tier"] == t), key=lambda b: rank.index(b["slug"]))
        items = "".join(f'<a href="/builds/{b["slug"]}/" class="rounded-md border bg-background p-3 hover:border-primary/60"><p class="font-semibold">{e(b["short"])}</p><p class="mt-1 text-xs text-muted-foreground">{e(reasons[b["slug"]])}</p></a>' for b in bs)
        color = {"S": "bg-primary text-primary-foreground", "A": "bg-shroud text-white", "B": "bg-secondary text-secondary-foreground"}[t]
        rows += f'<div class="flex flex-col gap-3 rounded-lg border bg-card p-3 sm:flex-row"><div class="flex h-14 w-full items-center justify-center rounded-md text-2xl font-bold sm:h-auto sm:w-20 {color}">{t}</div><div class="grid flex-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">{items}</div></div>'
    consensus = table(["Build", "Our tier", "enshroudedbuilder.com", "G2A News", "KeenGamer"], [
        ['<a href="/builds/battlemage/">Battlemage</a>', "S", "S", "#1 overall", "Best overall"],
        ['<a href="/builds/necromancer/">Necromancer / Summoner</a>', "S", "S", "#2, strongest new archetype", "Best summoner"],
        ['<a href="/builds/wizard/">Wizard</a>', "S", "A", "Grouped with Battlemage", "-"],
        ['<a href="/builds/barbarian/">Barbarian</a>', "S", "A (two-handed Warrior)", "-", "-"],
        ['<a href="/builds/ranger/">Ranger</a>', "A", "A", "#3, best ranged", "Best ranged"],
        ['<a href="/builds/warrior/">Warrior</a>', "A", "-", "#4, safest melee", "Best solo melee"],
        ['<a href="/builds/tank/">Tank</a>', "A", "B", "Co-op pick", "Best co-op defense"],
        ['<a href="/builds/healer/">Healer</a>', "A", "A", "Co-op pick", "Best co-op support"],
        ['<a href="/builds/assassin/">Assassin</a>', "B", "B", "#8", "-"],
    ])
    body = f'''
<div class="hero-glow border-b"><div class="container py-12">{ch}
<h1 class="text-3xl font-bold tracking-tight md:text-5xl">Enshrouded 1.0 Builds Tier List</h1>
<p class="mt-4 max-w-3xl text-lg text-muted-foreground">The best Enshrouded builds ranked for the 1.0 full release, based on damage, survivability, solo strength and how forgiving each build is.</p></div></div>
<div class="container py-10"><div class="space-y-4">{rows}</div>
<article class="prose-eb mx-auto mt-12 max-w-4xl">
<h2 class="!mt-0">How we rank Enshrouded builds</h2>
<p>Every build on this list can finish Enshrouded 1.0. For what Update 1.0 changed on October 15, 2026 and how to re-spec, read the <a href="/enshrouded-1-0-builds/">Enshrouded 1.0 builds guide</a>. The tiers measure how <em>efficient</em> and <em>forgiving</em> a build is at the new level 50 cap with gear up to level 55. We score four things: damage output, survivability, solo strength and ease of use. A-tier builds are not weak. Several of them, like the Tank and Healer, are more valuable than S-tier builds in a coordinated co-op group.</p>
<h2>S-tier Enshrouded builds</h2>
<p>The <a href="/builds/battlemage/">Battlemage</a> is the build almost every 1.0 guide ranks first: Unity and Arcane Deflection keep its mana nearly infinite, and a ward or shield covers mistakes. The <a href="/builds/necromancer/">Necromancer (summoner)</a> joins it in S-tier because Advanced Necromancy and Totem Mastery let skeletons and totems hold whole fights. The <a href="/builds/wizard/">Wizard</a> has the best area damage in the game thanks to the new 1.0 spells and Blast and Cast. The <a href="/builds/barbarian/">Barbarian</a> brings the highest physical damage, using two-handed stuns as defense.</p>
<h2>A-tier Enshrouded builds</h2>
<p>The <a href="/builds/tank/">Tank</a> and <a href="/builds/healer/">Healer</a> rank lower only because they shine in groups. The <a href="/builds/warrior/">Warrior</a> is the best build for beginners. The <a href="/builds/ranger/">Ranger</a> improved a lot with Eternal arrows and Puncture.</p>
<h2>B-tier Enshrouded builds</h2>
<p>The <a href="/builds/assassin/">Assassin</a> has the biggest single hit in the game: Sneak Attack deals +900% damage to unaware enemies, and daggers now live in its own tree. But sneak attacks are hard to land on bosses and the build has little armor, so most 1.0 guides rank it near the bottom. It is fun and strong in skilled hands.</p>
<h2 id="consensus">How other 1.0 guides rank these builds</h2>
<p>We compared our tiers with the other major Enshrouded 1.0 build rankings published in the first days after launch. Where we differ, the reason is explained above.</p>
{consensus}
<p>Tier lists change with patches. This list was last reviewed on {UPDATED_HUMAN}.</p>
{sources()}
</article>
<section class="mx-auto mt-12 max-w-5xl" aria-labelledby="all-builds"><h2 id="all-builds" class="mb-4 text-2xl font-bold">Every Enshrouded 1.0 build guide</h2>{all_builds_grid()}
<h3 class="mb-4 mt-10 text-lg font-semibold">More Enshrouded 1.0 guides</h3>{hub_links(path)}</section></div>'''
    title = "Enshrouded 1.0 Builds Tier List: Best Builds Ranked"
    desc = "Enshrouded 1.0 builds tier list: S-tier Battlemage, Necromancer, Wizard and Barbarian, A-tier Tank, Warrior, Healer and Ranger, B-tier Assassin."
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, active=path,
                     keywords="enshrouded builds tier list, enshrouded best build, enshrouded 1.0 tier list, best class enshrouded",
                     schemas=[article_schema(path, title, desc), cs]), "0.9")


# ============================================================ SKILL TREE

def skill_tree():
    path = "/skill-tree/"
    ch, cs = breadcrumb([("/", "Home"), (path, "Enshrouded Skill Tree Guide")])
    arche = table(["Area", "Archetype", "Focus", "Used by"], [
        ["Warrior", "<strong>Warrior</strong>", "One-handed melee, sustain", '<a href="/builds/warrior/">Warrior</a>'],
        ["Warrior", "<strong>Tank</strong>", "Heavy armor, blocking, aggro", '<a href="/builds/tank/">Tank</a>'],
        ["Warrior", "<strong>Barbarian</strong>", "Two-handed weapons, stuns", '<a href="/builds/barbarian/">Barbarian</a>'],
        ["Warrior", "<strong>Athlete</strong>", "Stamina and movement", "Melee utility"],
        ["Mage", "<strong>Wizard</strong>", "Elemental spell and staff damage", '<a href="/builds/wizard/">Wizard</a>'],
        ["Mage", "<strong>Battlemage</strong>", "Wands + shields", '<a href="/builds/battlemage/">Battlemage</a>'],
        ["Mage", "<strong>Healer</strong>", "Healing and support", '<a href="/builds/healer/">Healer</a>'],
        ["Mage", "<strong>Trickster</strong>", "Spell charge speed (Quick Charge), mana regen (Mana Currents), utility", '<a href="/builds/necromancer/">Necromancer</a>'],
        ["Ranger", "<strong>Ranger</strong>", "Bows, extra arrows, weak points", '<a href="/builds/ranger/">Ranger</a>'],
        ["Ranger", "<strong>Assassin</strong>", "Crits, daggers (since 1.0), glider", '<a href="/builds/assassin/">Assassin</a>'],
        ["Ranger", "<strong>Beastmaster</strong>", "Hunting and survival utility", "Utility"],
        ["Ranger", "<strong>Survivor</strong>", "Exploration and survival utility", "Utility"],
    ])
    attrs = table(["Attribute", "Effect", "Main builds"], [
        ["<strong>Strength</strong>", "+5% melee damage per point", "Warrior, Barbarian, Tank"],
        ["<strong>Dexterity</strong>", "+5% bow and dagger damage per point", "Ranger, Assassin"],
        ["<strong>Intelligence</strong>", "+5% magic damage per point (staff, wand, spells); also scales Water Aura and Life Essences", "Wizard, Battlemage, Healer, Necromancer"],
        ["<strong>Constitution</strong>", "+50 max health per point", "Every build, Tank most"],
        ["<strong>Spirit</strong>", "+20 max mana per point", "All mage builds"],
        ["<strong>Endurance</strong>", "+10 max stamina per point (not stamina regen)", "Melee and Assassin"],
    ])
    faq = [
        ("How many archetypes are in the Enshrouded skill tree?", "Twelve, in three combat areas: Warrior (Warrior, Tank, Barbarian, Athlete), Mage (Wizard, Battlemage, Healer, Trickster) and Ranger (Ranger, Assassin, Beastmaster, Survivor)."),
        ("How do you get skill points in Enshrouded?", "Three ways: 2 points per level up to the 1.0 cap of 50, 1 point for each Shroud Root you destroy, and 3 points for each Elixir Well you cleanse."),
        ("Can you reset skills in Enshrouded?", "Yes. Respec at a Flame Altar; the cost has been 1 Rune per skill point you spent since a 2024 update (not yet re-confirmed for 1.0). In the tree you can also unlearn single nodes from the end of a chain. Everyone also got one free reset when loading a save in 1.0."),
        ("How many skill points do you get at level 50?", "212 in total if you explore everything: 98 from levels 2–50, 60 from Shroud Roots and 54 from 18 Elixir Wells, according to community planners built from the 1.0 game files."),
    ]
    body = f'''
<div class="hero-glow border-b"><div class="container py-12">{ch}
<h1 class="text-3xl font-bold tracking-tight md:text-5xl">Enshrouded 1.0 Skill Tree Guide</h1>
<p class="mt-4 max-w-3xl text-lg text-muted-foreground">How the Enshrouded skill tree works in 1.0: all twelve archetypes, the six attributes, skill points and resets, and how to plan a build that reaches level 50.</p></div></div>
<div class="container py-10"><article class="prose-eb mx-auto max-w-4xl">
<h2 class="!mt-0">How the Enshrouded skill tree works</h2>
<p>The <strong>Enshrouded skill tree</strong> is one large connected web that every character shares. You start in the middle and unlock nodes outward with skill points earned from leveling. Some nodes are small attribute increases, others are passive bonuses, and a few are build-defining skills like Blink, Unity or Battle Heal. Nodes are grouped into archetypes, and your build is the shape your path makes through them.</p>
<h2 id="structure-1-0">The 1.0 skill tree layout</h2>
<p>In Update 1.0 the tree is organized as <strong>three main trees, Warrior, Ranger and Mage</strong>, branching out from a shared <strong>Core</strong> of general skills in the center. Community planners built from the 1.0 game files count <strong>231 nodes</strong> (243 if you include the 12 free "Spark" starting nodes) and <strong>178 distinct skills</strong>. The Core alone holds 19 skills that any build can take, such as Merciless Attack. Inside each main tree, the familiar archetype groups remain: Wizard, Battlemage, Healer and Trickster sit in the Mage tree, for example. That is why build guides, including ours, still name builds after archetypes.</p>
<p>A fully explored level 50 character has <strong>212 skill points</strong>: 98 from levels, 60 from Shroud Roots and 54 from Elixir Wells. Filling the whole tree would cost roughly 675 points, so you can afford about a third of it: enough to max one main tree and reach into a second. Try it in the <a href="/skill-planner/">skill planner</a>.</p>
<h2>All 12 Enshrouded archetypes</h2>
{arche}
<h2>Attributes explained</h2>
<p>Most nodes on the path to big skills are attribute nodes, so knowing what each attribute does is the first step toward a good <strong>Enshrouded build</strong>.</p>
{attrs}
<h2>Planning a build in 1.0</h2>
<p>Update 1.0 (October 15, 2026) reset every skill tree, so everyone is re-spending points right now. The <a href="/enshrouded-1-0-builds/">Enshrouded 1.0 builds guide</a> has the full re-spec checklist. With the level cap at 50, you have more points than in Early Access, but still not enough to fill everything. The best builds pick <strong>one main archetype</strong>, go deep for its key skills, and use a <strong>neighbouring archetype</strong> for support: Tank armor for a Warrior, Battlemage sustain for a Wizard, Assassin crits for a Ranger. Avoid spreading single points across the whole tree. Many weak nodes add up to much less than a few strong capstones.</p>
<p>Utility archetypes like <strong>Athlete, Trickster, Beastmaster and Survivor</strong> are rarely a build's main focus, but one or two of their nodes can help a lot with movement, control or exploring the Shroud.</p>
<h2 id="skill-points">Enshrouded skill points: how many you get</h2>
<p>You earn <strong>2 skill points per level</strong> after level 1, so 98 by the level 50 cap. Exploration adds the rest: <strong>1 point for each Shroud Root</strong> you destroy and <strong>3 points for each Elixir Well</strong> you cleanse, 114 points across the seven biomes. A fully explored level 50 character has <strong>212 skill points</strong>, while the whole tree (231 nodes, 178 different skills) costs 675. The <a href="/skill-planner/">Enshrouded skill planner</a> calculates your budget for any level and set of explored biomes.</p>
<h2 id="respec">How to respec in Enshrouded 1.0</h2>
<p>Every existing character got one <strong>free skill tree reset</strong> when loading a save in Update 1.0, with all points refunded. After that:</p>
<ul class="dots">
<li><strong>Full respec:</strong> use the <strong>Flame Altar</strong>. Since a 2024 update the cost has been 1 Rune per skill point you had spent; this has not been re-confirmed for 1.0 yet, so check the altar before you commit.</li>
<li><strong>Single nodes:</strong> you can unlearn a skill in the tree only if nothing you still own depends on it, so refund from the end of a chain.</li>
<li><strong>Plan first:</strong> build the new layout in the <a href="/skill-planner/">skill planner</a> so you only pay for one respec.</li>
</ul>
<h2>Skill tree FAQ</h2>
{accordion(faq)}
<h2 id="all-skills">All 178 Enshrouded 1.0 skills</h2>
<p>Every skill in the 1.0 tree with its ranks, point cost and effect at max rank, checked against the in-game skill text. Use <em>Open in planner</em> to see where a skill sits in the tree.</p>
</article>
<div class="mx-auto max-w-5xl">{skills_table()}</div>
<article class="prose-eb mx-auto max-w-4xl">
{sources()}
</article>
<section class="mx-auto mt-12 max-w-5xl" aria-labelledby="all-builds"><h2 id="all-builds" class="mb-4 text-2xl font-bold">Enshrouded 1.0 builds for every archetype</h2>{all_builds_grid()}
<h3 class="mb-4 mt-10 text-lg font-semibold">More Enshrouded 1.0 guides</h3>{hub_links(path)}</section></div>'''
    title = "Enshrouded 1.0 Skill Tree: All Skills, Points & Respec"
    desc = "Enshrouded 1.0 skill tree guide: all 178 skills with costs and effects, the 12 archetypes, attributes, skill points at level 50 and how to respec."
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, active=path,
                     keywords="enshrouded skill tree, enshrouded archetypes, enshrouded attributes, enshrouded respec, enshrouded 1.0 skill tree",
                     schemas=[article_schema(path, title, desc), cs, faq_schema(faq)]), "0.8")


# ============================================================ ABOUT / 404 / SEO FILES

def about():
    path = "/about/"
    ch, cs = breadcrumb([("/", "Home"), (path, "About")])
    body = f'''<div class="container py-12"><article class="prose-eb mx-auto max-w-3xl">{ch}
<h1 class="text-3xl font-bold md:text-4xl">About Enshrouded Builds</h1>
<p>EnshroudedBuilds.org is an independent fan site that publishes build guides for Enshrouded by Keen Games. Our goal is simple: clear, up-to-date Enshrouded builds for every playstyle, rewritten for the 1.0 full release.</p>
<h2 id="methodology">Methodology: how we keep guides accurate</h2>
<p>Enshrouded 1.0 launched on October 15, 2026 and reset every skill tree, so many guides online still show Early Access numbers. This is how every guide on this site is put together:</p>
<ul class="dots">
<li><strong>Official facts first.</strong> Release dates, new skills, new spells, the level cap and hotfix changes are taken from Keen Games' official 1.0 posts and the Steam patch notes.</li>
<li><strong>Skill values are checked against the game text.</strong> Keen does not publish every rank, percentage and point cost in its patch notes, so we compare every number in our guides with the in-game skill text exported from the 1.0 game files (Steam build 1267041). Gear and item names are checked against the official Enshrouded Wiki; anything we cannot confirm there is labeled as a community pick.</li>
<li><strong>Competitor and community guides are compared</strong> before a build is changed, so our tiers and skill orders reflect where the community agrees and explain where we differ.</li>
<li><strong>Every page shows the review date</strong> and the game version it was checked against (currently {GAME_VERSION}), and lists its sources at the bottom.</li>
<li><strong>Corrections are welcome.</strong> If a tooltip in your game shows a different value, tell us and we will re-check it.</li>
</ul>
<h2 id="skill-planner">The skill planner</h2>
<p>Our <a href="/skill-planner/">Enshrouded skill planner</a> draws the real 1.0 skill tree, with the node positions and links exported from the game files by the open-source <a href="https://github.com/rossicler/enshrouded-skill-tree" rel="noopener" target="_blank">rossicler/enshrouded-skill-tree</a> project (GPL-3.0). We checked that export against our own skill table: all 178 skills match on ranks and point costs. The planner code and its data are released under the GPL-3.0 as well.</p>
<h2>Disclaimer</h2>
<p>Enshrouded and all related names and artwork are trademarks of Keen Games GmbH. This site is not affiliated with or endorsed by Keen Games.</p>
</article></div>'''
    body = body.replace("</article></div>", sources() + "</article></div>")
    write(path, page(path=path, title="About Enshrouded Builds & Methodology", description="About EnshroudedBuilds.org, an independent fan site with Enshrouded 1.0 build guides: our sources, methodology and how we keep guides accurate.",
                     body=body, builds=BUILDS, schemas=[cs], og_type="website"), "0.3")


# ============================================================ PRIVACY / TERMS / CONTACT

POLICY_DATE, POLICY_DATE_HUMAN = "2026-10-20", "October 20, 2026"
MAIL = f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'


def simple_page(path, name, h1, title, desc, inner, priority="0.3"):
    ch, cs = breadcrumb([("/", "Home"), (path, name)])
    body = f'''<div class="container py-12"><article class="prose-eb mx-auto max-w-3xl">{ch}
<h1 class="text-3xl font-bold md:text-4xl">{h1}</h1>
{inner}
</article></div>'''
    write(path, page(path=path, title=title, description=desc, body=body, builds=BUILDS, schemas=[cs], og_type="website"),
          priority, POLICY_DATE)


def privacy():
    inner = f'''<p class="text-sm text-muted-foreground">Effective date: {POLICY_DATE_HUMAN}</p>
<p>This Privacy Policy explains what information EnshroudedBuilds.org ("we", "us", "this site") collects when you visit, how it is used, and the choices you have. This site is an independent fan guide to Enshrouded. You can read every page without an account, and we do not ask you to submit any personal information.</p>
<h2 id="information-we-collect">Information we collect</h2>
<p>We do not run user accounts, comment sections, newsletters or contact forms, so we do not collect your name, address or payment details. The information that is collected comes from the services below:</p>
<ul class="dots">
<li><strong>Analytics.</strong> We use Google Analytics 4 to understand which guides are read and how visitors find us. Google Analytics uses cookies and similar technologies to collect information such as pages viewed, time on page, referring site, approximate location (country or city), device type and browser. Google Analytics 4 does not log or store full IP addresses. We use these reports in aggregate only.</li>
<li><strong>Hosting and security.</strong> The site is served by Cloudflare. Like any web server, Cloudflare processes your IP address, browser user agent and the pages you request in order to deliver the site, protect it from attacks and keep short-lived logs. See the <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener" target="_blank">Cloudflare Privacy Policy</a>.</li>
<li><strong>Fonts.</strong> Our fonts are loaded from Google Fonts, which receives your IP address and browser details when the font files are downloaded.</li>
<li><strong>Email.</strong> If you email us, we receive your email address and whatever you write. We use it only to reply to you.</li>
</ul>
<h2 id="advertising">Advertising and cookies</h2>
<p>We use or plan to use <strong>Google AdSense</strong> to show ads that help pay for the site. When ads are shown:</p>
<ul class="dots">
<li>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites.</li>
<li>Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and/or other sites on the Internet.</li>
<li>You may opt out of personalized advertising by visiting Google's <a href="https://adssettings.google.com/" rel="noopener" target="_blank">Ads Settings</a>. You can also opt out of some third-party vendors' use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank">www.aboutads.info</a>.</li>
<li>If you are in the European Economic Area, the United Kingdom or Switzerland, you will be asked for consent before personalized ads or advertising cookies are used, through a consent message provided by Google. You can change your choice at any time from that message.</li>
</ul>
<p>Learn more in <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank">How Google uses information from sites or apps that use its services</a> and in the <a href="https://policies.google.com/privacy" rel="noopener" target="_blank">Google Privacy Policy</a>.</p>
<h2 id="local-storage">Information stored in your browser</h2>
<p>This site saves one setting in your browser's local storage: whether you chose the light or dark theme. It never leaves your device. The <a href="/skill-planner/">skill planner</a> keeps your build in the page address (the part after #), which is not sent to our server. Nothing is saved unless you copy or bookmark that link.</p>
<h2 id="your-choices">Your choices</h2>
<ul class="dots">
<li>You can block or delete cookies in your browser settings. The guides work without cookies.</li>
<li>You can stop Google Analytics from collecting data with the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener" target="_blank">Google Analytics opt-out browser add-on</a>.</li>
<li>You can turn off personalized ads in Google's <a href="https://adssettings.google.com/" rel="noopener" target="_blank">Ads Settings</a>.</li>
</ul>
<h2 id="your-rights">Your privacy rights</h2>
<p>Depending on where you live (for example under the GDPR in the EU and UK, or the CCPA/CPRA in California), you may have the right to access, correct or delete personal information about you, to object to or restrict its processing, and to opt out of the "sale" or "sharing" of personal information for targeted advertising. We do not sell personal information. Because we do not hold accounts or profiles, most data about your visit is held by Google and Cloudflare, and you can manage it through the links above. For any request, email us at {MAIL}.</p>
<h2 id="retention">Data retention</h2>
<p>Google Analytics data is kept for 14 months and then deleted automatically. Emails are kept only as long as needed to answer them.</p>
<h2 id="children">Children's privacy</h2>
<p>This site is a general-audience game guide and is not directed at children under 13. We do not knowingly collect personal information from children. If you believe a child has sent us personal information, contact us and we will delete it.</p>
<h2 id="third-party-links">Links to other sites</h2>
<p>Our guides link to other websites, such as Keen Games' official news, the Enshrouded Wiki and Steam. Their privacy practices are their own, so please read their policies.</p>
<h2 id="changes">Changes to this policy</h2>
<p>If we change this policy, we will update the effective date at the top of this page.</p>
<h2 id="contact">Contact</h2>
<p>Questions about this policy? Email {MAIL} or see our <a href="/contact/">contact page</a>.</p>'''
    simple_page("/privacy-policy/", "Privacy Policy", "Privacy Policy", "Privacy Policy | Enshrouded Builds",
                "How EnshroudedBuilds.org handles your data: Google Analytics, Google AdSense advertising cookies, Cloudflare hosting and your privacy choices.",
                inner)


def terms():
    inner = f'''<p class="text-sm text-muted-foreground">Effective date: {POLICY_DATE_HUMAN}</p>
<p>These Terms of Service ("Terms") apply to your use of EnshroudedBuilds.org (the "site"). By using the site you agree to these Terms. If you do not agree, please do not use the site.</p>
<h2 id="about-the-site">About the site</h2>
<p>EnshroudedBuilds.org is an independent, unofficial fan site with build guides, a skill tree guide and a skill planner for the game Enshrouded. It is not affiliated with, endorsed by or sponsored by Keen Games GmbH. Enshrouded and all related names, logos and artwork are trademarks of Keen Games GmbH and are used here only to identify the game.</p>
<h2 id="use-of-content">Use of our content</h2>
<p>You may read, share links to, and print our guides for personal, non-commercial use. You may quote short passages if you credit EnshroudedBuilds.org and link to the original page. You may not copy whole guides or large parts of them to another website, app or video description, or present them as your own work.</p>
<p>The <a href="/skill-planner/">skill planner</a> code and its skill tree data are licensed under the GNU General Public License v3.0 or later. That license, not these Terms, governs your use of that code and data. See the <a href="/assets/planner/LICENSE.txt">license notice</a> and the <a href="/about/#skill-planner">About page</a> for credits.</p>
<h2 id="accuracy">Accuracy of information</h2>
<p>We check our guides against the in-game skill text and official patch notes (see our <a href="/about/#methodology">methodology</a>), but Enshrouded is updated regularly, and values, tiers and recommendations can change with any patch. All content is provided for general information and entertainment, "as is" and without warranty of any kind. If you find a mistake, please <a href="/contact/">tell us</a>.</p>
<h2 id="acceptable-use">Acceptable use</h2>
<p>Do not use the site in a way that harms it or other visitors. That includes attempting to gain unauthorized access, overloading the site with automated requests, scraping it at a rate that degrades service, or using it to distribute malware.</p>
<h2 id="third-parties">Advertising and third-party links</h2>
<p>The site may show ads served by Google AdSense and links to other websites. We are not responsible for the content, products or privacy practices of advertisers or linked sites. How ads use cookies is explained in our <a href="/privacy-policy/">Privacy Policy</a>.</p>
<h2 id="liability">Limitation of liability</h2>
<p>To the fullest extent permitted by law, EnshroudedBuilds.org and its authors are not liable for any indirect, incidental or consequential damages arising from your use of the site, including lost game progress or decisions you make based on our guides.</p>
<h2 id="changes">Changes to these terms</h2>
<p>We may update these Terms from time to time. The effective date at the top shows when they last changed. Continuing to use the site after a change means you accept the new Terms.</p>
<h2 id="contact">Contact</h2>
<p>Questions about these Terms? Email {MAIL}.</p>'''
    simple_page("/terms/", "Terms of Service", "Terms of Service", "Terms of Service | Enshrouded Builds",
                "Terms of Service for EnshroudedBuilds.org, an unofficial Enshrouded fan guide: use of our content, accuracy, advertising and liability.",
                inner)


def contact():
    inner = f'''<p>EnshroudedBuilds.org is run by a small team of Enshrouded players. The best way to reach us is by email:</p>
<p class="not-prose my-6"><a href="mailto:{CONTACT_EMAIL}" class="inline-flex items-center gap-2 rounded-lg border bg-card px-5 py-4 text-lg font-semibold hover:bg-accent">{CONTACT_EMAIL}</a></p>
<p>We read every message and usually reply within a few days.</p>
<h2 id="what-to-send">What to write to us about</h2>
<ul class="dots">
<li><strong>Corrections.</strong> If a skill value, cost or item in a guide doesn't match your game, tell us the page and, if you can, attach a screenshot of the tooltip. We re-check it against the game data and fix it.</li>
<li><strong>Build suggestions.</strong> Found a strong setup we don't cover? Send the skills, gear and why it works.</li>
<li><strong>Privacy requests.</strong> Questions about the data described in our <a href="/privacy-policy/">Privacy Policy</a>.</li>
<li><strong>Partnerships and other questions.</strong> Anything else about the site.</li>
</ul>
<h2 id="game-support">Game support</h2>
<p>We are a fan site and can't help with game bugs, crashes, purchases or your Keen Games account. For those, contact Keen Games through the official Enshrouded support channels.</p>'''
    simple_page("/contact/", "Contact", "Contact Enshrouded Builds", "Contact | Enshrouded Builds",
                "Contact EnshroudedBuilds.org by email for guide corrections, build suggestions, privacy requests and other questions.",
                inner)


# ============================================================ BLOG

def published_posts():
    today = datetime.date.today().isoformat()
    return sorted((p for p in POSTS if p["date"] <= today), key=lambda p: p["date"], reverse=True)


def human_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def blog():
    posts = published_posts()
    path = "/blog/"
    ch, cs = breadcrumb([("/", "Home"), (path, "Blog")])
    items = "".join(f'''<li>{card(f"""<a href="/blog/{p["slug"]}/" class="block p-5 hover:bg-accent/40">
<p class="text-xs text-muted-foreground"><time datetime="{p["date"]}">{human_date(p["date"])}</time></p>
<h2 class="mt-1 text-lg font-semibold">{e(p["h1"])}</h2>
<p class="mt-2 text-sm text-muted-foreground">{e(p["summary"])}</p></a>""")}</li>''' for p in posts)
    body = f'''<div class="container py-12"><div class="mx-auto max-w-3xl">{ch}
<h1 class="text-3xl font-bold md:text-4xl">Enshrouded Blog: 1.0 Skill Changes, Builds and Patches</h1>
<p class="mt-4 text-lg text-muted-foreground">Notes on Enshrouded 1.0: what changed in the skill tree, how each class compares before and after the update, and what every patch means for your build. Values are checked against the 1.0 game files.</p>
<ul class="mt-8 space-y-4">{items}</ul></div></div>'''
    schema = {"@type": "Blog", "name": "Enshrouded Builds Blog", "url": SITE + path, "inLanguage": "en",
              "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": f"{SITE}/blog/{p['slug']}/", "datePublished": p["date"]} for p in posts]}
    write(path, page(path=path, title="Enshrouded Blog: 1.0 Skill Changes & Patch Notes",
                     description="Enshrouded 1.0 blog: skill tree changes, class before-and-after comparisons and patch analysis, checked against the game files.",
                     body=body, builds=BUILDS, schemas=[schema, cs], og_type="website"), "0.6", posts[0]["date"] if posts else UPDATED)
    for p in posts:
        blog_post(p)


def blog_post(p):
    path = f"/blog/{p['slug']}/"
    ch, cs = breadcrumb([("/", "Home"), ("/blog/", "Blog"), (path, p["h1"])])
    body = f'''<div class="container py-12"><article class="prose-eb mx-auto max-w-3xl">{ch}
<div class="flex flex-wrap gap-2">{badge("Enshrouded 1.0", "primary")}{badge("Checked against build " + BUILD_ID, "outline")}</div>
<h1 class="mt-4 text-3xl font-bold md:text-4xl">{e(p["h1"])}</h1>
<p class="text-sm text-muted-foreground">Published <time datetime="{p["date"]}">{human_date(p["date"])}</time> by the Enshrouded Builds team</p>
{p["body"]()}
{sources()}
</article></div>'''
    schema = {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "inLanguage": "en",
              "image": SITE + "/og-image.png", "datePublished": p["date"], "dateModified": p["date"], "mainEntityOfPage": SITE + path,
              "author": {"@type": "Organization", "name": "Enshrouded Builds", "url": SITE + "/"},
              "publisher": {"@type": "Organization", "name": "Enshrouded Builds", "url": SITE + "/"}, "citation": citations(),
              "about": {"@type": "VideoGame", "name": "Enshrouded", "author": {"@type": "Organization", "name": "Keen Games"}}}
    write(path, page(path=path, title=p["title"], description=p["description"], body=body, builds=BUILDS,
                     schemas=[schema, cs]), "0.6", p["date"])


def not_found():
    body = f'''<div class="container py-24 text-center"><p class="text-6xl font-bold text-primary">404</p>
<h1 class="mt-4 text-2xl font-bold">Lost in the Shroud</h1><p class="mt-2 text-muted-foreground">This page doesn't exist. Try one of our Enshrouded builds instead.</p>
<div class="mt-8 flex justify-center gap-3">{button("/builds/", "All builds")}{button("/", "Home", "outline")}</div></div>'''
    html = page(path="/404.html", title="Page Not Found | Enshrouded Builds", description="Page not found.", body=body, builds=BUILDS)
    write("/404.html", html.replace('content="index, follow, max-image-preview:large"', 'content="noindex"'))


def seo_files():
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>\n" for p, pr, lm in PAGES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(OUT, "ads.txt"), "w") as f:
        f.write("google.com, pub-7872976152483576, DIRECT, f08c47fec0942fa0\n")
    with open(os.path.join(OUT, "favicon.svg"), "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="5" fill="#0c0c10"/>'
                '<path fill="#f97316" d="M12 3c.5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3a2.5 2.5 0 0 0 2.5 2.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6z"/></svg>')


OG_BUILD = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../local-fonts.css">
<style>*{{margin:0;box-sizing:border-box}}body{{width:1200px;height:630px;overflow:hidden;font-family:Inter,sans-serif;color:#f5efe6;position:relative}}
.art{{position:absolute;inset:0}}.shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,9,13,.92) 0%,rgba(9,9,13,.7) 45%,rgba(9,9,13,0) 70%)}}
.wrap{{position:relative;height:100%;padding:56px 64px;display:flex;flex-direction:column;max-width:720px}}
.brand{{font-family:Cinzel,serif;font-weight:700;font-size:24px;letter-spacing:.06em}}.brand b{{color:#fb923c}}
.pill{{margin-top:56px;display:inline-flex;gap:10px;font-weight:700;font-size:18px}}.pill span{{padding:7px 14px;border-radius:999px;background:#f97316;color:#140a03}}.pill span+span{{background:rgba(255,255,255,.1);color:#f5efe6;border:1px solid rgba(255,255,255,.2)}}
h1{{font-family:Cinzel,serif;font-size:68px;line-height:1.05;margin-top:22px}}h1 em{{font-style:normal;color:{accent}}}
p{{margin-top:18px;font-size:24px;color:#d6d0dc;line-height:1.4}}.url{{margin-top:auto;font-size:21px;font-weight:600}}</style></head>
<body><img class="art" src="../../../public/assets/img/builds/{slug}.svg"><div class="shade"></div><div class="wrap">
<div class="brand">ENSHROUDED<b>BUILDS</b></div><div class="pill"><span>{tier}-TIER · 1.0</span><span>Level 1–50 skill order</span></div>
<h1>Enshrouded 1.0 <em>{short}</em> Build</h1><p>{role} · {weapon}</p><div class="url">enshroudedbuilds.org</div></div></body></html>"""


def write_art():
    """Write the build illustrations and the HTML sources for the per-build share images."""
    os.makedirs(os.path.join(OUT, "assets", "img", "builds"), exist_ok=True)
    tmp = os.path.join(ROOT, "src", "og", ".tmp")
    os.makedirs(tmp, exist_ok=True)
    jobs = []
    for b in BUILDS:
        with open(os.path.join(OUT, "assets", "img", "builds", b["slug"] + ".svg"), "w") as f:
            f.write(build_svg(b["slug"]))
        src = os.path.join(tmp, b["slug"] + ".html")
        with open(src, "w") as f:
            f.write(OG_BUILD.format(slug=b["slug"], accent=ART[b["slug"]][0], tier=b["tier"], short=e(b["short"]),
                                    role=e(b["role"]), weapon=e(b["weapon"])))
        jobs += [src, os.path.join(OUT, "og", b["slug"] + ".png")]
    os.makedirs(os.path.join(OUT, "og"), exist_ok=True)
    return jobs


if __name__ == "__main__":
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    home()
    builds_hub()
    for b in BUILDS:
        build_page(b)
    one_point_oh()
    patch_notes()
    tier_list()
    skill_planner()
    skill_tree()
    about()
    privacy()
    terms()
    contact()
    blog()
    not_found()
    seo_files()
    subprocess.run(["npx", "tailwindcss", "-c", "tailwind.config.js", "-i", "src/input.css",
                    "-o", "public/assets/styles.css", "--minify"], cwd=ROOT, check=True)
    # Share image: rendered from src/og/og.html with Playwright (skipped if Playwright is unavailable)
    og = subprocess.run(["node", "src/og/og.js", os.path.join(OUT, "og-image.png")], cwd=ROOT)
    og_builds = subprocess.run(["node", "src/og/og.js", *write_art()], cwd=ROOT)
    if og.returncode or og_builds.returncode:
        print("warning: og-image.png not rendered (install playwright to enable)")
    print(f"Built {len(PAGES)} pages into {OUT}")
