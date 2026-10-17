import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCK_PATH = ROOT / "mods.lock.json"
COMPANION_JAR = ROOT / "riftstar-companion" / "build" / "libs" / "riftstar_companion-0.1.0.jar"
PACKAGE_NAME = "RIFTSTAR-0.2.0-alpha.zip"


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def verify_pinned_mods(lock: dict) -> None:
    missing = []
    mismatched = []
    for mod in lock["mods"]:
        if mod["side"] == "deferred":
            continue
        path = ROOT / "mods" / mod["file"]
        if not path.is_file():
            missing.append(mod["file"])
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != mod["sha256"]:
            mismatched.append(mod["file"])
    if missing or mismatched:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if mismatched:
            details.append("hash mismatch: " + ", ".join(mismatched))
        raise SystemExit("Pinned dependencies are not restored (" + "; ".join(details) + ")")


def build_companion() -> None:
    if not COMPANION_JAR.is_file():
        raise SystemExit(
            f"Missing {COMPANION_JAR}. Build it with Java 17 before packaging."
        )


def copy_tree(source_name: str, target: Path) -> None:
    source = ROOT / source_name
    if source.is_dir():
        shutil.copytree(source, target / source_name, dirs_exist_ok=True)


def create_package(lock: dict) -> Path:
    staging = ROOT / "dist" / "alpha-staging"
    output = ROOT / "dist" / PACKAGE_NAME
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    run([sys.executable, "write_curseforge_manifest.py"])
    shutil.copy2(ROOT / "dist" / "curseforge" / "manifest.json", staging / "manifest.json")
    overrides = staging / "overrides"
    for name in ("config", "defaultconfigs", "kubejs", "resourcepacks"):
        copy_tree(name, overrides)
    mods = overrides / "mods"
    mods.mkdir(parents=True, exist_ok=True)
    shutil.copy2(COMPANION_JAR, mods / COMPANION_JAR.name)

    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(staging).as_posix())
    shutil.rmtree(staging)
    print(
        json.dumps(
            {
                "package": str(output),
                "bytes": output.stat().st_size,
                "companion": COMPANION_JAR.name,
                "minecraft": lock["minecraft"],
                "forge": lock["forge"],
            }
        )
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the RIFT//STAR Alpha 0.2 CurseForge pack.")
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore pinned CurseForge jars before packaging.",
    )
    args = parser.parse_args()
    if args.restore:
        run([sys.executable, "validate_mods_lock.py"])
        run([sys.executable, "fetch_mods.py"])
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    verify_pinned_mods(lock)
    build_companion()
    package = create_package(lock)
    with zipfile.ZipFile(package) as archive:
        required = {
            "manifest.json",
            "overrides/config",
            "overrides/defaultconfigs",
            "overrides/kubejs",
            "overrides/resourcepacks",
            "overrides/mods/" + COMPANION_JAR.name,
        }
        names = set(archive.namelist())
        for directory in required - {"manifest.json", "overrides/mods/" + COMPANION_JAR.name}:
            if not any(name.startswith(directory + "/") for name in names):
                raise SystemExit(f"Package is missing {directory}/")
        if "manifest.json" not in names or "overrides/mods/" + COMPANION_JAR.name not in names:
            raise SystemExit("Package is missing its manifest or companion jar")


if __name__ == "__main__":
    main()
