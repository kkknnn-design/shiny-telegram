import json,pypdfium2 as pdfium
from pathlib import Path
from PIL import Image,ImageDraw
books=json.loads(Path('work/textbook_sources.json').read_text(encoding='utf-8'))
for i in [1,2,3]:
 b=books[i]; d=pdfium.PdfDocument(b['file']); imgs=[]
 for n in ([12,13,14,15] if i==1 else [8,9,10,11] if i==3 else [14,15,16,17]):
  im=d[n].render(scale=1.3).to_pil().convert('RGB'); ImageDraw.Draw(im).text((10,10),f'PDF {n+1}',fill='red');imgs.append(im)
 w=max(x.width for x in imgs);h=max(x.height for x in imgs)
 sheet=Image.new('RGB',(w*2,h*2),'white')
 for j,im in enumerate(imgs): sheet.paste(im,((j%2)*w,(j//2)*h))
 sheet.save(f'work/science_source_{i}.jpg')
 print(i,b['file'],len(d))
