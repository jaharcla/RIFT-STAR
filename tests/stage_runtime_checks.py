"""Stage live integration checks in an assembled, disposable Forge server."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NATIVE_RECIPES = [
    "alloying/steel_ingot_from_alloying_iron_ingot_and_coals",
    "oxygen_loader", "cryo_freezer", "oxygen_distributor", "space_suit",
    "space_helmet", "nasa_workbench",
    *[f"{metal}_{part}" for part in ("engine", "tank")
      for metal in ("steel", "desh", "ostrum", "calorite")],
    *[f"nasa_workbench/tier_{tier}_rocket_from_nasa_workbench" for tier in range(1, 5)],
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("server", type=Path)
    target = parser.parse_args().server.resolve()
    if not (target / "run.sh").is_file() or not (target / "kubejs").is_dir():
        raise SystemExit("Assemble the disposable Forge server before staging checks")
    lock = json.loads((ROOT / "mods.lock.json").read_text())
    mod = next(mod for mod in lock["mods"] if mod["id"] == "ad_astra")
    jar_path = ROOT / "mods" / mod["file"]
    if hashlib.sha256(jar_path.read_bytes()).hexdigest() != mod["sha256"]:
        raise SystemExit("Ad Astra snapshot source does not match the pinned SHA-256")
    snapshots = []
    with zipfile.ZipFile(jar_path) as jar:
        for name in NATIVE_RECIPES:
            recipe = json.loads(jar.read(f"data/ad_astra/recipes/{name}.json"))
            record = recipe["type"] != "minecraft:crafting_shaped"
            snapshot = {"id": f"ad_astra:{name}", "record": record}
            if record:
                snapshot["inputs"] = recipe["ingredients"]
            else:
                pattern = recipe["pattern"]
                snapshot.update(width=len(pattern[0]), height=len(pattern))
                snapshot["inputs"] = [recipe["key"].get(symbol) for row in pattern for symbol in row]
            output = recipe["result"]
            snapshot.update(output=output.get("item", output.get("id")), count=output.get("count", 1))
            snapshots.append(snapshot)
    (target / "kubejs" / "native_recipe_snapshots.json").write_text(json.dumps(snapshots, indent=2) + "\n")
    shutil.copy2(ROOT / "tests" / "runtime_integrations.js",
                 target / "kubejs" / "server_scripts" / "zz_riftstar_runtime_checks.js")
    print(f"Staged live integration checks and {len(snapshots)} native recipe snapshots in {target}")


if __name__ == "__main__":
    main()
