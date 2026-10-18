import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "server"
LOCK = json.loads((ROOT / "mods.lock.json").read_text(encoding="utf-8"))


def main():
    assert (SERVER / "run.bat").is_file()
    (SERVER / "mods").mkdir(exist_ok=True)
    for mod in LOCK["mods"]:
        if mod["side"] not in ("both", "server"):
            continue
        source = ROOT / "mods" / mod["file"]
        target = SERVER / "mods" / mod["file"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == mod["sha256"]
        shutil.copy2(source, target)
    companion = ROOT / "riftstar-companion" / "build" / "libs" / "riftstar_companion-0.1.0.jar"
    if companion.is_file():
        shutil.copy2(companion, ROOT / "mods" / companion.name)
        shutil.copy2(companion, SERVER / "mods" / companion.name)
    for name in ("kubejs", "config", "defaultconfigs", "patchouli_books"):
        shutil.copytree(ROOT / name, SERVER / name, dirs_exist_ok=True)
    print(f"server mods: {len(list((SERVER / 'mods').glob('*.jar')))}")


if __name__ == "__main__":
    main()
