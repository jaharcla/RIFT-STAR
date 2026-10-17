# Prismara verified facts

These facts were read directly from the pinned jars restored by
`python fetch_mods.py`. The paths below are repository-relative jar paths and
must continue to match `mods.lock.json`.

## Blue Skies

- Jar: `mods/blue_skies-1.20.1-1.3.31.jar`
- Native dimension: `data/blue_skies/dimension/everbright.json`
- Native dimension ID: `blue_skies:everbright`
- Native entry milestone: `data/blue_skies/advancements/everbright/enter.json`
  uses `minecraft:changed_dimension` with `to: "blue_skies:everbright"`.
- Native portal icon: `blue_skies:everbright_portal`
- Verified Everbright ore: `blue_skies:everbright_diopside_ore`
- Verified gem: `blue_skies:diopside_gem`
- Verified smelting recipe:
  `data/blue_skies/recipes/diopside_gem_from_smelting_everbright_diopside_ore.json`
  maps the ore to `blue_skies:diopside_gem`.

## Ad Astra

- Jar: `mods/ad_astra-forge-1.20.1-1.15.21.jar`
- Verified steel plate recipe:
  `data/ad_astra/recipes/compressing/steel_plate_from_compressing_steel_ingots.json`
- The recipe output is `ad_astra:steel_plate`; its input is the
  `ad_astra:steel_ingots` tag.

## Travel decision

The expedition uses the native Blue Skies route and only observes the
dimension change. No World Portal link or custom dimension is introduced.
Native entry and return remain owned by Blue Skies.
