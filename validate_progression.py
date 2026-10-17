import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ADVANCEMENTS = ROOT / "kubejs" / "data" / "riftstar" / "advancements"
PACK_META = ROOT / "resourcepacks" / "RIFTSTAR_Visuals" / "pack.mcmeta"
RECIPE_SCRIPT = ROOT / "kubejs" / "server_scripts" / "riftstar_recipes.js"


def load_advancements() -> dict[str, dict]:
    loaded = {}
    for path in sorted(ADVANCEMENTS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        loaded[f"riftstar:{path.stem}"] = data
    return loaded


def validate_graph(advancements: dict[str, dict]) -> None:
    for advancement_id, data in advancements.items():
        parent = data.get("parent")
        if parent and parent.startswith("riftstar:") and parent not in advancements:
            raise SystemExit(f"{advancement_id} references missing parent {parent}")

    visiting = set()
    visited = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise SystemExit(f"Advancement cycle detected at {node}")
        if node in visited:
            return
        visiting.add(node)
        parent = advancements[node].get("parent")
        if parent in advancements:
            visit(parent)
        visiting.remove(node)
        visited.add(node)

    for advancement_id in advancements:
        visit(advancement_id)


def validate_recipe() -> None:
    recipe = RECIPE_SCRIPT.read_text(encoding="utf-8")
    required = {
        "'kubejs:prism_lens'",
        "'blue_skies:diopside_gem'",
        "'ad_astra:steel_plate'",
        "'minecraft:amethyst_shard'",
    }
    missing = sorted(token for token in required if token not in recipe)
    if missing:
        raise SystemExit(f"Recipe is missing verified IDs: {', '.join(missing)}")
    if recipe.count("'kubejs:prism_lens'") != 1:
        raise SystemExit("Recipe must define exactly one stable kubejs:prism_lens output")


def main() -> None:
    advancements = load_advancements()
    expected = {
        "riftstar:root",
        "riftstar:prismara_discovered",
        "riftstar:prismara_resource",
        "riftstar:first_colour",
    }
    if set(advancements) != expected:
        raise SystemExit(f"Unexpected advancement set: {sorted(advancements)}")
    validate_graph(advancements)
    validate_recipe()

    metadata = json.loads(PACK_META.read_text(encoding="utf-8"))
    if metadata["pack"]["pack_format"] != 15:
        raise SystemExit("RIFTSTAR_Visuals must target pack_format 15 for Minecraft 1.20.1")

    text = "\n".join(path.read_text(encoding="utf-8") for path in ADVANCEMENTS.glob("*.json"))
    referenced_ids = set(re.findall(r'"([a-z0-9_]+:[a-z0-9_/]+)"', text))
    allowed = {
        "minecraft:compass",
        "minecraft:overworld",
        "minecraft:changed_dimension",
        "minecraft:location",
        "minecraft:inventory_changed",
        "minecraft:amethyst_block",
        "blue_skies:everbright",
        "blue_skies:everbright_portal",
        "blue_skies:diopside_gem",
        "kubejs:prism_lens",
        "riftstar:root",
        "riftstar:prismara_discovered",
        "riftstar:prismara_resource",
    }
    unknown = sorted(referenced_ids - allowed)
    if unknown:
        raise SystemExit(f"Unknown advancement IDs: {', '.join(unknown)}")
    print(json.dumps({"advancements": len(advancements), "graph": "acyclic", "pack_format": 15}))


if __name__ == "__main__":
    main()
