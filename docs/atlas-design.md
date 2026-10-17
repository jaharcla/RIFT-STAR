# Atlas and Rift gating design options (design-only)

Context: Ad Astra has built-in rocket-tier progression, while Blue Skies and Alex's Caves are accessible early. World Portal is already pinned in `mods.lock.json`, so these options treat it as the rift travel layer.

## Option 1 — Atlas key unlock sequence (destination-by-destination)

Atlas starts inert. Each destination unlocks after crafting or obtaining a keyed lens item, then binding it to the Atlas.

- **Player loop:** obtain key item -> bind at Atlas -> destination becomes targetable in World Portal.
- **KubeJS scope:** item definitions, recipes, advancement triggers, data tags for unlock tokens, tooltip/status feedback.
- **Companion mod scope:** server-authoritative per-player unlock state, packet sync for Atlas status UI, destination permission checks before teleport.
- **Strength:** clear progression control and easy balancing knobs.
- **Risk:** can feel checklist-heavy if keys are too grindy.

## Option 2 — Anomaly signal tiers (progress by evidence scans)

Atlas progression is tied to anomaly scans from multiple biomes/dimensions; scans increase Atlas tier and unlock destination classes.

- **Player loop:** gather scan evidence -> submit to Atlas -> tier rises -> new destination pool unlocks.
- **KubeJS scope:** scan item drops/objectives, progression-facing advancements, lightweight UI text hooks.
- **Companion mod scope:** persistent scan ledger, tier calculation, anti-spoof validation for scan submissions, route-selection rules.
- **Strength:** supports narrative investigation framing.
- **Risk:** requires stronger UX signaling to avoid confusion.

## Option 3 — Energy network routing (shared progression + per-player access)

Destinations unlock when the server's Atlas grid reaches energy thresholds, while each player still needs personal attunement.

- **Player loop:** contribute materials/energy -> global node activates -> individual attune action grants personal access.
- **KubeJS scope:** contribution recipes, machine interaction hooks, advancement messaging for global/personal states.
- **Companion mod scope:** global node state persistence, per-player attunement records, safe-arrival routing and cooldown enforcement.
- **Strength:** supports multiplayer cooperation and server events.
- **Risk:** balancing solo vs. multiplayer pace is harder.

## Open questions for maintainer

1. Should Atlas unlocks be strictly per-player, server-global, or hybrid?
2. Should Blue Skies be gated before Moon, or stay available as early narrative foreshadowing?
3. Is world travel intended to remain mostly diegetic (in-world devices) or include explicit UI menus?
4. How strict should failure states be (misjump penalties, cooldown lockouts, item loss)?
5. Should Ad Astra rocket progression remain mandatory for first access, with Atlas as shortcut only after discovery?
