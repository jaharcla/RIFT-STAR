import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCK = json.loads((ROOT / "mods.lock.json").read_text(encoding="utf-8"))
OUT = ROOT / "dist" / "curseforge" / "manifest.json"


def main() -> None:
    files = []
    side_counts = {"both": 0, "client": 0, "server": 0, "deferred": 0}
    for mod in LOCK["mods"]:
        side = mod["side"]
        side_counts[side] = side_counts.get(side, 0) + 1
        if side in ("deferred", "server"):
            continue
        files.append(
            {
                "projectID": mod["project_id"],
                "fileID": mod["file_id"],
                "required": True,
            }
        )

    manifest = {
        "minecraft": {
            "version": LOCK["minecraft"],
            "modLoaders": [
                {
                    "id": f"forge-{LOCK['forge']}",
                    "primary": True,
                }
            ],
        },
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": "RIFT//STAR: The Fractured Cosmos",
        "version": "0.2.2-ATLAS",
        "author": "RIFT//STAR",
        "files": files,
        "overrides": "overrides",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(OUT), "files": len(files), "sides": side_counts}))


if __name__ == "__main__":
    main()
