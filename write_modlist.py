import html
import json
from pathlib import Path


root = Path(__file__).resolve().parent
lock = json.loads((root / "mods.lock.json").read_text(encoding="utf-8"))
rows = []
for mod in lock["mods"]:
    rows.append(f'<tr><td>{html.escape(mod["id"])}</td><td>{html.escape(mod["file"])}</td><td>{html.escape(mod["side"])}</td><td><a href="{html.escape(mod["source"])}">CurseForge file</a></td></tr>')
rows.append('<tr><td>riftstar_companion</td><td>riftstar_companion-0.1.0.jar</td><td>both</td><td>Local source: riftstar-companion/</td></tr>')
page = f'<!doctype html><meta charset="utf-8"><title>RIFT//STAR modlist</title><h1>RIFT//STAR · Minecraft {lock["minecraft"]} · Forge {lock["forge"]}</h1><table border="1"><tr><th>Mod</th><th>Exact file</th><th>Side</th><th>Source</th></tr>{"".join(rows)}</table>'
(root / "modlist.html").write_text(page, encoding="utf-8")
print("modlist.html", len(rows), "records")
