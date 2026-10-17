# Alpha 0.1 Prismara progression

```text
riftstar:root
  -> riftstar:prismara_discovered
    -> riftstar:prismara_resource
      -> riftstar:first_colour
```

| Advancement | Trigger | Verified payload |
|---|---|---|
| `riftstar:root` | `minecraft:location` | Player is in `minecraft:overworld` |
| `riftstar:prismara_discovered` | `minecraft:changed_dimension` | `blue_skies:everbright` |
| `riftstar:prismara_resource` | `minecraft:inventory_changed` | `blue_skies:diopside_gem` |
| `riftstar:first_colour` | `minecraft:inventory_changed` | `kubejs:prism_lens` |

The Prism Lens recipe is registered by KubeJS with the verified inputs
`blue_skies:diopside_gem`, `ad_astra:steel_plate`, and
`minecraft:amethyst_shard`. This graph is deliberately a cue-and-artifact
slice, not a replacement for Blue Skies portal construction or Ad Astra rocket
progression.
