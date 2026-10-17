import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCK = json.loads((ROOT / "mods.lock.json").read_text(encoding="utf-8"))
CLIENT = ROOT / "client"


def main() -> None:
    CLIENT.mkdir(exist_ok=True)
    (CLIENT / "mods").mkdir(exist_ok=True)
    for mod in LOCK["mods"]:
        if mod["side"] not in ("both", "client"):
            continue
        source = ROOT / "mods" / mod["file"]
        if not source.is_file():
            raise SystemExit(f"Missing restored dependency: {source}")
        if hashlib.sha256(source.read_bytes()).hexdigest() != mod["sha256"]:
            raise SystemExit(f"Hash mismatch: {source.name}")
        shutil.copy2(source, CLIENT / "mods" / source.name)
    companion = ROOT / "riftstar-companion" / "build" / "libs" / "riftstar_companion-0.1.0.jar"
    if not companion.is_file():
        raise SystemExit(f"Missing built companion: {companion}")
    shutil.copy2(companion, CLIENT / "mods" / companion.name)
    for name in ("config", "defaultconfigs", "kubejs", "resourcepacks"):
        shutil.copytree(ROOT / name, CLIENT / name, dirs_exist_ok=True)
    print(f"client mods: {len(list((CLIENT / 'mods').glob('*.jar')))}")


if __name__ == "__main__":
    main()
