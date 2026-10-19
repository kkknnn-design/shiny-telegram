from pathlib import Path
import sqlite3,json
root=Path(__file__).resolve().parents[1]
state=sqlite3.connect('file:C:/Users/zheng/.codex/state_5.sqlite?mode=ro',uri=True)
history=sqlite3.connect('file:C:/Users/zheng/.codex/thread_history_1.sqlite?mode=ro',uri=True)
titles=dict(state.execute('select id,title from threads'))
records=[]
for tid in titles:
 if tid=='01a13f3f-06b9-7f82-926c-d2cc19ac6577':continue
 messages=[]
 for (raw,) in history.execute("select item_json from thread_items where thread_id=? and item_type in ('userMessage','agentMessage') order by rollout_ordinal",(tid,)):
  d=json.loads(raw)
  if d.get('type')=='userMessage':s='\n'.join(x.get('text','') for x in d.get('content',[]) if x.get('type')=='text')
  else:s=d.get('text','')
  if not s:continue
  messages.append({'id':d.get('id'),'role':d.get('type'),'text':s})
 records.append({'id':tid,'title':titles[tid] or tid,'messages':messages,'source':'只读本地对话缓存'})
(root/'work/local_corpus.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('本地会话',len(records),'消息',sum(len(r['messages']) for r in records))
