package dev.riftstar.companion.satsu;

/**
 * One client observation. reactorFraction is null when the actual Satsu value is not
 * available: absent telemetry must NEVER be presented as an empty reactor.
 * confirmedFlight means a native Satsu signal or observed Minecraft flight flag.
 */
public record SuitTelemetry(
        long gameTick,
        boolean equipped,
        boolean confirmedFlight,
        boolean combatEvent,
        double healthFraction,
        Double reactorFraction,
        int visibleHostiles,
        boolean collisionAhead) {

    /** Backward-compatible constructor when obstacle telemetry is unavailable. */
    public SuitTelemetry(long gameTick, boolean equipped, boolean confirmedFlight,
            boolean combatEvent, double healthFraction, Double reactorFraction,
            int visibleHostiles) {
        this(gameTick, equipped, confirmedFlight, combatEvent, healthFraction,
                reactorFraction, visibleHostiles, false);
    }

    public SuitTelemetry {
        if (gameTick < 0) throw new IllegalArgumentException("negative tick");
        if (!Double.isFinite(healthFraction) || healthFraction < 0 || healthFraction > 1)
            throw new IllegalArgumentException("healthFraction outside [0,1]");
        if (reactorFraction != null && (!Double.isFinite(reactorFraction)
                || reactorFraction < 0 || reactorFraction > 1))
            throw new IllegalArgumentException("reactorFraction outside [0,1]");
        if (visibleHostiles < 0) throw new IllegalArgumentException("negative hostile count");
    }
}
