"""Base stats of the main 1.0 damage and utility spells, from the Enshrouded Wiki spell pages (checked October 26, 2026).
Summon spells live in summon_data.py."""

WIKI = "https://enshrouded.wiki.gg/wiki/"

# name, level, cast time (s), mana, damage, what it does, crafter, workshop
SPELLS = {
    "Fireball I": (10, 2.5, 53, 94, "Fire projectile that explodes on impact (2.6 m radius)", "Alchemist", ""),
    "Pillar Of Flames I": (12, 1.25, 54, 14, "Burning area for 4.5 s; burn debuff for 9 s", "Alchemist", "Mortar"),
    "Chain Lightning I": (12, 1.2, 65, 64, "Shock strike that jumps to nearby enemies and deals Stamina damage", "Alchemist", "Mortar"),
    "Blizzard I": (15, 2.0, 84, 9, "3 m storm for 9 s that damages and slows enemies by 50%", "Alchemist", ""),
    "Ball Lightning I": (20, 3.0, 99, 131, "Slow ball that passes through enemies for 6 s, striking everything within 4 m", "Alchemist", "Laboratory"),
    "Mana Drain I": (3, 0.5, 0, 0, "Beam that drains Mana from enemies (7 per pulse), no damage", "Hand-crafted", ""),
}


def wiki_url(name):
    return WIKI + name.replace(" ", "_")
