# RIFT//STAR progression graph

```text
riftstar:root
  -> riftstar:prismara_discovered
    -> riftstar:prismara_resource
      -> riftstar:first_colour
  -> riftstar:moonlit_misfit
  -> riftstar:honeyed_horizon
  -> riftstar:understone_rainbow
```

| Advancement | Trigger | Verified payload |
|---|---|---|
| `riftstar:root` | `minecraft:location` | Player is in `minecraft:overworld` |
| `riftstar:prismara_discovered` | `minecraft:changed_dimension` | `blue_skies:everbright` |
| `riftstar:prismara_resource` | `minecraft:inventory_changed` | `blue_skies:diopside_gem` |
| `riftstar:first_colour` | `minecraft:inventory_changed` | `kubejs:prism_lens` |
| `riftstar:moonlit_misfit` | `minecraft:changed_dimension` | `ad_astra:moon` |
| `riftstar:honeyed_horizon` | `minecraft:changed_dimension` | `the_bumblezone:the_bumblezone` |
| `riftstar:understone_rainbow` | `minecraft:location` | `alexscaves:primordial_caves` biome |

The Prism Lens recipe is registered by KubeJS with the verified inputs
`blue_skies:diopside_gem`, `ad_astra:steel_plate`, and
`minecraft:amethyst_shard`. This graph is deliberately a cue-and-artifact
slice, not a replacement for Blue Skies portal construction or Ad Astra rocket
progression. The three side threads branch independently from the root and are
optional; they record discoveries without changing native travel, gates,
bosses, or loot.
# RIFT//STAR progression threads

- **Prismara** (Blue Skies): enter Everbright, recover a diopside gem, then
  combine it with Ad Astra steel and vanilla amethyst to craft the Prism Lens.
- **Moonlit Misfit** (Ad Astra): visit the Moon through Ad Astra's own route.
- **Honeyed Horizon** (The Bumblezone): enter through the dimension's native
  discovery and portal flow.
- **Understone Rainbow** (Alex's Caves): find the Primordial Caves biome.

The three side threads are optional and independent. RIFT//STAR records
discoveries while leaving each mod's travel, gates, bosses, and loot intact.
