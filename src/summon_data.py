"""Enshrouded 1.0 summon spells, from the Enshrouded Wiki spell pages (checked October 25, 2026).
Skill values are not here: they come from the game export via tree_data."""

WIKI = "https://enshrouded.wiki.gg/wiki/"

# name, kind, level, rarity, mana, damage, duration (s), extra effect, crafter, workshop, ingredients, output
SPELLS = [
    ("Hollow Wretch I", "skeleton", 17, "Common", 102, 35, 60, "", "Collector", "",
     [("Ectoplasm Fragment", 20), ("Bones", 50)], 100),
    ("Eternal Hollow Wretch I", "skeleton", 28, "Epic", 203, 52, 80, "", "Collector", "",
     [("Ectoplasm Crystal", 60), ("Giant Bones", 4)], 1),
    ("Hollow Wretch II", "skeleton", 44, "Common", 231, 76, 100, "", "Collector", "",
     [("Ectoplasm Cluster", 20), ("Icy Giant Bones", 1)], 100),
    ("Eternal Hollow Wretch II", "skeleton", 45, "Legendary", 272, 77, 120, "", "Collector", "",
     [("Ectoplasm Aggregate", 100), ("Icy Giant Bones", 3), ("Diamond Dust", 2), ("Archaic Core", 2)], 1),
    ("Fire Totem I", "fire", 17, "Common", 37, 20, 8, "Explodes when it expires", "Alchemist", "Alchemy Station",
     [("Charcoal", 10), ("Bronze Bars", 1), ("Amber", 5), ("Straw", 2)], 20),
    ("Eternal Fire Totem I", "fire", 28, "Epic", 74, 30, 9, "Explodes when it expires", "Alchemist", "Laboratory",
     [("Obsidian", 15), ("Coal", 15), ("Raw Wool", 10), ("Amethyst", 20)], 1),
    ("Eternal Fire Totem II", "fire", 45, "Legendary", 99, 45, 10, "Explodes when it expires", "Alchemist", "Laboratory",
     [("Charcoal", 25), ("Diamond", 20), ("Fish Scales", 4), ("Magma Gel", 25)], 1),
    ("Ice Totem I", "ice", 17, "Common", 26, 19, 8, "50% slow for 5s", "Alchemist", "Alchemy Station",
     [("Shroud Adhesive", 3), ("Tin Bars", 1)], 20),
    ("Eternal Ice Totem I", "ice", 20, "Epic", 36, 22, 9, "50% slow for 5s", "Alchemist", "Laboratory",
     [("Iron Bars", 5), ("Enshrouded Oil", 5), ("Lapislazuli", 15)], 1),
    ("Ice Totem II", "ice", 38, "Common", 58, 37, 10, "50% slow for 5s", "Alchemist", "Laboratory",
     [("Aquamarine Dust", 2), ("Shroud Sludge", 2), ("Mother-Of-Pearl", 5)], 20),
    ("Eternal Ice Totem II", "ice", 45, "Legendary", 70, 43, 11, "50% slow for 5s", "Alchemist", "Laboratory",
     [("Diamond Dust", 30), ("Ice", 30), ("Celestium Bars", 15)], 1),
    ("Shock Totem I", "shock", 17, "Common", 19, 17, 8, "Stamina damage 20 + 1.5 × Intelligence", "Alchemist", "Alchemy Station",
     [("Bonemeal", 4), ("Tin Bars", 1), ("Calla Luna", 2)], 20),
    ("Shock Totem II", "shock", 38, "Common", 41, 34, 9, "Stamina damage 20 + 1.5 × Intelligence", "Alchemist", "Laboratory",
     [("Shroud Sludge", 5), ("Iron Dust", 1), ("Gold Bars", 1), ("Green Vitriol Dust", 1)], 20),
    ("Eternal Shock Totem", "shock", 45, "Legendary", 50, 39, 10, "Stamina damage 20 + 1.5 × Intelligence", "Alchemist", "Laboratory",
     [("Sparkling Dust", 25), ("Moonstone Dust", 10), ("Celestium Bars", 15), ("Magma Gel", 20)], 1),
]


def wiki_url(name):
    return WIKI + name.replace(" ", "_")
