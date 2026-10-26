package dev.riftstar.companion.satsu;

import java.util.List;

/** Zero-dependency Java 17 regression checks for the suit decision engine. */
public final class SuitEngineSmokeTest {
    public static void main(String[] args) {
        SuitIntelligence ai = new SuitIntelligence();
        check(ai.mode() == SuitMode.STANDBY, "initial state");
        check(mode(ai, 1, true, false, false, 1.0, null, 0)
                == SuitMode.INITIALIZING, "equipping boots");
        check(mode(ai, 35, true, false, false, 1.0, null, 0)
                == SuitMode.INITIALIZING, "boot delay");
        check(mode(ai, 36, true, false, false, 1.0, null, 0)
                == SuitMode.READY, "boot complete");

        var obstacle = ai.update(new SuitTelemetry(37, true, true, false,
                1.0, null, 0, true));
        check(obstacle.mode() == SuitMode.FLIGHT, "flight");
        check(has(obstacle.advisories(), "collision"), "obstacle warning");
        check(!has(obstacle.advisories(), "reactor_low"),
                "no invented energy warning");
        var obstacleSoon = ai.update(new SuitTelemetry(38, true, true, false,
                1.0, null, 0, true));
        check(!has(obstacleSoon.advisories(), "collision"), "collision cooldown");

        var combat = ai.update(new SuitTelemetry(39, true, true, true,
                1.0, null, 6, false));
        check(combat.mode() == SuitMode.COMBAT, "combat takes priority");
        check(has(combat.advisories(), "surrounded"), "hostile cluster warning");

        var lowEnergy = ai.update(new SuitTelemetry(40, true, false, false,
                1.0, 0.06, 0));
        check(lowEnergy.mode() == SuitMode.EMERGENCY, "known low reactor");
        check(has(lowEnergy.advisories(), "reactor_low"), "actual energy alert");

        check(mode(ai, 41, true, false, false, 1.0, null, 0)
                == SuitMode.EMERGENCY, "unknown reactor cannot clear an alert");
        check(mode(ai, 42, true, false, false, 1.0, 0.22, 0)
                == SuitMode.COMBAT, "confirmed energy recovery");

        check(mode(ai, 145, true, false, false, 1.0, 0.80, 0)
                == SuitMode.RECOVERY, "post-combat recovery");
        check(mode(ai, 210, true, false, false, 1.0, 0.80, 0)
                == SuitMode.READY, "recovery completes");
        check(mode(ai, 211, false, false, false, 1.0, null, 0)
                == SuitMode.STANDBY, "taking off suit");

        check(mode(ai, 212, true, false, false, 0.15, null, 0)
                == SuitMode.EMERGENCY, "critical low health");
        check(mode(ai, 213, true, false, false, 0.25, null, 0)
                == SuitMode.EMERGENCY, "health hysteresis");
        check(mode(ai, 214, true, false, false, 0.35, null, 0)
                == SuitMode.INITIALIZING, "health recovery confirmed");

        boolean invalidRejected = false;
        try { new SuitTelemetry(1, true, false, false, 0.5, Double.NaN, 0); }
        catch (IllegalArgumentException expected) { invalidRejected = true; }
        check(invalidRejected, "reject invalid power telemetry");

        check(mode(ai, 1, true, false, false, 1.0, null, 0)
                == SuitMode.INITIALIZING, "world-tick rollback safely resets state");

        System.out.println("JARVIS suit intelligence smoke tests PASSED");
    }

    private static SuitMode mode(SuitIntelligence ai, long tick, boolean armor,
            boolean flight, boolean combat, double health, Double energy, int hostiles) {
        return ai.update(new SuitTelemetry(tick, armor, flight, combat,
                health, energy, hostiles)).mode();
    }

    private static boolean has(List<SuitAdvisory> advisories, String code) {
        return advisories.stream().anyMatch(a -> a.code().equals(code));
    }

    private static void check(boolean ok, String description) {
        if (!ok) throw new AssertionError(description);
    }
}
