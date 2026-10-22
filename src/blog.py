"""Blog posts. A post goes live on the first build on or after its `date`, so the schedule is one post per day for
the first week and one per week after that. Values in posts are generated from the 1.0 game export, not typed by hand."""
from layout import e, table
from skills_data import PRESETS
from tree_data import (BIOMES, BUILD_ID, NODES, OUR, PROGRESSION, STAGES, build_preset, cheapest_path, cost, game_text, max_rank,
                       nodes_named, our_name, skill_cost)

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


def _tree_numbers():
    """Node count, full cost and per-area totals of the 1.0 tree, from the export."""
    nodes, points = {}, {}
    for nid, n in NODES.items():
        o = OUR.get(our_name(n["type"]))
        area = o[0] if o else "Core"
        nodes[area] = nodes.get(area, 0) + 1
        points[area] = points.get(area, 0) + cost(nid) * max_rank(nid)
    return nodes, points


def _biome_rows():
    """Per biome: Shroud Roots give 1 point and Elixir Wells 3, so the export's point and source counts give both."""
    rows = []
    for key, label in BIOMES:
        b = PROGRESSION["biomes"][key]
        wells = (b["points"] - b["unlocks"]) // 2
        rows.append((label, b["unlocks"] - wells, wells, b["points"]))
    return rows


