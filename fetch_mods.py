import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parent
GAME = "1.20.1"
PINS = [
    ("ad_astra", "ad-astra", 635042, 8833730, "both"),
    ("botarium", "botarium", 704113, 5486070, "both"),
    ("resourcefulconfig", "resourceful-config", 714059, 6231176, "both"),
    ("resourcefullib", "resourceful-lib", 570073, 5659871, "both"),
    ("blue_skies", "blue-skies", 312918, 5010316, "both"),
    ("structure_gel", "structure-gel-api", 378802, 5278429, "both"),
    ("alexscaves", "alexs-caves", 924854, 5848216, "both"),
    ("citadel", "citadel", 331936, 7476570, "both"),
    ("worldportal", "worldportal", 1205026, 9106802, "both"),
    ("kubejs", "kubejs", 238086, 8020595, "both"),
    ("rhino", "rhino", 416294, 6186971, "both"),
    ("architectury", "architectury-api", 419699, 5137938, "both"),
    ("embeddium", "embeddium", 908741, 5681725, "client"),
    ("modernfix", "modernfix", 790626, 9124107, "both"),
    ("the_bumblezone", "the-bumblezone-forge", 362479, 8899333, "both"),
    ("oculus", "oculus", 581495, 6020952, "deferred"),
    ("ferritecore", "ferritecore", 429235, 4810975, "both"),
    ("jade", "jade", 324717, 5876199, "both"),
    ("jei", "jei", 238222, 8778011, "client"),
    ("patchouli", "patchouli", 306770, 4636277, "both"),
    ("packetfixer", "packet-fixer", 689467, 7872374, "both"),
]


def fetch(pin):
    name, slug, project_id, file_id, side = pin
    api = f"https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}"
    metadata = requests.get(api, timeout=30).json()["data"]
    assert metadata["projectId"] == project_id and metadata["id"] == file_id
    assert GAME in metadata["gameVersions"] and "Forge" in metadata["gameVersions"]
    filename = metadata["fileName"]
    url = f"https://mediafilez.forgecdn.net/files/{file_id // 1000}/{file_id % 1000}/{quote(filename)}"
    record = {
        "id": name,
        "file": filename,
        "side": side,
        "project_id": project_id,
        "file_id": file_id,
        "source": f"https://www.curseforge.com/minecraft/mc-mods/{slug}/files/{file_id}",
        "download": url,
        "bytes": metadata["fileLength"],
        "release_type": metadata["releaseType"],
    }
    if side == "deferred":
        return record
    target = ROOT / "mods" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.stat().st_size != metadata["fileLength"]:
        with requests.get(url, stream=True, timeout=120) as response:
            response.raise_for_status()
            with target.open("wb") as output:
                for chunk in response.iter_content(1024 * 1024):
                    output.write(chunk)
    assert target.stat().st_size == metadata["fileLength"], filename
    record["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    return record


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(fetch, PINS))
    lock = {"minecraft": GAME, "forge": "47.4.10", "mods": records}
    (ROOT / "mods.lock.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len([r for r in records if "sha256" in r]), "bytes": sum(r.get("bytes", 0) for r in records if "sha256" in r), "deferred": [r["id"] for r in records if r["side"] == "deferred"]}))


if __name__ == "__main__":
    main()
