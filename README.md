# RIFT//STAR: The Fractured Cosmos

RIFT//STAR is a Minecraft Java Edition 1.20.1 Forge modpack plus a small companion Forge mod that wires baseline progression hooks and cross-mod glue logic.

## Versions

- Minecraft: **1.20.1**
- Forge: **47.4.10**
- Java: **17**

## Restore required mods

1. Run `python fetch_mods.py` to download the pinned CurseForge artifacts listed in `mods.lock.json`.
2. Run `python inspect_mods.py` after download to inspect each jar's `mods.toml` metadata and dependency declarations.
3. Keep `mods.lock.json` as the source of truth for exact versions, sides, and hashes.

The client profile uses Embeddium. The server omits it. The files marked `deferred` in `mods.lock.json` are audited but not installed.

## Build the companion mod

- Companion project path: `riftstar-companion/`
- Fallback local build command: `python riftstar-companion/build_local.py`
- Gradle build command (when wrapper/runtime is available): `./gradlew build`

## Assemble a playable client

1. Run `python bootstrap_forge.py` to obtain Forge installer assets.
2. Place this repository's `config/`, `defaultconfigs/`, `kubejs/`, and `resourcepacks/` into the target Forge 1.20.1 instance.
3. Place downloaded mod jars in `mods/` according to `mods.lock.json`.

An isolated local CurseForge profile is installed at `C:\Users\Owner\curseforge\minecraft\Instances\RIFTSTAR - The Fractured Cosmos` with Forge 47.4.10. Client title-screen testing remains pending.

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

## Known problems and compatibility notes

- Historical ForgeGradle issue: dependency transformation can fail with `ReadOnlyFileSystemException` in this environment.
- `build_local.py` is the Java 17 fallback path used when ForgeGradle is not usable.
- This source baseline does not include third-party mod jars or Forge runtime libraries; commands that inspect or compile against those files fail until dependencies are restored.

See `docs/compatibility-audit.md`, `docs/development-log.md`, `docs/test-matrix.md`, and `docs/destinations.md`.
