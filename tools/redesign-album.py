from pathlib import Path
import re, json, math
from PIL import Image, ImageDraw, ImageFilter

root=Path('.')
html=Path('album.html').read_text(encoding='utf-8')
catalog=re.search(r'const ALBUMS = (\[[\s\S]*?\n\]);',html).group(0)
style=Path('tools/album-style.css').read_text(encoding='utf-8')
body=Path('tools/album-body.html').read_text(encoding='utf-8')
app=Path('tools/album-app.js').read_text(encoding='utf-8')
head='''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer"><meta name="theme-color" content="#faf9f7">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="每日专辑"><meta name="description" content="每日专辑推荐，支持专辑搜索、风格筛选与浏览记录。">
<link rel="icon" type="image/svg+xml" href="album-assets/icon.svg">
<link rel="apple-touch-icon" href="album-assets/icon-180.png"><link rel="manifest" href="album.webmanifest">
<title>每日专辑</title><style>'''
data_helpers='''
const seen = new Set();
const ALBUM_DB = ALBUMS.filter(a => {const key=a.t+'|'+a.a;if(seen.has(key))return false;seen.add(key);return true;});
'''
Path('album.html').write_text(head+style+'</style></head><body>\n'+body+'\n<script>\n'+catalog+data_helpers+app+'\n</script></body></html>\n',encoding='utf-8')

assets=Path('album-assets');assets.mkdir(exist_ok=True)
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<defs><linearGradient id="vinyl" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#464440"/><stop offset="1" stop-color="#181816"/></linearGradient><filter id="shadow" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#3d382d" flood-opacity=".13"/></filter></defs>
<rect width="512" height="512" rx="112" fill="#faf9f7"/>
<g filter="url(#shadow)"><circle cx="319" cy="233" r="139" fill="url(#vinyl)"/><g fill="none" stroke="#79756c" stroke-opacity=".3" stroke-width="2"><circle cx="319" cy="233" r="121"/><circle cx="319" cy="233" r="111"/><circle cx="319" cy="233" r="100"/><circle cx="319" cy="233" r="88"/></g><circle cx="319" cy="233" r="44" fill="#d96b56"/><circle cx="319" cy="233" r="9" fill="#faf9f7"/>
<g transform="rotate(-12 207 294)"><rect x="88" y="177" width="238" height="238" rx="10" fill="white" stroke="#e4e1db" stroke-width="3"/><path d="M108 195h65" stroke="#e9e6df" stroke-width="5" stroke-linecap="round"/><circle cx="207" cy="296" r="39" fill="#f4f1eb"/><circle cx="207" cy="296" r="27" fill="#252522"/><circle cx="207" cy="296" r="9" fill="#d96b56"/><path d="M108 390h48" stroke="#d96b56" stroke-width="5" stroke-linecap="round"/></g></g></svg>'''
(assets/'icon.svg').write_text(svg,encoding='utf-8')
# Render the same geometric design at high resolution for home-screen PNG icons.
s=3
image=Image.new('RGB',(512*s,512*s),'#faf9f7');d=ImageDraw.Draw(image)
def box(coords):return tuple(int(v*s) for v in coords)
d.ellipse(box((180,94,458,372)),fill='#252522')
for r in [121,111,100,88]:d.ellipse(box((319-r,233-r,319+r,233+r)),outline='#484741',width=2*s)
d.ellipse(box((275,189,363,277)),fill='#d96b56');d.ellipse(box((310,224,328,242)),fill='#faf9f7')
sleeve=Image.new('RGBA',(512*s,512*s));sd=ImageDraw.Draw(sleeve)
sd.rounded_rectangle(box((88,177,326,415)),radius=10*s,fill='white',outline='#e4e1db',width=3*s)
sd.line(box((108,195,173,195)),fill='#e9e6df',width=5*s)
sd.ellipse(box((168,257,246,335)),fill='#f4f1eb');sd.ellipse(box((180,269,234,323)),fill='#252522');sd.ellipse(box((198,287,216,305)),fill='#d96b56');sd.line(box((108,390,156,390)),fill='#d96b56',width=5*s)
sleeve=sleeve.rotate(12,resample=Image.Resampling.BICUBIC,center=(207*s,294*s))
shadow=Image.new('RGBA',sleeve.size);shadow.putalpha(sleeve.getchannel('A').point(lambda v:int(v*.10)));shadow=shadow.filter(ImageFilter.GaussianBlur(10*s))
image.paste(shadow,(0,10*s),shadow);image.paste(sleeve,(0,0),sleeve)
for size in [180,192,512]:image.resize((size,size),Image.Resampling.LANCZOS).save(assets/f'icon-{size}.png')
manifest={'id':'./album.html','name':'每日专辑','short_name':'每日专辑','description':'专辑推荐与曲库浏览','lang':'zh-CN','start_url':'./album.html','scope':'./','display':'standalone','background_color':'#faf9f7','theme_color':'#faf9f7','icons':[{'src':f'album-assets/icon-{size}.png','sizes':f'{size}x{size}','type':'image/png','purpose':'any maskable'} for size in [192,512]]}
Path('album.webmanifest').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Updated album.html and white vinyl icon assets.')
