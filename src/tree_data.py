"""Skill tree graph for the planner, built from the vendored GPL-3.0 game export (src/vendor/enshrouded-skill-tree).

SPDX-License-Identifier: GPL-3.0-or-later
"""
import heapq
import json
import os

from skills_data import FILL, PRESETS, flat

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor", "enshrouded-skill-tree")
RAW = json.load(open(os.path.join(VENDOR, "gameSkillData.json"), encoding="utf-8"))
PROGRESSION = json.load(open(os.path.join(VENDOR, "gameProgression.json"), encoding="utf-8"))
BUILD_ID = RAW["provenance"]["gameBuild"].split("|")[0]

BIOMES = [("springlands", "Springlands"), ("revelwood", "Revelwood"), ("nomad_highlands", "Nomad Highlands"),
          ("kindlewastes", "Kindlewastes"), ("albaneve_summits", "Albaneve Summits"), ("veilwater_basin", "Veilwater Basin"),
          ("cinders_cradle", "Cinder's Cradle")]

# names in the export that differ cosmetically from skills_data
ALIASES = {"Warrior's Path": "The Warrior's Path", "Waters Of Life": "Waters of Life", "Fisherman’s Resolve": "Fisherman's Resolve",
           "Constitution": "Constitution node", "Dexterity": "Dexterity node", "Endurance": "Endurance node",
           "Intelligence": "Intelligence node", "Spirit": "Spirit node", "Strength": "Strength node"}

OUR = {f[2]: f for f in flat()}  # name -> (area, group, name, ranks, cost, effect, flags, id)


def our_name(type_key):
    name = RAW["types"][type_key]["name"]
    return ALIASES.get(name, name)


NODES = {nid: n for nid, n in RAW["nodes"].items()}
ADJ = {nid: set() for nid in NODES}
for a, b in RAW["edges"]:
    ADJ[a].add(b)
    ADJ[b].add(a)


def cost(nid):
    return RAW["types"][NODES[nid]["type"]]["cost"]


def max_rank(nid):
    return RAW["types"][NODES[nid]["type"]].get("maxLevel", 1)


def nodes_named(name):
    return [nid for nid, n in NODES.items() if our_name(n["type"]) == name]


def cheapest_path(owned, target):
    """Cheapest list of new nodes (ending at target) that connects target to the owned set or a base node."""
    if target in owned:
        return []
    dist, prev, heap = {}, {}, []
    for nid in NODES:
        if nid in owned:
            dist[nid] = 0
            heapq.heappush(heap, (0, nid))
        elif NODES[nid].get("base"):
            dist[nid] = cost(nid)
            heapq.heappush(heap, (cost(nid), nid))
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, 1e9):
            continue
        if u == target:
            break
        for v in ADJ[u]:
            nd = d + (0 if v in owned else cost(v))
            if nd < dist.get(v, 1e9):
                dist[v], prev[v] = nd, u
                heapq.heappush(heap, (nd, v))
    path, u = [], target
    while u not in owned:
        path.append(u)
        if u not in prev:
            break
        u = prev[u]
    return list(reversed(path))


