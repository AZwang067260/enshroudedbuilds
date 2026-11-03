"""Community builds from the r/Enshrouded thread "Share your best 1.0 build" (posted 2026-10-24).
Upvotes as of SNAPSHOT. Every link was opened in our planner and checked against its point budget.
Summaries paraphrase each author's own comment; nothing here is our recommendation."""

THREAD = "https://www.reddit.com/r/Enshrouded/comments/1xdwxjr/share_your_best_10_build_lets_make_a_community/"
SNAPSHOT = "November 3, 2026"
C = "https://www.reddit.com/r/Enshrouded/comments/1xdwxjr/comment/"

# slug, name (<=40 chars, printed on the share image), group, author, upvotes, comment id, planner code,
# level, points spent, summary, closest guide
BUILDS = [
    ("survival-mage", "Survival Mage", "mage", "LynessaMay", 19, "19rkdzm21zpb4",
     "132MreV1NsaMWjVLntIFmVBYGnvyvFC2Ap6CStndNvXSyZ2tYs7Hi", 50, 212,
     "A mage that invests heavily in health and stamina. The author's reasoning: with a big health pool, Blood Magic "
     "(health turned into mana) never takes a scary chunk, and Water Aura keeps healing you back up. Wand for groups, "
     "staff for bosses. Best solo; in a group you can go all in on magic instead. Its weak spot is mage armor, which "
     "has low defense when something does hit you.", "/builds/wizard/"),
    ("barbarian-1h-2h", "1H/2H Barbarian", "melee", "Fit-Marzipan-4186", 16, "19rki1e7cpp7p",
     "1hEwkHFJzVHHb09rFY9jfwK7Y4yHdNcVSbi48HfQr5BxtM5gM", 50, 212,
     "One- and two-handed cutting weapons. The tree takes every damage and crit skill first, then maxes health. "
     "It skips block, parry and Merciless Attack on purpose: you keep swinging, time your heavy attacks and use "
     "Evasion Attack when you need to. Drop either the 1H or 2H skills if you only use one.", "/builds/barbarian/"),
    ("bow-dagger-ranger", "Bow & Dagger Ranger", "bow", "Fit-Marzipan-4186", 16, "19rki1e7cpp7p",
     "1U4tUpdKnaYOtd7no4lsIOjcMvXRxNx1UBZ5CgbtQQAp96bYN2oA", 50, 212,
     "Bow plus dagger, without the dagger focus skill or heavy attacks. Explosive arrows are the main ammo, Eternal "
     "arrows otherwise. The tree takes all damage skills, Water Aura and two heals from the Warrior side, then maxes "
     "health.", "/builds/ranger/"),
    ("blizzard-wizard", "Blizzard Battlemage Wizard", "mage", "Fit-Marzipan-4186", 16, "19rki1e7cpp7p",
     "130RcB7SPXElKg07TX4plUFVSTYratvKFo3xG6M4L1zgAix028LbU6", 50, 212,
     "Staff and wand, built around Eternal Blizzard and Eternal Ball Lightning. Terror keeps everything inside a "
     "Blizzard stunned and Bloodletting drops resource orbs, while a mana-leech staff covers mana. The author timed "
     "boss kills and arena waves for all their builds, and this one came out on top for both.", "/builds/wizard/"),
    ("aragorn", "The Aragorn Build", "melee", "Paladin_of_Vengeance", 16, "19rks0dzebtgg",
     "122OFBzI8uwbl65Jompm98gsyCVolKCsyPvw1IAWICDPsx2kJVZu", 50, 211,
     "Sword and shield plus a bow, the way the author plays every game. In their words it isn't optimal or meta, "
     "\"it's role-play, not a math test\". A good pick if you want a character, not a spreadsheet.", "/builds/warrior/"),
    ("wand-slinger-mage", "Classic Wand-Slinger Mage", "mage", "elpadreHC", 6, "19rkxwp4u92ow",
     "12HGOSrEfXfJTi5wiFT7chScGU42IJHxwPm5j6jAzkVggAfoffTK", 50, 206,
     "A well-rounded caster that can take a couple of hits, with good endurance and sprint, crit and backstab for "
     "area spells, and food buffs. The loop: cast Blizzard, swap to the wand for about five seconds, swap back for "
     "the next Blizzard. 6 points are left free for elemental resistances or a node your gear boosts.", "/builds/wizard/"),
    ("tank-battlemage", "Tank Battlemage", "mage", "dubious_moral_ground", 4, "19rwjetw8q50g",
     "1SqrDsVBqZJ0w7PzRJevsRXoCeVAiqt78YH3ghEOaI1Ednmrh8", 50, 212,
     "A battle mage as a tank that controls the fight with spells: the full Warrior kit for armor and health, the "
     "fire staff skills filled out, Water Aura for spot heals and Life Essences for more health. Drop Pillar of "
     "Flames around yourself, let Terror stun the crowd and finish stragglers in melee to get mana back through Soul "
     "Leech. The original comment lists the exact gear it needs.", "/builds/battlemage/"),
    ("sword-board-tank", "Sword & Board Tank", "melee", "IndieMasco", 4, "19rkouc5k7m5d",
     "16GxGF6OOHuAc8cqe7RDE9C3VQdcPCQMqQ8ERwkovz1peqVdqw", 50, 212,
     "A solo one-handed sword and shield character built for toughness and survival. Its points in the Wizard "
     "branch add elemental damage, elemental resistance and some passive healing, and the only other weapon is a bow. "
     "This is the updated version they posted in the thread.", "/builds/tank/"),
    ("magic-hybrid", "Magic Hybrid", "mage", "ZonTwitch", 3, "19rki2pfjunz6",
     "130vBRdoMLUm5PWHkIHnKM1NCUavw0QTV1Kc2BR4gpWgdVlpKQY", 50, 212,
     "A Wizard, Battlemage, Healer and Tank hybrid. The author's pitch: everything melts fast, enemies stay stunned, "
     "hits refill health and mana, Shroud time refills quickly, and you have plenty of health, mana, stamina and "
     "resistances. The gear comes from the author's own magic build guide on r/Enshrouded.", "/builds/battlemage/"),
    ("eternal-arrow-ranger", "Eternal Arrow Ranger", "bow", "HauntingReddit", 3, "19rl2h53s3bac",
     "13NObIJW4kUrFLNljPVaaY6zR7gmhKUdQTAQTB99vpJtBk9JcOFK", 50, 212,
     "A pure bow build. The author's view: once you have Eternal arrows and Explosive arrows, daggers stop pulling "
     "their weight, so the points go into the bow instead.", "/builds/ranger/"),
    ("undying-paladin", "Undying Paladin", "melee", "icysunflare", 3, "19rmgoeaw5omb",
     "175YJICWuRWiR90hWTidKwMOeLzgi5W1awNScjXhYaNMjoyYPzS", 50, 212,
     "A solo one-handed and shield build. Start with movement, Warrior and Healer skills, then follow your own "
     "preferences, and switch between the slashing and blunt damage skills to match your weapon. The author beat the "
     "whole game with it and rarely died.", "/builds/tank/"),
    ("skeleton-summoner", "Skeleton Summoner (Lv 32)", "summoner", "HeimdallCanSeeYou", 3, "19ro95grd81r6",
     "11AUwl9hd5IPLNDDcMRBB211jqMcWmij6nTMJAFJOTxSQV076C", 32, 134,
     "A mid-game summoner at level 32. The skeletons tank, so hits rarely land, and the author spams staff spells, "
     "mostly Fireball, using the wand only to refill mana.", "/builds/necromancer/"),
    ("op-wizard", "OP Blizzard Wizard", "mage", "thebabo88", 1, "19rxvdg9cqj8j",
     "1BtWALWESL69GRg8KfJ9KukqU9DnOrIprND3xov8Bh65xkdd1TdQec", 50, 212,
     "Tested on Hard with 4x enemy health, solo and in a group. Blizzard plus Terror stunlocks everything, and "
     "Bloodletting with Good Metabolism fills the ground with health, stamina and mana orbs for the whole group. Use "
     "a staff with percentage mana leech. Backstab Mastery helps Chain Lightning, and three Ranger nodes (Counter "
     "Battery, Fatal Precision, Eagle's Bane) add damage. The author drops wands, summons and auras late game.",
     "/builds/wizard/"),
    ("block-tank-start", "Block Tank (starter route)", "starter", "Kuirem", 1, "19rs5vuox571e",
     "1DEc99gz1IUpzK", 50, 20,
     "The first 20 or so points of a tank. Instead of the Tank path, climb through Warrior and side-step to Nemesis: "
     "you get Heavy and Shiny Plates later, but one-handed damage early, which is better solo. Breach helps allies "
     "who use bows or melee.", "/builds/tank/"),
    ("crash-tank-start", "Crash Tank (starter route)", "starter", "Kuirem", 1, "19rs5vuox571e",
     "13Ya2zxScyChZM5VZu2", 50, 24,
     "Crash Down is risky because enemies get hits in, which a tank can afford, and the area attack helps hold "
     "aggro. Add Upwards Slash Attack for flyers and the health bonuses in Athlete. Works with any melee weapon.",
     "/builds/tank/"),
    ("paladin-start", "Paladin (starter route)", "starter", "Kuirem", 1, "19rs5vuox571e",
     "1ANNNNOSZssDRKesmAPk8tu9vkhjgYSuW2Pdm", 50, 20,
     "A magic tank: the Tank path has mana generation, so mix Tank and Wizard for Counterstrike and Radiant Aura, "
     "which reward being the one who gets hit. Cast, then swap to a melee weapon (ideally with fire damage) to get "
     "mana back from kills. The author calls it still theoretical.", "/builds/tank/"),
]

