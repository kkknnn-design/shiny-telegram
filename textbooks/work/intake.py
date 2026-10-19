from pathlib import Path
import json,re,sqlite3
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'work/history'
records=[]
for f in H.glob('*.json'):
 d=json.loads(f.read_text(encoding='utf-8'))
 if 'thread' not in d:continue
 msgs=[]
 for t in reversed(d.get('turns',[])):
  for x in t.get('items',[]):
   if x.get('type')=='userMessage':
    s='\n'.join(a.get('text','') for a in x.get('content',[]) if a.get('type')=='text')
   elif x.get('type')=='agentMessage':s=x.get('text','')
   else:continue
   msgs.append({'id':x.get('id'),'role':x['type'],'text':s})
 records.append({'id':d['thread']['id'],'title':d['thread'].get('title') or d['thread']['id'],'messages':msgs,'page':d.get('page')})
(ROOT/'work/corpus.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'work/reading_digest.txt').open('w',encoding='utf-8') as w:
 for r in records:
  w.write('\n### '+r['id']+' '+r['title']+'\n')
  for m in r['messages']:
   if m['role']=='userMessage':w.write('问：'+m['text'][:350].replace('\n',' ')+'\n')
  answers=[m['text'] for m in r['messages'] if m['role']=='agentMessage']
  if answers:w.write('答摘录：'+answers[-1][:800].replace('\n',' ')+'\n')
print('对话',len(records),'消息',sum(len(r['messages']) for r in records),'待分页',[(r['title'],r['page']) for r in records if r['page'] and r['page'].get('hasMore')])
base=Path('C:/Users/zheng/OneDrive/first CC/output/pdf')
files=[base/'C程序设计语言_第2版_KR_中文版.pdf',base/'数字电子技术基础_第6版_阎石.pdf',base/'费曼物理学讲义/费曼物理学讲义_第1卷_新千年版_中文版.pdf',next((base/'朗道理论物理学教程').glob('*卷01*'))]
meta=[]
for n,f in enumerate(files):
 r=PdfReader(f); pages=[]
 for i in range(min(18,len(r.pages))):
  s=r.pages[i].extract_text() or ''
  if s.strip():pages.append({'pdf_page':i+1,'text':s[:10000]})
 meta.append({'file':str(f),'pages':len(r.pages),'front_matter':pages})
 doc=pdfium.PdfDocument(f)
 contact=Image.new('RGB',(1200,1000),'#dddddd');draw=ImageDraw.Draw(contact)
 for i in range(min(12,len(doc))):
  im=doc[i].render(scale=.45).to_pil().convert('RGB');im.thumbnail((290,300))
  x=(i%4)*300;y=(i//4)*333
  contact.paste(im,(x,y+20));draw.text((x+5,y+4),str(i+1),fill='black')
 contact.save(ROOT/f'work/source_{n}.jpg')
(ROOT/'work/textbook_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print('教材前部文字',[(x['file'],len(x['front_matter'])) for x in meta])
