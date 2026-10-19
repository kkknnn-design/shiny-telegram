from pathlib import Path
import json,re,zipfile,hashlib,datetime
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium
from PIL import Image,ImageDraw,ImageFont
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs';B=OUT/'教材';Q=ROOT/'work/qa';Q.mkdir(exist_ok=True)
stats=[];thumbs=[];issues=[]
for f in sorted(B.glob('*.pdf')):
 r=PdfReader(f);assert not r.is_encrypted;doc=pdfium.PdfDocument(f)
 with pdfplumber.open(f) as pl:
  for k,p in enumerate(pl.pages):
   chars=p.chars
   # Header/footer have independent margins; body allows one hanging punctuation.
   bodychars=[c for c in chars if c['text'].strip() and not (c['size']<=8.1 and (25<c['top']<50 or c['top']>790))]
   bad=[c for c in bodychars if c['x0']<55 or c['x1']>544 or c['top']<50 or c['bottom']>787]
   if bad:issues.append({'file':f.name,'page':k+1,'boundary':[(c['text'],round(c['x0']),round(c['x1']),round(c['top'])) for c in bad[:12]]})
   if '\ufffd' in (p.extract_text() or ''):issues.append({'file':f.name,'page':k+1,'replacement_char':True})
 for k in range(len(doc)):
  im=doc[k].render(scale=.43).to_pil().convert('RGB');im.thumbnail((236,335));thumbs.append((f.stem,k+1,im.copy()))
 stats.append({'file':f.name,'title':(r.metadata.title if r.metadata else f.stem),'pages':len(r.pages),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 # Detail pages to review formulas, code, and Russian.
 picks=[min(3,len(doc)-1)]
 if f.name.startswith('01'):picks=[3,14,29,33]
 if f.name.startswith('05'):picks=[3,5,6]
 if f.name.startswith('09'):picks=[2,3,4]
 for k in picks:doc[k].render(scale=1.5).to_pil().save(Q/f'{f.stem}_{k+1}.png')
font=ImageFont.truetype('C:/Windows/Fonts/simsun.ttc',12)
for start in range(0,len(thumbs),16):
 sheet=Image.new('RGB',(1024,1480),'#d9dfe3');draw=ImageDraw.Draw(sheet)
 for j,(name,p,im) in enumerate(thumbs[start:start+16]):
  x=(j%4)*256;y=(j//4)*370;draw.text((x+4,y+5),name[:17]+' / '+str(p),font=font,fill='#172a3c');sheet.paste(im,(x+10,y+26))
 sheet.save(Q/f'contact_{start//16+1:02}.jpg')
(Q/'qa_report.json').write_text(json.dumps({'stats':stats,'pages':len(thumbs),'issues':issues},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'books':len(stats),'pages':len(thumbs),'issue_count':len(issues),'issues_preview':issues[:3]},ensure_ascii=False))
