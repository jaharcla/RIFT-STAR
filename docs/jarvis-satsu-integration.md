# RIFT//STAR JARVIS + Satsu 3.8.0: Suit intelligence core

Status: **implemented as an optional client-side adapter and tested deterministic engine, NOT integrated into the newer local JARVIS checkout yet**.

This branch applies to the older `RIFT-STAR` companion source (Forge 1.20.1, 47.4.10). The current Windows JARVIS project is a separate, newer checkout and is not present in this GitHub snapshot. Port the package into that checkout; do not overwrite its current JARVIS/Satsu integration.

## What this branch actually does

- A Java 17, independent `SuitIntelligence` state engine prioritizes **STANDBY > INITIALIZING > READY / FLIGHT / COMBAT / EMERGENCY / RECOVERY** based on observations, with emergency taking highest priority.
- Brief action-bar announcements on state transitions, including low health and *verified* low arc-reactor reserve.
- 8-block velocity-direction raycast for forward terrain collisions while flying, with a 90-tick warning cooldown.
- Nearby line-of-sight hostile counts, with a clustered-hostiles warning only after actual combat begins.
- 100-tick combat-memory window, 60-tick recovery mode, and repeated-alert cooldowns.
- Persistent emergency latch for reactor values until a **verified recharge reading**; an unknown reading can never falsely clear the warning.
- A `TelemetryProvider` interface that lets the real JARVIS/Satsu integration inject authoritative suit, Palladium, reactor, flight, and combat information.
- A `voiceSink` that emits typed `SuitAdvisory` objects into the existing JARVIS voice engine without replacing it.
- No weapons, navigation, AI command, movement, energy-routing, armour equipment, nanite activation, or network actions are autonomously executed.

## Wiring the existing Satsu bridge

The fallback implementation uses item registry namespaces containing `satsu` to detect armour; this is **not a verified mapping for every Satsu suit**. It reads vanilla Minecraft health, nearby hostile entities, and vanilla flight flags, not Satsu-specific data. It cannot know how much energy/nanites exist. Satsu 3.8.0 internals must be inspected in the actual local installation to bind their real IDs.

Attach to the existing JARVIS integration *on the client thread* with the supplied hooks:

```java
ForgeSuitClientBridge.setTelemetryProvider((player, tick) -> {
    // Adapt from your EXISTING verified Satsu integration (example interfaces only).
    // Return null if authoritative suit status cannot be sampled this tick,
    // and the safe fallback sampler will run.
    return new SuitTelemetry(
        tick,
        realSatsuBridge.isSuitEquipped(),
        realSatsuBridge.isFlying(),
        realSatsuBridge.wasRecentlyAttackingOrAttacked(),
        Math.max(0.0, Math.min(1.0, player.getHealth() / player.getMaxHealth())),
        realSatsuBridge.reactorFractionOrNull(), // null, NOT 0, if unknown
        realSatsuBridge.visibleHostileCount(),
        realSatsuBridge.obstacleAlongVelocity());
});

ForgeSuitClientBridge.setVoiceSink(advisory -> {
    // Use current JARVIS TTS with your existing rate-limiting/speech queue.
    jarvisVoice.enqueue(advisory.level(), advisory.code(), advisory.text());
});
```

The illustrative `realSatsuBridge` and `jarvisVoice` identifiers are NOT bundled APIs. Replace them with actual existing classes from the newer local project. Do not call the client setter from common setup or a dedicated server.

If Satsu has a different item namespace, prefer confirmed Palladium power state through the telemetry provider instead of extending substring guessing.

## Tests

The state engine does not depend on Forge, making Java 17 CI checks possible:

```bash
ROOT=riftstar-companion/src/main/java/dev/riftstar/companion/satsu
TEST=riftstar-companion/src/test/java/dev/riftstar/companion/satsu/SuitEngineSmokeTest.java
mkdir -p build/jarvis-satsu-tests
javac --release 17 -d build/jarvis-satsu-tests \
  "$ROOT/SuitMode.java" "$ROOT/SuitTelemetry.java" \
  "$ROOT/SuitAdvisory.java" "$ROOT/SuitIntelligence.java" "$TEST"
java -cp build/jarvis-satsu-tests dev.riftstar.companion.satsu.SuitEngineSmokeTest
```

The `ForgeSuitClientBridge` must separately be built with ForgeGradle and tested **in an actual Satsu 3.8.0 instance**. This branch does not include Satsu proprietary jars or a runnable test world.

## Follow-up for local JARVIS integration

1. Inspect current local `compat/satsu` or equivalent and wire its real telemetry provider to this engine.
2. Have the existing voice pipeline accept `SuitAdvisory` with priority and interrupt policy.
3. Verify that the suit-detection and flight flags work in real Satsu armour before enabling default messages.
4. Test in survival and creative, armour deployment/unequip, low reactor charge, world switch, multiplayer and dedicated servers.
5. Only implement automatic repulsor or power rerouting after a confirmed Satsu/Palladium API and permission model exist.

No claim of completed game integration is made until these steps pass.
