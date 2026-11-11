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
const storageKey='daily-album-history-v2', themeKey='daily-album-theme';
const albumKey=a=>a.a+'|'+a.t;
const NOTES=window.ALBUM_NOTES||{};
const $=id=>document.getElementById(id);
const root=document.documentElement;
const CJK=/[぀-ヿ一-鿿]/;
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;}
try {
  const saved=JSON.parse(localStorage.getItem(storageKey)||'[]');
  if(Array.isArray(saved)) history=saved.map(k=>ALBUM_DB.findIndex(a=>albumKey(a)===k)).filter(i=>i>=0).slice(-MAX_HISTORY);
} catch {}
function remember(index) {
  history=history.filter(i=>i!==index);history.push(index);history=history.slice(-MAX_HISTORY);
  try {localStorage.setItem(storageKey,JSON.stringify(history.map(i=>albumKey(ALBUM_DB[i]))));}catch{}
}
// Theme: follow the system until the listener picks a side.
function applyTheme(theme){root.dataset.theme=theme;document.querySelector('meta[name=theme-color]').content=theme==='dark'?'#131211':'#f3eee4';}
let savedTheme=null;try{savedTheme=localStorage.getItem(themeKey);}catch{}
applyTheme(savedTheme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'));
$('btnTheme').addEventListener('click',()=>{const next=root.dataset.theme==='dark'?'light':'dark';applyTheme(next);try{localStorage.setItem(themeKey,next);}catch{}});

function getGradientCSS(album) {
  const hue=simpleHash(albumKey(album))%360;
  return `linear-gradient(135deg,hsl(${hue},25%,66%),hsl(${hue},25%,33%))`;
}
function setTint(h,s){root.style.setProperty('--h',String(Math.round(h)));root.style.setProperty('--s',Math.round(s)+'%');}
// Pull the dominant colourful hue out of the sleeve so each record tints the page.
function tintFromImage(img,album) {
  try {
    const c=document.createElement('canvas');c.width=c.height=24;
    const ctx=c.getContext('2d',{willReadFrequently:true});ctx.drawImage(img,0,0,24,24);
    const d=ctx.getImageData(0,0,24,24).data;let x=0,y=0,w=0,sat=0;
    for(let i=0;i<d.length;i+=4){
      const r=d[i]/255,g=d[i+1]/255,b=d[i+2]/255,max=Math.max(r,g,b),min=Math.min(r,g,b),delta=max-min;
      if(delta<.08)continue;
      const l=(max+min)/2,s=delta/(1-Math.abs(2*l-1)||1);
      let h=max===r?((g-b)/delta)%6:max===g?(b-r)/delta+2:(r-g)/delta+4;h*=Math.PI/3;
      const weight=s*s*(1-Math.abs(l-.5)*1.4);if(weight<=0)continue;
      x+=Math.cos(h)*weight;y+=Math.sin(h)*weight;w+=weight;sat+=s*weight;
    }
    if(w<3){setTint(simpleHash(albumKey(album))%360,7);return;}
    setTint((Math.atan2(y,x)*180/Math.PI+360)%360,Math.min(62,Math.max(26,sat/w*70)));
  } catch { setTint(simpleHash(albumKey(album))%360,34); }
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
    if(await testImage(url)) return {url,source:url===album.localCover?'首发版封面':'在线封面'};
  }
  const url=await fetchITunesCover(album);
  if(url && await testImage(url))return {url,source:'Apple Music 封面'};
  return {url:null,source:'封面暂时无法加载'};
}
function updateHistoryUI() {
  const list=$('historyList');list.replaceChildren();
  if(!history.length){list.append(el('span','history-empty','还没有记录。'));return;}
  for(const i of [...history].reverse()) {
    const a=ALBUM_DB[i],b=el('button','history-tag'+(i===currentIndex?' active':''));b.type='button';b.title=a.a+' · '+a.t;
    const img=el('img');img.src=a.localCover||a.c;img.alt='';img.loading='lazy';img.addEventListener('error',()=>{img.style.visibility='hidden';});
    b.append(img,el('span','',a.t));b.addEventListener('click',()=>{selectAlbum(i,true);renderCatalog();});list.append(b);
  }
}
function setGenre(genre) {
  const filter=$('genreFilter');filter.value=[...filter.options].some(o=>o.value===genre)?genre:'全部';
  filter.dispatchEvent(new Event('change',{bubbles:true}));
}
function renderAlbum(index) {
  const album=ALBUM_DB[index];if(!album)return;
  const seq=++renderSeq,note=NOTES[albumKey(album)],cjk=CJK.test(album.t);
  const title=$('albumTitle');title.textContent=album.t;
  title.className=(cjk?'cjk':'')+(album.t.length>(cjk?9:26)?' long':'');
  $('albumArtist').textContent=album.a;
  $('issueNumber').replaceChildren('No. ',el('b','',String(index+1).padStart(3,'0')),' / '+ALBUM_DB.length);
  $('recordLabel').textContent=isDaily?'今日推荐 · TODAY’S RECORD':'你的发现 · A NEW DISCOVERY';
  const meta=$('metaRow');meta.replaceChildren(el('span','badge badge-year',String(album.y)));
  const genres=[...$('genreFilter').options].map(o=>o.value).filter(v=>v!=='全部');
  for(const text of album.g) {
    const match=genres.find(g=>text.includes(g));
    const b=el(match?'button':'span','badge',text);
    if(match){b.type='button';b.title='在唱片架中筛选「'+match+'」';b.addEventListener('click',()=>{setGenre(match);$('catalogGrid').scrollIntoView({behavior:'smooth',block:'center'});});}
    meta.append(b);
  }
  const ratings=$('ratings');ratings.replaceChildren();
  const scores=[];
  if(album.pf)scores.push(['Pitchfork',album.pf.toFixed(1),'/ 10']);
  if(album.ry)scores.push(['RateYourMusic',album.ry.toFixed(2),'/ 5']);
  if(album.rs)scores.push(['Rolling Stone','#'+album.rs.r,album.rs.ry+' 版榜单']);
  for(const [source,value,max] of scores){const item=el('div','rating-item');item.append(el('div','rating-source',source),el('div','rating-score',value),el('div','rating-max',max));ratings.append(item);}
  ratings.hidden=!scores.length;
  $('bioText').textContent=album.bio;
  const bg=$('noteBg'),rv=$('noteRv');
  bg.textContent=note?.b||'这张唱片的背景介绍正在整理中。';rv.textContent=note?.r||'这张唱片的赏析正在整理中。';
  bg.classList.toggle('liner-empty',!note?.b);rv.classList.toggle('liner-empty',!note?.r);
  const tracks=$('keyTracks');tracks.replaceChildren();
  for(const name of note?.k||[]){const li=el('li');li.append(el('span','',name));tracks.append(li);}
  $('tracksBox').hidden=!(note?.k||[]).length;
  $('linerMeta').textContent=album.a+' · '+album.y;
  $('btnDetails').href=album.w||'https://music.apple.com/us/search?term='+encodeURIComponent(album.a+' '+album.t);
  const img=$('coverImg'),fallback=$('fallbackCover'),sleeve=$('coverWrap');
  img.style.display='none';img.removeAttribute('src');fallback.style.display='flex';fallback.style.background=getGradientCSS(album);
  fallback.querySelector('.album-title').textContent=album.t;fallback.querySelector('.album-artist').textContent=album.a;
  img.alt=album.a+'《'+album.t+'》专辑封面';$('coverSource').textContent='正在读取封面…';
  sleeve.classList.remove('ready');setTint(simpleHash(albumKey(album))%360,30);
  loadCover(album).then(result=>{
    if(seq!==renderSeq)return;
    $('coverSource').textContent=result.source+(result.url?' · '+album.y:'');
    requestAnimationFrame(()=>sleeve.classList.add('ready'));
    if(!result.url)return;
    img.onerror=()=>{if(seq!==renderSeq)return;img.style.display='none';fallback.style.display='flex';$('coverSource').textContent='封面暂时无法加载';};
    img.onload=()=>{if(seq===renderSeq)tintFromImage(img,album);};
    img.src=result.url;img.style.display='block';fallback.style.display='none';
  });
  const today=new Date().toLocaleDateString('zh-CN',{year:'numeric',month:'long',day:'numeric',weekday:'long'});
  $('mastDate').textContent=today;$('footerDate').textContent=(isDaily?'今日推荐 · ':'正在聆听 · ')+today;
  document.title=album.t+' — '+album.a+' · 每日专辑';
  try{window.history.replaceState(null,'',isDaily?location.pathname+location.search:'#'+encodeURIComponent(albumKey(album)));}catch{}
  updateHistoryUI();
  const card=$('card');card.classList.add('switching');setTimeout(()=>card.classList.remove('switching'),160);
}
function selectAlbum(index,scroll=false) {
  currentIndex=index;isDaily=index===getDailyIndex();remember(index);renderAlbum(index);
  if(scroll) $('card').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});
}
function currentPool(){return getFilteredIndices($('albumSearch').value,$('genreFilter').value);}
function showRandom() {
  const candidates=currentPool().filter(i=>i!==currentIndex);if(!candidates.length)return;
  const unseen=candidates.filter(i=>!history.includes(i));const pool=unseen.length?unseen:candidates;
  selectAlbum(pool[Math.floor(Math.random()*pool.length)]);
}
function sortPool(pool) {
  const order=$('sortOrder').value,A=ALBUM_DB;
  if(order==='new')return [...pool].sort((x,y)=>A[y].y-A[x].y);
  if(order==='old')return [...pool].sort((x,y)=>A[x].y-A[y].y);
  if(order==='az')return [...pool].sort((x,y)=>A[x].a.localeCompare(A[y].a,'zh-CN')||A[x].y-A[y].y);
  return pool;
}
function renderCatalog() {
  const pool=sortPool(currentPool()),grid=$('catalogGrid');grid.replaceChildren();
  $('catalogCount').textContent=pool.length===ALBUM_DB.length?ALBUM_DB.length+' 张唱片':pool.length+' / '+ALBUM_DB.length+' 张唱片';
  $('catalogEmpty').hidden=pool.length>0;
  $('btnMore').hidden=pool.length<=pageSize;
  $('btnRefresh').disabled=!pool.some(i=>i!==currentIndex);
  for(const chip of $('genreChips').children)chip.setAttribute('aria-pressed',String(chip.dataset.genre===$('genreFilter').value));
  pool.slice(0,pageSize).forEach((i,n)=>{
    const a=ALBUM_DB[i],tile=el('button','album-tile');tile.type='button';tile.setAttribute('aria-label',a.a+' · '+a.t);
    if(i===currentIndex)tile.setAttribute('aria-current','true');
    tile.style.animationDelay=Math.min(n%24,18)*22+'ms';
    const cover=el('span','tile-cover'),image=el('img');image.src=a.localCover||a.c;image.alt=a.t+' 封面';image.loading='lazy';image.decoding='async';
    image.addEventListener('error',()=>{image.style.display='none';cover.style.background=getGradientCSS(a);});
    cover.append(image);tile.append(cover,el('span','tile-title',a.t),el('span','tile-artist',a.a),el('span','tile-year',a.y));
    tile.addEventListener('click',()=>{selectAlbum(i,true);renderCatalog();});grid.append(tile);
  });
}
for(const option of $('genreFilter').options) {
  const chip=el('button','chip',option.value);chip.type='button';chip.dataset.genre=option.value;
  chip.addEventListener('click',()=>setGenre(option.value));$('genreChips').append(chip);
}
$('btnRefresh').addEventListener('click',()=>{showRandom();renderCatalog();});
$('btnToday').addEventListener('click',()=>{$('albumSearch').value='';$('genreFilter').value='全部';pageSize=12;selectAlbum(getDailyIndex());renderCatalog();});
$('albumSearch').addEventListener('input',()=>{pageSize=12;renderCatalog();});
$('genreFilter').addEventListener('change',()=>{pageSize=12;renderCatalog();});
$('sortOrder').addEventListener('change',()=>{pageSize=12;renderCatalog();});
$('btnMore').addEventListener('click',()=>{pageSize+=24;renderCatalog();});
document.addEventListener('keydown',e=>{
  if(e.target.closest('input,textarea,select,button,a')||e.ctrlKey||e.metaKey||e.altKey)return;
  if(e.key===' '||e.key==='ArrowRight'){e.preventDefault();showRandom();renderCatalog();}
  if(e.key==='t'||e.key==='T'||e.key==='Home'){e.preventDefault();$('btnToday').click();}
  if(e.key==='/'){e.preventDefault();$('albumSearch').focus();}
});
// A shared link (#artist|title) opens that record instead of today's pick.
try {
  const wanted=decodeURIComponent(location.hash.slice(1)),found=wanted?ALBUM_DB.findIndex(a=>albumKey(a)===wanted):-1;
  if(found>=0){currentIndex=found;isDaily=found===getDailyIndex();}
} catch {}
remember(currentIndex);renderAlbum(currentIndex);renderCatalog();
const isMobile=/Mobi|Android/i.test(navigator.userAgent),isFileProtocol=location.protocol==='file:';
if(isMobile||isFileProtocol){$('mobileTip').style.display='block';$('hostHint').style.display=isFileProtocol?'inline':'none';}
// Relative static assets keep installation reliable under GitHub Pages subpaths.
if('serviceWorker' in navigator && !isFileProtocol){navigator.serviceWorker.register('album-sw.js',{scope:'./'}).catch(()=>{});}
let deferredPrompt=null;const btnInstall=$('btnInstall');
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferredPrompt=e;btnInstall.hidden=false;});
btnInstall.addEventListener('click',async()=>{if(!deferredPrompt)return;await deferredPrompt.prompt();const result=await deferredPrompt.userChoice;if(result.outcome==='accepted')btnInstall.hidden=true;deferredPrompt=null;});
window.addEventListener('appinstalled',()=>{btnInstall.hidden=true;deferredPrompt=null;});
