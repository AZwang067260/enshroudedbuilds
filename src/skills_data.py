"""Enshrouded 1.0 skill list used by the skill planner and the skills table.

Each skill: (name, ranks, cost per rank, effect at max rank, flags). Flags: "new" = added in 1.0,
"disputed" = sources disagree on the value. Values come from community planners built from the
1.0 game files (build 1267041), cross-checked where a second 1.0 source exists. Keen Games does not
publish these numbers, so the in-game tooltip always wins.
"""

# area -> [(group, [skills])]
TREE = [
    ("Core", [
        ("Core", [
            ("Merciless Attack", 1, 2, "+500% damage against overpowered (stunned) enemies. Not with wands, staves or bows.", ""),
            ("Sneak Attack", 1, 3, "+900% damage against unaware enemies. Not with wands, staves or bows.", ""),
            ("Double Jump", 1, 2, "A second jump in mid-air (10 stamina).", ""),
            ("Airborne Architect", 1, 3, "Fly freely in first person while building inside your base.", "new"),
            ("Snap", 1, 2, "Merciless Attacks restore 20% mana.", ""),
            ("Power Parry", 3, 1, "+30% parry power.", ""),
            ("Opportunity", 3, 1, "Bigger Merciless Attack multiplier.", "disputed"),
            ("Saviour", 3, 1, "Revive allies 3 s faster (default 6 s).", ""),
            ("Inner Fires", 3, 1, "+3 min time in the Shroud.", ""),
            ("Giant Slayer Hook", 1, 3, "Grapple onto large enemies in combat.", ""),
            ("Grounding Hook", 1, 4, "Grapple onto flying enemies.", ""),
            ("Felling Axe Specialization", 1, 2, "Unlocks the felling axe special ability.", ""),
            ("Pickaxe Specialization", 1, 2, "Unlocks the pickaxe special ability.", ""),
            ("Quality Gear", 1, 1, "Tools have a 20% chance to restore 1 durability on hit.", ""),
            ("Miner", 1, 2, "10% chance of an extra resource when mining.", ""),
            ("Lumberjack", 3, 1, "+30% damage to wood.", ""),
            ("Mason", 3, 1, "+30% damage to stone.", ""),
            ("Prospector", 3, 1, "+30% damage to metal.", ""),
            ("Well Rested", 3, 1, "Longer Rested buff.", "disputed"),
            ("Fisherman's Resolve", 3, 1, "More fishing endurance.", "disputed"),
        ]),
    ]),
    ("Mage", [
        ("Wizard", [
            ("Intelligence node", 11, 1, "+1 Intelligence each (+5% magic damage per point).", "attr:int"),
            ("Wizard", 3, 2, "+6% wand and staff crit chance.", ""),
            ("Mage Apprentice", 3, 1, "+15% wand and staff damage.", ""),
            ("Arsonist", 3, 2, "+30% fire damage.", ""),
            ("Iceman", 3, 2, "+30% ice damage.", ""),
            ("Thunder", 3, 2, "+30% shock damage.", ""),
            ("Dark Arts", 3, 2, "+30% Shroud damage.", ""),
            ("Frost", 3, 2, "Melee attackers are slowed for 9 s.", ""),
            ("Bone to Ash", 3, 1, "+15% damage against Hollow enemies.", ""),
            ("Chain Hit", 1, 3, "Hits jump to a second enemy within 15 m (5 shock per Intelligence).", ""),
            ("Mass Destruction", 1, 3, "2 shock per Intelligence to every enemy within 15 m of the target.", ""),
            ("Radiant Aura", 3, 1, "Nearby Fell enemies take fire damage every second (scales with Intelligence).", ""),
            ("Fire Resistance", 3, 1, "+15% fire resistance.", ""),
            ("Ice Resistance", 3, 1, "+15% ice resistance.", ""),
            ("Shock Resistance", 3, 1, "+15% shock resistance.", ""),
            ("Advanced Necromancy", 3, 2, "+3 Hollow skeleton cap (+1 per rank).", "new"),
            ("Totem Mastery", 3, 2, "+3 totem cap (+1 per rank).", "new"),
        ]),
        ("Healer", [
            ("Spirit node", 11, 1, "+1 Spirit each (+20 max mana per point).", "attr:spi"),
            ("Healer", 3, 1, "+45% healing from spells and Water Aura.", "disputed"),
            ("Water Aura", 3, 1, "Heals you and allies within 15 m (1 health per 2 Intelligence).", ""),
            ("Waters of Life", 1, 2, "Doubles Water Aura healing.", ""),
            ("Healing Revive", 3, 1, "Revived allies get 24% health (default 10%).", ""),
            ("Life Essences", 3, 1, "Max health +9 per point of Intelligence.", "disputed"),
            ("Necromancer", 3, 1, "Magic-weapon kills have a 15% chance to summon a skull.", ""),
            ("Righteous Fire", 3, 2, "60% of your healing also burns nearby Fell enemies.", ""),
            ("Shared Misery", 3, 2, "Spreads debuff damage to nearby enemies.", "disputed"),
            ("Shroud Mitigation", 3, 1, "Magic hits can restore Shroud time for you and allies.", ""),
            ("Shroud Resistance", 3, 1, "+15% Shroud resistance.", ""),
            ("Blink", 1, 4, "Your dodge becomes a short teleport (20 stamina).", ""),
            ("Emergency Blink", 1, 2, "Blink while stunned to break the stun.", ""),
            ("Divine Surge", 1, 4, "Healing spells can crit.", ""),
        ]),
        ("Battlemage", [
            ("Wand Mastery", 3, 1, "+15% wand damage.", ""),
            ("Wand Specialization", 1, 3, "Unlocks wand special abilities (Focus).", ""),
            ("Unity", 3, 1, "Wand hits have a 30% chance to restore 6% max mana.", "disputed"),
            ("Sting", 1, 3, "+20% damage from repeated wand hits.", ""),
            ("Eternal Spark", 3, 1, "Wand hits have a 45% chance to restore 1 durability.", ""),
            ("Arcane Deflection", 3, 1, "Parrying restores 30 mana.", ""),
            ("Arcane Proliferation", 1, 3, "30% chance to double wand projectiles (extra ones deal 50% less).", ""),
            ("Blink Attack", 1, 2, "Blinking into an enemy causes a fire burst (scales with Intelligence).", ""),
            ("Evasion Attack", 1, 4, "Melee dash during an evade for +50% weapon damage.", ""),
            ("Life Burst", 1, 4, "Magic-weapon kills heal nearby players (scales with Intelligence).", ""),
            ("Exalted", 1, 5, "+1 Intelligence per 2 Flame levels.", "flame:int"),
            ("Aerial Wand Attack", 1, 3, "Mid-air shot that explodes on impact for +50% weapon damage.", "new"),
            ("Wand Evasion Attack", 1, 4, "Dodging fires a piercing wand disc.", "new"),
        ]),
        ("Trickster", [
            ("Arcane Concentration", 1, 5, "+1 Spirit per 2 Flame levels.", "flame:spi"),
            ("Blast and Cast", 1, 3, "A wand crit gives your next staff attack +50% base damage within 10 s.", "new"),
            ("Quick Charge", 3, 1, "-30% spell charge time.", ""),
            ("Mana Currents", 3, 1, "+15 base mana regeneration.", ""),
            ("Spellslinger", 3, 1, "+15% staff damage.", ""),
            ("Terror", 3, 2, "Spell crits have a 60% chance to stun for 2 s.", ""),
            ("Bloodletting", 3, 2, "Spell crits can drop resource orbs.", "disputed"),
            ("Counterstrike", 3, 1, "24% chance to reflect 60% of damage taken as fire.", ""),
            ("Blood Magic", 1, 4, "Below 20% mana, converts health into mana (2 min cooldown).", ""),
            ("Begone!", 1, 3, "Mana-powered stun punch replaces unarmed attacks.", ""),
            ("Sleight of Hand", 3, 1, "+90% unarmed damage.", ""),
        ]),
    ]),
    ("Warrior", [
        ("Tank", [
            ("Constitution node", 11, 1, "+1 Constitution each (+50 max health per point).", "attr:con"),
            ("Thick Skin", 1, 5, "+1 Constitution per 2 Flame levels.", "flame:con"),
            ("Heavy Plates", 3, 1, "+12% physical armor from gear.", ""),
            ("Shiny Plates", 3, 1, "+12% magical armor from gear.", ""),
            ("Tower", 1, 3, "+10% physical resistance with 3+ enemies within 20 m.", ""),
            ("Warden", 1, 3, "+10% magical resistance with 3+ enemies within 20 m.", ""),
            ("Nemesis", 3, 2, "+30% threat from enemies.", ""),
            ("Earth Aura", 3, 2, "+10% physical and magical resistance for nearby allies (12 m).", ""),
            ("Martyr", 1, 3, "If you die, allies within 30 m heal 50% and get +100 max health for 15 min.", ""),
            ("Veteran", 3, 2, "+6% melee and dagger crit chance.", ""),
            ("Absorb", 3, 1, "12% chance on magic damage taken to restore mana.", ""),
            ("Purification", 3, 1, "Melee kills of Shroud enemies add 9 s of Shroud time.", ""),
            ("Soul Leech", 3, 2, "Melee kills restore 45 mana to players within 15 m.", ""),
        ]),
        ("Warrior", [
            ("Strength node", 11, 1, "+1 Strength each (+5% melee damage per point).", "attr:str"),
            ("The Warrior's Path", 3, 1, "+15% damage with one-handed axes, clubs and swords.", ""),
            ("Slasher", 3, 2, "+30% melee cutting damage.", ""),
            ("Swift Blades", 1, 4, "+15% one-handed attack speed.", ""),
            ("One-Handed Specialization", 1, 3, "Unlocks one-handed special abilities.", ""),
            ("Battle Heal", 3, 2, "Melee crits heal a share of your max health.", "disputed"),
            ("Bash", 3, 2, "Parries bash the enemy for blunt damage (scales with Strength).", ""),
            ("Breach", 1, 3, "Overpowered enemies take +100% melee physical damage for 3 s.", ""),
            ("Heavy Handed", 3, 1, "Fill a blocking enemy's stun bar 30% faster.", ""),
            ("Shockwave", 1, 3, "Parries and overpowers knock back nearby enemies.", ""),
        ]),
        ("Barbarian", [
            ("Barbarian", 1, 5, "+1 Strength per 2 Flame levels.", "flame:str"),
            ("Barbarian's Path", 3, 1, "+15% damage with two-handed axes, clubs and hammers.", ""),
            ("Titan Edge", 3, 1, "+15% greatsword damage.", "disputed"),
            ("Brute", 3, 2, "+30% melee blunt damage.", ""),
            ("Heavy Hitter", 1, 4, "+10% two-handed attack speed.", ""),
            ("Blood Rage", 3, 2, "A melee kill within 15 m gives +15% melee damage for 10 s.", ""),
            ("Relentless", 1, 5, "Two-handed crits give +8% crit chance on the next hit.", ""),
            ("Two-Handed Specialization", 1, 3, "Unlocks two-handed special abilities.", ""),
            ("Whirlwind Crescendo", 1, 3, "Two-handed combo finisher becomes a whirl attack.", ""),
            ("Steadfast", 3, 2, "Melee kills restore 3 durability.", ""),
        ]),
        ("Athlete", [
            ("Athlete", 3, 1, "Max health +9 per point of Strength.", ""),
            ("Vigorous Deflection", 3, 1, "Parrying restores 45 stamina.", ""),
            ("Crash Down Attack", 1, 3, "Slam from a jump: +50% weapon damage in an area.", ""),
            ("Crash Down: Force", 1, 3, "Crash Down from a double jump deals +20% damage.", ""),
            ("Upwards Slash Attack", 1, 3, "Upward strike while jumping, for flying enemies.", ""),
            ("Blood Warrior", 1, 3, "Sneak or Merciless Attack kills drop a health orb.", ""),
            ("Finesse", 3, 1, "One-handed weapons and daggers can restore durability on hit.", ""),
            ("Splash Dash", 1, 3, "Evasive dash while swimming.", ""),
            ("Wet Dog", 1, 3, "Wet and Soaked penalty reduced to 20%.", ""),
            ("Soaked Dog", 1, 3, "Wet and Soaked penalty reduced to 10%.", ""),
        ]),
    ]),
    ("Ranger", [
        ("Ranger", [
            ("Dexterity node", 7, 1, "+1 Dexterity each (+5% bow and dagger damage per point).", "attr:dex"),
            ("Ranger", 3, 2, "+3 Dexterity and +3 Endurance in total.", "attr:ranger"),
            ("Marksman", 3, 1, "+15% bow damage.", ""),
            ("Sniper", 3, 2, "+6% bow crit chance.", ""),
            ("Puncture", 3, 2, "+30% ranged piercing damage.", "new"),
            ("Barrage", 3, 1, "Bow hits have a 45% chance to restore 1 durability.", "new"),
            ("Skill Shot", 3, 1, "+60% weak-point damage.", ""),
            ("Fatal Precision", 3, 1, "More crit chance and crit damage.", "disputed"),
            ("Bow Specialization", 1, 3, "Unlocks bow special abilities.", ""),
            ("Blessed Arrows", 3, 1, "Bow crits restore up to 24 mana.", ""),
            ("Counter Battery", 3, 1, "+24% damage against ranged enemies.", ""),
            ("Multi Shot", 1, 4, "Regular arrows have a 20% chance to fire a flurry.", ""),
            ("Multi Shot Spread", 1, 3, "25% chance of an extra arrow in the flurry.", ""),
            ("Multi Shot Trigger", 1, 3, "Special arrows also trigger the flurry.", ""),
            ("Shrapnel Blast", 1, 3, "+10% explosive arrow damage per target hit.", ""),
            ("Echoing Explosives", 1, 4, "40% chance of a secondary explosion.", ""),
            ("Eagle's Bane", 3, 1, "+30% damage against flying enemies.", ""),
            ("Vitality Surge", 3, 1, "Bow, dagger and throwable crits restore 9 stamina.", ""),
            ("Cutthroat", 3, 1, "+300% Sneak Attack damage.", ""),
            ("Silent Stride", 3, 1, "Move faster while sneaking.", "disputed"),
        ]),
        ("Assassin", [
            ("Graceful Stride", 1, 5, "+1 Dexterity per 2 Flame levels.", "flame:dex"),
            ("Dagger Mastery", 3, 1, "+15% dagger damage.", ""),
            ("Dagger Specialization", 1, 3, "Unlocks dagger special abilities.", ""),
            ("Backstab Mastery", 3, 1, "+60% backstab damage.", ""),
            ("Expose Weakness", 1, 4, "Dagger crits: target takes +25% physical damage for 5 s.", ""),
            ("Thrust", 3, 2, "+30% melee piercing damage.", ""),
            ("Venomous Blades", 1, 2, "Raises the dagger poison chance to 30%.", ""),
            ("Venom Mastery", 1, 3, "Doubles Venomous Blades damage.", ""),
            ("Slice And Dice", 1, 3, "A dagger crit gives your next bow shot +50% base damage within 10 s.", ""),
            ("Veiled Vigor", 3, 1, "Max health +9 per point of Dexterity.", ""),
            ("Vile Concoction", 3, 1, "+36% throwable damage.", ""),
            ("Shell Shock", 1, 3, "Explosive ranged attacks stun for 2 s.", ""),
            ("Airborne", 3, 1, "Your glider uses 36% less stamina.", ""),
            ("Updraft", 1, 4, "Jump while gliding to gain lift once per flight.", ""),
            ("Quick Reflex Block", 1, 3, "Dagger blocks get a brief block boost.", ""),
        ]),
        ("Beastmaster", [
            ("Beast Master", 1, 4, "Wild animals within 50 m attack whoever targets you.", ""),
            ("Calm Spirit", 1, 3, "Wild animals within 50 m stay passive unless provoked.", ""),
            ("Vukah Language", 1, 3, "Vukah within 50 m stay passive unless provoked.", ""),
            ("Vukah Culture", 1, 4, "Vukah within 50 m attack whoever targets you.", ""),
            ("Cull the Herd", 3, 1, "+15% damage against wildlife.", ""),
            ("Primal Force", 3, 1, "+15% damage against Vukah.", ""),
            ("Snake Eater", 3, 2, "+12% poison resistance.", ""),
            ("Mithridatist", 1, 2, "25% chance to avoid being poisoned.", ""),
            ("Bee Sting", 1, 3, "Aiming a bow in mid-air slows your fall.", ""),
            ("Eagle Eye", 1, 3, "Much greater bow zoom.", ""),
            ("Bounty Bonanza", 1, 2, "+5 XP for the group when a Skillshot kills a Fell enemy.", ""),
            ("Endurance of the Flame", 1, 5, "+1 Endurance per 2 Flame levels.", "flame:end disputed"),
        ]),
        ("Survivor", [
            ("Endurance node", 8, 1, "+1 Endurance each (+10 max stamina per point).", "attr:end"),
            ("Survival Instinct", 3, 1, "Bow or dagger kills of Shroud enemies restore 9 s of Shroud time.", "new"),
            ("Runner", 3, 1, "+15% sprint speed and -15% sprint stamina cost.", ""),
            ("Rebound", 3, 2, "+30% base stamina regeneration.", ""),
            ("Arachnoid", 3, 1, "-60% stamina cost while climbing.", ""),
            ("Swiftshot Sustenance", 3, 1, "Bow kills have a 36% chance to drop a stamina orb.", ""),
            ("Wanderlust", 1, 3, "Cheaper sprinting on roads.", ""),
            ("Good Metabolism", 1, 3, "Orbs restore 30% (up from 10%); potions restore 20% more.", ""),
            ("Sweet Tooth", 1, 3, "+50% stamina regeneration from sweets.", ""),
            ("Dessert Stomach", 1, 4, "+1 food slot.", ""),
            ("Last Meal", 1, 5, "Food buffs survive death at half duration.", ""),
            ("Kick", 1, 3, "Attack while blocking to kick.", ""),
            ("Strategic Maneuver", 1, 1, "Sideways dodge roll while locked on.", ""),
        ]),
    ]),
]


