# Alpha 0.1 Phase 1 test report

This report records the reproducible commands used for the Phase 1 foundation.
Generated jars, Forge libraries, downloaded mods, logs, and ZIP files are not
tracked in Git.

## Environment

- Repository baseline: `main` at the Phase 1 implementation merge base
- Target Minecraft: 1.20.1
- Target Forge: 47.4.10
- Required Java: 17
- Python: 3.11 or newer

## Commands and results

| Command | Result |
| --- | --- |
| `python validate_mods_lock.py` | Passes when the lockfile schema is valid. |
| `python fetch_mods.py` | Restores the exact non-deferred CurseForge artifacts and records SHA-256 values. |
| `python bootstrap_forge.py` | Downloads the pinned Forge installer and MDK into ignored `tools/`. |
| `java -jar tools/forge-1.20.1-47.4.10-installer.jar --installServer server` | Installs the ignored Forge server runtime. |
| `python riftstar-companion/build_local.py` | Pass; compiles the companion with `javac --release 17` against the installed Forge library. |
| `python assemble_client.py` | Pass; builds an ignored local client tree with 19 jars, verified mod hashes, and the companion jar. |
| `python assemble_server.py` | Pass; builds an ignored server tree with 17 jars and pack files. |
| `python package_alpha.py` | Pass; creates and validates `dist/RIFTSTAR-0.1.0-alpha.zip` (13,431 bytes in this run). |
| `server/run.bat` with Java 17, bounded to 90 seconds | Passes startup: Forge reaches `Done (14.972s)!`; the process is then stopped by the test timeout because it is a long-running server. |
| `python -m py_compile *.py riftstar-companion/build_local.py` | Validates Python syntax. |

## Runtime blockers

The manual client checklist in `docs/alpha-client-checklist.md` requires a
graphical Minecraft launcher and cannot be completed headlessly. The local
headless server reached a clean `Done` line, but client title-screen and
multiplayer checks remain manual. Forge or CurseForge network availability can
also block dependency restoration; the lockfile hashes detect incomplete or
substituted downloads.

No gameplay, KubeJS recipes/advancements, or `docs/atlas-design.md` files are
changed by Phase 1 packaging work.
