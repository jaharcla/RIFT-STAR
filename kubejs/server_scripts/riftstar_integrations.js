// Optional material bridges; every native route and machine tier remains available.
ServerEvents.recipes(event => {
  // Silica glass from either Blue Skies world fits spacefaring components.
  event.replaceInput({ mod: 'ad_astra' }, 'minecraft:glass', '#riftstar:technical_glass')
  event.replaceInput({ mod: 'ad_astra' }, 'minecraft:glass_pane', '#riftstar:technical_glass_panes')

  // Sunstone supplies light, not carbon: only decorative lighting accepts it.
  event.replaceInput({ id: /^ad_astra:.*industrial_lamp$/ }, 'minecraft:glowstone_dust', '#riftstar:decorative_light_sources')
  event.replaceInput({ id: /^ad_astra:glowing_.*_pillar$/ }, 'minecraft:glowstone_dust', '#riftstar:decorative_light_sources')

  // Native Snowcap cooling ratios are 400:1600:1600:2000. Four pinheads also
  // craft one block, so processing either form returns the same amount of fuel.
  // Native ice shards remain much more efficient (25 mB in 60 ticks).
  const coolants = [
    ['blue_skies:snowcap_pinhead', 'snowcap_pinhead', 1],
    ['blue_skies:snowcap_mushroom', 'snowcap_mushroom', 4],
    ['blue_skies:snowcap_mushroom_block', 'snowcap_mushroom_block', 4],
    ['blue_skies:snowcap_mushroom_stem', 'snowcap_mushroom_stem', 5],
    // Six crafted frostmints cost one blue ice (10 mB natively) plus peppermint;
    // at 1 mB each this route cannot multiply the blue ice's fuel value.
    ['alexscaves:frostmint', 'frostmint', 1]
  ]
  coolants.forEach(coolant => {
    event.custom({
      type: 'ad_astra:cryo_freezing',
      cookingtime: 120,
      energy: 40,
      ingredient: { item: coolant[0] },
      result: { fluid: 'ad_astra:cryo_fuel', millibuckets: coolant[2] }
    }).id('riftstar:cryo_from_' + coolant[1])
  })

  // Pollen substitutes for one of the native recipe's two guano, not both.
  event.shapeless('alexscaves:fertilizer', [
    'alexscaves:guano', 'the_bumblezone:pollen_puff', 'minecraft:bone_meal'
  ]).id('riftstar:pollinated_fertilizer')

  // Spend honey residue directly on construction without creating generic slime.
  event.shapeless('minecraft:sticky_piston', [
    'minecraft:piston',
    'the_bumblezone:sticky_honey_residue',
    'the_bumblezone:sticky_honey_residue'
  ]).id('riftstar:honey_sticky_piston')
})