def slug(name):
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-").replace("--", "-")


def flat():
    """[(area, group, name, ranks, cost, effect, flags, id)] in tree order."""
    return [(area, group, *sk, slug(sk[0])) for area, groups in TREE for group, skills in groups for sk in skills]


# Planner presets: skill name -> ranks, matching the level 50 path on each build page
PRESETS = {
    "wizard": {"Intelligence node": 11, "Spirit node": 8, "Constitution node": 4, "Wizard": 3, "Mage Apprentice": 3, "Wand Specialization": 1, "Wand Mastery": 3,
               "Blink": 1, "Unity": 3, "Arcane Deflection": 3, "Chain Hit": 1, "Arsonist": 3, "Quick Charge": 3, "Mass Destruction": 1,
               "Blast and Cast": 1, "Aerial Wand Attack": 1, "Wand Evasion Attack": 1, "Spellslinger": 3, "Exalted": 1, "Radiant Aura": 3, "Double Jump": 1},
    "battlemage": {"Intelligence node": 11, "Constitution node": 8, "Spirit node": 4, "Mage Apprentice": 3, "Wand Specialization": 1, "Wand Mastery": 3,
                   "Arcane Proliferation": 1, "Sting": 1, "Unity": 3, "Arcane Deflection": 3, "Life Burst": 1, "Chain Hit": 1, "Wand Evasion Attack": 1,
                   "Aerial Wand Attack": 1, "Blink": 1, "Blast and Cast": 1, "Wizard": 3, "Exalted": 1, "Power Parry": 3, "Double Jump": 1},
    "necromancer": {"Intelligence node": 11, "Spirit node": 11, "Constitution node": 3, "Wizard": 3, "Mage Apprentice": 3, "Wand Mastery": 3,
                    "Advanced Necromancy": 3, "Totem Mastery": 3, "Necromancer": 3, "Quick Charge": 3, "Mana Currents": 3, "Unity": 3,
                    "Life Burst": 1, "Chain Hit": 1, "Bone to Ash": 3, "Arcane Concentration": 1, "Blink": 1, "Double Jump": 1},
    "healer": {"Spirit node": 11, "Intelligence node": 9, "Constitution node": 4, "Healer": 3, "Water Aura": 3, "Wand Mastery": 3, "Waters of Life": 1,
               "Healing Revive": 3, "Saviour": 3, "Unity": 3, "Life Burst": 1, "Divine Surge": 1, "Life Essences": 3, "Righteous Fire": 3,
               "Totem Mastery": 3, "Blink": 1, "Double Jump": 1},
    "warrior": {"Strength node": 11, "Constitution node": 9, "Endurance node": 4, "The Warrior's Path": 3, "Battle Heal": 3, "Veteran": 3, "Swift Blades": 1,
                "Vigorous Deflection": 3, "One-Handed Specialization": 1, "Slasher": 3, "Blood Rage": 3, "Merciless Attack": 1, "Power Parry": 3,
                "Heavy Plates": 3, "Bash": 3, "Double Jump": 1},
    "tank": {"Constitution node": 11, "Strength node": 8, "Endurance node": 4, "Heavy Plates": 3, "Battle Heal": 3, "Shiny Plates": 3, "Tower": 1,
             "Thick Skin": 1, "Nemesis": 3, "Warden": 1, "Martyr": 1, "Earth Aura": 3, "Merciless Attack": 1, "Absorb": 3, "Vigorous Deflection": 3,
             "Power Parry": 3, "The Warrior's Path": 3, "Double Jump": 1},
    "barbarian": {"Strength node": 11, "Constitution node": 9, "Endurance node": 5, "Barbarian's Path": 3, "Brute": 3, "Battle Heal": 3, "Heavy Hitter": 1,
                  "Two-Handed Specialization": 1, "Blood Rage": 3, "Merciless Attack": 1, "Barbarian": 1, "Relentless": 1, "Veteran": 3,
                  "Whirlwind Crescendo": 1, "Double Jump": 1},
    "ranger": {"Dexterity node": 7, "Constitution node": 6, "Endurance node": 6, "Ranger": 3, "Marksman": 3, "Bow Specialization": 1, "Skill Shot": 3,
               "Sniper": 3, "Puncture": 3, "Blessed Arrows": 3, "Fatal Precision": 3, "Multi Shot": 1, "Barrage": 3, "Survival Instinct": 3,
               "Graceful Stride": 1, "Double Jump": 1},
    "assassin": {"Dexterity node": 7, "Endurance node": 8, "Constitution node": 4, "Dagger Mastery": 3, "Sneak Attack": 1, "Dagger Specialization": 1,
                 "Backstab Mastery": 3, "Cutthroat": 3, "Expose Weakness": 1, "Graceful Stride": 1, "Venomous Blades": 1, "Venom Mastery": 1,
                 "Slice And Dice": 1, "Survival Instinct": 3, "Veiled Vigor": 3, "Airborne": 3, "Ranger": 3, "Double Jump": 1},
}

