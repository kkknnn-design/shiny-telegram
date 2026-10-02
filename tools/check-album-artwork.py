from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib

albums=json.loads(Path('tools/album-catalog.json').read_text(encoding='utf-8'))
groups={}
for a in albums:
    f=Path(a['localCover'])
    with Image.open(f) as im:
        im.verify()
    groups.setdefault(hashlib.sha256(f.read_bytes()).hexdigest(),[]).append(a['a']+' / '+a['t'])
duplicates=[v for v in groups.values() if len(v)>1]
print(f'{len(albums)} artwork files decoded successfully. Duplicate image groups: {duplicates}')
selected=[a for a in albums if a['a'] in ['周杰倫','陳綺貞','萬能青年旅店','竇唯','Lamp','Tatsuro Yamashita','伍佰 & China Blue','Godspeed You! Black Emperor']]
sheet=Image.new('RGB',(1050,((len(selected)+4)//5)*250),'#faf9f7')
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',12)
d=ImageDraw.Draw(sheet)
for i,a in enumerate(selected):
    x=(i%5)*210+10;y=(i//5)*250+10
    with Image.open(a['localCover']) as im:
        im=im.convert('RGB');im.thumbnail((190,190));sheet.paste(im,(x,y))
    d.text((x,y+198),a['a'][:26],font=font,fill='#262521')
    d.text((x,y+218),a['t'][:24],font=font,fill='#77756e')
sheet.save('tmp/album-cover-check.jpg')
