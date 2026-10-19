from pathlib import Path
import json,re,hashlib,datetime,zipfile,html
from collections import defaultdict
from pypdf import PdfReader,PdfWriter
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs';B=OUT/'教材'
previous_state=json.loads((ROOT/'work/update_state.json').read_text(encoding='utf-8'))
previous_public=json.loads((OUT/'教材清单.json').read_text(encoding='utf-8'))
# Refuse to re-label old exports after the Markdown or renderer has changed.
check_file=ROOT/'work/pdf_build_sources.json'
built=json.loads(check_file.read_text(encoding='utf-8')) if check_file.exists() else {}
qa_file=ROOT/'work/qa/qa_report.json'
qa=json.loads(qa_file.read_text(encoding='utf-8')) if qa_file.exists() else {}
qa_by_file={r['file']:r for r in qa.get('stats',[])}
renderer_hash=hashlib.sha256((ROOT/'work/build_pdf.py').read_bytes()).hexdigest()
for md in sorted(B.glob('*.md')):
 check=built.get(md.name,{})
 pdf=md.with_suffix('.pdf')
 if check.get('source_sha256')!=hashlib.sha256(md.read_bytes()).hexdigest() or check.get('renderer_sha256')!=renderer_hash:
  raise SystemExit('PDF未按当前源稿和渲染器重建：'+md.name)
 if not pdf.exists() or check.get('pdf_sha256')!=hashlib.sha256(pdf.read_bytes()).hexdigest():
  raise SystemExit('PDF构建检查点不匹配：'+pdf.name)
 if qa_by_file.get(pdf.name,{}).get('sha256')!=check['pdf_sha256'] or qa.get('issues'):
  raise SystemExit('当前PDF缺少一致的页面检查：'+pdf.name)

NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)));STAMP=NOW.date().isoformat()
records={};details={}
for f in (ROOT/'work/history').glob('*.json'):
 d=json.loads(f.read_text(encoding='utf-8'))
 if 'thread' not in d:continue
 tid=d['thread']['id'];r=records.setdefault(tid,{'id':tid,'title':d['thread'].get('title') or tid,'kind':d['thread'].get('kind'),'updated_at':d['thread'].get('updatedAt'),'messages':{}})
 if d['thread'].get('title'):r['title']=d['thread']['title']
 for t in d.get('turns',[]):
  for m in t.get('items',[]):
   if m.get('type')=='userMessage':s='\n'.join(x.get('text','') for x in m.get('content',[]) if x.get('type')=='text')
   elif m.get('type')=='agentMessage':s=m.get('text','')
   else:continue
   mid=m.get('id') or hashlib.sha256(s.encode()).hexdigest()
   r['messages'][mid]=hashlib.sha256(s.encode()).hexdigest()
   placeholder=('chatgpt-content-reference' in s or 'image contents were not included' in s or s.strip()=='<EXTERNAL SESSION IMPORTED>')
   r.setdefault('message_read_states',{})[mid]='placeholder_requires_review' if placeholder else 'text_retrieved_requires_knowledge_audit'
   details.setdefault(tid,[]).append(s)
for r in json.loads((ROOT/'work/local_corpus.json').read_text(encoding='utf-8')):
 if r['id'] not in records:records[r['id']]={'id':r['id'],'title':r['title'],'kind':'codex','messages':{}}
 for m in r['messages']:
  records[r['id']]['messages'][m['id']]=hashlib.sha256(m['text'].encode()).hexdigest()
  details.setdefault(r['id'],[]).append(m['text'])

for recovery_file in (ROOT/'work/source_recovery').glob('*.json'):
 recovery=json.loads(recovery_file.read_text(encoding='utf-8'))
 tid=recovery.get('thread_id')
 if tid not in records:continue
 r=records[tid]
 for key,read_state in [('assistant_message_id','ui_body_recovered_and_audited'),('user_message_id','attachment_recovered_and_audited')]:
  mid=recovery.get(key)
  if not mid or mid not in r['messages']:continue
  r.setdefault('message_read_states',{})[mid]=read_state
  r.setdefault('recovered_messages',{})[mid]={'file':str(recovery_file.relative_to(ROOT)),
    'content_hash':recovery.get('recovered_text_sha256'),'coverage_file':'work/knowledge_coverage.json'}
 # Attachment-level reading must not be promoted to recovered assistant text.
 for audit in recovery.get('message_audits',[]):
  mid=audit.get('message_id')
  if mid not in r['messages'] or audit.get('raw_sha256')!=r['messages'][mid]:continue
  r.setdefault('message_read_states',{})[mid]=audit['read_state']
  r.setdefault('message_audits',{})[mid]={'file':str(recovery_file.relative_to(ROOT)),
    'outcome':audit['outcome'],'message_attachment_mapping':recovery.get('message_attachment_mapping')}

# Preserve verified read states and scope exclusions when message content is unchanged.
for old in previous_state.get('threads',[]):
 current=records.get(old['id'])
 if current is None:
  records[old['id']]=old
  continue
 for mid,value in old.get('message_read_states',{}).items():
  if current['messages'].get(mid)==old.get('messages',{}).get(mid):
   current.setdefault('message_read_states',{})[mid]=value
 for key in ['recovered_messages','recovery_file','exclusion_reason']:
  if key in old:current[key]=old[key]

