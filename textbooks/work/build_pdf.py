from pathlib import Path
import re,json,html,math,textwrap,datetime
from xml.etree import ElementTree as ET
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Preformatted,XPreformatted,Table,TableStyle,Flowable,KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing,Group,Rect,Line,String
from reportlab.graphics.shapes import Path as GraphicsPath
from reportlab.graphics.svgpath import SvgPath
from reportlab.graphics import renderPDF
from reportlab.lib import textsplit as rltextsplit
from reportlab.platypus import paragraph as rlparagraph
# Include Chinese full-width punctuation in the line-start prohibition set.
rltextsplit.ALL_CANNOT_START += '，。；：？！、）》】”’％‰'
rlparagraph.ALL_CANNOT_START = rltextsplit.ALL_CANNOT_START
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/教材'
STAMP=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()
pdfmetrics.registerFont(TTFont('Song','C:/Windows/Fonts/simsun.ttc',subfontIndex=0))
pdfmetrics.registerFont(TTFont('Roman','C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('Code','C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFontFamily('Song',normal='Song',bold='Song',italic='Song',boldItalic='Song')
W,H=595.276,841.89;M=22*mm;CW=W-2*M
styles={
 'body':ParagraphStyle('body',fontName='Song',fontSize=11,leading=19,autoLeading='max',wordWrap='CJK',alignment=TA_JUSTIFY,firstLineIndent=22,spaceAfter=6,allowWidows=0,allowOrphans=0),
 'h2':ParagraphStyle('h2',fontName='Song',fontSize=17,leading=26,alignment=TA_CENTER,textColor=colors.HexColor('#172a3c'),spaceBefore=23,spaceAfter=15,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='Song',fontSize=12.5,leading=19,spaceBefore=10,spaceAfter=5,keepWithNext=True),
 'quote':ParagraphStyle('quote',fontName='Song',fontSize=10,leading=16.5,wordWrap='CJK',backColor=colors.HexColor('#f1f4f6'),borderPadding=6,spaceAfter=8),
 'code':ParagraphStyle('code',fontName='Code',fontSize=8.3,leading=12.5,backColor=colors.HexColor('#f4f5f6'),borderPadding=7,spaceBefore=8,spaceAfter=10),
 'table':ParagraphStyle('table',fontName='Song',fontSize=8.8,leading=13,autoLeading='max',wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='Song',fontSize=9,leading=15,textColor=colors.HexColor('#5a6b79'),wordWrap='CJK',spaceAfter=6),
 'center':ParagraphStyle('center',fontName='Song',fontSize=11,leading=20,alignment=TA_CENTER,spaceAfter=9),
 'h4':ParagraphStyle('h4',fontName='Song',fontSize=11.5,leading=19,spaceBefore=8,spaceAfter=5,keepWithNext=True)
}
FIDX={k.replace('\r\n','\n').replace('\r','\n'):v for k,v in json.loads((ROOT/'work/formulas/index.json').read_text(encoding='utf-8')).items()}
RASTER_INDEX=ROOT/'work/formula_rasters_v1/index.json'
RASTERS=json.loads(RASTER_INDEX.read_text(encoding='utf-8')) if RASTER_INDEX.exists() else {}
def svg_drawing(file,fontsize=12):
 e=ET.parse(file).getroot()
 if len(list(e.iter('{http://www.w3.org/2000/svg}svg')))>1:
  raise RuntimeError('Nested SVG requires node work/prepare_formula_rasters.mjs')
 v=list(map(float,e.attrib['viewBox'].split()));vx,vy,vw,vh=v;factor=fontsize/1000
 drawing=Drawing(vw*factor,vh*factor)
 base=Group();base.transform=(factor,0,0,-factor,-vx*factor,(vy+vh)*factor)
 def make(el):
  tag=el.tag.split('}')[-1];a=el.attrib
  if tag in ['g','svg']:
   ob=Group()
   for c in el:
    child=make(c)
    if child is not None:ob.add(child)
   if tag=='svg' and el is not e and 'viewBox' in a:
    bx,by,bw,bh=map(float,a['viewBox'].split())
    sw=float(a.get('width',bw));sh=float(a.get('height',bh))
    sx,sy=sw/bw,sh/bh
    if a.get('preserveAspectRatio','xMidYMid meet')!='none':sx=sy=min(sx,sy)
    viewport=Group();viewport.transform=(sx,0,0,sy,float(a.get('x',0))-bx*sx+(sw-bw*sx)/2,float(a.get('y',0))-by*sy+(sh-bh*sy)/2)
    clip=GraphicsPath(isClipPath=1,fillColor=None,strokeColor=None,strokeWidth=0);clip.moveTo(bx,by);clip.lineTo(bx+bw,by);clip.lineTo(bx+bw,by+bh);clip.lineTo(bx,by+bh);clip.closePath()
    clipped=Group();clipped.add(clip);clipped.add(ob)
    viewport.add(clipped);ob=viewport
  elif tag=='path':
   if not a.get('d','').strip():return None
   ob=SvgPath(a.get('d',''),fillColor=None if a.get('fill')=='none' else colors.black,strokeColor=colors.black if a.get('stroke') not in [None,'none'] else None,strokeWidth=float(a.get('stroke-width',1))).provideNode()
  elif tag=='rect':ob=Rect(float(a.get('x',0)),float(a.get('y',0)),float(a.get('width',0)),float(a.get('height',0)),fillColor=None if a.get('fill')=='none' else colors.black,strokeColor=colors.black if a.get('stroke') not in [None,'none'] else None,strokeWidth=float(a.get('stroke-width',1)))
  elif tag=='line':ob=Line(*[float(a.get(k,0)) for k in ['x1','y1','x2','y2']],strokeColor=colors.black)
  elif tag=='text':
   text=''.join(el.itertext());size=float(re.sub('[a-zA-Z]','',a.get('font-size','884')))
   ob=Group();ob.translate(float(a.get('x',0)),float(a.get('y',0)));ob.scale(1,-1)
   ob.add(String(0,0,text,fontName='Song' if re.search('[\u4e00-\u9fff]',text) else 'Roman',fontSize=size,fillColor=colors.black))
  else:return None
  tr=a.get('transform','')
  if tr:
   g=Group()
   for op,s in re.findall(r'([a-zA-Z]+)\(([^)]*)\)',tr):
    z=[float(x) for x in re.findall(r'-?\d*\.?\d+(?:e[-+]?\d+)?',s)]
    if op=='translate':g.translate(z[0],z[1] if len(z)>1 else 0)
    elif op=='scale':g.scale(z[0],z[1] if len(z)>1 else z[0])
    elif op=='matrix':g.transform=tuple(z)
    elif op=='rotate':g.rotate(z[0])
   g.add(ob);return g
  return ob
 base.add(make(e));drawing.add(base);return drawing
class Formula(Flowable):
 def __init__(self,tex):
  super().__init__();name=FIDX[tex.strip()];self.raster=RASTERS.get(name)
  if self.raster:
   self.nw=self.raster['viewbox_width']*12/1000
   self.nh=self.raster['viewbox_height']*12/1000
  else:
   self.d=svg_drawing(ROOT/'work/formulas'/name);self.nw=self.d.width;self.nh=self.d.height
  self.spaceBefore=7;self.spaceAfter=9
 def wrap(self,aw,ah):
  self.scale=min(1,aw/self.nw) if self.nw else 1
  self.width=aw;self.height=self.nh*self.scale+3
  return self.width,self.height
 def draw(self):
  self.canv.saveState()
  x=(self.width-self.nw*self.scale)/2
  if self.raster:
   self.canv.drawImage(str(ROOT/'work/formula_rasters_v1'/self.raster['file']),
    x,2,width=self.nw*self.scale,height=self.nh*self.scale,mask='auto')
  else:
   self.canv.translate(x,2);self.canv.scale(self.scale,self.scale);renderPDF.draw(self.d,self.canv,0,0)
  self.canv.restoreState()
class BookDoc(BaseDocTemplate):
 def __init__(self,file,title):
  super().__init__(str(file),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=22*mm,bottomMargin=22*mm,title=title,author='个人学习教材',allowSplitting=True)
  self.booktitle=title;self.addPageTemplates(PageTemplate(id='main',frames=[Frame(M,22*mm,CW,H-44*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.footer))
 def footer(self,c,d):
  if d.page==1:return
  c.saveState();c.setFont('Song',8);c.setFillColor(colors.HexColor('#61717e'));c.drawCentredString(W/2,H-13*mm,self.booktitle);c.setLineWidth(.25);c.setStrokeColor(colors.HexColor('#b9c3ca'));c.line(M,H-16*mm,W-M,H-16*mm);c.drawCentredString(W/2,12*mm,str(d.page));c.restoreState()
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and getattr(f,'toc',False):
   key='h'+str(self.seq.nextf('heading'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,level=0);self.notify('TOCEntry',(0,f.getPlainText(),self.page,key))
def inline(s,maxwidth=CW):
 code_tokens=[]
 def code_capture(m):
  code_tokens.append(m[1]);return 'CODEPROTECT'+str(len(code_tokens)-1)+'END'
 s=re.sub(r'`([^`]+)`',code_capture,s)
 math_tokens=[]
 def capture(m):
  tex=m[1].strip();name=FIDX.get(tex)
  if not name:return tex
  raster=RASTERS.get(name)
  if raster:
   dest=ROOT/'work/formula_rasters_v1'/raster['file']
   dw=raster['viewbox_width']*10.5/1000
   dh=raster['viewbox_height']*10.5/1000
  else:
   cache=ROOT/'work/inline_math_v6';cache.mkdir(exist_ok=True)
   dest=cache/(name+'.png');d=svg_drawing(ROOT/'work/formulas'/name,fontsize=10.5)
   if not dest.exists():
    import io,pypdfium2 as pdfium
    from reportlab.pdfgen import canvas
    b=io.BytesIO();c=canvas.Canvas(b,pagesize=(d.width+2,d.height+2));renderPDF.draw(d,c,1,1);c.showPage();c.save()
    pdf=pdfium.PdfDocument(b.getvalue());pdf[0].render(scale=4).to_pil().save(dest)
   dw=d.width+2;dh=d.height+2
  token='MATHPLACEHOLDER'+str(len(math_tokens))+'END'
  scale=min(1,maxwidth/dw)
  math_tokens.append(f'<img src="{dest.as_posix()}" width="{dw*scale:.3f}" height="{dh*scale:.3f}" valign="middle"/>')
  return token
 s=re.sub(r'\\\((.*?)\\\)',capture,s)
 s=s.replace('−','-').replace('—','-').replace('–','-')
 s=html.escape(s)
 subs=dict(zip('₀₁₂₃₄₅₆₇₈₉ᵢⱼₖₙₓₜₚₕₛᵤₐₘᵣᵧᶻᵥᴄᴇ','0123456789ijknxtphsuamryzvCE'))
 sups=dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ⁿᵗ','0123456789-+nt'))
 s=re.sub('['+''.join(subs)+']+',lambda m:'<sub>'+''.join(subs[x] for x in m[0])+'</sub>',s)
 s=re.sub('['+''.join(sups)+']+',lambda m:'<super>'+''.join(sups[x] for x in m[0])+'</super>',s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s)
 # Render Cyrillic with a proportional serif face, keeping Chinese in SimSun.
 s=re.sub(r'([А-Яа-яЁё][А-Яа-яЁё\s/-]*)',r'<font name="Roman">\1</font>',s)
 for i,c in enumerate(code_tokens):s=s.replace('CODEPROTECT'+str(i)+'END','<font name="Code" size="9">'+code_text(c)+'</font>')
 for i,t in enumerate(math_tokens):s=s.replace('MATHPLACEHOLDER'+str(i)+'END',t)
 return s
def code_text(s):
 s=html.escape(s)
 return re.sub(r'([\u4e00-\u9fff，。；：（）【】、]+)',r'<font name="Song">\1</font>',s)
def paragraph(s,style='body'):
 return formatted_paragraph(inline(s),styles[style])

def formatted_paragraph(markup,style):
 # Give inline images an object-replacement character for CJK line breaking.
 # Their actual width/drawing still comes from cbDefn; no glyph is printed.
 p=Paragraph(markup,style)
 for frag in p.frags:
  if not frag.text and getattr(getattr(frag,'cbDefn',None),'kind',None)=='img':
   frag.text='\ufffc'
 return p
def story_for(text,title):
 lines=text.splitlines();subtitle=next((x for x in lines[1:] if x.strip() and not x.startswith('#')),'中文学习教材')
 story=[Spacer(1,48*mm),Paragraph('个人学科教材 · 修订版',styles['center']),Spacer(1,12*mm),Paragraph(title,ParagraphStyle('cover',fontName='Song',fontSize=29,leading=44,alignment=TA_CENTER,textColor=colors.HexColor('#172a3c'))),Spacer(1,9*mm),paragraph(subtitle,'center'),Spacer(1,28*mm),paragraph('宋体正文 · 数学公式排版','center'),paragraph('概念、推导与讲解型例题','center'),paragraph(STAMP,'center'),PageBreak()]
 toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='Song',fontSize=10.5,leading=18,leftIndent=0,firstLineIndent=0,spaceBefore=3)];story +=[Paragraph('目录',styles['h2']),toc,PageBreak()]
 i=1;sub_skipped=False
 while i<len(lines):
  s=lines[i].strip()
  if not s:i+=1;continue
  if not sub_skipped and s==subtitle:sub_skipped=True;i+=1;continue
  if s.startswith('```'):
   code=[];i+=1
   while i<len(lines) and not lines[i].strip().startswith('```'):code.append(lines[i].expandtabs(4));i+=1
   code=[part for line in code for part in (textwrap.wrap(line,width=80,replace_whitespace=False,drop_whitespace=False) or [''])]
   i+=1
   block=XPreformatted(code_text('\n'.join(code)),styles['code'])
   story.append(KeepTogether([block]) if len(code)<=38 else block)
   continue
  if s in ['\\[','$$']:
   close='\\]' if s=='\\[' else '$$';tex=[];i+=1
   while i<len(lines) and lines[i].strip()!=close:tex.append(lines[i]);i+=1
   i+=1;story.append(Formula('\n'.join(tex)));continue
  if s.startswith('## '):
   p=paragraph(s[3:],'h2');p.toc=True;story.append(p);i+=1;continue
  if s.startswith('### '):story.append(paragraph(s[4:],'h3'));i+=1;continue
  if s.startswith('#### '):story.append(paragraph(s[5:],'h4'));i+=1;continue
  if s.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',c) for c in cells):rows.append(cells)
    i+=1
   n=max(map(len,rows))
   # Give prose columns more room than short labels.
   scores=[max(4,min(35,max(len(re.sub('<[^>]+>','',row[j] if j<len(row) else '')) for row in rows))) for j in range(n)]
   widths=[CW*x/sum(scores) for x in scores]
   data=[[formatted_paragraph(inline(c,widths[j]-10),styles['table']) for j,c in enumerate(row+['']*(n-len(row)))] for row in rows]
   t=Table(data,colWidths=widths,repeatRows=1,hAlign='CENTER')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf1f4')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#bdc8d0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([t,Spacer(1,6)]);continue
  if s=='---':story.append(Spacer(1,7));i+=1;continue
  if s.startswith('>'):story.append(paragraph(s.lstrip('> '),'quote'));i+=1;continue
  if s.startswith('- '):story.append(paragraph('• '+s[2:]));i+=1;continue
  para=[s];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#{1,4} |\||```|\\\[|\$\$|> |- )',lines[i].strip()):para.append(lines[i].strip());i+=1
  story.append(paragraph(' '.join(para)))
 return story
if __name__=='__main__':
 import sys
 files=sorted(OUT.glob('*.md'));filters=sys.argv[1:]
 for f in files:
  if filters and not any(f.name.startswith(p) for p in filters):continue
  text=f.read_text(encoding='utf-8');title=text.splitlines()[0][2:];doc=BookDoc(f.with_suffix('.pdf'),title);doc.multiBuild(story_for(text,title));print(f.name,doc.page)
  checkpoints=ROOT/'work/pdf_build_sources.json'
  built=json.loads(checkpoints.read_text(encoding='utf-8')) if checkpoints.exists() else {}
  import hashlib
  built[f.name]={'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),
   'pdf_sha256':hashlib.sha256(f.with_suffix('.pdf').read_bytes()).hexdigest(),
   'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
   'built_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()}
  checkpoints.write_text(json.dumps(built,ensure_ascii=False,indent=2),encoding='utf-8')
