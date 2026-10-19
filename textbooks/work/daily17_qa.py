from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw,ImageFont
dest=Path('work/qa/daily17');dest.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/simsun.ttc',14)
picks={'05':[13,14,15,16,18],'07':[10,11],'09':[6,7,14,15,16,17,18],'13':[3,4]}
for code,pages in picks.items():
 f=next(Path('outputs/教材').glob(code+'_*.pdf'));d=pdfium.PdfDocument(str(f))
 for k in pages:d[k-1].render(scale=1.6).to_pil().save(dest/(code+'_'+str(k)+'.png'))
 sheet=Image.new('RGB',(1024,((len(d)+3)//4)*370),'#d9dfe3');draw=ImageDraw.Draw(sheet)
 for i in range(len(d)):
  im=d[i].render(scale=.5).to_pil().convert('RGB');im.thumbnail((235,335))
  x=(i%4)*256;y=(i//4)*370
  draw.text((x+10,y+5),code+' / '+str(i+1),font=font,fill='black');sheet.paste(im,(x+10,y+25))
 sheet.save(dest/(code+'_contact.jpg'))
print('four contact sheets and targeted detail pages rendered')
