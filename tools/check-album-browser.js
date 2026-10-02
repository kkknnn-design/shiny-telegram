(async()=>{
  const results=[];
  function check(condition,message){if(!condition)throw new Error(message);results.push(message);}
  const search=document.getElementById('albumSearch'),filter=document.getElementById('genreFilter');
  function input(value){search.value=value;search.dispatchEvent(new Event('input',{bubbles:true}));}
  input('周杰伦');check(document.querySelectorAll('.album-tile').length===5,'Simplified Chinese search finds all five Jay Chou records');
  filter.value='爵士';filter.dispatchEvent(new Event('change',{bubbles:true}));
  check(!document.getElementById('catalogEmpty').hidden&&document.getElementById('btnRefresh').disabled,'Search and genre intersection produces a safe empty state');
  input('no-such-album-xyz');document.getElementById('btnRefresh').click();
  check(ALBUM_DB[currentIndex]!==undefined,'Empty-result random action never selects an invalid album');
  document.getElementById('btnToday').click();
  check(currentIndex===getDailyIndex()&&search.value===''&&filter.value==='全部','Return-to-today restores the daily pick and clears filters');
  const previous=pageSize;document.getElementById('btnMore').click();
  check(pageSize>previous&&document.querySelectorAll('.album-tile').length===36,'Load-more shows the next records');
  const target=ALBUM_DB.findIndex(a=>a.a==='Radiohead'&&a.t==='In Rainbows');
  selectAlbum(0);selectAlbum(1);selectAlbum(target);
  await new Promise(resolve=>setTimeout(resolve,600));
  check(document.getElementById('coverImg').src.endsWith(ALBUM_DB[target].localCover),'Rapid switching keeps the final album artwork');
  check(JSON.parse(localStorage.getItem(storageKey)).at(-1)===albumKey(ALBUM_DB[target]),'History stores stable artist/title keys');
  check(document.documentElement.scrollWidth<=innerWidth,'Mobile layout has no horizontal overflow');
  const manifest=await (await fetch('album.webmanifest')).json();
  for(const icon of manifest.icons){const r=await fetch(icon.src);check(r.ok,icon.sizes+' install icon loads under the Pages subpath');}
  const registration=await navigator.serviceWorker.ready;
  check(new URL(registration.scope).pathname==='/shiny-telegram/','Service worker scope respects the GitHub Pages subpath');
  check((await caches.keys()).includes('daily-album-white-v1'),'Offline shell cache was created');
  return {passed:results.length,results};
})();
