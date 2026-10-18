// Patchouli standalone modpack books in /patchouli_books use the patchouli: namespace.
// The old riftstar:fractured_atlas ID was not registered.
const ATLAS_BOOK = 'patchouli:fractured_atlas'
const ATLAS_ITEM = 'patchouli:guide_book'

function atlasBook() {
  return Item.of(ATLAS_ITEM, { 'patchouli:book': ATLAS_BOOK })
}
function hasAtlasBook(player) {
  let found = false
  player.inventory.allItems.forEach(stack => {
    if (String(stack.id) !== ATLAS_ITEM || !stack.nbt) return
    if (String(stack.nbt.getString('patchouli:book')) === ATLAS_BOOK) found = true
  })
  return found
}
PlayerEvents.loggedIn(event => {
  const player = event.player
  // Give existing players the correct book even if they have an invalid old copy.
  if (!hasAtlasBook(player)) player.give(atlasBook())
})
ServerEvents.recipes(event => {
  event.shapeless(atlasBook(), ['minecraft:book', 'minecraft:amethyst_shard'])
    .id('riftstar:fractured_atlas_manual')
})
