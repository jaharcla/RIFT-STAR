# RIFT//STAR Companion

Forge 1.20.1 / 47.4.10 / Java 17 standalone mod project, bootstrapped from the official MDK.

Current source is a minimal real Forge entrypoint. No rift, Atlas, scanner, teleport, or endpoint mechanics are claimed yet.

Planned Java responsibilities: server-authoritative route checks, safe arrivals, persisted anomaly endpoints, per-player Atlas records, networking, and eventual Atlas UI. These enter only after the base pack's dimension and server tests pass.

Build with `JAVA_HOME` set to Java 17:

```text
gradlew.bat build
```

The repository tracks the official Gradle 8.8 wrapper JAR. It is compatible with
the wrapper properties in this project, but is not the original archive binary.
The tracked file is 43,453 bytes with SHA-256
`cb0da6751c2b753a16ac168bb354870ebb1e162e9083f116729cec9c781156b8`.
It was downloaded from the official Gradle v8.8.0 source tree.
The fallback `python build_local.py` path remains available when ForgeGradle
dependency transformation cannot run in the local environment.
