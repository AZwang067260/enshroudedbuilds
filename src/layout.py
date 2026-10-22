"""Shared layout: <head>, header, footer and shadcn-style UI helpers."""
import json
from html import escape

SITE = "https://enshroudedbuilds.org"
SITE_NAME = "Enshrouded Builds"
CONTACT_EMAIL = "contact@enshroudedbuilds.org"
UPDATED = "2026-10-20"
UPDATED_HUMAN = "October 20, 2026"
# game version the facts were last checked against
GAME_VERSION = "1.0.0.2 (Steam build 1269579)"
# Google Analytics 4 measurement ID (e.g. "G-XXXXXXXXXX"); leave empty to disable tracking
GA_ID = "G-ZFZ6Q4KKHS"

NAV = [
    ("/builds/", "All Builds"),
    ("/enshrouded-1-0-builds/", "1.0 Builds"),
    ("/enshrouded-1-0-patch-notes/", "1.0 Patch Notes"),
    ("/tier-list/", "Tier List"),
    ("/skill-tree/", "Skill Tree"),
    ("/skill-planner/", "Skill Planner"),
]

JS = """
(function(){
  var root = document.documentElement;
  document.querySelectorAll('[data-theme-toggle]').forEach(function(b){
    b.addEventListener('click', function(){
      var dark = root.classList.toggle('dark');
      try { localStorage.setItem('eb-theme', dark ? 'dark' : 'light'); } catch(e) {}
    });
  });
  var mb = document.getElementById('menu-btn'), mn = document.getElementById('mobile-nav');
  if (mb && mn) mb.addEventListener('click', function(){
    var open = mn.classList.toggle('hidden') === false; mb.setAttribute('aria-expanded', open);
  });
  document.querySelectorAll('[data-tabs]').forEach(function(t){
    var btns = t.querySelectorAll('[role=tab]'), panels = t.querySelectorAll('[role=tabpanel]');
    btns.forEach(function(b, i){ b.addEventListener('click', function(){
      btns.forEach(function(x, j){ x.setAttribute('aria-selected', i===j); panels[j].hidden = i!==j; });
    }); });
  });
})();
"""

THEME_BOOT = ("(function(){try{var t=localStorage.getItem('eb-theme');}catch(e){}"
              "if(t!=='light')document.documentElement.classList.add('dark');})();")

ICON_SUN = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_FLAME = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>'
ICON_CHEV = '<svg class="chev transition-transform" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
ICON_MENU = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>'


def e(s):
    return escape(str(s), quote=True)


# ---------- shadcn-style components ----------

def badge(text, variant="secondary"):
    styles = {
        "secondary": "border-transparent bg-secondary text-secondary-foreground",
        "primary": "border-transparent bg-primary text-primary-foreground",
        "outline": "text-foreground",
        "shroud": "border-transparent bg-shroud/15 text-shroud",
    }
    return (f'<span class="inline-flex shrink-0 items-center whitespace-nowrap rounded-md border px-2.5 py-0.5 text-xs font-semibold '
            f'{styles[variant]}">{e(text)}</span>')


def button(href, text, variant="primary"):
    styles = {
        "primary": "bg-primary text-primary-foreground hover:bg-primary/90 shadow",
        "outline": "border bg-background hover:bg-accent hover:text-accent-foreground",
        "ghost": "hover:bg-accent hover:text-accent-foreground",
    }
    return (f'<a href="{e(href)}" class="btn inline-flex h-10 items-center justify-center gap-2 rounded-md px-5 '
            f'text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 '
            f'focus-visible:ring-ring {styles[variant]}">{e(text)}</a>')


def card(inner, extra=""):
    return f'<div class="rounded-lg border bg-card text-card-foreground shadow-sm {extra}">{inner}</div>'


def alert(title, body):
    return (f'<div role="note" class="my-6 rounded-lg border border-primary/40 bg-primary/5 p-4">'
            f'<p class="mb-1 font-semibold">{e(title)}</p>'
            f'<p class="text-sm text-muted-foreground leading-relaxed">{body}</p></div>')


