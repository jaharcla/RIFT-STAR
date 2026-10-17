# Source archive inventory (metadata only)

**Archive:** `riftstar-forge-1201.rar` (RAR5; approximately 366 MiB compressed).  
**Inspection:** 892 archive entries, approximately 680 MB uncompressed. Filenames and sizes were readable; **file contents, integrity and runnable compatibility have not been verified** because the available RAR5 decoder rejected the compression dictionary.

## Top-level source and assets observed

- `riftstar-companion/` (Forge project, Gradle build scripts, Java entrypoint and local build helper)
- `kubejs/` (startup item script, server recipe script, an advancement and a Prism Lens texture)
- `config/`, `defaultconfigs/` (selected mod configurations)
- `resourcepacks/RIFTSTAR_Visuals/pack.mcmeta`
- `docs/` (compatibility audit, destinations, test matrix, development log, JAR audit)
- `mods.lock.json`, `modlist.html`, `fetch_mods.py`, `assemble_server.py`, `bootstrap_forge.py`
- `server/` (server install, world, logs, libraries and duplicated pack assets — not appropriate to commit wholesale)

## Mod JAR names seen in `mods/`

```text
ad_astra-forge-1.20.1-1.15.21.jar
alexscaves-2.0.2.jar
architectury-9.2.14-forge.jar
blue_skies-1.20.1-1.3.31.jar
botarium-forge-1.20.1-2.3.4.jar
citadel-2.6.3-1.20.1.jar
embeddium-0.3.31+mc1.20.1.jar
ferritecore-6.0.1-forge.jar
Jade-1.20.1-Forge-11.12.2.jar
jei-1.20.1-forge-15.56.0.205.jar
kubejs-forge-2001.6.5-build.26.jar
modernfix-forge-5.27.88+mc1.20.1.jar
resourcefulconfig-forge-1.20.1-2.1.3.jar
resourcefullib-forge-1.20.1-2.1.29.jar
rhino-forge-2001.2.3-build.10.jar
riftstar_companion-0.1.0.jar
structure_gel-1.20.1-2.16.2.jar
the_bumblezone-7.14.0+1.20.1-forge.jar
worldportal-forge-0.0.11+1.20.1.jar
```

This is an **observed archive inventory**, not a tested or endorsed dependency lock. The research design report discussed World Portal 0.0.10; the uploaded archive instead contains 0.0.11.

## Extraction blocker and next input

The RAR5 compression dictionary exceeds this environment's installed archive decoder limits. To import the actual source, provide a small **ZIP** of `riftstar-companion/`, `kubejs/`, `config/`, `defaultconfigs/`, `resourcepacks/`, `docs/`, `mods.lock.json` and root `*.py`/README files, excluding `build/`, `.gradle/`, `server/`, `mods/`, `libraries/` and logs. This avoids re-uploading hundreds of megabytes of downloadable jars.
