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

## Milestone ledger

| Milestone | State |
|---|---|
| Foundation inventory and project structure | Complete |
| Dedicated server boot and dimension chunk loading | Passed |
| First artifact + cross-mod recipe | Registered on server; in-game craft untested |
| Companion mod skeleton | Java 17 fallback jar built and loaded; Gradle build blocked |
| Persistent anomaly and Atlas mechanics | Future |

## 2026-10-17 — Task pass follow-up

- Companion ForgeGradle diagnosis in this repo is currently blocked by missing source-import files under `riftstar-companion/`: no `build.gradle`, no Gradle wrapper scripts, and no `src/main/resources/META-INF/mods.toml` are present to execute or compare against the Forge 47.4.10 MDK.
- Verified local Java toolchain in this environment is Java 17 (`java`/`javac` 17.0.20.1 with `JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64`).
- `riftstar-companion/build_local.py` remains in place as fallback, but still depends on missing Forge server libraries (`server/libraries/...`) and missing companion resource metadata (`mods.toml`) to produce a loadable mod jar.
- Attempted Forge MDK metadata retrieval and mod fetch/server assembly flow, but outbound resolution to Forge/CurseForge hosts failed in this sandbox, so launch verification here remained blocked.
- Attempted to open follow-up GitHub issues from this environment, but CLI issue creation is blocked without `GH_TOKEN`/authenticated credentials in this run.
- Added lockfile/CI automation and distribution-manifest generation scripts (see repository root scripts and `.github/workflows/lockfile-validation.yml`).

### Source-import gaps observed from README/docs references vs. repository contents

- Missing referenced file: `docs/compatibility-audit.md` (README references it directly).
- Missing expected generated file: `docs/jar-audit.json` (referenced by `docs/test-matrix.md` and produced by `inspect_mods.py` only after jars are downloaded and inspected).
- Missing companion Forge project files referenced by companion README/build flow:
  - `riftstar-companion/build.gradle`
  - `riftstar-companion/gradlew`
  - `riftstar-companion/gradlew.bat`
  - `riftstar-companion/src/main/resources/META-INF/mods.toml`

### Example local path moved from README

- Example only: `C:\Users\Owner\curseforge\minecraft\Instances\RIFTSTAR - The Fractured Cosmos`