def tree_changes_post():
    lv = PROGRESSION["leveling"]
    per_level, cap = lv["skillPointsPerLevel"], lv["playerLevelCap"]
    from_levels = per_level * (cap - 1)
    biomes = _biome_rows()
    roots, wells, explore = sum(r[1] for r in biomes), sum(r[2] for r in biomes), sum(r[3] for r in biomes)
    budget = from_levels + explore
    nodes, points = _tree_numbers()
    full = sum(points.values())
    flame = PROGRESSION["flame"]["flameLevelCap"]
    added = per_level * 5 + 12 + 6
    biome_table = table(["Biome", "Shroud Roots (1 pt)", "Elixir Wells (3 pt)", "Skill points"],
                        [[label, str(r), str(w), f"<strong>{pts}</strong>"] for label, r, w, pts in biomes]
                        + [["<strong>Total</strong>", f"<strong>{roots}</strong>", f"<strong>{wells}</strong>", f"<strong>{explore}</strong>"]])
    area_table = table(["Area", "Nodes", "Points to fill it", "Share of a 212-point budget"],
                       [[a, str(nodes[a]), str(points[a]), f"{round(100 * points[a] / budget)}%"] for a in ("Mage", "Ranger", "Warrior", "Core")]
                       + [["<strong>Whole tree</strong>", f"<strong>{sum(nodes.values())}</strong>", f"<strong>{full}</strong>", f"{round(100 * full / budget)}%"]])
    moved = ["Dagger Mastery", "Dagger Specialization", "Backstab Mastery", "Expose Weakness", "Slice And Dice", "Quick Reflex Block"]
    moved_table = table(["Skill", "Now in", "Cost", "In-game effect at max rank"],
                        [[f"<strong>{n}</strong>", f"{OUR[n][0]} / {OUR[n][1]}", _ranks(n), e(game_text(n))] for n in moved])
    repos = ["Veteran", "One-Handed Specialization", "Inner Fires", "Snap"]
    repos_table = table(["Skill", "1.0 position", "1.0 cost", "In-game effect at max rank"],
                        [[f"<strong>{n}</strong>", f"{OUR[n][0]} / {OUR[n][1]}", _ranks(n), e(game_text(n))] for n in repos])
    return f'''
<p>Enshrouded 1.0 did more to the skill tree than add a few nodes. It reset every character, raised the level cap, added Shroud Roots that pay out extra points, and moved or re-priced a number of existing skills. This post goes through each change with numbers taken from the 1.0 game files (build {BUILD_ID}) and quotes from Keen Games' 1.0 changelog.</p>
<p><strong>Short version:</strong> a fully explored level {cap} character now has <strong>{budget} skill points</strong>. The changelog adds at least <strong>{added} points</strong> to that maximum: {per_level * 5} from the five new levels and 18 from new Shroud Roots. The whole tree has <strong>{sum(nodes.values())} nodes</strong> and costs <strong>{full} points</strong> to fill, so you can still only afford about {round(100 * budget / full)}% of it. Choosing a direction matters as much as before.</p>
<h2 id="reset">Every skill tree was reset</h2>
<p>The changelog opens with "a public safety announcement": when you first load an existing save in 1.0, <strong>the skill tree is reset</strong> and all points come back to you. Your level, gear and bases stay. Spend the points before you head out, because a character with an empty tree is much weaker than the one you left. If you don't have a plan yet, build one in the <a href="/skill-planner/">skill planner</a> first. It costs nothing to try layouts there.</p>
<h2 id="skill-points">Skill points: level 50 and 18 new Shroud Roots</h2>
<p>You still earn skill points in three ways: <strong>{per_level} per level</strong> after level 1, <strong>1 per Shroud Root</strong> you destroy and <strong>3 per Elixir Well</strong> you cleanse. 1.0 changed the first two:</p>
<ul class="dots">
<li><strong>Level cap 45 → {cap}.</strong> Five more levels are {per_level * 5} more points, for {from_levels} from levels in total.</li>
<li><strong>Cinder's Cradle</strong>, the new biome in the north, "brings 12 new Shroud Roots" according to the changelog.</li>
<li><strong>Edge-of-the-world areas.</strong> Springlands, Blackmire and the Kindlewastes in particular got new playable areas near the map edge with "6 additional Shroud Roots".</li>
</ul>
<p>The 1.0 game data lists how many points each biome holds and how many point sources it has. Because a Root is worth 1 point and a Well 3, those two numbers tell you how many of each there are:</p>
{biome_table}
<p>That's {roots} Roots and {wells} Wells for {explore} exploration points, plus {from_levels} from levels: <strong>{budget} in total</strong>. Cinder's Cradle has no Elixir Wells in the data, only Roots. Exploration is a big share early on: a level 15 character who has cleared Springlands and Revelwood has {per_level * 14} points from levels and {biomes[0][3] + biomes[1][3]} from those two biomes. Our build guides use exactly these stage budgets (level 15 with 2 biomes, level 35 with 4, level 50 with all 7).</p>
<h2 id="tree-in-numbers">The 1.0 tree in numbers</h2>
<p>The 1.0 tree has <strong>{sum(nodes.values())} nodes</strong> and {len(OUR)} different skills, split into three combat areas around a shared Core. Filling every node to max rank would cost {full} points:</p>
{area_table}
<p>Filling the Mage or Ranger area alone would take more than your whole budget, and the Warrior area would eat {round(100 * points['Warrior'] / budget)}% of it, so every build is a path through an area, not the whole area. Most of our <a href="/builds/">1.0 builds</a> spend nearly all of their points in one area and reach a few nodes into a neighbour, for example Tank armor nodes for a Warrior. The <a href="/skill-tree/">skill tree guide</a> explains the twelve archetypes inside these areas.</p>
<h2 id="new-and-moved">New, moved and re-priced skills</h2>
<p><strong>New skills.</strong> The changelog names eight new combat skills (Aerial Wand Attack, Wand Evasion Attack, Advanced Necromancy, Totem Mastery, Blast and Cast, Puncture, Barrage, Survival Instinct) and one building skill, Airborne Architect, "at the center of the skill tree". We covered all of them rank by rank in <a href="/blog/enshrouded-1-0-new-skills/">Enshrouded 1.0 new skills</a>.</p>
<p><strong>Dagger skills moved.</strong> Keen Games "moved dagger-related skills from the warrior area of the skill tree to the assassin tree, where it makes much more sense." In 1.0 these dagger skills sit in the Ranger area's Assassin group:</p>
{moved_table}
<p>For dagger players this is the biggest change in the tree: you no longer split points between the Warrior and Ranger areas. For Warriors it means fewer dagger nodes in the way. More in our <a href="/builds/assassin/">Assassin build</a>.</p>
<p><strong>Re-priced and repositioned.</strong> The changelog says Keen "reduced the costs and buffed the effects of many skills based on feedback from the community", and "adjusted the position of a few skills such as Veteran, One-Handed Specialization, Inner Fires and Snap". The notes don't list the old values, so we only show where these four are now and what they cost:</p>
{repos_table}
<h2 id="shroud-time">Shroud time: weaker stacking, more hourglasses</h2>
<p>One change hits skills without touching the tree. Keen Games found that stacking Shroud time bonuses pushed the Shroud timer "very far into the background" in the late game, so the <strong>overall effectiveness of stacked Shroud time extensions was reduced</strong>. To balance it, hourglass capsules now appear in many more places, add about 70% more time when used, and also drop from large Fell enemies.</p>
<p>In practice, Inner Fires ({_ranks("Inner Fires")}) and Survival Instinct ({_ranks("Survival Instinct")}) are still worth their points, but stacking every timer bonus you can find gives less than it did in Early Access. Pick up hourglasses instead of spending extra points on more Shroud time.</p>
<h2 id="flame">Flame level {flame} and attribute points</h2>
<p>The Flame also feeds your stats. In the 1.0 data each Flame level above 1 adds <strong>+1 to every attribute</strong>, and the Flame now goes up to level {flame}, so a max-Flame character gets +{flame - 1} to each attribute without spending a skill point. A few "Flame" nodes (Thick Skin, Barbarian, Exalted, Arcane Concentration, Graceful Stride, Endurance of the Flame) add one more point of their attribute for every two Flame levels. They get better as you progress, which makes them good late-game picks. The <a href="/skill-planner/">planner</a> includes the Flame level in its stat totals.</p>
<h2 id="what-to-do">What this means for your build</h2>
<ul class="dots">
<li><strong>Plan first, then spend.</strong> With {budget} points and a {full}-point tree, a layout planned in the <a href="/skill-planner/">skill planner</a> beats spending as you go.</li>
<li><strong>Explore for points.</strong> {explore} of your {budget} points come from Roots and Wells. Clearing them as you reach each biome keeps you ahead of the level curve.</li>
<li><strong>Dagger users:</strong> rebuild around the Assassin group. <strong>Mages:</strong> look at the new wand and summon skills in the <a href="/builds/battlemage/">Battlemage</a> and <a href="/builds/necromancer/">Necromancer</a> guides.</li>
<li><strong>Compare builds</strong> in the <a href="/tier-list/">1.0 tier list</a> and read the full <a href="/enshrouded-1-0-patch-notes/">1.0 patch notes summary</a> for spells and gear.</li>
</ul>
'''


