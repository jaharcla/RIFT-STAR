package dev.riftstar.companion.satsu;

import java.util.ArrayList;
import java.util.List;

/**
 * Deterministic, side-effect-free suit advisor. A caller supplies actual observations
 * every tick; this class never estimates reactor energy or fires weapons.
 * Call once per client tick on the main game thread.
 */
public final class SuitIntelligence {
    private static final int BOOT_TICKS = 35;
    private static final int COMBAT_MEMORY_TICKS = 100;
    private static final int RECOVERY_TICKS = 60;
    private static final int REPEAT_WARNING_TICKS = 400;

    private SuitMode mode = SuitMode.STANDBY;
    private long deployedAt = -1, lastCombatAt = -1, recoveryUntil = -1;
    private long lastEnergyWarningAt = Long.MIN_VALUE / 2;
    private long lastHealthWarningAt = Long.MIN_VALUE / 2;
    private long lastCollisionWarningAt = Long.MIN_VALUE / 2;
    private long lastThreatWarningAt = Long.MIN_VALUE / 2;
    private long lastTick = -1;
    private boolean powerCriticalLatched = false, healthCriticalLatched = false;

    public record Update(SuitMode mode, List<SuitAdvisory> advisories) {
        public Update { advisories = List.copyOf(advisories); }
    }

    public SuitMode mode() { return mode; }

    public void reset() {
        mode = SuitMode.STANDBY;
        deployedAt = -1;
        lastCombatAt = -1;
        recoveryUntil = -1;
        lastEnergyWarningAt = Long.MIN_VALUE / 2;
        lastHealthWarningAt = Long.MIN_VALUE / 2;
        lastCollisionWarningAt = Long.MIN_VALUE / 2;
        lastThreatWarningAt = Long.MIN_VALUE / 2;
        lastTick = -1;
        powerCriticalLatched = false;
        healthCriticalLatched = false;
    }

    public Update update(SuitTelemetry t) {
        if (t.gameTick() < lastTick) reset(); // world reload, server change, or time rollback
        lastTick = t.gameTick();
        List<SuitAdvisory> events = new ArrayList<>();
        SuitMode previous = mode;
        if (!t.equipped()) {
            if (previous != SuitMode.STANDBY)
                events.add(new SuitAdvisory(SuitAdvisory.Level.INFO,
                        "suit_offline", "Suit telemetry offline. Standing by."));
            reset();
            lastTick = t.gameTick();
            return new Update(mode, events);
        }

        if (deployedAt == -1) deployedAt = t.gameTick();
        if (t.combatEvent()) lastCombatAt = t.gameTick();

        boolean energyCritical = t.reactorFraction() != null
                && t.reactorFraction() <= 0.10;
        boolean healthCritical = t.healthFraction() <= 0.20;
        if (energyCritical) powerCriticalLatched = true;
        else if (t.reactorFraction() != null && t.reactorFraction() >= 0.18)
            powerCriticalLatched = false; // unknown energy is never recovery evidence
        if (healthCritical) healthCriticalLatched = true;
        else if (t.healthFraction() >= 0.32) healthCriticalLatched = false;

        if (powerCriticalLatched || healthCriticalLatched) {
            mode = SuitMode.EMERGENCY;
        } else if (t.gameTick() - deployedAt < BOOT_TICKS) {
            mode = SuitMode.INITIALIZING;
        } else if (lastCombatAt >= 0 && t.gameTick() - lastCombatAt <= COMBAT_MEMORY_TICKS) {
            mode = SuitMode.COMBAT;
        } else if (t.confirmedFlight()) {
            mode = SuitMode.FLIGHT;
        } else if ((previous == SuitMode.FLIGHT || previous == SuitMode.COMBAT
                || previous == SuitMode.EMERGENCY) && recoveryUntil < t.gameTick()) {
            recoveryUntil = t.gameTick() + RECOVERY_TICKS;
            mode = SuitMode.RECOVERY;
        } else if (recoveryUntil >= t.gameTick()) {
            mode = SuitMode.RECOVERY;
        } else {
            mode = SuitMode.READY;
        }

        if (mode != previous) {
            switch (mode) {
                case INITIALIZING -> events.add(info("boot", "Suit detected. Initializing tactical assistance."));
                case READY -> events.add(info("ready", "Suit systems monitored. Standing by."));
                case FLIGHT -> events.add(info("flight", "Flight telemetry active. Terrain awareness enabled."));
                case COMBAT -> events.add(new SuitAdvisory(SuitAdvisory.Level.CAUTION,
                        "combat", "Combat detected. Tactical monitoring engaged."));
                case EMERGENCY -> events.add(new SuitAdvisory(SuitAdvisory.Level.CRITICAL,
                        "emergency", "Critical suit condition. Prioritize disengagement."));
                case RECOVERY -> events.add(info("recovery", "Threat response cleared. Running recovery checks."));
                default -> { }
            }
        }

        // A warning is only supported by a real numeric observation, never by a guess.
        if (t.reactorFraction() != null && t.reactorFraction() <= 0.20
                && t.gameTick() - lastEnergyWarningAt >= REPEAT_WARNING_TICKS) {
            events.add(new SuitAdvisory(energyCritical ? SuitAdvisory.Level.CRITICAL
                    : SuitAdvisory.Level.CAUTION, "reactor_low",
                    "Arc reactor reserve low: " + Math.round(t.reactorFraction() * 100) + "%."));
            lastEnergyWarningAt = t.gameTick();
        }
        if (t.healthFraction() <= 0.30
                && t.gameTick() - lastHealthWarningAt >= REPEAT_WARNING_TICKS) {
            events.add(new SuitAdvisory(healthCritical ? SuitAdvisory.Level.CRITICAL
                    : SuitAdvisory.Level.CAUTION, "vitals_low",
                    "Vital signs critical: " + Math.round(t.healthFraction() * 100) + "% health."));
            lastHealthWarningAt = t.gameTick();
        }
        if (mode == SuitMode.FLIGHT && t.collisionAhead()
                && t.gameTick() - lastCollisionWarningAt >= 90) {
            events.add(new SuitAdvisory(SuitAdvisory.Level.CAUTION, "collision",
                    "Obstacle along flight vector. Adjust course."));
            lastCollisionWarningAt = t.gameTick();
        }
        if (mode == SuitMode.COMBAT && t.visibleHostiles() >= 4
                && t.gameTick() - lastThreatWarningAt >= 200) {
            events.add(new SuitAdvisory(SuitAdvisory.Level.CAUTION, "surrounded",
                    t.visibleHostiles() + " nearby hostiles. Keep an escape route open."));
            lastThreatWarningAt = t.gameTick();
        }
        return new Update(mode, events);
    }

    private static SuitAdvisory info(String code, String message) {
        return new SuitAdvisory(SuitAdvisory.Level.INFO, code, message);
    }
}
