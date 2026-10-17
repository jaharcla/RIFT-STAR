# RIFT//STAR: The Fractured Cosmos

RIFT//STAR is a Minecraft Java Edition 1.20.1 Forge modpack plus a small companion Forge mod that wires baseline progression hooks and cross-mod glue logic.

## Versions

- Minecraft: **1.20.1**
- Forge: **47.4.10**
- Java: **17**

## Prerequisites

- Python 3.11 or newer
- Java 17
- Network access to Forge Maven and CurseForge when restoring dependencies

Install the Python helper dependency once:

```text
python -m pip install -r requirements.txt
```

## Restore required mods

1. Run `python fetch_mods.py` to download the pinned CurseForge artifacts listed in `mods.lock.json`.
2. Run `python inspect_mods.py` after download to inspect each jar's `mods.toml` metadata and dependency declarations.
3. Keep `mods.lock.json` as the source of truth for exact versions, sides, and hashes.

The client profile uses Embeddium. The server omits it. The files marked `deferred` in `mods.lock.json` are audited but not installed.

## Build the companion mod

- Companion project path: `riftstar-companion/`
- Fallback local build command: `python riftstar-companion/build_local.py`
- Gradle build command (Windows): `riftstar-companion\gradlew.bat build`
- Gradle build command (Unix): `./riftstar-companion/gradlew build`
- The tracked wrapper downloads Gradle 8.8 on first use.

## Assemble a playable client

1. Run `python fetch_mods.py` to restore the exact pinned mod jars.
2. Build the companion with Java 17 and run `python assemble_client.py` for a local client tree.
3. Run `python package_alpha.py` to create `dist/RIFTSTAR-0.1.0-alpha.zip` for CurseForge import.

Client files can be copied into any Forge 1.20.1 instance; no machine-specific
directory is required. Client title-screen testing remains pending in this
environment.

See `docs/alpha-installation.md` for the short installation procedure and
`docs/alpha-client-checklist.md` for the manual smoke checklist.

## Assemble the dedicated server

1. Complete Forge server install (1.20.1-47.4.10).
2. Run `python riftstar-companion/build_local.py` to produce the companion jar.
3. Run `python assemble_server.py` to copy server-side pack files into `server/`.

## Implemented systems (baseline)

- Blue Skies' actual `blue_skies:diopside_gem` and Ad Astra's actual `ad_astra:steel_plate` craft a Prism Lens.
- Carrying the lens grants the `riftstar:first_colour` advancement.
- Ad Astra, Blue Skies, and Alex's Caves retain their native progression and dimensions.
- Forge companion mod entrypoint and metadata are present in `riftstar-companion/`.

## Unfinished systems

- Rift travel mechanics
- Atlas mechanics
- Client smoke/regression verification beyond reported historical checks

## Automated validation

```text
python validate_mods_lock.py
python validate_progression.py
python -m json.tool mods.lock.json
python -m py_compile assemble_client.py assemble_server.py bootstrap_forge.py check_mod_dependencies.py fetch_mods.py inspect_mods.py make_icon.py package_alpha.py validate_mods_lock.py write_curseforge_manifest.py write_modlist.py
python write_curseforge_manifest.py
```

`inspect_mods.py` and `check_mod_dependencies.py` require the restored `mods/`
directory and generate `docs/jar-audit.json`; downloaded artifacts are ignored
by Git.

## Known problems and compatibility notes

- Historical ForgeGradle issue: dependency transformation can fail with `ReadOnlyFileSystemException` in this environment.
- `build_local.py` is the Java 17 fallback path used when ForgeGradle is not usable.
- This source baseline does not include third-party mod jars or Forge runtime libraries; commands that inspect or compile against those files fail until dependencies are restored.

See `docs/compatibility-audit.md`, `docs/development-log.md`, `docs/test-matrix.md`, `docs/destinations.md`, and `docs/atlas-design.md`.

The source baseline and companion project are restored. No bundled third-party
mod JARs or server save data are tracked.
