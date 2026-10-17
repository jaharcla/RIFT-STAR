# Development log

## 2026-10-17 — Foundation

- Selected Forge 47.4.10 and Java 17 from official Forge release/MDK.
- Cross-checked every installed jar's CurseForge file metadata, bytes, SHA-256, `mods.toml`, and required dependency ranges.
- Updated World Portal from the report's 0.0.10 to 0.0.11 and recorded the TOML config migration.
- Downloaded the pinned jars, installed Forge dedicated-server files, and created reproducible fetch/inspection scripts.
- Added KubeJS Prism Lens registration, an Ad Astra + Blue Skies recipe, and a vanilla inventory advancement.
- Bootstrapped a separate Forge companion project from the exact 47.4.10 MDK.
- Accepted the dedicated-server EULA with user authorization; Forge reached `Done` twice and shut down cleanly.
- Loaded, force-loaded, unloaded, saved, and reloaded chunks in Everbright, Everdawn, and all 11 packaged Ad Astra dimensions. KubeJS registered the item and added one recipe with zero script or recipe errors.
- The client and physical travel are still untested. The companion Gradle build fails during ForgeGradle access transformation before source compilation. The Java 17 fallback build compiles the companion class, packages the mod metadata, and was recognized by Forge as a valid mod on a clean server boot.
- Created an isolated CurseForge profile `RIFTSTAR - The Fractured Cosmos` with Forge 47.4.10; all 15 client jars match the project copies by SHA-256. CurseForge did not expose a launchable window in this environment, so title-screen testing remains open.
- Inspected the pinned Blue Skies and Ad Astra jars directly and recorded the
  exact native Everbright, diopside, and steel plate paths in
  `docs/prismara-facts.md`.
- Added the four-node Prismara advancement graph, stable `kubejs:prism_lens`
  recipe validation, language entries, and player-facing documentation.

## Milestone ledger

| Milestone | State |
|---|---|
| Foundation inventory and project structure | Complete |
| Dedicated server boot and dimension chunk loading | Passed |
| First artifact + cross-mod recipe | Registered on server; in-game craft untested |
| Companion mod skeleton | Java 17 fallback jar built and loaded; Gradle build blocked |
| Persistent anomaly and Atlas mechanics | Future |
