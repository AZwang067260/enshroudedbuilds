"""Eternal arrows in Enshrouded 1.0, from the Enshrouded Wiki item pages (checked October 27, 2026).
The wiki's Arrows page: "Eternal Arrows cost mana to shoot, but are not consumed when used." """

WIKI = "https://enshrouded.wiki.gg/wiki/"
ARROWS_PAGE = WIKI + "Arrows"

# name, element, level, rarity, how to get
ETERNAL_ARROWS = [
    ("Eternal Frost Arrow I", "Ice", 9, "Rare", "Quest reward: the Bard's quest Eternally Piercing sends you to the Hermit Camp in the Blackmire"),
    ("Eternal Ember Arrow I", "Fire", 15, "Rare", "Hunter: 20 Alchemical Base, 20 Glow Dust, 15 Fossilized Bone Dust"),
    ("Eternal Voltaic Arrow I", "Shock", 20, "Rare", "Hunter: 20 Glass, 25 Sulfur, 15 Spice"),
    ("Eternal Ember Arrow II", "Fire", 28, "Epic", "Hunter: 25 Flammable Goo, 15 Silver Dust, 15 Mauveine"),
    ("Eternal Frost Arrow II", "Ice", 29, "Epic", "Hunter: 25 Ice, 15 Steel Bars, 1 Enshrouded Cyclops Eye (the eye unlocks the recipe)"),
    ("Eternal Voltaic Arrow II", "Shock", 36, "Epic", "Hunter: 15 Aquamarine Dust, 15 Gleam Root Dust, 10 Iron Dust"),
    ("Eternal Giant Bone Arrow I", "Bone", 36, "Epic", "Collector: 100 Giant Bone Arrow IV, 10 Ectoplasm Cluster, 1 Icy Giant Bones"),
    ("Eternal Ember Arrow III", "Fire", 45, "Legendary", "Hunter: 2 Archaic Infusion, 15 Sparkling Dust, 25 Magma Gel"),
    ("Eternal Frost Arrow III", "Ice", 45, "Legendary", "Hunter: 25 Ice, 15 Celestium Bars, 2 Archaic Core"),
    ("Eternal Voltaic Arrow III", "Shock", 45, "Legendary", "Hunter: 2 Archaic Infusion, 15 Sparkling Dust, 15 Celestium Bars"),
    ("Eternal Giant Bone Arrow II", "Bone", 45, "Legendary", "Collector: 100 Ectoplasm Aggregate, 3 Icy Giant Bones, 2 Archaic Core"),
]


def wiki_url(name):
    return WIKI + name.replace(" ", "_")