# Extra picks used to fill each preset up to the level 50 budget, in priority order
FILL = {
    "wizard": ["Constitution node", "Spirit node", "Mana Currents", "Iceman", "Thunder", "Fire Resistance", "Shock Resistance", "Ice Resistance",
               "Emergency Blink", "Terror", "Counterstrike", "Bone to Ash", "Arcane Concentration", "Dark Arts", "Frost", "Bloodletting", "Shroud Resistance"],
    "battlemage": ["Constitution node", "Spirit node", "Eternal Spark", "Blink Attack", "Mana Currents", "Quick Charge", "Thunder", "Arsonist",
                   "Fire Resistance", "Shock Resistance", "Ice Resistance", "Emergency Blink", "Heavy Plates", "Shiny Plates", "Bone to Ash", "Radiant Aura", "Shroud Resistance"],
    "necromancer": ["Constitution node", "Arsonist", "Iceman", "Thunder", "Mass Destruction", "Exalted", "Emergency Blink", "Healer", "Water Aura",
                    "Fire Resistance", "Shock Resistance", "Ice Resistance", "Radiant Aura", "Shroud Resistance", "Shroud Mitigation", "Spellslinger"],
    "healer": ["Constitution node", "Intelligence node", "Shroud Mitigation", "Mana Currents", "Quick Charge", "Necromancer", "Emergency Blink", "Arcane Concentration",
               "Shroud Resistance", "Fire Resistance", "Ice Resistance", "Shock Resistance", "Earth Aura", "Arsonist", "Exalted", "Advanced Necromancy"],
    "warrior": ["Constitution node", "Endurance node", "Breach", "Heavy Handed", "Shockwave", "Shiny Plates", "Tower", "Warden", "Athlete", "Thick Skin",
                "Brute", "Opportunity", "Snap", "Finesse", "Upwards Slash Attack", "Crash Down Attack", "Steadfast", "Earth Aura"],
    "tank": ["Strength node", "Endurance node", "Thick Skin", "Bash", "Shockwave", "Heavy Handed", "Purification", "Soul Leech", "Veteran", "Athlete",
             "Swift Blades", "One-Handed Specialization", "Opportunity", "Snap", "Saviour", "Breach", "Slasher"],
    "barbarian": ["Constitution node", "Endurance node", "Titan Edge", "Steadfast", "Athlete", "Heavy Handed", "Breach", "Opportunity", "Power Parry",
                  "Crash Down Attack", "Crash Down: Force", "Upwards Slash Attack", "Heavy Plates", "Thick Skin", "Slasher", "Rebound", "Runner"],
    "ranger": ["Constitution node", "Endurance node", "Counter Battery", "Eagle's Bane", "Vitality Surge", "Multi Shot Spread", "Multi Shot Trigger",
               "Shrapnel Blast", "Echoing Explosives", "Rebound", "Runner", "Swiftshot Sustenance", "Dagger Mastery", "Slice And Dice", "Bee Sting", "Eagle Eye", "Arachnoid"],
    "assassin": ["Constitution node", "Thrust", "Vitality Surge", "Quick Reflex Block", "Updraft", "Marksman", "Sniper", "Fatal Precision", "Silent Stride",
                 "Bow Specialization", "Skill Shot", "Rebound", "Runner", "Vile Concoction", "Shell Shock", "Finesse", "Arachnoid"],
}


def preset(build, budget=212):
    """Core picks for a build plus FILL extras (rank by rank) until the point budget is used."""
    info = {f[2]: f for f in flat()}
    picks = dict(PRESETS[build])
    spent = sum(info[n][4] * r for n, r in picks.items())
    area = {"wizard": "Mage", "battlemage": "Mage", "necromancer": "Mage", "healer": "Mage", "warrior": "Warrior", "tank": "Warrior",
            "barbarian": "Warrior", "ranger": "Ranger", "assassin": "Ranger"}[build]
    rest = [f[2] for f in flat() if f[0] == area and f[2] not in FILL[build] and "Specialization" not in f[2]]
    rest += [f[2] for f in flat() if f[0] == "Core" and f[2] not in FILL[build] and "Specialization" not in f[2]]
    for name in FILL[build] + rest:
        ranks, cost = info[name][3], info[name][4]
        while picks.get(name, 0) < ranks and spent + cost <= budget:
            picks[name] = picks.get(name, 0) + 1
            spent += cost
    return picks, spent
