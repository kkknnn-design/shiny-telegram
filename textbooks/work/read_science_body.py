import json,pypdfium2 as p
from pathlib import Path
from PIL import Image,ImageDraw
b=json.loads(Path('work/textbook_sources.json').read_text(encoding='utf-8'))
for key,idx,nums in [('landau_body',3,[12,13,14,15]),('digital_body',1,[17,18,23,24]),('feynman_body',2,[54,55,209,210])]:
 d=p.PdfDocument(b[idx]['file']); ims=[]
 for n in nums:
  im=d[n].render(scale=1.6).to_pil().convert('RGB');ImageDraw.Draw(im).text((5,5),f'PDF {n+1}',fill='red');ims.append(im)
 w=max(i.width for i in ims);h=max(i.height for i in ims);s=Image.new('RGB',(w*2,h*2),'white')
 for j,im in enumerate(ims):s.paste(im,((j%2)*w,(j//2)*h))
 s.save('work/'+key+'.jpg')
