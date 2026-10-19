from pathlib import Path
import json,re,datetime
root=Path(__file__).resolve().parents[1]
book=root/'outputs/教材/01_C语言程序设计.md'
text=book.read_text(encoding='utf-8')
spec=[
('10-07','中位数为半整数时 double 与浮点除法各自的作用','中位数为什么要用double','平均值与整数除法','2.0','expanded_detail'),
('10-07','显示数量与零起点下标相差一，十列输出的换行条件','if ((i + 1) % 10','程序变量与显示格式','已打印数量相差一','expanded_detail'),
('10-07','max_index 保存下标及内层搜索状态','for (i = 0; i < 99','选择排序的状态变化','第二轮 i=1','expanded_detail'),
('10-07','重复值占据秩区间 L+1 到 L+E','if (less < 50','顺序统计量与中位数','L<k','reorganized_existing'),
('10-07','两个 if 在不同候选迭代中给 x 与 y 赋值','为什么x+y','顺序统计量与中位数','每一轮的 i 却不同','clarified'),
('10-07','英文注释、英文输出和 // 注释格式','printf里面','选择排序及循环不变量','Original numbers','preference_applied'),
('10-07—10-13','指针数组的比较对象与交换对象不同','第一个程序能通过换地址','同一算法的两种存储方案','比较 `*p[j]`','expanded_detail'),
('10-07—10-13','交换函数接收指针数组与两个位置','temp = p[i]','选择排序及循环不变量','int *temp = p[i]','covered'),
('10-07—10-13','局部数组与指针数组声明并不初始化元素','int a[100];','程序变量与显示格式','声明本身不会生成随机数','expanded_detail'),
('10-07—10-13','第二个程序保持普通数组且不排序','第二个就不用地址','顺序统计量与中位数','int x = 0, y = 0','covered'),
('10-13','单指针相邻交换与双指针任意交换的边界','为什么图片中的可以交换相邻','同一算法的两种存储方案','只能操作当前位置及紧邻','expanded_detail'),
('10-13','下标式 pv[0] 仍是解引用，可传两个地址','能用图片中那种数组','同一算法的两种存储方案','left[0] = right[0]','covered'),
('10-07—10-13','_CRT_SECURE_NO_WARNINGS 的工具链范围与位置','第一行再打上','程序变量与显示格式','不是 `#nowarning`','newly_explained'),
('10-15','一维数组、数组地址和二维数组行的指针类型',None,'多维数组与行指针','int (*row)[5] = An2','newly_added'),
('10-15','二维下标分两次按行和按元素寻址',None,'多维数组与行指针','*(*(An2 + i) + j)','newly_added'),
('10-15','void * 的转换、运算限制与合法比较',None,'通用对象指针与地址比较','void *pv3 = &An1[0]','newly_added'),
('10-15','连续 == 并非连等；最终更正为 &An1[0]',None,'通用对象指针与地址比较','(pv1 == pv2) == pv3','newly_added'),
('10-15','字面量与新建可写字符数组的对象差别',None,'字面量、变量与字符存储','只建立一个指向字面量的指针','newly_added'),
('10-15','字符串字面量的 C/C++ 初始化规则差别',None,'字符数组与字符串字面量','现代标准 C++','newly_added'),
('10-15','结束符、部分初始化补零与恰好满容量的例外',None,'字符编码与零结尾表示','char e[10]','newly_added'),
('10-15','%c/%d/%x/%s 的参数与显示含义',None,'字符编码与零结尾表示','ASCII 环境','newly_added'),
('10-15','字符指针数组与双下标、const 写入限制',None,'字符串指针数组与双下标','sarr[1][2]','newly_added'),
('10-15','strlen、sizeof、size_t 与转义字符计数',None,'字符串长度与对象大小','3 3 5 和 10 4 6','newly_added'),
('10-15','ls 为变量名而非数字1s或关键字',None,'字符串长度与对象大小','小写字母 l 和 s','newly_added'),
('10-15','strcpy 复制结束符及容量、重叠前提',None,'字符串的逐字符复制','区域不能重叠','newly_added'),
('10-15','strncpy 不一定补结束符，旧尾部仍在',None,'定长复制与零填充','DEFDEFG','newly_added'),
('10-15','strcpy_s 三参、strncpy_s 四参与 _countof 扩展',None,'strcpy_s、strncpy_s 与微软扩展','有四个','newly_added'),
('教学衔接','从下标复制到指针移动、赋值条件及后缀自增',None,'从下标循环到指针循环','copy_text_pointer','curriculum_bridge'),
]
sources=[]
for name in ['C_older','01a11207-26bb-7762-b3be-97f3458f0a78']:
 d=json.loads((root/'work/history'/f'{name}.json').read_text(encoding='utf-8'))
 for turn in d.get('turns',[]):
  for m in turn.get('items',[]):
   if m.get('type')=='userMessage':
    s='\n'.join(x.get('text','') for x in m.get('content',[]))
    sources.append({'thread_id':d['thread']['id'],'message_id':m.get('id'),'text':s})
items=[]
for i,(date,concept,needle,section,evidence,change) in enumerate(spec,1):
 assert evidence in text,(concept,evidence)
 found=[s for s in sources if needle and needle in s['text']]
 line=next((j for j,x in enumerate(text.splitlines(),1) if section in x and x.startswith('#')),None)
 items.append({'id':f'C-{i:03}','source_date':date,'knowledge':concept,'source_messages':[{'thread_id':x['thread_id'],'message_id':x['message_id']} for x in found],'source_thread':'6ad09922-41a8-83ed-b388-acce6c2d9cae' if date=='10-15' else None,'source_read_method':'visible_chat_page_reply' if date=='10-15' else ('history_text' if needle else 'curriculum_bridge'),'textbook_section':section,'source_file':str(book),'line':line,'evidence':evidence,'status':'integrated','change':change})
ledger={'schema_version':2,'updated_at':datetime.datetime.now().isoformat(),'meaning':'哈希仅检查消息变化；本表逐项记录实际知识覆盖，不把同名模块当作覆盖证据。','items':items,'unresolved':[{'source':'history attachments and content references','status':'not_fully_verified','detail':'今日C已从页面补读讲解正文，但原照片模糊字符仍未逐张转录；其余会话未返回正文的引用不算已读。'}],'other_subject_audits':['work/math_rewrite_audit.md','work/science_rewrite_audit.md','work/language_cs_rewrite_audit.md']}
(root/'work/knowledge_coverage.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
md='# 内容增补核对记录\n\n以具体知识变化为单位核对。下列记录位于教材之外，不作为教材章节。\n\n## C 语言\n\n'
for it in items:
 md+=f"- {it['source_date']}：{it['knowledge']}。位置：{it['textbook_section']}；状态：已融入讲解（{it['change']}）。\n"
md+='\n## 尚未核实的来源\n\n今日 C 已从实际页面补读文字讲解。原照片模糊字符及其他未返回的历史附件不计作已核实；引用占位不能等同于正文。\n'
for name in ['math_rewrite_audit','science_rewrite_audit','language_cs_rewrite_audit']:
 p=root/'work'/f'{name}.md'
 if p.exists():md+='\n---\n\n'+p.read_text(encoding='utf-8')+'\n'
(root/'outputs/内容增补核对记录.md').write_text(md,encoding='utf-8')
print('C knowledge points',len(items))
