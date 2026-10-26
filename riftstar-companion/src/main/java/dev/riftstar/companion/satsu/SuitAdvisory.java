package dev.riftstar.companion.satsu;

/** An event for JARVIS speech, captions, or a HUD: no direct gameplay side effects. */
public record SuitAdvisory(Level level, String code, String text) {
    public enum Level { INFO, CAUTION, CRITICAL }
    public SuitAdvisory {
        if (level == null || code == null || text == null)
            throw new IllegalArgumentException("missing advisory field");
    }
}
