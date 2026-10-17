import json
import tomllib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCK = json.loads((ROOT / "mods.lock.json").read_text(encoding="utf-8"))


def main():
    report = []
    for mod in LOCK["mods"]:
        if mod["side"] == "deferred":
            continue
        with zipfile.ZipFile(ROOT / "mods" / mod["file"]) as jar:
            names = jar.namelist()
            metadata = tomllib.loads(jar.read("META-INF/mods.toml").decode("utf-8"))
            ids = [entry["modId"] for entry in metadata.get("mods", [])]
            dependencies = []
            for key, entries in metadata.get("dependencies", {}).items():
                dependencies.extend({"owner": key, "id": entry["modId"], "mandatory": entry.get("mandatory", False), "range": entry.get("versionRange", ""), "side": entry.get("side", "BOTH")} for entry in entries)
            report.append({"name": mod["id"], "mod_ids": ids, "version": [m.get("version") for m in metadata.get("mods", [])], "dependencies": dependencies, "dimensions": [n for n in names if n.startswith("data/") and "/dimension/" in n and n.endswith(".json")], "dimension_types": [n for n in names if n.startswith("data/") and "/dimension_type/" in n and n.endswith(".json")]})
    (ROOT / "docs" / "jar-audit.json").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "docs" / "jar-audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for item in report:
        print(item["name"], item["mod_ids"], [(d["id"], d["range"]) for d in item["dependencies"] if d["mandatory"] and d["id"] not in ("forge", "minecraft")])


if __name__ == "__main__":
    main()