GROUPS = [
    ("mage", "Mage and battlemage builds"),
    ("melee", "Melee and tank builds"),
    ("bow", "Bow builds"),
    ("summoner", "Summoner builds"),
    ("starter", "Tank starter routes (first 20 points)"),
]


def planner_url(code):
    return "/skill-planner/#c=" + code


def comment_url(cid):
    return C + cid + "/"


def decode(code):
    """Read a planner #c= code (same format as packCode in planner.js): level and points spent per tree area."""
    from planner import AREA_COLORS
    from tree_data import client_data
    D = client_data(AREA_COLORS)
    B62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    assert code[0] == "1"
    n = 0
    for ch in code[1:]:
        n = n * 62 + B62.index(ch)
    def take(r):
        nonlocal n
        n, d = divmod(n, r)
        return d
    take(len([k for k in D["presets"] if ":" not in k]) + 1)
    level = take(D["levelCap"] + 1)
    take(D["flameCap"] + 1)
    take(1 << len(D["biomes"]))
    areas = {"Core": 0, "Mage": 0, "Warrior": 0, "Ranger": 0}
    for node in D["nodes"]:
        t = D["types"][node[1]]
        if take(2):
            r = take(t["m"]) + 1 if t["m"] > 1 else 1
            areas[t["a"]] += r * t["c"]
    return level, areas
