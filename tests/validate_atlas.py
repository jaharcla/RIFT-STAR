"""Static validation for the 1.20.1 external Patchouli modpack guide."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'patchouli_books' / 'fractured_atlas'
book = json.loads((BOOK / 'book.json').read_text(encoding='utf-8'))
assert book['name'] == 'The Fractured Atlas'
assert 'use_resource_pack' not in book or book['use_resource_pack'] is False
categories = {}
for p in (BOOK / 'en_us' / 'categories').glob('*.json'):
    categories['patchouli:' + p.stem] = json.loads(p.read_text(encoding='utf-8'))
assert len(categories) >= 2
for p in (BOOK / 'en_us' / 'entries').glob('*.json'):
    entry = json.loads(p.read_text(encoding='utf-8'))
    assert entry['category'] in categories, p
    assert entry['pages'], p
assert len(list((BOOK / 'en_us' / 'entries').glob('*.json'))) >= 6
delivery = (ROOT / 'kubejs' / 'server_scripts' / 'riftstar_atlas_delivery.js').read_text(encoding='utf-8')
assert "const ATLAS_BOOK = 'patchouli:fractured_atlas'" in delivery
assert "'patchouli:book'" in delivery
print('Fractured Atlas static validation passed')
