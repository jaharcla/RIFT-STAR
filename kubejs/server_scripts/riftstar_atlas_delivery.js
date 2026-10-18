const ATLAS_BOOK = 'riftstar:fractured_atlas'
const ATLAS_ITEM = 'patchouli:guide_book'
const DELIVERED_KEY = 'riftstar_atlas_delivered'

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
  let player = event.player
  let delivered = player.persistentData.getBoolean(DELIVERED_KEY)
  if (!delivered || !hasAtlasBook(player)) {
    player.give(atlasBook())
    player.persistentData.putBoolean(DELIVERED_KEY, true)
  }
})