def build_preset(build, budget=212):
    """Connected selection {node_id: rank}: core skills first, then FILL extras, each reached by its cheapest path."""
    sel = {}
    spent = lambda: sum(cost(n) * r for n, r in sel.items())

    def take(nid, ranks):
        path = cheapest_path(set(sel), nid)
        extra = sum(cost(p) for p in path) + cost(nid) * (ranks - 1)
        if spent() + extra > budget:
            return False
        for p in path:
            sel[p] = 1
        sel[nid] = max(sel.get(nid, 1), ranks)
        return True

    def want(name, count):
        ids = nodes_named(name)
        if not ids:
            return
        if name.endswith(" node"):  # attribute nodes: take the `count` nearest ones
            for _ in range(count):
                free = [i for i in ids if i not in sel]
                if not free:
                    return
                best = min(free, key=lambda i: sum(cost(p) for p in cheapest_path(set(sel), i)))
                if not take(best, 1):
                    return
        else:
            take(ids[0], min(count, max_rank(ids[0])))

    order = sorted(PRESETS[build].items(), key=lambda kv: kv[0].endswith(" node"))
    for name, count in order:
        want(name, count)
    for name in FILL[build]:
        ids = nodes_named(name)
        want(name, max_rank(ids[0]) if ids and not name.endswith(" node") else 11)
    # spend what is left on the cheapest reachable skills of the build's own area
    area = {"wizard": "Mage", "battlemage": "Mage", "necromancer": "Mage", "healer": "Mage", "warrior": "Warrior",
            "tank": "Warrior", "barbarian": "Warrior", "ranger": "Ranger", "assassin": "Ranger"}[build]
    while True:
        options = []
        for nid, n in NODES.items():
            o = OUR.get(our_name(n["type"]))
            if not o or o[0] != area or sel.get(nid, 0) >= max_rank(nid):
                continue
            extra = cost(nid) if nid in sel else sum(cost(p) for p in cheapest_path(set(sel), nid))
            options.append((extra, nid))
        options = [o for o in options if spent() + o[0] <= budget]
        if not options:
            break
        _, nid = min(options)
        if nid in sel:
            sel[nid] += 1
        else:
            take(nid, 1)
    return sel, spent()


def stage_budget(level, biome_count):
    return PROGRESSION["leveling"]["skillPointsPerLevel"] * (level - 1) + sum(
        PROGRESSION["biomes"][k]["points"] for k, _ in BIOMES[:biome_count])


# (label, point budget, biomes explored) for the three build stages; biomes follow their level ranges
STAGES = [("Levels 1–15", stage_budget(15, 2), 2), ("Levels 16–35", stage_budget(35, 4), 4), ("Levels 36–50", stage_budget(50, 7), 7)]


def type_of(name):
    for key in RAW["types"]:
        if our_name(key) == name:
            return key
    return None


def game_text(name, rank=None):
    """In-game description of a skill at the given rank (max rank by default), tags stripped."""
    key = type_of(name)
    if not key:
        return ""
    t = RAW["types"][key]
    rank = rank or t.get("maxLevel", 1)
    def sub(m):
        k = m.group(1)
        if k in t.get("gameLevelValues", {}):
            return str(t["gameLevelValues"][k][rank - 1])
        return str(t.get("gameValues", {}).get(k, m.group(0)))
    import re
    lines = [re.sub(r"\.(?=[A-Z])", ". ", re.sub(r"\{\{(\w+)\}\}", sub, re.sub(r"<[^>]+>", "", d))) for d in t.get("description", [])]
    return lines[0] if lines else ""


def skill_cost(name):
    key = type_of(name)
    t = RAW["types"][key]
    return t["cost"], t.get("maxLevel", 1)


def client_data(area_colors):
    """Compact data for the browser planner."""
    types = {}
    for key, t in RAW["types"].items():
        name = our_name(key)
        o = OUR.get(name)
        types[key] = {"n": t["name"], "c": t["cost"], "m": t.get("maxLevel", 1), "d": t.get("description", []),
                      "v": t.get("gameValues", {}), "lv": t.get("gameLevelValues", {}), "s": t.get("stats", {}),
                      "a": o[0] if o else "Core", "g": o[1] if o else "", "f": o[6] if o else "", "id": o[7] if o else ""}
    nodes = []
    for nid, n in NODES.items():
        p = n["position"]
        row = [nid, n["type"], round(p["x"], 2), round(p["y"], 2)]
        if n.get("base"):
            a = n["baseAnchor"]
            row += [round(a["x"], 2), round(a["y"], 2)]
        nodes.append(row)
    presets = {}
    for b in PRESETS:
        presets[b] = build_preset(b)[0]
        for i, (_, budget, _) in enumerate(STAGES[:-1], 1):
            presets[f"{b}:{i}"] = build_preset(b, budget)[0]
    return {"build": BUILD_ID, "types": types, "nodes": nodes, "edges": RAW["edges"], "presets": presets, "colors": area_colors,
            "biomes": [[k, label, PROGRESSION["biomes"][k]["points"]] for k, label in BIOMES],
            "flameCap": PROGRESSION["flame"]["flameLevelCap"], "levelCap": PROGRESSION["leveling"]["playerLevelCap"]}