def _max_from_scratch(name):
    """Points to reach a skill from an empty tree by the cheapest path, then max its ranks."""
    path = cheapest_path(set(), nodes_named(name)[0])
    c, ranks = skill_cost(name)
    return sum(cost(n) for n in path) + c * (ranks - 1), len(path) - 1


def _stage_has(build, names):
    """First stage label whose planner preset already has every skill in `names` at max rank."""
    for label, budget, _ in STAGES:
        sel = build_preset(build, budget)[0]
        got = {}
        for nid, r in sel.items():
            n = our_name(NODES[nid]["type"])
            got[n] = max(got.get(n, 0), r)
        if all(got.get(n, 0) >= skill_cost(n)[1] for n in names):
            return label, budget
    return None, None


def necromancer_post():
    from content_builds import BUILDS
    NECRO_TIER = next(b["tier"] for b in BUILDS if b["slug"] == "necromancer")
    summon = ["Advanced Necromancy", "Totem Mastery"]
    an_pts, an_steps = _max_from_scratch("Advanced Necromancy")
    tm_pts, tm_steps = _max_from_scratch("Totem Mastery")
    stage, stage_budget = _stage_has("necromancer", summon + ["Necromancer"])
    skills = table(["Skill", "Area / group", "Cost", "Rank 1", "Max rank"], [
        [f"<strong>{n}</strong>", f"{OUR[n][0]} / {OUR[n][1]}", _ranks(n), e(game_text(n, 1)), e(game_text(n))]
        for n in ["Necromancer"] + summon])
    compare = table(["", "Before 1.0", "In 1.0"], [
        ["Where minions come from", "Kills only: the Necromancer skill and the Gem of Lesser Necromancy raise allies from enemies you kill", "Summon spells you cast on demand, plus the old kill-based sources"],
        ["Control", "Random: you can't choose when a minion appears", "Full: you cast skeletons and place totems before or during a fight"],
        ["Skills that raise the cap", "None", f"Advanced Necromancy and Totem Mastery, +3 each at max rank ({_total(summon)} points together)"],
        ["Limits", "Few", "Gem of Lesser Necromancy has a spawn limit, gem companions decay out of combat, and a global cap replaces your oldest creature"],
        ["Viable as a main build?", "No, a bonus on top of a mage build", f'Yes: our <a href="/builds/necromancer/">Necromancer build</a> is {NECRO_TIER}-tier'],
    ])
    core = [k for k in PRESETS["necromancer"] if not k.endswith(" node")]
    return f'''
<p>Before Update 1.0, "necromancer" in Enshrouded meant a mage who sometimes got a free skeleton after a kill. In 1.0 it's a build you can play from start to finish: you cast your minions, you place your totems, and two new skills raise how many you keep out. This post compares the two versions and shows how to skill the new one, with values from the 1.0 game files (build {BUILD_ID}) and quotes from Keen Games' 1.0 changelog.</p>
<p><strong>Short version:</strong> 1.0 added spells that summon Hollow skeletons and three elemental totems, plus <strong>Advanced Necromancy</strong> and <strong>Totem Mastery</strong>, which each add up to 3 more summons for {_total(summon)} points together. It also put limits on the old gem-raised minions. The result is a summoner you control, not one you hope for.</p>
<h2 id="before">Before 1.0: minions were a lucky bonus</h2>
<p>Early Access had two ways to get undead allies, and both depended on kills:</p>
<ul class="dots">
<li><strong>The Necromancer skill</strong> (Mage area, Healer group): {e(game_text("Necromancer", 1))[:-1].lower()} at rank 1, rising to 15% at rank 3. It's still in the tree in 1.0.</li>
<li><strong>Gem of Lesser Necromancy</strong>, a weapon gem: according to the Enshrouded Wiki, killing an enemy while you have no allied unarmored Hollow gives a chance to spawn one. It drops from the Hollow Reaper in the Nomad Highlands Hollow Halls.</li>
</ul>
<p>Neither gave you control. You couldn't call a minion before a boss, and a bad run of kills meant no minions at all. That's why Early Access mage builds generally treated summons as a bonus on top of a Wizard or Healer, not as a build.</p>
<h2 id="after">What 1.0 added for summoners</h2>
<p>The changelog's own summary: "Players can now actively summon skeletons to fight alongside them. They work for free, never complain, and only occasionally get in the way." Among the nine new spell types are a Hollow skeleton summon and Fire, Ice and Shock totems, and every spell now has an Eternal version that doesn't use charges. Keen Games says this, "combined with new 'Necromancy' weapon gems and support skills, allows players to create an impressive amount of undead minions."</p>
<p>The support skills are two new nodes in the Mage area's Wizard group. Here they are next to the old Necromancer skill:</p>
{skills}
<p>Note what they do: they don't add damage. They raise the number of Hollow allies from spells and the number of totems you can have out at once. More bodies on the field means more damage and more targets for enemies that aren't you.</p>
<h2 id="limits">The new limits: summoning isn't unlimited</h2>
<p>1.0 didn't just add minions, it also capped them. From the changelog:</p>
<ul class="dots">
<li><strong>A global creature cap.</strong> "Some of the new spells made it necessary to implement a new feature that counts the currently active creatures spawned by players and enforces a maximum. When players cast more creatures than the allowed maximum, the oldest creature gets replaced."</li>
<li><strong>Gem of Lesser Necromancy</strong> "now has a limit for the resurrected companions it can spawn", which Keen calls necessary because of the new spells and Gems of Necromancy.</li>
<li><strong>Companions from Gems of Necromancy</strong> "start to lose health after a while when out of combat", so you can't carry a gem army from fight to fight.</li>
<li>On the plus side, "the attacks of skeleton companions are no longer interrupted by enemy attacks."</li>
</ul>
<p>In practice: recast before each big fight instead of trying to keep an army alive, and don't overcast. The newest summon pushes out the oldest one.</p>
<h2 id="compare">Necromancer before vs after 1.0</h2>
{compare}
<h2 id="how-to-skill">How to skill a Necromancer in 1.0</h2>
<p>The summon skills are cheap to reach. Starting from an empty tree, maxing Advanced Necromancy costs <strong>{an_pts} points</strong> by the cheapest path ({an_steps} nodes on the way), and Totem Mastery <strong>{tm_pts} points</strong>. Our planner preset already has both of them and the Necromancer skill at max rank by the end of the <strong>{stage.lower()}</strong> stage, within its {stage_budget}-point budget.</p>
<p>The full core of our preset: {", ".join(e(c) for c in core)}. The Trickster nodes Quick Charge and Mana Currents matter more than they look. Summoning is mana-hungry, and shorter charge times get your skeletons and totems out faster at the start of a fight.</p>
<p>Open the <a href="/skill-planner/#b=necromancer&amp;s=1">level 1–15 Necromancer preset</a> in the planner to see the path, or the <a href="/skill-planner/#b=necromancer">full level 50 build</a>. The <a href="/builds/necromancer/">Necromancer build guide</a> has the complete skill order, spells and gear.</p>
<h2 id="should-you-switch">Should you switch to Necromancer?</h2>
<p>If you liked a Wizard or Healer before 1.0 but found solo fights hard because everything ran at you, yes. Minions and totems give you the frontline a mage never had. Expect to manage your mana, and expect your summons to sometimes pull an extra pack. If you want the highest single-target burst, the <a href="/builds/wizard/">Wizard</a> still does more. For the full picture of what changed in the tree, read <a href="/blog/enshrouded-1-0-skill-tree-changes/">what changed in the 1.0 skill tree</a> and our breakdown of <a href="/blog/enshrouded-1-0-new-skills/">all eight new 1.0 skills</a>.</p>
'''


