const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { test } = require('node:test');
const html = fs.readFileSync('album.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({ console, Map, Set, URL, Date });
vm.runInContext(script.slice(0, script.indexOf('const MAX_HISTORY')), context);
test('daily recommendation changes at local midnight, not UTC midnight', () => {
  assert.equal(vm.runInContext('getLocalDateKey(new Date(2026, 9, 3, 1, 30))', context), '2026-10-03');
});
test('search and genre filters compose and empty results stay empty', () => {
  const rows = vm.runInContext('getFilteredIndices("radiohead", "摇滚").map(i => ALBUM_DB[i])', context);
  assert.ok(rows.length > 0);
  assert.ok(rows.every(a => a.a === 'Radiohead'));
  assert.equal(vm.runInContext('getFilteredIndices("no-such-album-xyz", "全部").length', context), 0);
  assert.equal(vm.runInContext('getFilteredIndices("周杰伦", "华语").length', context), 5);
});
test('matching rejects tribute records and unrelated same-title releases', () => {
  assert.equal(vm.runInContext('isAlbumMatch({t:"OK Computer",a:"Radiohead"}, {collectionName:"OK Computer",artistName:"Vitamin String Quartet"})', context), false);
  assert.equal(vm.runInContext('isAlbumMatch({t:"OK Computer",a:"Radiohead"}, {collectionName:"OK Computer (Deluxe Edition)",artistName:"Radiohead"})', context), true);
});
test('catalog contains at least 300 unique records and a real local cover for each', () => {
  const albums = vm.runInContext('ALBUM_DB', context);
  assert.ok(albums.length >= 300, `only ${albums.length} records`);
  assert.equal(new Set(albums.map(a => a.t + '|' + a.a)).size, albums.length);
  for (const a of albums) {
    assert.ok(a.localCover && fs.existsSync(a.localCover), `missing cover: ${a.a} / ${a.t}`);
    assert.ok(fs.statSync(a.localCover).size > 1000);
  }
});
