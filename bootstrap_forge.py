import hashlib
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent
VERSION = "1.20.1-47.4.10"
BASE = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{VERSION}/"


def download(name):
    path = ROOT / "tools" / name
    path.parent.mkdir(exist_ok=True)
    if not path.exists():
        response = requests.get(BASE + name, timeout=120)
        response.raise_for_status()
        path.write_bytes(response.content)
    assert zipfile.is_zipfile(path), path
    print(name, path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest())
    return path


def main():
    download(f"forge-{VERSION}-installer.jar")
    mdk = download(f"forge-{VERSION}-mdk.zip")
    target = ROOT / "riftstar-companion"
    if not target.exists():
        target.mkdir()
        with zipfile.ZipFile(mdk) as archive:
            for item in archive.infolist():
                path = (target / item.filename).resolve()
                assert path == target.resolve() or target.resolve() in path.parents
            archive.extractall(target)
    print("MDK", target)


if __name__ == "__main__":
    main()
