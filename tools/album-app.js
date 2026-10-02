// Pure catalog helpers (also exercised by the regression checks).
function getLocalDateKey(date = new Date()) {
  return [date.getFullYear(), String(date.getMonth()+1).padStart(2,'0'), String(date.getDate()).padStart(2,'0')].join('-');
}
function simpleHash(str) {
  let h=0; for(let i=0;i<str.length;i++) h=((h<<5)-h+str.charCodeAt(i))|0;
  return Math.abs(h);
}
function getDailyIndex() { return simpleHash(getLocalDateKey()) % ALBUM_DB.length; }
function normalizeCatalogText(s) {
  const traditional='倫葉間愛認風箏張懸陳綺貞陽蘇綠無與麗後萬師醜飛趙羅樹竇長搖滾夢樂詩國';
  const simplified='伦叶间爱认风筝张悬陈绮贞阳苏绿无与丽后万师丑飞赵罗树窦长摇滚梦乐诗国';
  return String(s).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/&/g,'and')
    .replace(/[\u4e00-\u9fff]/g,c=>traditional.includes(c)?simplified[traditional.indexOf(c)]:c).replace(/[^\p{L}\p{N}]/gu,'');
}
function isAlbumMatch(album, record) {
  const artist=normalizeCatalogText(album.a), ra=normalizeCatalogText(record.artistName||'');
  const title=normalizeCatalogText(album.t), rt=normalizeCatalogText(record.collectionName||'');
  return artist===ra && (title===rt || title.length>=8 && rt.startsWith(title)) && !/tribute|karaoke|instrumental version/i.test(record.collectionName||'');
}
function getFilteredIndices(query='', genre='全部') {
  const q=normalizeCatalogText(query);
  return ALBUM_DB.map((a,i)=>({a,i})).filter(({a})=>
    (!q || normalizeCatalogText([a.t,a.a,a.y].join(' ')).includes(q)) &&
    (genre==='全部' || a.g.some(g=>g.includes(genre)))) .map(({i})=>i);
}
const MAX_HISTORY=20;
let currentIndex=getDailyIndex(), isDaily=true, renderSeq=0, pageSize=12;
let history=[];
const storageKey='daily-album-history-v2';
const albumKey=a=>a.a+'|'+a.t;
try {
  const saved=JSON.parse(localStorage.getItem(storageKey)||'[]');
  if(Array.isArray(saved)) history=saved.map(k=>ALBUM_DB.findIndex(a=>albumKey(a)===k)).filter(i=>i>=0).slice(-MAX_HISTORY);
} catch {}
function remember(index) {
  history=history.filter(i=>i!==index);history.push(index);history=history.slice(-MAX_HISTORY);
  try {localStorage.setItem(storageKey,JSON.stringify(history.map(i=>albumKey(ALBUM_DB[i]))));}catch{}
}
function getGradientCSS(album) {
  const hue=simpleHash(albumKey(album))%360;
  return `linear-gradient(135deg,hsl(${hue},25%,66%),hsl(${hue},25%,33%))`;
}
function testImage(url) {
  return new Promise(resolve=> {
    const img=new Image();const timer=setTimeout(()=>finish(false),4000);
    function finish(ok){clearTimeout(timer);img.onload=img.onerror=null;resolve(ok);}
    img.onload=()=>finish(true);img.onerror=()=>finish(false);img.referrerPolicy='no-referrer';img.src=url;
  });
}
async function fetchITunesCover(album) {
  try {
    const params=new URLSearchParams({term:album.a+' '+album.t,entity:'album',country:album.country||'us',limit:'10'});
    const resp=await fetch('https://itunes.apple.com/search?'+params,{signal:AbortSignal.timeout(5000)});
    if(!resp.ok)return null;
    const data=await resp.json();const row=(data.results||[]).find(r=>isAlbumMatch(album,r));
    return row?.artworkUrl100?.replace('100x100bb','600x600bb')||null;
  }catch{return null;}
}
async function loadCover(album) {
  for(const url of [album.localCover,album.c].filter(Boolean)) {
    if(await testImage(url)) return {url,source:url===album.localCover?'本地封面':'在线封面'};
  }
  const url=await fetchITunesCover(album);
  if(url && await testImage(url))return {url,source:'Apple Music'};
  return {url:null,source:'封面暂时无法加载'};
}
function updateHistoryUI() {
  const list=document.getElementById('historyList');list.replaceChildren();
  for(const i of [...history].reverse()) {
    const a=ALBUM_DB[i],b=document.createElement('button');b.type='button';b.className='history-tag'+(i===currentIndex?' active':'');
    b.textContent=a.t;b.title=a.a+' · '+a.t;b.addEventListener('click',()=>{selectAlbum(i);renderCatalog();});list.append(b);
  }
}
function renderAlbum(index) {
  const album=ALBUM_DB[index];if(!album)return;
  const seq=++renderSeq;
  document.getElementById('albumTitle').textContent=album.t;
  document.getElementById('albumArtist').textContent=album.a;
  document.getElementById('issueNumber').firstChild.textContent=String(index+1).padStart(3,'0');
  document.getElementById('recordLabel').textContent=isDaily?'今日推荐 / SELECTED FOR TODAY':'你的发现 / A NEW DISCOVERY';
  const meta=document.getElementById('metaRow');meta.replaceChildren();
  for(const text of [...album.g,album.y+' 年']) {const b=document.createElement('span');b.className='badge'+(text.endsWith(' 年')?' badge-year':'');b.textContent=text;meta.append(b);}
  const ratings=document.getElementById('ratings');ratings.replaceChildren();
  const scores=[];
  if(album.pf)scores.push(['Pitchfork',album.pf.toFixed(1),'/ 10']);
  if(album.ry)scores.push(['RateYourMusic',album.ry.toFixed(2),'/ 5']);
  if(album.rs)scores.push(['Rolling Stone','#'+album.rs.r,album.rs.ry+' 版']);
  for(const [source,value,max] of scores){const item=document.createElement('div');item.className='rating-item';for(const [cls,text] of [['rating-source',source],['rating-score',value],['rating-max',max]]){const e=document.createElement('div');e.className=cls;e.textContent=text;item.append(e);}ratings.append(item);}
  if(!scores.length){const n=document.createElement('div');n.className='rating-note';n.textContent='编辑选曲 · 暂无已核实评分';ratings.append(n);}
  document.getElementById('bioTitle').textContent=album.country?'听赏笔记 / LISTENING NOTES':'艺术家与唱片 / ABOUT THE RECORD';
  document.getElementById('bioText').textContent=album.bio;document.getElementById('bioText').classList.remove('expanded');
  const toggle=document.getElementById('bioToggle');toggle.textContent='展开阅读';toggle.setAttribute('aria-expanded','false');
  requestAnimationFrame(()=>{const text=document.getElementById('bioText');toggle.hidden=text.scrollHeight<=text.clientHeight+1;});
  document.getElementById('btnNetease').href='https://music.163.com/#/search/m/?s='+encodeURIComponent(album.a+' '+album.t)+'&type=10';
  document.getElementById('btnDetails').href=album.w||'https://music.apple.com/us/search?term='+encodeURIComponent(album.a+' '+album.t);
  const img=document.getElementById('coverImg'),fallback=document.getElementById('fallbackCover'),bg=document.getElementById('coverBg');
  img.style.display='none';img.removeAttribute('src');fallback.style.display='flex';fallback.style.background=getGradientCSS(album);
  fallback.querySelector('.album-title').textContent=album.t;fallback.querySelector('.album-artist').textContent=album.a;
  bg.style.backgroundImage='none';img.alt=album.a+'《'+album.t+'》专辑封面';document.getElementById('coverSource').textContent='正在读取封面…';
  loadCover(album).then(result=>{
    if(seq!==renderSeq)return;
    document.getElementById('coverSource').textContent=result.source;
    if(result.url){img.onerror=()=>{if(seq!==renderSeq)return;img.style.display='none';fallback.style.display='flex';document.getElementById('coverSource').textContent='封面暂时无法加载';};img.src=result.url;img.style.display='block';fallback.style.display='none';bg.style.backgroundImage=`url("${result.url}")`;}
  });
  document.getElementById('footerDate').textContent=(isDaily?'今日推荐 · ':'正在聆听 · ')+new Date().toLocaleDateString('zh-CN');
  updateHistoryUI();
  const card=document.getElementById('card');card.classList.add('switching');setTimeout(()=>card.classList.remove('switching'),150);
}
function selectAlbum(index,scroll=false) {
  currentIndex=index;isDaily=index===getDailyIndex();remember(index);renderAlbum(index);
  if(scroll) document.getElementById('card').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});
}
function currentPool(){return getFilteredIndices(document.getElementById('albumSearch').value,document.getElementById('genreFilter').value);}
function showRandom() {
  const candidates=currentPool().filter(i=>i!==currentIndex);if(!candidates.length)return;
  const unseen=candidates.filter(i=>!history.includes(i));const pool=unseen.length?unseen:candidates;
  selectAlbum(pool[Math.floor(Math.random()*pool.length)]);
}
function renderCatalog() {
  const pool=currentPool(),grid=document.getElementById('catalogGrid');grid.replaceChildren();
  document.getElementById('catalogCount').textContent=pool.length+' / '+ALBUM_DB.length+' 张唱片';
  document.getElementById('catalogEmpty').hidden=pool.length>0;
  document.getElementById('btnMore').hidden=pool.length<=pageSize;
  document.getElementById('btnRefresh').disabled=!pool.some(i=>i!==currentIndex);
  for(const i of pool.slice(0,pageSize)) {
    const a=ALBUM_DB[i],tile=document.createElement('button');tile.type='button';tile.className='album-tile';tile.setAttribute('aria-label',a.a+' · '+a.t);
    const cover=document.createElement('span');cover.className='tile-cover';const image=document.createElement('img');image.src=a.localCover||a.c;image.alt=a.t+' 封面';image.loading='lazy';image.decoding='async';
    image.addEventListener('error',()=>{image.style.display='none';cover.style.background=getGradientCSS(a);});
    const play=document.createElement('span');play.className='tile-play';play.textContent='↗';cover.append(image,play);tile.append(cover);
    for(const [cls,text] of [['tile-title',a.t],['tile-artist',a.a],['tile-year',a.y]]){const el=document.createElement('span');el.className=cls;el.textContent=text;tile.append(el);}
    tile.addEventListener('click',()=>{selectAlbum(i,true);renderCatalog();});grid.append(tile);
  }
}
document.getElementById('btnRefresh').addEventListener('click',()=>{showRandom();renderCatalog();});
document.getElementById('btnToday').addEventListener('click',()=>{document.getElementById('albumSearch').value='';document.getElementById('genreFilter').value='全部';pageSize=12;selectAlbum(getDailyIndex());renderCatalog();});
document.getElementById('albumSearch').addEventListener('input',()=>{pageSize=12;renderCatalog();});
document.getElementById('genreFilter').addEventListener('change',()=>{pageSize=12;renderCatalog();});
document.getElementById('btnMore').addEventListener('click',()=>{pageSize+=24;renderCatalog();});
document.getElementById('bioToggle').addEventListener('click',()=>{const expanded=document.getElementById('bioText').classList.toggle('expanded');const b=document.getElementById('bioToggle');b.setAttribute('aria-expanded',String(expanded));b.textContent=expanded?'收起':'展开阅读';});
document.addEventListener('keydown',e=>{
  if(e.target.closest('input,textarea,select,button,a')||e.ctrlKey||e.metaKey||e.altKey)return;
  if(e.key===' '||e.key==='ArrowRight'){e.preventDefault();showRandom();renderCatalog();}
  if(e.key==='t'||e.key==='Home'){e.preventDefault();document.getElementById('btnToday').click();}
});
remember(currentIndex);renderAlbum(currentIndex);renderCatalog();
const isMobile=/Mobi|Android/i.test(navigator.userAgent),isFileProtocol=location.protocol==='file:';
if(isMobile||isFileProtocol){document.getElementById('mobileTip').style.display='block';document.getElementById('hostHint').style.display=isFileProtocol?'inline':'none';}
// Relative static assets keep installation reliable under GitHub Pages subpaths.
if('serviceWorker' in navigator && !isFileProtocol){navigator.serviceWorker.register('album-sw.js',{scope:'./'}).catch(()=>{});}
let deferredPrompt=null;const btnInstall=document.getElementById('btnInstall');
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferredPrompt=e;btnInstall.style.display='inline-block';});
btnInstall.addEventListener('click',async()=>{if(!deferredPrompt)return;await deferredPrompt.prompt();const result=await deferredPrompt.userChoice;if(result.outcome==='accepted')btnInstall.style.display='none';deferredPrompt=null;});
window.addEventListener('appinstalled',()=>{btnInstall.style.display='none';deferredPrompt=null;});
