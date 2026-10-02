const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=process.cwd();
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.webmanifest':'application/manifest+json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.json':'application/json'};
http.createServer((req,res)=>{
  let name;try{name=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/shiny-telegram\//,'/').slice(1);}catch{res.writeHead(400).end();return;}
  if(!name)name='album.html';
  if(!['album.html','album.webmanifest','album-sw.js'].includes(name)&&!/^album-assets\/[a-zA-Z0-9/_.-]+$/.test(name)){res.writeHead(404).end();return;}
  const file=path.join(root,name);
  fs.readFile(file,(error,data)=>{if(error){res.writeHead(404).end();return;}res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':'no-cache'});res.end(data);});
}).listen(8787,'127.0.0.1',()=>console.log('Album preview: http://127.0.0.1:8787/album.html'));