def table(headers, rows):
    th = "".join(f'<th class="h-10 px-3 text-left align-middle font-medium text-muted-foreground">{e(h)}</th>'
                 for h in headers)
    body = ""
    for r in rows:
        tds = "".join(f'<td class="p-3 align-top">{c}</td>' for c in r)
        body += f'<tr class="border-b transition-colors hover:bg-muted/50">{tds}</tr>'
    return (f'<div class="my-5 w-full overflow-x-auto rounded-lg border"><table class="w-full caption-bottom text-sm">'
            f'<thead class="bg-muted/50"><tr class="border-b">{th}</tr></thead><tbody>{body}</tbody></table></div>')


def tabs(items):
    """items: list of (label, html)."""
    btns = "".join(
        f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" '
        f'class="tab-btn inline-flex flex-1 items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 '
        f'text-sm font-medium transition-all">{e(lbl)}</button>'
        for i, (lbl, _) in enumerate(items))
    panels = "".join(
        f'<div role="tabpanel" class="mt-4" {"" if i == 0 else "hidden"}>{html}</div>'
        for i, (_, html) in enumerate(items))
    return (f'<div data-tabs class="my-5"><div role="tablist" class="inline-flex h-10 w-full items-center rounded-md '
            f'bg-muted p-1 text-muted-foreground">{btns}</div>{panels}</div>')


def accordion(faqs):
    out = '<div class="divide-y rounded-lg border">'
    for q, a in faqs:
        out += (f'<details class="group px-4"><summary class="flex items-center justify-between gap-4 py-4 '
                f'font-medium hover:underline"><h3 class="text-base font-medium">{e(q)}</h3>{ICON_CHEV}</summary>'
                f'<div class="pb-4 text-sm leading-relaxed text-muted-foreground">{a}</div></details>')
    return out + "</div>"


def faq_schema(faqs):
    import re
    return {
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                       for q, a in faqs],
    }


def breadcrumb(items):
    """items: list of (url, name). Returns (html, schema)."""
    parts = []
    for i, (url, name) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span class="text-foreground" aria-current="page">{e(name)}</span>')
        else:
            parts.append(f'<a href="{url}" class="hover:text-foreground">{e(name)}</a>')
    html = ('<nav aria-label="Breadcrumb" class="mb-6 flex flex-wrap items-center gap-1.5 text-sm text-muted-foreground">'
            + '<span aria-hidden="true">/</span>'.join(parts) + '</nav>')
    schema = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (u, n) in enumerate(items)]}
    return html, schema


# ---------- page shell ----------

def header(active):
    links = ""
    for href, label in NAV:
        cls = "text-foreground" if href == active else "text-muted-foreground"
        links += f'<a href="{href}" class="text-sm font-medium transition-colors hover:text-foreground {cls}">{label}</a>'
    mlinks = "".join(f'<a href="{h}" class="block rounded-md px-3 py-2 text-sm hover:bg-accent">{l}</a>' for h, l in NAV)
    return f'''
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground">Skip to content</a>
<header class="sticky top-0 z-40 w-full border-b bg-background/85 backdrop-blur supports-[backdrop-filter]:bg-background/70">
  <div class="container flex h-16 items-center justify-between gap-4">
    <a href="/" class="flex items-center gap-2 font-display text-lg font-bold tracking-wide" aria-label="Enshrouded Builds home">
      <span class="text-primary">{ICON_FLAME}</span><span>Enshrouded<span class="text-primary"> Builds</span></span>
    </a>
    <nav class="hidden items-center gap-6 md:flex" aria-label="Main">{links}</nav>
    <div class="flex items-center gap-1">
      <button type="button" data-theme-toggle class="inline-flex h-9 w-9 items-center justify-center rounded-md hover:bg-accent" aria-label="Toggle dark mode">{ICON_SUN}</button>
      <button type="button" id="menu-btn" class="inline-flex h-9 w-9 items-center justify-center rounded-md hover:bg-accent md:hidden" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav">{ICON_MENU}</button>
    </div>
  </div>
  <nav id="mobile-nav" class="hidden border-t md:hidden" aria-label="Mobile"><div class="container py-2">{mlinks}</div></nav>
</header>'''