specs=[
 ('01','C 语言程序设计','程序与表达式 → 控制流与函数 → 指针和数组 → 字符串 → 交换、排序与中位数'),
 ('02','线性代数','矩阵 → 行列式与求逆 → 消元和秩 → 方程组 → 特征值与对角化'),
 ('03','解析几何','向量 → 点积与叉积 → 平面直线 → 空间平面与直线 → 交集与自由度'),
 ('04','微积分与微分方程','极限与级数 → 泰勒展开 → 导数和积分 → 梯度 → 微分方程 → 变分'),
 ('05','大学物理','运动学 → 受力与守恒 → 碰撞 → 刚体转动 → 振动 → 拉格朗日与课程衔接'),
 ('06','概率统计与实验数据处理','频率与密度 → 正态分布 → 样本统计 → 不确定度 → 声学实验'),
 ('07','逻辑学','命题 → 蕴含与等价变换 → 范式 → 逻辑基 → 谓词和量词 → 推理'),
 ('08','数字电子技术基础','数制 → 逻辑门 → 布尔代数 → 完备基 → 组合电路 → 时序衔接'),
 ('09','俄语','性数格 → 物主代词与 свой → 数词和时间 → 构词 → 科技阅读和输出'),
 ('10','自动控制与仿真','输入输出与状态 → 反馈 → 连续模型 → 碰撞事件 → 数值仿真与报告'),
 ('11','经济学与家庭财务','货币与核算 → 名义与实际量 → 价格指数 → 收支 → 资产负债与利息'),
 ('12','数学建模与优化','问题与变量 → 线性规划 → 储能约束 → 预测 → MPC → 复核与交付'),
 ('13','计算机科学基础','信息表示 → 算法 → 逻辑与状态 → 自动机 → 图灵机 → 可计算性与复杂度')]
books=[]
for code,title,route in specs:
 route=next((x['route'] for x in previous_public.get('books',[]) if x['code']==code),route)
 md=next(B.glob(code+'_*.md'));p=md.with_suffix('.pdf');r=PdfReader(p)
 books.append({'code':code,'title':title,'route':route,'file':p.name,'source':md.name,'pages':len(r.pages),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})

