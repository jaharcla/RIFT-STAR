ItemEvents.tooltip(event => {
  event.add([
    'blue_skies:crystal_glass', 'blue_skies:midnight_glass',
    'blue_skies:crystal_glass_pane', 'blue_skies:midnight_glass_pane'
  ], Text.gray('Fits Ad Astra glass components, including helmets, pipes and doors.'))
  event.add('blue_skies:sunstone_crystal', Text.gray('Also lights Ad Astra industrial lamps and glowing pillars.'))
  event.add([
    'blue_skies:snowcap_pinhead', 'blue_skies:snowcap_mushroom',
    'blue_skies:snowcap_mushroom_block', 'blue_skies:snowcap_mushroom_stem',
    'alexscaves:frostmint'
  ], Text.gray('An optional coolant for the Ad Astra Cryo Freezer.'))
  event.add('alexscaves:guano', Text.gray('Combine with pollen and bone meal for cave fertilizer.'))
  event.add('the_bumblezone:pollen_puff', Text.gray('Combine with guano and bone meal for cave fertilizer.'))
  event.add('the_bumblezone:sticky_honey_residue', Text.gray('Two residues and a piston make a sticky piston.'))
  event.add('#alexscaves:rock_candies', Text.gray('Can lure Bumblezone Honey Slimes.'))
  event.add('alexscaves:peppermint_powder', Text.gray('Can lure Bumblezone Honey Slimes.'))
})
