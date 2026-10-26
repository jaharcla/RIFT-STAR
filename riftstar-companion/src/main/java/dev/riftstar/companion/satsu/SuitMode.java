package dev.riftstar.companion.satsu;

/** Mutually exclusive presentation modes; never grants or activates a Palladium power. */
public enum SuitMode {
    STANDBY, INITIALIZING, READY, FLIGHT, COMBAT, EMERGENCY, RECOVERY
}
