# RIFT//STAR: The Fractured Cosmos

Minecraft Java 1.20.1 / Forge 47.4.10 foundation. Java 17 required.

## Reproduce

1. Run `python fetch_mods.py` to fetch the pinned CurseForge files and verify their metadata and SHA-256 hashes in `mods.lock.json`.
2. Run `python bootstrap_forge.py` to obtain the official Forge installer and MDK.
3. Run `python inspect_mods.py` to inspect the jars' `mods.toml` dependency declarations.
4. Use this directory's `mods/`, `config/`, `defaultconfigs/`, `kubejs/`, and `resourcepacks/` as the client instance contents.
5. Run `python riftstar-companion/build_local.py` and `python assemble_server.py` after Forge's server install to copy the server-side files into `server/`.

The client profile uses Embeddium. The server omits it. The files marked `deferred` in `mods.lock.json` are audited but not installed.

An isolated local CurseForge profile is installed at `C:\Users\Owner\curseforge\minecraft\Instances\RIFTSTAR - The Fractured Cosmos` with Forge 47.4.10. Client title-screen testing remains pending.

## Current slice

- Blue Skies' actual `blue_skies:diopside_gem` and Ad Astra's actual `ad_astra:steel_plate` craft a Prism Lens.
- Carrying the lens grants the `riftstar:first_colour` advancement.
- Ad Astra, Blue Skies, and Alex's Caves retain their native progression and dimensions.
- The Forge companion is a separate source module. `build_local.py` produces its minimal jar with Java 17; ForgeGradle currently fails during dependency transformation. Rift travel and Atlas mechanics are future work.

See `docs/compatibility-audit.md`, `docs/development-log.md`, `docs/test-matrix.md`, and `docs/destinations.md`.

**GitHub import status:** Core scripts and some code have been committed, but not every source-archive file has been imported yet. The original upload is retained separately. No bundled third-party mod JARs or server save data are tracked.
