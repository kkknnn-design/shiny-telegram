// Run from the repository root: node tools/sync-album-covers.cjs
// Download verified artwork once so browsing does not depend on search APIs.
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const path = require('node:path');
const html = fs.readFileSync('album.html', 'utf8');
const original = vm.runInNewContext(html.match(/const ALBUMS = (\[[\s\S]*?\n\]);/)[1]);
const additions = fs.readFileSync('tools/album-additions.tsv','utf8').split(/\r?\n/)
  .filter(l => l && !l.startsWith('#')).map(l => {
    const [a,t,y,g,bio,country] = l.split('|');
    return {t,a,y:Number(y),g:g.split(','),pf:null,ry:null,rs:null,c:'',bio,country,
      w:'https://music.apple.com/'+country+'/search?term='+encodeURIComponent(a+' '+t)};
  });
const seen = new Set();
const albums = [...original, ...additions].filter(a => {
  // Two spellings of the same Bowie album occurred in the old database.
  if (a.a === 'David Bowie' && a.t === 'Ziggy Stardust') return false;
  const key = a.a+'|'+a.t;
  if (seen.has(key)) return false;
  seen.add(key); return true;
});
fs.mkdirSync('album-assets/covers', {recursive:true});
const norm = s => s.replace(/[萬樹竇長搖滾夢倫陳認無趙國]/g,c=>({'萬':'万','樹':'树','竇':'窦','長':'长','搖':'摇','滾':'滚','夢':'梦','倫':'伦','陳':'陈','認':'认','無':'无','趙':'赵','國':'国'}[c])).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase()
  .replace(/&/g,'and').replace(/[^\p{L}\p{N}]/gu,'').replace(/^the/,'');
const aliases = {
  'The Rise and Fall of Ziggy Stardust':['The Rise and Fall of Ziggy Stardust and the Spiders from Mars'],
  'Lift Your Skinny Fists...':['Lift Your Skinny Fists Like Antennas to Heaven'],
  'Money Store':['The Money Store'], 'Blond':['Blonde'],
  'I Never Loved a Man...':['I Never Loved a Man the Way I Love You'],
  'Moon & Antarctica':['The Moon & Antarctica'],
  'When the Pawn...':['When the Pawn Hits the Conflicts He Thinks Like a King'],
  'When We All Fall Asleep':['When We All Fall Asleep, Where Do We Go?'],
  'Whatever People Say I Am...':["Whatever People Say I Am, That's What I'm Not"],
  'Piñata':['Pinata'], 'Shoso Strip':['勝訴ストリップ'],
  'Muzai Moratorium':['無罪モラトリアム'], 'First Love':['First Love (Remastered 2014)'],
  'Uchu Nippon Setagaya':['宇宙 日本 世田谷'], 'For Lovers':['恋人へ'],
  'Yume':['ゆめ'], "That's Why I Gave Up on Music":['だから僕は音楽を辞めた'],
  '十一月的蕭邦':["November's Chopin"], '孫燕姿':['Sun Yan-Zi'], 'Stefanie':['Sun Yan Zi - Stefanie'],
  '陶喆':['David Tao'], '浴室':['Bathroom'], '若你碰到他':['If You See Him'],
  '愛愛愛':['This Love'], '橙月':['Orange Moon'], '生如夏花':['Life Like Summer Flowers'],
  '梵高先生':['Mr. Van Gogh (梵高先生)'], 'Cross':['Justice','† (Anniversary Edition)'],
  'Shoso Strip':['Shouso Strip -Winning Strip-','勝訴ストリップ']
};
const artistAliases = {'Hikaru Utada':['宇多田ヒカル'], 'Sheena Ringo':['椎名林檎'],
  'Ryuichi Sakamoto':['坂本龍一'], 'Haruomi Hosono':['細野晴臣'],
  'Tatsuro Yamashita':['山下達郎'], 'Taeko Onuki':['大貫妙子'],
  'Ichiko Aoba':['青葉市子'], 'Kenshi Yonezu':['米津玄師'], 'Yurushika':['ヨルシカ'],
  '伍佰 & China Blue':['伍佰','伍佰 & China Blue'],
  '萬能青年旅店':['万能青年旅店'], '竇唯':['窦唯'], '朴樹':['朴树'], '趙雷':['赵雷'],
  'Tyler, the Creator':['Tyler, The Creator'], 'Stan Getz & João Gilberto':['Stan Getz','João Gilberto'],
  'Madvillain':['Madvillain','Madlib','MF DOOM'], 'Freddie Gibbs & Madlib':['Freddie Gibbs','Madlib'],
  'Bill Evans Trio':['Bill Evans'], 'Dave Brubeck Quartet':['The Dave Brubeck Quartet'],
  '周杰倫':['Jay Chou'], '陳奕迅':['Eason Chan'], '孫燕姿':['Sun Yan-Zi','Stefanie Sun'],
  '陶喆':['David Tao'], '陳綺貞':['Cheer Chen'], '蔡健雅':['Tanya Chua'], '林俊傑':['JJ Lin'],
  '方大同':['Khalil Fong'], '朴樹':['Pu Shu','朴树'], '李志':['Li Zhi (李志)'],
  'Milton Nascimento & Lô Borges':['Milton Nascimento'],
  'Godspeed You! Black Emperor':['Godspeed You Black Emperor']};
