"""Original SVG illustrations for each build (no game assets): a Shroud-valley scene plus a weapon emblem."""

W, H = 1200, 630

# accent colour and emblem artwork per build; emblems are drawn in a 200x200 box
ART = {
    "wizard": ("#fb923c", "Staff topped with a fire orb", """
<g transform="rotate(-14 100 110)">
  <rect x="95" y="62" width="10" height="138" rx="4" fill="url(#wood)"/>
  <rect x="91" y="150" width="18" height="7" rx="2" fill="url(#metal)"/>
  <path d="M100 70 C80 66 74 46 82 30 M100 70 C120 66 126 46 118 30" stroke="url(#metal)" stroke-width="6" fill="none" stroke-linecap="round"/>
</g>
<circle cx="88" cy="40" r="34" fill="url(#halo)"/>
<circle cx="88" cy="40" r="19" fill="url(#orb)"/>
<path d="M88 2 C98 16 104 22 100 34 C97 26 92 24 88 18 C84 26 78 28 76 36 C72 22 80 14 88 2Z" fill="url(#flame)"/>"""),
    "battlemage": ("#22d3ee", "Wand crossed with a glowing arcane ward", """
<circle cx="118" cy="92" r="64" fill="url(#halo)"/>
<circle cx="118" cy="92" r="56" fill="none" stroke="var(--a)" stroke-width="4"/>
<circle cx="118" cy="92" r="44" fill="none" stroke="var(--a)" stroke-width="1.5" stroke-dasharray="4 6"/>
<path d="M118 50 L154 113 L82 113Z M118 134 L82 71 L154 71Z" fill="none" stroke="var(--a)" stroke-width="2.5" stroke-linejoin="round"/>
<circle cx="118" cy="92" r="9" fill="url(#orb)"/>
<g transform="rotate(38 60 140)">
  <rect x="55" y="70" width="9" height="120" rx="4" fill="url(#wood)"/>
  <rect x="52" y="150" width="15" height="6" rx="2" fill="url(#metal)"/>
</g>
<path d="M24 68 l6 14 14 6 -14 6 -6 14 -6 -14 -14 -6 14 -6z" fill="url(#orb)"/>"""),
    "necromancer": ("#a78bfa", "Glowing skull between two summoning totems", """
<circle cx="100" cy="80" r="70" fill="url(#halo)"/>
<path d="M100 26 C134 26 150 50 150 76 C150 94 142 104 134 110 L134 126 C134 132 130 136 124 136 L76 136 C70 136 66 132 66 126 L66 110 C58 104 50 94 50 76 C50 50 66 26 100 26Z" fill="url(#bone)"/>
<ellipse cx="80" cy="82" rx="13" ry="15" fill="#0b0712"/><ellipse cx="120" cy="82" rx="13" ry="15" fill="#0b0712"/>
<circle cx="80" cy="84" r="5" fill="var(--a)"/><circle cx="120" cy="84" r="5" fill="var(--a)"/>
<path d="M100 98 L92 114 L108 114Z" fill="#0b0712"/>
<path d="M82 136 V124 M94 136 V124 M106 136 V124 M118 136 V124" stroke="#0b0712" stroke-width="3"/>
<g fill="url(#wood)"><rect x="14" y="120" width="22" height="70" rx="3"/><rect x="164" y="120" width="22" height="70" rx="3"/></g>
<g fill="url(#orb)"><path d="M25 132 l7 10 -7 10 -7 -10z"/><path d="M175 132 l7 10 -7 10 -7 -10z"/></g>
<path d="M10 120 h30 l-4 -10 h-22z M160 120 h30 l-4 -10 h-22z" fill="url(#metal)"/>"""),
    "healer": ("#34d399", "Healing water drop with a glowing cross", """
<circle cx="100" cy="112" r="78" fill="url(#halo)"/>
<path d="M100 18 C128 62 152 92 152 124 A52 52 0 0 1 48 124 C48 92 72 62 100 18Z" fill="url(#orb)" stroke="var(--a)" stroke-width="3"/>
<path d="M92 98 h16 v18 h18 v16 h-18 v18 h-16 v-18 h-18 v-16 h18z" fill="#f0fdf4"/>
<path d="M68 112 C66 96 76 80 86 68" stroke="#f0fdf4" stroke-opacity=".6" stroke-width="5" fill="none" stroke-linecap="round"/>
<circle cx="100" cy="122" r="76" fill="none" stroke="var(--a)" stroke-width="1.5" stroke-dasharray="3 7"/>"""),
    "warrior": ("#fbbf24", "One-handed sword crossed over a heater shield", """
<circle cx="100" cy="100" r="80" fill="url(#halo)"/>
<path d="M92 44 L142 58 L140 108 C137 143 118 163 92 178 C66 163 47 143 44 108 L42 58Z" fill="url(#shield)" stroke="url(#gold)" stroke-width="6" stroke-linejoin="round"/>
<path d="M92 60 V160 M54 96 H130" stroke="url(#gold)" stroke-width="5"/>
<g transform="rotate(-38 120 120)">
  <path d="M115 0 L125 0 L126 128 L114 128Z" fill="url(#metal)"/>
  <path d="M120 -4 L126 8 L114 8Z" fill="#e5e7eb"/>
  <rect x="92" y="126" width="56" height="9" rx="3" fill="url(#gold)"/>
  <rect x="115" y="135" width="10" height="38" rx="3" fill="url(#wood)"/>
  <circle cx="120" cy="178" r="8" fill="url(#gold)"/>
</g>"""),
    "tank": ("#94a3b8", "Tower shield with a flanged mace", """
<circle cx="100" cy="100" r="82" fill="url(#halo)"/>
<rect x="30" y="30" width="96" height="158" rx="16" fill="url(#shield)" stroke="url(#metal)" stroke-width="7"/>
<circle cx="78" cy="108" r="18" fill="url(#metal)"/><circle cx="78" cy="108" r="7" fill="var(--a)"/>
<g fill="url(#metal)"><circle cx="44" cy="44" r="4"/><circle cx="112" cy="44" r="4"/><circle cx="44" cy="174" r="4"/><circle cx="112" cy="174" r="4"/></g>
<g transform="rotate(28 150 110)">
  <rect x="145" y="70" width="10" height="130" rx="4" fill="url(#wood)"/>
  <circle cx="150" cy="58" r="20" fill="url(#metal)"/>
  <path d="M150 30 l6 12 h-12z M150 86 l6 -12 h-12z M122 58 l12 -6 v12z M178 58 l-12 -6 v12z" fill="url(#metal)"/>
</g>"""),
    "barbarian": ("#ef4444", "Two-handed greataxe with a double-bit head", """
<circle cx="100" cy="90" r="80" fill="url(#halo)"/>
<g transform="rotate(22 100 100)">
  <rect x="94" y="20" width="12" height="178" rx="5" fill="url(#wood)"/>
  <rect x="92" y="150" width="16" height="30" rx="3" fill="#3f2a1d"/>
  <path d="M106 40 C140 22 162 34 168 46 C160 66 160 86 168 106 C150 114 128 106 106 92Z" fill="url(#metal)"/>
  <path d="M94 40 C60 22 38 34 32 46 C40 66 40 86 32 106 C50 114 72 106 94 92Z" fill="url(#metal)"/>
  <path d="M166 48 C158 68 158 86 166 104 M34 48 C42 68 42 86 34 104" stroke="#fef2f2" stroke-width="3" fill="none" opacity=".7"/>
  <rect x="90" y="34" width="20" height="64" rx="4" fill="url(#gold)"/>
</g>"""),
    "ranger": ("#84cc16", "Longbow drawn with an arrow", """
<circle cx="100" cy="100" r="80" fill="url(#halo)"/>
<path d="M66 12 Q160 100 66 188" stroke="url(#wood)" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M66 12 L44 100 L66 188" stroke="#ecfccb" stroke-width="2" fill="none"/>
<rect x="44" y="97" width="130" height="6" rx="3" fill="url(#wood)"/>
<path d="M196 100 L170 88 L176 100 L170 112Z" fill="url(#metal)"/>
<path d="M44 100 L28 86 L56 86Z M44 100 L28 114 L56 114Z" fill="var(--a)"/>
<rect x="104" y="92" width="10" height="16" rx="2" fill="#3f2a1d"/>"""),
    "assassin": ("#e879f9", "Two crossed daggers dripping poison", """
<circle cx="100" cy="100" r="78" fill="url(#halo)"/>
<g transform="rotate(40 100 100)">
  <path d="M100 6 C110 30 108 70 106 104 L94 104 C92 70 90 30 100 6Z" fill="url(#metal)"/>
  <rect x="80" y="104" width="40" height="8" rx="3" fill="url(#gold)"/>
  <rect x="95" y="112" width="10" height="34" rx="3" fill="#2b1d33"/>
</g>
<g transform="rotate(-40 100 100)">
  <path d="M100 6 C110 30 108 70 106 104 L94 104 C92 70 90 30 100 6Z" fill="url(#metal)"/>
  <rect x="80" y="104" width="40" height="8" rx="3" fill="url(#gold)"/>
  <rect x="95" y="112" width="10" height="34" rx="3" fill="#2b1d33"/>
</g>
<path d="M100 150 C106 162 108 168 100 176 C92 168 94 162 100 150Z" fill="var(--a)"/>"""),
}


