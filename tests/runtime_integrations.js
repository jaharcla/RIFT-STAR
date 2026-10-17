// Disposable validation fixture. Do not ship with the pack.
// Reads the live server's parsed recipes, tags and generated loot.
ServerEvents.loaded(event => {
  let server = event.server
  let ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
  let ForgeRegistries = Java.loadClass('net.minecraftforge.registries.ForgeRegistries')
  let checks = []
  let failures = []
  let location = id => new ResourceLocation(id)
  let check = (label, condition) => {
    if (!condition) throw new Error(label)
    checks.push(label)
  }
  let section = (label, callback) => {
    try {
      callback()
      console.info('[RIFTSTAR_RUNTIME] PASS ' + label)
    } catch (error) {
      let message = label + ': ' + error
      failures.push(message)
      console.error('[RIFTSTAR_RUNTIME] FAIL ' + message)
    }
  }
  let manager = server.getRecipeManager()
  let recipe = id => {
    let result = manager.byKey(location(id))
    check('recipe registered: ' + id, result.isPresent())
    return result.get()
  }
  let itemIds = ingredient => {
    let result = []
    let iterator = ingredient.itemIds.iterator()
    while (iterator.hasNext()) result.push(String(iterator.next()))
    result.sort()
    return result
  }
  let expectedIngredient = input => {
    if (!input) return []
    if (input.item === 'minecraft:glass') return itemIds(Ingredient.of('#riftstar:technical_glass'))
    if (input.item === 'minecraft:glass_pane') return itemIds(Ingredient.of('#riftstar:technical_glass_panes'))
    return itemIds(Ingredient.of(input.item || '#' + input.tag))
  }
  let sameItems = (actual, expected, label) => check(label + ': expected ' + expected + ', got ' + actual,
    JSON.stringify(actual) === JSON.stringify(expected))
  let accepts = (ingredients, id) => {
    for (let i = 0; i < ingredients.size(); i++) {
      if (ingredients.get(i).test(Item.of(id))) return true
    }
    return false
  }
  let assertTag = (name, expected, exact) => {
    let actual = itemIds(Ingredient.of('#' + name))
    expected.forEach(id => check(name + ' contains ' + id, actual.indexOf(id) >= 0))
    if (exact) sameItems(actual, expected.slice().sort(), 'exact membership of ' + name)
  }

  section('registered item IDs and additive tag membership', () => {
    assertTag('riftstar:technical_glass', ['minecraft:glass', 'blue_skies:crystal_glass', 'blue_skies:midnight_glass'], true)
    assertTag('riftstar:technical_glass_panes', ['minecraft:glass_pane', 'blue_skies:crystal_glass_pane', 'blue_skies:midnight_glass_pane'], true)
    assertTag('riftstar:decorative_light_sources', ['minecraft:glowstone_dust', 'blue_skies:sunstone_crystal'], true)
    assertTag('alexscaves:raw_meats', ['blue_skies:venison', 'blue_skies:charscale_moki', 'blue_skies:grittle_flatfish', 'blue_skies:municipal_monkfish'], false)
    let candies = itemIds(Ingredient.of('#alexscaves:rock_candies'))
    check('native rock candy tag is nonempty', candies.length > 0)
    assertTag('the_bumblezone:mob_luring/honey_slime', candies.concat(['alexscaves:peppermint_powder']), false)
    check('Prism Lens registered', String(Item.of('kubejs:prism_lens').id) === 'kubejs:prism_lens')
    check('sunstone not added to generic coals', !Ingredient.of('#minecraft:coals').test(Item.of('blue_skies:sunstone_crystal')))
  })

  section('five parsed cryo recipes and cooling ratios', () => {
    let coolants = [
      ['snowcap_pinhead', 'blue_skies:snowcap_pinhead', 1],
      ['snowcap_mushroom', 'blue_skies:snowcap_mushroom', 4],
      ['snowcap_mushroom_block', 'blue_skies:snowcap_mushroom_block', 4],
      ['snowcap_mushroom_stem', 'blue_skies:snowcap_mushroom_stem', 5],
      ['frostmint', 'alexscaves:frostmint', 1]
    ]
    coolants.forEach(entry => {
      let id = 'riftstar:cryo_from_' + entry[0]
      let current = recipe(id)
      check(id + ' parsed into native CryoFreezingRecipe', String(current.getClass().getName()) === 'earth.terrarium.adastra.common.recipes.machines.CryoFreezingRecipe')
      sameItems(itemIds(current.input()), [entry[1]], id + ' accepts exactly its intended input')
      check(id + ' 120 ticks', current.cookingTime() === 120)
      check(id + ' 40 energy', current.energy() === 40)
      check(id + ' correct fluid', String(ForgeRegistries.FLUIDS.getKey(current.result().getFluid())) === 'ad_astra:cryo_fuel')
      check(id + ' correct mB', Number(current.result().getFluidAmount()) === entry[2])
    })
    check('pinhead block conversion cannot multiply fuel',
      Number(recipe('riftstar:cryo_from_snowcap_pinhead').result().getFluidAmount()) * 4 ===
      Number(recipe('riftstar:cryo_from_snowcap_mushroom_block').result().getFluidAmount()))
    let nativeShard = recipe('ad_astra:cryo_freezing/cryo_fuel_from_cryo_freezing_ice_shard')
    check('native ice shard route retains 25 mB', Number(nativeShard.result().getFluidAmount()) === 25)
    check('native ice shard route retains 60 ticks', nativeShard.cookingTime() === 60)
  })

  section('parsed shapeless recipes preserve costs and output counts', () => {
    let recipes = [
      ['riftstar:pollinated_fertilizer', ['alexscaves:guano', 'the_bumblezone:pollen_puff', 'minecraft:bone_meal'], 'alexscaves:fertilizer'],
      ['riftstar:honey_sticky_piston', ['minecraft:piston', 'the_bumblezone:sticky_honey_residue', 'the_bumblezone:sticky_honey_residue'], 'minecraft:sticky_piston']
    ]
    recipes.forEach(entry => {
      let current = recipe(entry[0])
      check(entry[0] + ' native shapeless recipe', String(current.getSerializer()) === String(Java.loadClass('net.minecraft.world.item.crafting.RecipeSerializer').SHAPELESS_RECIPE))
      let actual = []
      let ingredients = current.getIngredients()
      for (let i = 0; i < ingredients.size(); i++) actual.push(itemIds(ingredients.get(i)).join('|'))
      actual.sort()
      sameItems(actual, entry[1].slice().sort(), entry[0] + ' full ingredient multiset')
      let result = current.getResultItem(server.registryAccess())
      check(entry[0] + ' output', String(result.id) === entry[2])
      check(entry[0] + ' output count', result.count === 1)
    })
  })

  section('nineteen native machine and rocket progression recipes retained', () => {
    let snapshots = JSON.parse(String(JsonIO.readString('kubejs/native_recipe_snapshots.json')))
    check('native snapshots available', snapshots !== null && snapshots.length === 19)
    snapshots.forEach(snapshot => {
      let current = recipe(snapshot.id)
      let ingredients = snapshot.record ? current.ingredients() : current.getIngredients()
      check(snapshot.id + ' ingredient count retained', ingredients.size() === snapshot.inputs.length)
      snapshot.inputs.forEach((input, index) => {
        sameItems(itemIds(ingredients.get(index)), expectedIngredient(input), snapshot.id + ' native ingredient ' + index)
      })
      let result = snapshot.record ? current.result() : current.getResultItem(server.registryAccess())
      check(snapshot.id + ' native output retained', String(result.id) === snapshot.output && result.count === snapshot.count)
      if (snapshot.width) {
        check(snapshot.id + ' shape retained', current.getWidth() === snapshot.width && current.getHeight() === snapshot.height)
      }
    })
    let steel = recipe('ad_astra:alloying/steel_ingot_from_alloying_iron_ingot_and_coals')
    check('sunstone rejected by native steel alloying', !accepts(steel.ingredients(), 'blue_skies:sunstone_crystal'))
  })

  section('live decorative recipes accept sunstone and retain steel requirements', () => {
    let lamp = recipe('ad_astra:white_industrial_lamp')
    check('industrial lamp accepts glowstone', accepts(lamp.getIngredients(), 'minecraft:glowstone_dust'))
    check('industrial lamp accepts sunstone', accepts(lamp.getIngredients(), 'blue_skies:sunstone_crystal'))
    check('industrial lamp still requires steel', accepts(lamp.getIngredients(), 'ad_astra:steel_ingot'))
    let pillar = recipe('ad_astra:glowing_steel_pillar')
    check('glowing pillar accepts sunstone', accepts(pillar.getIngredients(), 'blue_skies:sunstone_crystal'))
    check('glowing pillar accepts native glowstone', accepts(pillar.getIngredients(), 'minecraft:glowstone_dust'))
    check('glowing pillar still requires its native pillar', accepts(pillar.getIngredients(), 'ad_astra:steel_pillar'))
    let pipe = recipe('ad_astra:desh_fluid_pipe')
    check('desh fluid pipe accepts crystal glass', accepts(pipe.getIngredients(), 'blue_skies:crystal_glass'))
    check('desh fluid pipe accepts midnight glass', accepts(pipe.getIngredients(), 'blue_skies:midnight_glass'))
    check('desh fluid pipe still accepts vanilla glass', accepts(pipe.getIngredients(), 'minecraft:glass'))
    let helmet = recipe('ad_astra:space_helmet')
    check('space helmet accepts crystal pane', accepts(helmet.getIngredients(), 'blue_skies:crystal_glass_pane'))
    check('space helmet accepts midnight pane', accepts(helmet.getIngredients(), 'blue_skies:midnight_glass_pane'))
    check('space helmet still accepts vanilla pane', accepts(helmet.getIngredients(), 'minecraft:glass_pane'))
    check('space helmet still requires steel plates', accepts(helmet.getIngredients(), 'ad_astra:steel_plate'))
  })

  section('loot modifier resource visibility', () => {
    let resources = server.getResourceManager()
    check('library modifier resource visible', resources.getResource(location('riftstar:loot_modifiers/library_cave_tablet.json')).isPresent())
    let manifests = resources.getResourceStack(location('forge:loot_modifiers/global_loot_modifiers.json'))
    for (let i = 0; i < manifests.size(); i++) {
      let resource = manifests.get(i)
      console.info('[RIFTSTAR_RUNTIME] GLM manifest pack=' + resource.sourcePackId())
    }
  })

  section('actual Blue Skies library loot retains books and yields primordial CaveBiome tablets', () => {
    let LootParamsBuilder = Java.loadClass('net.minecraft.world.level.storage.loot.LootParams$Builder')
    let LootContextParams = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParams')
    let LootContextParamSets = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParamSets')
    let Vec3 = Java.loadClass('net.minecraft.world.phys.Vec3')
    let tableId = location('blue_skies:chests/blinding_dungeon/library_chest')
    let table = server.getLootData().getLootTable(tableId)
    console.info('[RIFTSTAR_RUNTIME] Library table runtime ID=' + table.getLootTableId())
    check('library table carries its queried loot ID', String(table.getLootTableId()) === String(tableId))
    let params = new LootParamsBuilder(server.overworld())
      .withParameter(LootContextParams.ORIGIN, new Vec3(0, 100, 0))
      .create(LootContextParamSets.CHEST)
    let nativeRolls = 0
    let tabletRolls = 0
    let tabletCount = 0
    for (let seed = 1845; seed < 2101; seed++) {
      let stacks = table.getRandomItems(params, seed)
      let nativeCount = 0
      let currentTablets = 0
      for (let i = 0; i < stacks.size(); i++) {
        let stack = stacks.get(i)
        let id = String(stack.id)
        if (id === 'minecraft:book' || id === 'minecraft:paper' || id === 'minecraft:enchanted_book') nativeCount += stack.count
        if (id === 'alexscaves:cave_tablet') {
          currentTablets += stack.count
          check('generated tablet carries primordial CaveBiome', String(stack.nbt.getString('CaveBiome')) === 'alexscaves:primordial_caves')
        }
      }
      check('library native loot retained in roll ' + seed, nativeCount > 0)
      nativeRolls++
      if (currentTablets > 0) tabletRolls++
      tabletCount += currentTablets
    }
    check('primordial tablets generated in samples', tabletCount > 0)
    check('tablet is optional rather than guaranteed', tabletRolls < nativeRolls)
    console.info('[RIFTSTAR_RUNTIME] Loot samples=' + nativeRolls + ' tablet rolls=' + tabletRolls + ' tablets=' + tabletCount)
  })

  JsonIO.write('kubejs/riftstar-runtime-results.json', { checks: checks.length, failures: failures, passedChecks: checks })
  console.info('[RIFTSTAR_RUNTIME] COMPLETE checks=' + checks.length + ' failures=' + failures.length)
})
