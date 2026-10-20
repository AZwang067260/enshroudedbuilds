"""Blog posts. A post goes live on the first build on or after its `date`, so the schedule is one post per day for
the first week and one per week after that. Values in posts are generated from the 1.0 game export, not typed by hand."""
from layout import e, table
from skills_data import PRESETS
from tree_data import OUR, game_text, skill_cost

NEW_SKILLS = ["Blast and Cast", "Aerial Wand Attack", "Wand Evasion Attack", "Advanced Necromancy", "Totem Mastery",
              "Puncture", "Barrage", "Survival Instinct"]
BUILD_NAMES = {"wizard": "Wizard", "battlemage": "Battlemage", "necromancer": "Necromancer", "healer": "Healer",
               "warrior": "Warrior", "tank": "Tank", "barbarian": "Barbarian", "ranger": "Ranger", "assassin": "Assassin"}


def _ranks(name):
    cost, ranks = skill_cost(name)
    return f"{cost} pt" if ranks == 1 else f"{cost} pt × {ranks}"


def _total(names):
    return sum(c * r for c, r in (skill_cost(n) for n in names))


def _per_rank(name):
    _, ranks = skill_cost(name)
    return "<br>".join(f"Rank {r}: {e(game_text(name, r))}" for r in range(1, ranks + 1))


def _users(name):
    return ", ".join(f'<a href="/builds/{b}/">{BUILD_NAMES[b]}</a>' for b in PRESETS if name in PRESETS[b]) or "None of our presets"