function match(a,r) {
  if (!r.artworkUrl100) return false;
  const ar = norm(r.artistName || ''), tr = norm(r.collectionName || '');
  const am = [a.a,...(artistAliases[a.a]||[])].some(v => ar === norm(v) || ar.startsWith(norm(v)+'and'));
  const tm = [a.t,...(aliases[a.t]||[])].some(v => {
    const n = norm(v); return tr === n || tr.startsWith(n) && n.length >= 8 || norm((r.collectionName||'').replace(/\s*[([{].*$/,''))===n;
  });
  return am && tm && !/tribute|karaoke|instrumental version|live at|live from|live in/i.test(r.collectionName);
}
async function get(url) {
  for(let attempt=0;attempt<3;attempt++) {
    try {
      const r = await fetch(url,{signal:AbortSignal.timeout(18000),headers:{'User-Agent':'AlbumShelf/1.0'}});
      if(r.ok) return r;
      if(r.status!==429 && r.status<500) return null;
    } catch {}
    await new Promise(r=>setTimeout(r,1500*(attempt+1)));
  }
  return null;
}
async function download(url,file) {
  const r = await get(url); if(!r || !r.headers.get('content-type')?.startsWith('image/')) return false;
  const buf = Buffer.from(await r.arrayBuffer()); if(buf.length<1000) return false;
  fs.writeFileSync(file,buf); return true;
}
const auditPath = 'album-assets/cover-sources.json';
const audit = fs.existsSync(auditPath) ? JSON.parse(fs.readFileSync(auditPath,'utf8')) : {};
const overrides=JSON.parse(fs.readFileSync('tools/album-cover-overrides.json','utf8'));
let cursor=0,done=0,failed=[];
async function worker() {
  while(cursor<albums.length) {
    const a=albums[cursor++], key=a.a+'|'+a.t;
    const filename=crypto.createHash('sha256').update(key).digest('hex').slice(0,16)+'.jpg';
    const file=path.posix.join('album-assets/covers',filename);
    if(fs.existsSync(file)) {a.localCover=file;done++;continue;}
    let resolved=false;
    if(overrides[key]) {
      const override=overrides[key];let cover=override.url;
      if(!cover) {
        const page=await get(override.page);
        if(page){const body=await page.text();cover=body.match(/<meta[^>]*property="og:image"[^>]*content="([^"]+)"/)?.[1]?.replaceAll('&amp;','&');}
      }
      if(cover && await download(cover,file)) {
        a.localCover=file;a.c=cover;
        audit[key]={source:'verified album page',title:a.t,artist:a.a,url:cover,page:override.page,checked:'2026-10-03'};
        resolved=true;
      }
    }
    // Deezer's album search supplies artist-labelled artwork without a browser CORS dependency.
    for (const title of resolved ? [] : [a.t, ...(aliases[a.t]||[]),'']) {
      const r=await get('https://api.deezer.com/search/album?'+new URLSearchParams({q:(artistAliases[a.a]?.[0]||a.a)+' '+title,limit:'30'}));
      if(!r) continue;
      let data; try {data=await r.json();} catch {continue;}
      const matches=(data.data||[]).filter(x=>match(a,{artistName:x.artist?.name,collectionName:x.title,artworkUrl100:x.cover_big}));
      for(const record of matches) {
        if(await download(record.cover_big,file)) {
          a.localCover=file;a.c=record.cover_big;
          audit[key]={source:'Deezer',title:record.title,artist:record.artist.name,url:record.cover_big,page:record.link,checked:'2026-10-03'};
          if(a.country) a.w=record.link;
          resolved=true;break;
        }
      }
      if(resolved) break;
    }
    const country=a.country||'us';
    const queries=[[a.a,a.t,country]];
    if(artistAliases[a.a]) queries.push([artistAliases[a.a][0],aliases[a.t]?.[0]||a.t,country]);
    if(aliases[a.t]) queries.push([a.a,aliases[a.t][0],country]);
    // Single artist searches can resolve long titles and region-specific naming.
    queries.push([artistAliases[a.a]?.[0]||a.a,'',country]);
    for(const [artist,title,store] of resolved ? [] : queries) {
      const u='https://itunes.apple.com/search?'+new URLSearchParams({term:artist+' '+title,entity:'album',country:store,limit:'100'});
      const r=await get(u); if(!r) continue;
      let data;try {data=await r.json();} catch {continue;}
      const matches=(data.results||[]).filter(x=>match(a,x)).sort((x,y)=>Number(norm(y.collectionName)===norm(a.t))-Number(norm(x.collectionName)===norm(a.t)));
      for(const record of matches) {
        const cover=record.artworkUrl100.replace(/100x100bb/, '600x600bb');
        if(await download(cover,file)) {
          a.localCover=file; a.c=cover;
          audit[key]={source:'Apple Music / iTunes',title:record.collectionName,artist:record.artistName,url:cover,page:record.collectionViewUrl,checked:'2026-10-03'};
          if(a.country) a.w=record.collectionViewUrl||a.w;
          resolved=true;break;
        }
      }
      if(resolved) break;
    }
    if(!resolved && a.c && await download(a.c,file)) {
      a.localCover=file; audit[key]={source:'existing Wikimedia artwork',url:a.c,checked:'2026-10-03'}; resolved=true;
    }
    if(!resolved) {failed.push({a:a.a,t:a.t,country});console.log('UNRESOLVED '+key);}
    done++;
    if(done%20===0) console.log(`${done}/${albums.length}, unresolved ${failed.length}`);
    fs.writeFileSync(auditPath,JSON.stringify(audit,null,2)+'\n');
  }
}
(async()=>{
  console.log(`Catalog: ${albums.length} albums; additions: ${additions.length}`);
  await Promise.all(Array.from({length:3},worker));
  fs.writeFileSync('tools/album-catalog.json',JSON.stringify(albums,null,2)+'\n');
  fs.writeFileSync('tools/album-unresolved.json',JSON.stringify(failed,null,2)+'\n');
  // Only replace the data block; keep simultaneous UI edits intact.
  const current=fs.readFileSync('album.html','utf8');
  fs.writeFileSync('album.html',current.replace(/const ALBUMS = \[[\s\S]*?\n\];/,'const ALBUMS = '+JSON.stringify(albums,null,2)+';'));
  console.log(`Finished: ${albums.length-failed.length}/${albums.length} local covers. Unresolved: ${JSON.stringify(failed)}`);
})();