def _defs(accent):
    return f"""<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0a12"/><stop offset=".6" stop-color="#1b1326"/><stop offset="1" stop-color="#2b1a2e"/></linearGradient>
<radialGradient id="glow" cx=".72" cy=".48" r=".45"><stop offset="0" stop-color="{accent}" stop-opacity=".45"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<radialGradient id="shroud" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#a78bfa" stop-opacity=".35"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></radialGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{accent}" stop-opacity=".55"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<radialGradient id="orb" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity=".6"/></radialGradient>
<linearGradient id="flame" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f97316"/><stop offset="1" stop-color="#fde68a"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1f5f9"/><stop offset=".5" stop-color="#94a3b8"/><stop offset="1" stop-color="#475569"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fde68a"/><stop offset="1" stop-color="#b45309"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7c4a2a"/><stop offset=".5" stop-color="#a86b3c"/><stop offset="1" stop-color="#5b341c"/></linearGradient>
<linearGradient id="bone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f5f0e6"/><stop offset="1" stop-color="#b9ae9a"/></linearGradient>
<linearGradient id="shield" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b2a20"/><stop offset="1" stop-color="#1c1410"/></linearGradient>
<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="lift"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".6"/></filter>
</defs>"""


def _scene(accent, emblem):
    stars = "".join(f'<circle cx="{(i * 137) % W}" cy="{(i * 71) % 260 + 12}" r="{1 + i % 2}" fill="#fff" opacity="{0.25 + (i % 4) * 0.12:.2f}"/>'
                    for i in range(46))
    embers = "".join(f'<circle cx="{560 + (i * 53) % 560}" cy="{180 + (i * 97) % 380}" r="{2 + i % 3}" fill="{accent}" opacity="{0.35 + (i % 3) * 0.2:.2f}"/>'
                     for i in range(22))
    return f"""<rect width="{W}" height="{H}" fill="url(#sky)"/>{stars}
<rect width="{W}" height="{H}" fill="url(#glow)"/>
<path d="M0 470 L120 380 L210 430 L330 330 L450 420 L560 360 L700 440 L820 350 L960 430 L1080 370 L1200 420 V630 H0Z" fill="#171221"/>
<path d="M0 520 L150 450 L290 500 L420 440 L600 510 L760 455 L900 505 L1050 460 L1200 500 V630 H0Z" fill="#100c18"/>
<g filter="url(#blur)"><ellipse cx="300" cy="560" rx="420" ry="70" fill="url(#shroud)"/><ellipse cx="900" cy="585" rx="460" ry="60" fill="url(#shroud)"/></g>
{embers}
<g transform="translate(740 155) scale(1.6)" filter="url(#lift)" style="--a:{accent}">{emblem}</g>"""


def build_svg(slug):
    accent, _, emblem = ART[slug]
    emblem = emblem.replace("var(--a)", accent)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'{_defs(accent)}{_scene(accent, emblem)}</svg>')


def alt_text(slug, name):
    return f"Enshrouded 1.0 {name} build illustration: {ART[slug][1].lower()}"
