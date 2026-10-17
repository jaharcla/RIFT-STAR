# Test matrix

| Check | Status | Evidence / next action |
|---|---|---|
| Exact Forge and mod-file metadata | Pass | `mods.lock.json`; `docs/jar-audit.json` |
| Forge dedicated-server install | Pass | `server/run.bat`, Forge 47.4.10 libraries |
| Server loader + world creation | Pass | Forge `Done` on two launches; clean stop and reload in `server/logs/latest.log` |
| KubeJS item + recipe registration | Pass | 1 startup script and 1 server script, zero errors; 1 added recipe, zero failures |
| Prismara advancement graph and referenced IDs | Pass | `python validate_progression.py`; four nodes, acyclic graph |
| Prism Lens crafting + advancement trigger | Not run | Requires client inventory/crafting test |
| Overworld + Everbright/Everdawn | Partial | Dimension chunks force-loaded, saved, unloaded, and reloaded; native portal travel not run |
| Moon/Mars/Glacio + other Ad Astra dimensions | Partial | All 11 dimension chunks loaded and saved; native travel untested |
| Alex's Caves Candy Cavity/Abyssal Chasm | Pending | Locate biomes in generated Overworld |
| World Portal fixed link | Not applicable | Native Blue Skies entry/return is preserved; no World Portal link was added |
| Forge companion local build + server load | Pass | `build_local.py` compiled on Java 17; Forge `debug.log` found valid `riftstar_companion` 0.1.0 and server reached `Done` |
| ForgeGradle build | Blocked | Access Transformer throws `ReadOnlyFileSystemException` before Java compilation, including with Java 21 |
| Client profile assembly | Pass | Isolated CurseForge Forge 47.4.10 profile; 15 jar hashes match project |
| Client launch + join | Not run | CurseForge window unavailable from this environment; title screen and in-game crafting unverified |
| Two-player progression acceptance | Not run | Requires a client-capable multiplayer test |

Chunk loading proves these dimensions can generate and persist server-side. It does not prove their client rendering or native travel flow.
