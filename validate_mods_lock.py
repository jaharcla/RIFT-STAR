import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCK_PATH = ROOT / "mods.lock.json"
VALID_SIDES = {"both", "client", "server", "deferred"}
REQUIRED_FIELDS = {
    "id",
    "file",
    "side",
    "project_id",
    "file_id",
    "source",
    "download",
    "bytes",
    "release_type",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def fail(message: str) -> None:
    raise SystemExit(f"mods.lock.json validation failed: {message}")


def main() -> None:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    mods = lock.get("mods")
    if not isinstance(mods, list):
        fail("top-level 'mods' must be an array")

    seen_ids = set()
    deferred_without_hash = []
    for index, mod in enumerate(mods):
        if not isinstance(mod, dict):
            fail(f"mods[{index}] must be an object")
        missing = sorted(REQUIRED_FIELDS - set(mod))
        if missing:
            fail(f"mods[{index}] missing required fields: {', '.join(missing)}")

        mod_id = mod["id"]
        if mod_id in seen_ids:
            fail(f"duplicate mod id detected: {mod_id}")
        seen_ids.add(mod_id)

        side = mod["side"]
        if side not in VALID_SIDES:
            fail(f"mods[{index}] has invalid side '{side}'")

        sha256 = mod.get("sha256")
        if side == "deferred":
            if sha256:
                if not SHA256_RE.fullmatch(sha256):
                    fail(f"mods[{index}] has invalid deferred sha256 format")
            else:
                deferred_without_hash.append(mod_id)
        else:
            if not isinstance(sha256, str) or not SHA256_RE.fullmatch(sha256):
                fail(f"mods[{index}] must include a valid sha256")

    if "oculus" in deferred_without_hash:
        print("validated deferred hash exception: oculus has no sha256 by design")
    print(
        json.dumps(
            {
                "mods": len(mods),
                "unique_ids": len(seen_ids),
                "deferred_without_sha256": deferred_without_hash,
            }
        )
    )


if __name__ == "__main__":
    main()