def new_skills_post():
    glance = table(["Skill", "Area / archetype", "Cost", "In-game effect at max rank"], [
        [f"<strong>{n}</strong>", f"{OUR[n][0]} / {OUR[n][1]}", _ranks(n), e(game_text(n))] for n in NEW_SKILLS])
    ranked = lambda names: table(["Skill", "What each rank gives (in-game text)"], [[f"<strong>{n}</strong>", _per_rank(n)] for n in names])
    who = table(["Skill", "Taken by our 1.0 presets", "Verdict"], [
        ["<strong>Blast and Cast</strong>", _users("Blast and Cast"), "Must-have for any caster that carries both a wand and a staff."],
        ["<strong>Aerial Wand Attack</strong>", _users("Aerial Wand Attack"), "Cheap utility. Take it when the path to Blast and Cast passes it."],
        ["<strong>Wand Evasion Attack</strong>", _users("Wand Evasion Attack"), "Best wand addition: it turns every dodge into damage."],
        ["<strong>Advanced Necromancy</strong>", _users("Advanced Necromancy"), "Core for summoners, skip it otherwise."],
        ["<strong>Totem Mastery</strong>", _users("Totem Mastery"), "Core for summoners, good for healers who drop totems."],
        ["<strong>Puncture</strong>", _users("Puncture"), "Highest-value bow node in 1.0: a flat 30% for 6 points."],
        ["<strong>Barrage</strong>", _users("Barrage"), "Quality of life. Saves repair trips on long bow runs."],
        ["<strong>Survival Instinct</strong>", _users("Survival Instinct"), "Strong for any bow or dagger build that explores the Shroud."],
    ])
    mage, summon, archer = NEW_SKILLS[:3], NEW_SKILLS[3:5], NEW_SKILLS[5:]
    return f'''
<p>Enshrouded 1.0 added <strong>eight new combat skills</strong> to the skill tree: five for mages and three for archers. Keen Games' release notes name them, but they do not list ranks, point costs or the exact numbers. We pulled all of that from the in-game skill text in the 1.0 game files (build 1267041), so every value below is what your tooltip shows at that rank.</p>
<p>Short version: all eight together cost <strong>{_total(NEW_SKILLS)} skill points</strong>. That's about 16% of the 212 points a fully explored level 50 character has, so no build takes all of them. Wand casters want the three wand skills, summoners want the two summon skills, and bow builds want all three archer skills.</p>
<h2 id="at-a-glance">The 8 new 1.0 skills at a glance</h2>
{glance}
<h2 id="mage">Mage: Blast and Cast and the two wand skills</h2>
<p>The three wand skills cost <strong>{_total(mage)} points</strong> in total and all sit in the Mage area.</p>
<p><strong>Blast and Cast</strong> (Trickster) is the one that changes how mages play. After a wand critical hit, your next staff attack within 10 seconds deals 50% more base damage. That gives the wand a job beyond chip damage: land a crit, swap, and open with a boosted staff shot. Both our <a href="/builds/wizard/">Wizard</a> and <a href="/builds/battlemage/">Battlemage</a> guides take it.</p>
<p><strong>Wand Evasion Attack</strong> (Battlemage) fires a magical disc when you press the use-item key while evading. The disc pierces enemies and deals 50% additional weapon damage, for 50 mana. Battlemages dodge constantly, so this is free damage on top of movement you were going to make anyway.</p>
<p><strong>Aerial Wand Attack</strong> (Battlemage) adds a special attack when you hold the use-item key during a jump. It costs 25 stamina. It's the weakest of the three on its own, but it is cheap and sits on the path most wand builds walk anyway.</p>
<h2 id="summoner">Summoner: Advanced Necromancy and Totem Mastery</h2>
<p>These two skills are why the <a href="/builds/necromancer/">Necromancer</a> exists as a real build in 1.0. Each has three ranks and both together cost <strong>{_total(summon)} points</strong>. They don't add damage directly. They raise how many summons you can keep up at once, which matters because 1.0 also added four summon spells: Summon Fire Totem, Summon Ice Totem, Summon Shock Totem and Summon Hollow Skeleton.</p>
{ranked(summon)}
<p>Healers can take Totem Mastery too: an Ice Totem slows enemies that are chasing the group, which keeps your allies alive without a single heal.</p>
<h2 id="archer">Archer: Puncture, Barrage and Survival Instinct</h2>
<p>The three archer skills cost <strong>{_total(archer)} points</strong>. <strong>Puncture</strong> (Ranger) is the one to grab first: +10% ranged piercing damage per rank, 30% at rank 3, with no condition attached. <strong>Barrage</strong> (Ranger) gives bow hits a 15% chance per rank to restore 1 durability, which saves repair trips on long bow runs. <strong>Survival Instinct</strong> (Survivor) restores 3 seconds of Shroud time per rank when you kill a Shroud enemy with a bow or a dagger. That's why our <a href="/builds/assassin/">Assassin</a> takes it as well as the <a href="/builds/ranger/">Ranger</a>.</p>
{ranked(archer)}
<h2 id="airborne-architect">The building skill: Airborne Architect</h2>
<p>1.0 also added <strong>Airborne Architect</strong> in the Core area at the center of the tree ({_ranks("Airborne Architect")}). It's not a combat skill: inside your base you turn into a spark and fly freely in first person while building. It does nothing for your build's damage, so leave it for later unless you build a lot.</p>
<h2 id="who-should-take-them">Which builds should take the new skills</h2>
<p>This table shows which of our nine 1.0 guides use each skill in their level 50 preset, and our verdict:</p>
{who}
<p>Warrior, Tank and Barbarian don't take any of them: the new skills are all ranged or magic. To see a skill's exact position and the path to it, open it in the <a href="/skill-planner/">Enshrouded skill planner</a>, or read how the areas fit together in the <a href="/skill-tree/">skill tree guide</a>. For every new spell and the full list of changes, see the <a href="/enshrouded-1-0-patch-notes/">Enshrouded 1.0 patch notes</a>.</p>
'''


# slug, publish date, title (<=60), description (<=155), H1, body function
POSTS = [
    {"slug": "enshrouded-1-0-new-skills", "date": "2026-10-20",
     "title": "Enshrouded 1.0 New Skills: Ranks, Costs & Who Needs Them",
     "description": "All 8 new combat skills in Enshrouded 1.0 with point costs and per-rank values from the game files, plus which builds should take each one.",
     "h1": "Enshrouded 1.0 New Skills: Every Rank, Cost and Who Should Take Them",
     "summary": "All eight new 1.0 combat skills with costs and per-rank values from the game files, and which builds should take them.",
     "body": new_skills_post},
]