def footer(builds):
    blinks = "".join(f'<li><a href="/builds/{b["slug"]}/" class="hover:text-foreground">{e(b["short"])} Build</a></li>'
                     for b in builds)
    return f'''
<footer class="mt-24 border-t">
  <div class="container grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-4">
    <div class="lg:col-span-2">
      <a href="/" class="flex items-center gap-2 font-display text-lg font-bold"><span class="text-primary">{ICON_FLAME}</span>Enshrouded Builds</a>
      <p class="mt-3 max-w-md text-sm leading-relaxed text-muted-foreground">EnshroudedBuilds.org is an independent fan guide to the best Enshrouded builds for the 1.0 release: skill tree paths, attribute priorities, gear, spells and playstyle tips for every archetype. Last reviewed {UPDATED_HUMAN}.</p>
    </div>
    <div><p class="mb-3 text-sm font-semibold">Class Builds</p><ul class="space-y-2 text-sm text-muted-foreground">{blinks}</ul></div>
    <div><p class="mb-3 text-sm font-semibold">Guides</p><ul class="space-y-2 text-sm text-muted-foreground">
      <li><a href="/enshrouded-1-0-builds/" class="hover:text-foreground">Enshrouded 1.0 Builds</a></li>
      <li><a href="/enshrouded-1-0-patch-notes/" class="hover:text-foreground">Enshrouded 1.0 Patch Notes</a></li>
      <li><a href="/tier-list/" class="hover:text-foreground">Builds Tier List</a></li>
      <li><a href="/skill-tree/" class="hover:text-foreground">Skill Tree Guide</a></li>
      <li><a href="/skill-planner/" class="hover:text-foreground">Skill Planner</a></li>
      <li><a href="/respec/" class="hover:text-foreground">How to Respec</a></li>
      <li><a href="/builds/" class="hover:text-foreground">All Builds</a></li>
      <li><a href="/blog/" class="hover:text-foreground">Blog</a></li>
    </ul></div>
  </div>
  <div class="border-t"><div class="container flex flex-col gap-3 py-6 text-xs text-muted-foreground md:flex-row md:items-center md:justify-between">
    <p>Enshrouded is a trademark of Keen Games GmbH. This is an unofficial fan site and is not affiliated with or endorsed by Keen Games.</p>
    <nav aria-label="Legal" class="flex flex-wrap gap-x-4 gap-y-1">
      <a href="/about/" class="hover:text-foreground">About &amp; Disclaimer</a>
      <a href="/privacy-policy/" class="hover:text-foreground">Privacy Policy</a>
      <a href="/terms/" class="hover:text-foreground">Terms of Service</a>
      <a href="/contact/" class="hover:text-foreground">Contact</a>
    </nav>
  </div></div>
</footer>'''


def analytics():
    if not GA_ID:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            f"gtag('js',new Date());gtag('config','{GA_ID}');</script>\n")


def page(*, path, title, description, body, builds, active="", schemas=(), og_type="article", keywords="", og_image="/og-image.png", og_alt="Best Enshrouded Builds for 1.0 - EnshroudedBuilds.org"):
    url = SITE + path
    graph = [{"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": SITE_NAME,
              "inLanguage": "en"}] + list(schemas)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    kw = f'\n<meta name="keywords" content="{e(keywords)}">' if keywords else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">{kw}
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="theme-color" content="#0c0c10">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
{analytics()}<script>{THEME_BOOT}</script>
<link rel="stylesheet" href="/assets/styles.css">
<script type="application/ld+json">{ld}</script>
</head>
<body class="min-h-screen font-sans">
{header(active)}
<main id="main">
{body}
</main>
{footer(builds)}
<script>{JS}</script>
</body>
</html>
'''