state={**previous_state,'schema_version':1,'updated_at':NOW.isoformat(),'timezone':'Asia/Shanghai','automation_id':'automation','daily_time':'22:00','excluded_subjects':['国情','ОРГ','俄罗斯国情与文化'],'threads':list(records.values()),'books':books,'limitations':['历史附件和图片并非全部重新读取；无法核验的原题不复刻。','导入或远端会话只以实际可返回正文为准，不能断言账户全历史已穷尽。','参考教材已核目录及相关主题，未逐页通读数千页扫描书。','C示例已作逻辑审阅，本环境未找到C编译器，未声称已编译运行。']}
state['knowledge_coverage_file']='work/knowledge_coverage.json'
state['hashes_are_not_integration_proof']=True
(ROOT/'work/update_state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
total=sum(b['pages'] for b in books)

pdfmetrics.registerFont(TTFont('Song','C:/Windows/Fonts/simsun.ttc',subfontIndex=0))
st=ParagraphStyle('body',fontName='Song',fontSize=11,leading=19,wordWrap='CJK',alignment=1,spaceAfter=9)
small=ParagraphStyle('small',fontName='Song',fontSize=9,leading=15,wordWrap='CJK')
h=ParagraphStyle('title',fontName='Song',fontSize=27,leading=40,alignment=1,textColor=colors.HexColor('#172a3c'),spaceAfter=20)
tocrows=[[Paragraph('学科',st),Paragraph('合集页码',st),Paragraph('学习顺序',st)]]
pos=3
for b in books:
 b['combined_start']=pos;b['combined_end']=pos+b['pages']-1
 tocrows.append([Paragraph(b['title'],small),Paragraph(str(pos)+'-'+str(b['combined_end']),small),Paragraph(b['route'],small)]);pos+=b['pages']
toc=Table(tocrows,colWidths=[110,60,315],repeatRows=1)
toc.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.35,colors.HexColor('#bcc8d0')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf1f4')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
cover=ROOT/'work/combined_front.pdf'
story=[Spacer(1,45*mm),Paragraph('各学科个人教材',h),Paragraph('概念、推导与讲解型例题 · 修订版',st),Spacer(1,12*mm),Paragraph(f'{len(books)} 个学科 · 分册共 {total} 页 · {STAMP}',st),Paragraph('中文正文宋体 · 章标题与独立公式居中',st),Spacer(1,15*mm),Paragraph('程序设计 · 数学 · 物理 · 逻辑与数字技术<br/>俄语 · 控制与建模 · 经济学 · 计算机科学',st),Paragraph('按各学科的概念联系与先修关系编排，结合现有课程与 first CC 教材的相关讲解。',st),Paragraph('每日北京时间 22:00 检查新对话，有实质内容时增补到相应章节。',st),PageBreak(),Paragraph('分科目录',h),toc,Spacer(1,8*mm),Paragraph('可使用 PDF 书签跳转各册及其章节。各册页脚为本册页码，上表为合集页码。来源范围与待核实部分见随包说明。',small)]
SimpleDocTemplate(str(cover),pagesize=(595.276,841.89),leftMargin=51,rightMargin=51,topMargin=51,bottomMargin=51).build(story)
assert len(PdfReader(cover).pages)==2
w=PdfWriter();w.append(cover,import_outline=False)
for b in books:w.append(B/b['file'],outline_item=b['title'],import_outline=True)
w.add_metadata({'/Title':'各学科个人教材合集 - '+STAMP,'/Author':'个人学习教材','/Subject':'宋体正文、矢量公式、按知识依赖组织'})
combined=OUT/'各学科教材合集.pdf'
with combined.open('wb') as f:w.write(f)
assert len(PdfReader(combined).pages)==total+2

index='# 各学科教材总目录\n\n'+f'更新日期：{STAMP}。共 {len(books)} 科，分册合计 {total} 页；合集含总封面与总目录，共 {total+2} 页。国情作业不纳入。\n\n'
index+='[打开教材合集](各学科教材合集.pdf) · [下载分册与源文件包](各学科教材_分册与源文件.zip)\n\n'
for b in books:
 index+=f"## {b['code']}. {b['title']}\n\n[PDF 分册](教材/{b['file']}) · [离线阅读](教材/{b['source'].replace('.md','.html')}) · [可编辑源文件](教材/{b['source']}) · {b['pages']} 页\n\n{b['route']}。\n\n"
index+='## 阅读与更新\n\n各科均以先修关系组织，不按聊天日期排序。新内容插入对应章节，重复追问合并。每日北京时间 22:00 检查新增对话。没有新内容时不重复改写或通知。\n\n[来源覆盖与编写说明](来源覆盖与编写说明.md) · [更新日志](更新日志.md)\n'
(OUT/'教材总目录.md').write_text(index,encoding='utf-8')
public={**previous_public,'date':STAMP,'book_count':len(books),'book_pages':total,'combined_pages':total+2,'books':books,'qa':{'formula_errors':json.loads((ROOT/'work/formulas/errors.json').read_text()),'checks':'全页渲染、字体、页码、目录、边界和重点页检查；源代码未实际编译'},'automation':{'id':'automation','time':'22:00','timezone':'Asia/Shanghai','status':'ACTIVE'}}
(OUT/'教材清单.json').write_text(json.dumps(public,ensure_ascii=False,indent=2),encoding='utf-8')

# Source coverage is an editorial record; packaging must not replace it with an old template.
scope=(OUT/'来源覆盖与编写说明.md').read_text(encoding='utf-8')

log=OUT/'更新日志.md'
if not log.exists():
 log.write_text(f'''# 教材更新日志

## {STAMP} · 首版

- 建立 13 科教材，按知识先修关系组织；国情作业排除。
- 合并历史追问、已有 C 语言笔记与 first CC 参考材料，补充个性化易错点、推导、例题及练习。
- C 语言重新编排章节，把近期数组、排序和中位数放到对应基础之后。
- 统一宋体正文、清晰矢量公式、等宽代码与俄语字体，生成分册、合集、可编辑源文件与离线 HTML。
- 建立每日北京时间 22:00 的增量维护、消息哈希检查点和来源范围说明。

每日更新必须在本文件新增条目，说明实际改变的科目与知识点；没有新知识时不伪造更新。
''',encoding='utf-8')

links=''.join(f'<li><h2>{html.escape(b["title"])}</h2><p>{html.escape(b["route"])}</p><a href="教材/{b["file"]}">PDF · {b["pages"]} 页</a>　<a href="教材/{b["source"].replace(".md",".html")}">离线阅读</a>　<a href="教材/{b["source"]}">源文件</a></li>' for b in books)
hub=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>个人学科教材</title><style>body{{font-family:SimSun,serif;max-width:900px;margin:60px auto;padding:0 24px;line-height:1.9;color:#172a3c}}h1{{font-size:32px}}h2{{font-size:22px;margin-bottom:4px}}a{{color:#285675}}ul{{padding:0;list-style:none}}li{{padding:15px 0;border-top:1px solid #ccd4da}}small{{color:#637684}}</style><h1>个人学科教材</h1><p>{len(books)} 个学科 · {total} 页分册 · {STAMP}</p><p>宋体正文，规范数学排版；按知识先修关系组织，合并重复追问。国情作业已排除。</p><p><a href="各学科教材合集.pdf">打开全部教材</a>　<a href="各学科教材_分册与源文件.zip">下载分册和源文件</a></p><ul>{links}</ul><p><a href="来源覆盖与编写说明.md">来源与编写范围</a>　<a href="更新日志.md">更新日志</a></p><small>每天北京时间22:00检查增量；无新增内容时保持安静。</small></html>'''
(OUT/'教材总目录.html').write_text(hub,encoding='utf-8')
import runpy
runpy.run_path(str(ROOT/'work/finalize_pdf_exports.py'),run_name='__main__')