# slug, publish date, title (<=60), description (<=155), H1, body function
POSTS = [
    {"slug": "enshrouded-1-0-new-skills", "date": "2026-10-20",
     "title": "Enshrouded 1.0 New Skills: Ranks, Costs & Who Needs Them",
     "description": "All 8 new combat skills in Enshrouded 1.0 with point costs and per-rank values from the game files, plus which builds should take each one.",
     "h1": "Enshrouded 1.0 New Skills: Every Rank, Cost and Who Should Take Them",
     "summary": "All eight new 1.0 combat skills with costs and per-rank values from the game files, and which builds should take them.",
     "body": new_skills_post},
    {"slug": "enshrouded-1-0-skill-tree-changes", "date": "2026-10-21",
     "title": "Enshrouded 1.0 Skill Tree Changes: Points, Roots & Moves",
     "description": "What changed in the Enshrouded 1.0 skill tree: the reset, level 50, 18 new Shroud Roots, 212 skill points, moved dagger skills and the Shroud time nerf.",
     "h1": "What Changed in the Enshrouded 1.0 Skill Tree",
     "summary": "The reset, level 50, 18 new Shroud Roots and 212 skill points, the dagger move, re-priced skills and the Shroud time nerf, with numbers from the game files.",
     "body": tree_changes_post},
    {"slug": "enshrouded-necromancer-before-after-1-0", "date": "2026-10-22",
     "title": "Enshrouded Necromancer Before vs After 1.0: What Changed",
     "description": "How the Enshrouded Necromancer changed in 1.0: summon spells, Advanced Necromancy and Totem Mastery, the new creature cap, and how to skill it now.",
     "h1": "Enshrouded Necromancer: Before and After Update 1.0",
     "summary": "From lucky skeletons on kills to a summoner you control: the new summon spells and skills, the 1.0 creature cap, and how to skill a Necromancer now.",
     "body": necromancer_post},
]
