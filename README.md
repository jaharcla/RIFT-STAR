# RIFT//STAR — The Fractured Cosmos

A Minecraft Forge 1.20.1 modpack connecting psychedelic dimensions, strange cave biomes, and space exploration through a simple shared progression system.

**Status: source import pending.** This repository has been initialized for the ongoing project; it does **not** yet contain the full Codex project. The uploaded RAR archive was inventoried but could not be extracted in the current environment because its RAR5 compression dictionary exceeds the available decoder's limit.

## Experience goals

- Colourful, bizarre, obviously modded worlds, without complicated onboarding.
- Existing mods supply most world content. Configuration, KubeJS scripts and a small Forge companion provide integration.
- Ad Astra for rockets; Blue Skies and The Bumblezone for dimensions; Alex's Caves for rare Overworld cave biomes.
- World Portal for stable links; custom companion behavior only when ordinary datapacks and scripts cannot handle it.
- Keep progression exploratory rather than a sprawling quest grind.

## Known baseline (from Codex's reports)

- Minecraft 1.20.1 / Forge 47.4.10 / Java 17.
- Codex reported successfully booting a dedicated server with the companion mod and loading/saving Blue Skies and Ad Astra dimensions.
- Client launch, portal traversal, custom gameplay and shaders have **not** been demonstrated.
- RAR inventory includes World Portal Forge **0.0.11**, not the 0.0.10 mentioned in the design research.
- The modpack's current KubeJS scripts are minimal; the actual cross-mod progression remains to be implemented.

See [Archive inventory](docs/archive-inventory.md) for the dependency names observed without unpacking.

## Development workflow

1. Import the source and configs from an extractable source-only ZIP (omit bundled downloads, caches, logs and saved worlds).
2. Check exact mod dependencies and configs and preserve a version-locked manifest.
3. Verify both dedicated-server and client launch.
4. Build a single complete exploration loop before expanding progression.
5. Test compatibility, multiplayer and visuals against a documented matrix.

Third-party mod JARs should be downloaded from their legitimate distribution sources and kept out of Git history.
