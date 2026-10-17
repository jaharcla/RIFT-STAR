import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCK = json.loads((ROOT / "mods.lock.json").read_text(encoding="utf-8"))
AUDIT = json.loads((ROOT / "docs" / "jar-audit.json").read_text(encoding="utf-8"))


def main() -> None:
    known_mod_ids = set()
    for mod in AUDIT:
        known_mod_ids.update(mod.get("mod_ids", []))

    missing = []
    for mod in AUDIT:
        for dependency in mod.get("dependencies", []):
            if not dependency.get("mandatory", False):
                continue
            dep_id = dependency["id"]
            if dep_id in {"forge", "minecraft"}:
                continue
            if dep_id not in known_mod_ids:
                missing.append(
                    {
                        "owner": mod["name"],
                        "dependency": dep_id,
                        "range": dependency.get("range", ""),
                    }
                )

    if missing:
        details = ", ".join(
            f"{entry['owner']} -> {entry['dependency']} {entry['range']}".strip()
            for entry in missing
        )
        raise SystemExit(f"Missing mandatory mod dependencies: {details}")

    deferred = [mod["id"] for mod in LOCK["mods"] if mod["side"] == "deferred"]
    print(
        json.dumps(
            {
                "checked_mods": len(AUDIT),
                "known_mod_ids": len(known_mod_ids),
                "deferred": deferred,
            }
        )
    )


if __name__ == "__main__":
    main()
