from pypdf import PdfReader
import json
from pathlib import Path
r=PdfReader('outputs/各学科教材合集.pdf')
pmap={p.indirect_reference.idnum:i for i,p in enumerate(r.pages)}
bad=[];targets=[]
for i,p in enumerate(r.pages):
 for an in p.get('/Annots',[]):
  a=an.get_object();action=a.get('/A')
  d=a.get('/Dest') or (action.get('/D') if action else None)
  if d and isinstance(d,list):
   t=pmap.get(d[0].idnum) if hasattr(d[0],'idnum') else None
   if t is None:bad.append((i,str(d)))
   targets.append((i,t))
print(json.dumps({'links':len(targets),'bad':bad[:5],'first':targets[:8],'C_destinations':sorted(set(t for i,t in targets if i in [3,4]))},ensure_ascii=False))
assert not bad
