# Compatibility audit — 2026-10-17

Baseline: [official Forge 1.20.1 recommended 47.4.10](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.20.1.html). Java 17.

`mods.lock.json` is the authoritative inventory: exact file, CurseForge project/file IDs, source URL, download URL, size, SHA-256, and client/server status. `jar-audit.json` records each downloaded jar's mod IDs, required dependency ranges, and packaged dimensions.

| Component | Locked Forge 1.20.1 file | Required dependencies from its jar |
|---|---|---|
| Ad Astra | `ad_astra-forge-1.20.1-1.15.21.jar` | Resourceful Lib >=2.1.23; Resourceful Config >=2.1.0; Botarium >=2.3.0 |
| Botarium | `botarium-forge-1.20.1-2.3.4.jar` | — |
| Resourceful Lib | `resourcefullib-forge-1.20.1-2.1.29.jar` | — |
| Resourceful Config | `resourcefulconfig-forge-1.20.1-2.1.3.jar` | — |
| Blue Skies | `blue_skies-1.20.1-1.3.31.jar` | Structure Gel >=2.13.0 |
| Structure Gel | `structure_gel-1.20.1-2.16.2.jar` | — |
| Alex's Caves | `alexscaves-2.0.2.jar` | Citadel >=2.6.0 |
| Citadel | `citadel-2.6.3-1.20.1.jar` | — |
| World Portal | `worldportal-forge-0.0.11+1.20.1.jar` | — |
| KubeJS | `kubejs-forge-2001.6.5-build.26.jar` | Rhino >=2001.2.2-build.1; Architectury >=9.1.12 |
| Rhino | `rhino-forge-2001.2.3-build.10.jar` | — |
| Architectury | `architectury-9.2.14-forge.jar` | — |
| ModernFix | `modernfix-forge-5.27.88+mc1.20.1.jar` | — |
| Embeddium | `embeddium-0.3.31+mc1.20.1.jar` | Client only |

Audited, deferred: Bumblezone 7.14.0, Oculus 1.8.0, FerriteCore 6.0.1, Jade 11.12.2, JEI 15.56.0.205. Their exact official file URLs are in the lockfile. Deferral keeps the first boot and dimension tests small.

Corrections to the supplied report:

- World Portal has a newer Forge 1.20.1 version, **0.0.11**, and changed its config to `worldportal-common.toml`. [Author's configuration guide](https://www.curseforge.com/minecraft/mc-mods/worldportal)
- Resourceful Lib is locked to a verified 2.1.29 Forge file; Architectury to a verified 9.2.14 Forge file. Their minimums come from the actual Ad Astra and KubeJS jars.
- Jade 11.12.2 is newer than the report's 11.11.1. JEI 15.56.0.205 is a release file; the report's 15.71.0.224 beta is not part of this baseline.
- Alex's Caves' Candy Cavity and Abyssal Chasm are Overworld biomes, not dimension registry entries. The jars contain Ad Astra's planetary dimensions and Blue Skies' Everbright/Everdawn dimensions.

No custom portal definitions are enabled yet; this avoids bypassing native entry/progression before portal behaviour is tested. No Ad Astra recipes or config values have been guessed.
