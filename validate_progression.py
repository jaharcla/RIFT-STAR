import json
import re
import struct
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
        "riftstar:moonlit_misfit",
        "riftstar:honeyed_horizon",
        "riftstar:understone_rainbow",
    }
    if set(advancements) != expected:
        raise SystemExit(f"Unexpected advancement set: {sorted(advancements)}")
    validate_graph(advancements)
    validate_recipe()

    metadata = json.loads(PACK_META.read_text(encoding="utf-8"))
    if metadata["pack"]["pack_format"] != 15:
        raise SystemExit("RIFTSTAR_Visuals must target pack_format 15 for Minecraft 1.20.1")
    background = ROOT / "resourcepacks" / "RIFTSTAR_Visuals" / "assets" / "riftstar" / "textures" / "gui" / "advancements" / "backgrounds" / "fractured_cosmos.png"
    if not background.is_file():
        raise SystemExit("The custom Fractured Cosmos advancement background is missing")
    lens_texture = ROOT / "kubejs" / "assets" / "kubejs" / "textures" / "item" / "prism_lens.png"
    for texture, expected_size in ((background, (256, 128)), (lens_texture, (16, 16))):
        if not texture.is_file():
            raise SystemExit(f"Missing visual asset: {texture.relative_to(ROOT)}")
        with texture.open("rb") as image:
            header = image.read(24)
        if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"Invalid PNG asset: {texture.relative_to(ROOT)}")
        dimensions = struct.unpack(">II", header[16:24])
        if dimensions != expected_size:
            raise SystemExit(f"Unexpected dimensions for {texture.relative_to(ROOT)}: {dimensions}")

    language = json.loads((ROOT / "kubejs" / "assets" / "kubejs" / "lang" / "en_us.json").read_text(encoding="utf-8"))
    for advancement_id in expected:
        key = advancement_id.removeprefix("riftstar:")
        for suffix in ("title", "description"):
            if f"advancements.riftstar.{key}.{suffix}" not in language:
                raise SystemExit(f"Missing English advancement text for {advancement_id} ({suffix})")

    text = "\n".join(path.read_text(encoding="utf-8") for path in ADVANCEMENTS.glob("*.json"))
    referenced_ids = set(re.findall(r'"([a-z0-9_]+:[a-z0-9_/]+)"', text))
    allowed = {
        "minecraft:compass",
        "minecraft:overworld",
        "minecraft:changed_dimension",
        "minecraft:location",
        "minecraft:inventory_changed",
        "minecraft:amethyst_block",
        "minecraft:spyglass",
        "minecraft:honey_bottle",
        "minecraft:glow_berries",
        "blue_skies:everbright",
        "blue_skies:everbright_portal",
        "blue_skies:diopside_gem",
        "ad_astra:moon",
        "the_bumblezone:the_bumblezone",
        "alexscaves:primordial_caves",
        "kubejs:prism_lens",
        "riftstar:root",
        "riftstar:prismara_discovered",
        "riftstar:prismara_resource",
    }
    unknown = sorted(referenced_ids - allowed)
    if unknown:
        raise SystemExit(f"Unknown advancement IDs: {', '.join(unknown)}")
    print(json.dumps({"advancements": len(advancements), "graph": "acyclic", "pack_format": 15, "visuals": "present"}))


if __name__ == "__main__":
    main()
