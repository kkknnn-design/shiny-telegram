from pathlib import Path
import json,hashlib,datetime,re
ROOT=Path(__file__).resolve().parents[1]; B=ROOT/'outputs/教材'; W=ROOT/'work'; OUT=ROOT/'outputs'
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
REV='2026-10-17-daily-01'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def insert(code,anchor,fragment):
 p=next(B.glob(code+'_*.md'));s=p.read_text(encoding='utf-8');f=(W/fragment).read_text(encoding='utf-8').strip()
 assert f.splitlines()[0] not in s, 'already inserted'
 assert s.count(anchor)==1
 p.write_text(s.replace(anchor,f+'\n\n'+anchor),encoding='utf-8')
insert('05','## 12. 广义坐标与拉格朗日方程','daily17_physics.md')
insert('07','## 9. 量词推演、三段论与存在条件','daily17_logic.md')
insert('09','## 3. 物主代词与修饰语一致','daily17_russian_grammar.md')
insert('09','## 10. 科技句子的逐层阅读','daily17_russian_terms.md')
insert('09','## 11. 科技叙述与报告衔接','daily17_russian_reading.md')
insert('13','## 2. 位置记数法与进制转换','daily17_cs.md')
p=next(B.glob('07_*.md'));s=p.read_text(encoding='utf-8').replace('在带通常顺序的有限集合中通常为假，因为有限集合有最大元。','在带通常顺序的非空有限集合中为假，因为这样的集合有最大元，而最大元没有更大的域内元素。');p.write_text(s,encoding='utf-8')
p=next(B.glob('05_*.md'));s=p.read_text(encoding='utf-8');s+='\n2026-10-17增补另实际视觉阅读first CC朗道《力学》本地PDF第38、73—74页：一维运动先由守恒能量分离变量，自由振动先在稳定平衡位置展开势能，再引入正弦、余弦解与振幅、相位，最后联系能量。第11.2—11.4节按这一概念衔接独立展开，另补积分分支和竖直弹簧等课程延伸；不照搬书中习题。\n';p.write_text(s,encoding='utf-8')

ids=['6ad25723-e714-83ed-8e25-fb8e74bee65e','6ad2520c-6fb0-83eb-b018-111f63194c93','6ad22731-6000-83ed-8d54-e45b4e2cbe2f','6ad21cbd-9afc-83eb-9c87-361f4831cc36','6ad1cf65-7a10-83ed-9c7e-891a26dfdb38','6ad1b313-dca4-83ed-94d3-3a15602a1199']
excerpts=[
 ['IMG_8070.jpeg','原教材印刷第21页：同一信息的解释依赖接收者；认识功能对应产生、表示、存储、感知，交际功能对应传递、分配，管理功能联系有目的的系统行为。底部提问不收入教材。'],
 ['IMG_8069.jpeg','原教材印刷第20页：Понятие информации；说明多学科中的信息概念、信源与接收者、信号、连续与离散；不把其哲学式定义认定为所有学科的唯一结论。'],
 ['IMG_8068.jpeg','可辨认作业板书：с. 20–21 текст «Понятие информации»；прочитать до конца и перевести；дописать до конца план текста；вопросный и тезисный。截断部分不补猜。'],
 ['IMG_1C98CB1A-B1FC-4D2F-ADD0-3483E73C52A0.jpeg','显示教材第20页信号、连续、离散段落，与完整页照片交叉核对；被人物遮挡部分不单独转录。'],
 ['IMG_8066.jpeg','显示教材第20页источник、приёмник与信息传递段落，与完整页照片交叉核对；左侧遮挡内容不补猜。'],
 ['IMG_F77E4A4D-8A47-41BE-B10C-6A8F86D55559.jpeg','笔记可辨认：проявляется информация только при взаимодействии объектов, причём обмен информацией может совершаться ...；представляют собой организованную структуру；обмен ... в животном и растительном мире, между живой и неживой природой, людьми и устройствами。原笔记及中文旁注不作为科学结论直接复制。'],
 ['IMG_03718D4F-BCA4-418E-B387-90E6EC781369.jpeg','同一笔记的局部照片：проявляется информация только при взаимодействии объектов, причём обмен информацией。与另一张合读，不据局部照片推定完整句末。'],
 ['IMG_D6118C21-19F5-4EDF-B2CE-8AF853E2A3C0.jpeg','原图清楚显示整数后继的∀x∃y与∃y∀x例子、量词否定、喜欢书的否定、受限全称用蕴含与受限存在用合取。既有正文已覆盖这些直接知识，另作讲解延伸。'],
 ['IMG_7968.jpeg','科技俄语课本要求识别一般科学概念及定义、构成Adj+N与N+属格N短语。可见21词：категория, явление, предмет, объект, знак, атрибут, факт, событие, критерий, процесс, структура, система, концепция, знания, элемент, материя, энергия, функция, семантика, метод, теория。提取术语与构词知识，不保留作业题或外部搜索任务。'],
 ['IMG_C06D0818-0574-47C3-807D-3EBDAB40334A.jpeg','可辨认x=x0 cos(ω0t)、v=-x0ω0 sin(ω0t)、势能∝cos²、动能∝sin²以及能量随时间图；边缘截断公式不补猜。'],
 ['IMG_C49CDBE5-F32A-48B7-8393-66FD82F91B4A.jpeg','可辨认arcsin(x/x0)=±ω0t+π/2、x=x0 cos(ω0t)、ω0=√(k/m)、Ek+Ep=E0和功微元。反正弦主值与方向分支须在新教材中明确限制。'],
 ['IMG_7AD9073D-1C6B-45A7-8157-511D5CDE0693.jpeg','与前图重叠，进一步可见从初始端点到x的反正弦定积分；人遮挡的能量式片段不认定逐字读全。'],
 ['IMG_5B518AEF-287D-4F46-ADED-B8722F3AF185.jpeg','重叠板书显示正弦转余弦及振幅A记号，遮挡部分不独立重构。'],
 ['IMG_CE882238-DC8F-418E-9771-FCE42ED6B3CB.jpeg','可辨认dx/√(x0²−x²)=±ω0dt及归一化变量d(x/x0)/√(1−(x/x0)²)的积分结构。积分下限遮挡处不作逐字声称。'],
 ['IMG_DC83A94E-7344-4CD0-8013-4E78B7C731AB.jpeg','可辨认столовая (комната)、поднимать(ся) / поднять(ся)、как?、на лифте、по лестнице、пешком及格编号；底部被手遮挡处不补猜。'],
 ['IMG_FD18F630-E6A0-4206-A4CE-5F87FBE402B6.jpeg','与前图重叠：столовая、поднимать(ся) / поднять(ся)、на лифте清楚可读。'],
 ['IMG_653F75D7-BC15-4BDD-8E4B-2D5F041CD8AF.jpeg','可辨认посылать / послать деньги；через банк、через приложение банка、по почте；окружность与круг；осматривать / осмотреть музей, город, больного (человека)，及что/кого宾格标注。']]
recoveries={}
for tid in ids:
 d=read(W/'history'/f'{tid}.json');imgs=[]
 for a in d.get('attachments',[]):
  p=W/'history/attachments'/(tid+'_'+a['name']);entry=next(x for x in excerpts if x[0]==a['name'])
  imgs.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p),'status':'visually_read_readable_regions','reading_notes':entry[1]})
 audits=[]
 for turn in d['turns']:
  for m in turn['items']:
   user=m['type']=='userMessage';raw='\n'.join(x.get('text','') for x in m.get('content',[]) if x['type']=='text') if user else m.get('text','')
   audits.append({'message_id':m['id'],'raw_sha256':hashlib.sha256(raw.encode()).hexdigest(),'read_state':'thread_attachments_reviewed_mapping_unavailable' if user else 'placeholder_ui_body_unavailable','outcome':'对应会话的原附件已逐图审读；工具未给出图片与消息的一一映射，不虚构绑定。' if user else '工具仅返回引用占位；已登录页面停在验证页，未恢复旧回答正文。'})
 rec={'thread_id':tid,'title':d['thread']['title'],'retrieved_at':NOW,'revision':REV,'raw_messages_preserved':True,'read_method':'original exported attachment visual reading; assistant UI bodies unavailable','message_attachment_mapping':'not provided by connector; source concepts bind exact attachment hash at thread level, not invented message pairing','attachments':imgs,'message_audits':audits,'still_unread':'所有引用占位对应的旧回答正文；原附件裁切、遮挡或无法辨认的部分','scope':'仅提取实际可读的教学知识，不复刻作业题，不包含国情/ОРГ。'}
 write(W/'source_recovery'/f'{tid}.json',rec);recoveries[tid]=rec

entries=[]
def item(code,section,knowledge,evidence,tid=None,kind='curriculum_extension',change='expanded_detail'):
 p=next(B.glob(code+'_*.md'));s=p.read_text(encoding='utf-8');assert section in s and evidence in s,(section,evidence)
 idx=s.index(evidence);entry={'id':f'D17-{code}-{sum(x["book_code"]==code for x in entries)+1:02d}','revision':REV,'book_code':code,'source_kind':kind,'knowledge':knowledge,'source_messages':[],'source_thread':tid,'source_read_method':'visually_read_original_attachment' if tid else 'independent_derivation_in_course_sequence','textbook_section':section,'source_file':str(p),'line':s[:idx].count('\n')+1,'evidence':evidence,'status':'source_integrated','pdf_status':'pending','change':change}
 if tid:
  entry['source_recovery_file']=f'work/source_recovery/{tid}.json';entry['source_attachments']=[{'file':a['file'],'sha256':a['sha256']} for a in recoveries[tid]['attachments']]
  entry['source_message_candidates']=[a['message_id'] for a in recoveries[tid]['message_audits'] if a['read_state'].startswith('thread_')]
  entry['message_attachment_mapping']='unavailable; no exact per-message attachment claim'
 entries.append(entry)
phy=ids[4];logic=ids[2];ru=ids[5];info=ids[0];note=ids[1];terms=ids[3]
for sec,k,e,tid,kind in [
 ('11.2','由守恒能量得到速度、按方向选择正负分支','开平方出现的正负号',phy,'conversation_attachment'),
 ('11.2','归一化变量后的反正弦积分与端点瑕积分','端点处的收敛瑕积分',phy,'conversation_attachment'),
 ('11.2','反正弦主值只覆盖半周期，转折后需换分支','只覆盖从右端到左端',phy,'source_correction'),
 ('11.2','初始位置、释放端点、平衡位置与振幅不可混用','符号的含义需要先明确',phy,'source_correction'),
 ('11.2','一般势能允许运动区域与周期积分成立条件','相邻两个简单转折点',None,'curriculum_extension'),
 ('11.3','动势能随时间的平方表达式与总能量','E_p&=E',phy,'conversation_attachment'),
 ('11.3','位移图、势能位置图与能量时间图区分','横轴不同',phy,'conversation_attachment'),
 ('11.3','能量周期T/2与两倍角频率','对应角频率',None,'curriculum_extension'),
 ('11.3','等能位置和速度绝对值及一周期四个时刻','一个周期内共有四个',None,'curriculum_extension'),
 ('11.3','周期平均动势能相等不同于瞬时相等','这是周期平均相等',None,'curriculum_extension'),
 ('11.3','带单位完整示例选择首次到达的时间与负速度','t=\\pi/15',None,'curriculum_extension'),
 ('11.3','能量相椭圆及演化方向，不是空间轨迹','相平面中的曲线',None,'curriculum_extension'),
 ('11.4','竖直弹簧平衡平移与重力势能配方','y_{\\rm eq}',None,'curriculum_extension'),
 ('11.4','自然长度释放的振幅及最大伸长','最低点伸长',None,'curriculum_extension'),
 ('11.4','串并联等效劲度推导与轻连接点假设','中间连接点质量忽略',None,'curriculum_extension')]:item('05',sec,k,e,tid,kind)
for sec,k,e,kind,change in [
 ('8. 谓词','整数后继、量词次序和量词否定已在原正文覆盖','代入 \\(x=0\\)', 'conversation_attachment','verified_existing'),
 ('8.1','受限全称蕴含、受限存在合取及空类已覆盖','存在见证必须同时满足身份与能力','conversation_attachment','verified_existing'),
 ('8.3','二元素模型穷尽候选，分别选见证与统一见证的区别','所有候选都失败','curriculum_extension','expanded_detail'),
 ('8.3','三重量词中见证允许依赖哪些前置变量','允许 y 同时依赖两个对象','curriculum_extension','expanded_detail'),
 ('8. 谓词','非空有限全序集合必有最大元的明确条件','非空有限集合中为假','source_correction','clarified_condition')]:item('07',sec,k,e,logic if kind!='curriculum_extension' else None,kind,change)
for sec,k,e,tid,kind in [
 ('2.4','目的层宾格、乘电梯前置格、沿楼梯与格及同形区别','по лестнице 表沿楼梯',ru,'conversation_attachment'),
 ('2.4','поднимать/поднять及反身对的及物性、体、过程结果','поднимать / поднять 是及物动词对',ru,'conversation_attachment'),
 ('2.4','посылать/послать宾语、收件人与格及人的词义变体','послать курьера',ru,'conversation_attachment'),
 ('2.4','через银行应用宾格、по почте与格和属格中心关系','через 接宾格',ru,'conversation_attachment'),
 ('2.4','осмотреть参观与诊察、阳性有生命无生命宾格差异','больного 是阳性有生命宾格',ru,'conversation_attachment'),
 ('2.4','一至六格编号对应关系','课堂标注',ru,'conversation_attachment'),
 ('9.2','21个一般科学术语按概念关系说明意义和多义边界','категория 是用于归类',terms,'conversation_attachment'),
 ('9.2','Adj+N一致与N+属格N补语，системы同形对照','两个 системы 外形相同',terms,'conversation_attachment'),
 ('9.2','столовая和больной的名词化及形容词型变格','столовая комната',ru,'conversation_attachment'),
 ('9.2','окружность圆周与круг区域，长度和面积的区别','длина окружности',ru,'conversation_attachment'),
 ('10.2','信息传递句的от属格、к与格及反身被动表达','к приёмнику 是趋向接收者',info,'conversation_attachment'),
 ('10.2','при взаимодействии объектов、обмен内容工具格及между','обмен информацией',note,'conversation_attachment'),
 ('10.2','представлять собой固定表达后接宾格','固定表达',note,'conversation_attachment'),
 ('10.2','科技文连续离散副词、取决于属格链、限制对比与并列','в зависимости от настройки приёмника',info,'conversation_attachment'),
 ('10.2','原信息文概念—主体—信号—分类—功能的段落主线','认识、交际和管理功能',info,'conversation_attachment'),
 ('10.3','问题式提纲与论点式提纲的形式及保持中心关系','тезисный план',info,'conversation_attachment')]:item('09',sec,k,e,tid,kind)
for sec,k,e,kind in [
 ('1.1','信号、数据、信息、知识的操作性区分与领域条件','在这一操作性区分中','curriculum_extension'),
 ('1.1','信源、编码、信道、接收与解释链路','信源、编码、信道','conversation_attachment'),
 ('1.1','存储跨时间、通信跨位置及复制不等于搬移物体','跨时间保存记录','conversation_attachment'),
 ('1.1','接收者语义理解与非语义信息的边界，修正绝对化说法','无法理解语义','source_correction'),
 ('1.2','连续时间、采样离散时间、量化有限幅值的区分','采样把时间位置离散化','curriculum_extension'),
 ('1.2','温度采样与理想舍入半格误差，不含传感器误差','0.05','curriculum_extension'),
 ('1.2','采集表示存储传输处理解释的连续工作过程','采集产生记录','conversation_attachment'),
 ('1.2','认识交际管理功能与温控反馈实例','不是互斥的三种数据格式','conversation_attachment')]:item('13',sec,k,e,info if kind!='curriculum_extension' else None,kind)
coverage=read(W/'knowledge_coverage.json');coverage['items'].extend(entries);coverage['updated_at']=NOW
coverage.setdefault('source_gaps',[]).append({'revision':REV,'threads':ids,'issue':'旧回答均为引用占位；UI停在验证页。17张附件的可读部分已逐图核读，消息与图片对应关系未提供，按会话及附件哈希定位。','status':'unresolved_assistant_bodies_and_exact_message_attachment_mapping'})
write(W/'knowledge_coverage.json',coverage)
edition=read(W/'edition_status.json');edition.update(revision=REV,updated_at=NOW,source_status='updated',html_status='pending',pdf_status='pending',combined_pdf_status='pending',legacy_zip_status='previous_edition_preserved',pending=['4 affected PDFs','HTML','page QA','combined PDF and ZIP','coverage finalization'],blocker=None,new_source_items=sum(x['source_kind']!='curriculum_extension' for x in entries),curriculum_extension_items=sum(x['source_kind']=='curriculum_extension' for x in entries));write(W/'edition_status.json',edition)
state=read(W/'update_state.json');state.update(last_source_scan_at=NOW,last_source_update_date='2026-10-17',pending_build={'revision':REV,'affected_books':['05','07','09','13']},latest_scan={'listed_threads':len(read(W/'daily17_listing.json')['threads']),'new_threads':6,'new_messages':32,'original_attachments_read':17,'assistant_bodies_recovered':0,'unavailable_hosts':[],'unavailable_sources':[]});write(W/'update_state.json',state)
audit=OUT/'内容增补核对记录.md';s=audit.read_text(encoding='utf-8');s+='\n\n## 2026-10-17 · 每日增补\n\n6段新增会话共32条消息，原工具消息ID与正文哈希已保存；17张原附件逐图核读。旧回答仅为引用占位，历史UI停在验证页，未恢复正文。图片与消息的一一对应关系未由工具提供，以下概念按会话、附件文件及SHA-256定位，不虚构某图属于某条消息。原附件遮挡、裁切部分不推测。\n\n'
for x in entries:s+=f'- {x["id"]}：{x["knowledge"]}。教材：{x["book_code"]}／{x["textbook_section"]}；来源：'+(recoveries[x['source_thread']]['title']+'原附件' if x['source_thread'] else '课程自然延伸，独立推导')+f'；处理：{x["change"]}；状态：源稿已写入，导出待核验。\n'
s+='\n《翻译俄语作业》实际为科技术语和名词短语构造，按正文吸收语言知识；不属于国情/ОРГ。量词原图的大部分直接知识已有覆盖，标明verified_existing，没有冒充全部新写。\n\n本轮再读first CC朗道《力学》本地PDF第38、73—74页，借鉴能量积分与稳定平衡—二次势—简谐解—能量的推进。未找到对应first CC俄语、逻辑学或计算机科学原书，未虚构参照。\n'
audit.write_text(s,encoding='utf-8')
scope=OUT/'来源覆盖与编写说明.md';s=scope.read_text(encoding='utf-8');s=re.sub(r'更新时间：[^。]+。','更新时间：2026-10-17。',s,count=1);s=re.sub(r'\*\*本轮13科源稿、HTML、PDF与完整下载包已同步；[^*]+\*\*','**本轮4科源稿增补完成，PDF、合集与下载包正在核验；历史导出保持至重建完成。**',s,count=1);s+='\n\n## 2026-10-17 来源核读与增补\n\n新增6段对话的17张原附件已逐图核读，覆盖物理、逻辑、俄语与信息概念。原工具旧回答均仅返回引用，已登录历史页面停在验证页，故旧回答正文继续记为不可读；原图仍可独立提供可核实的教学内容。连接器没有返回逐条消息与图片的对应关系，未编造映射。概念记录关联确切附件文件及哈希，消息逐条保留未恢复状态。没有把这些哈希计为全文已读或内容已融入证明。\n\n再读first CC朗道《力学》PDF第38、73—74页；新物理正文借鉴其从能量积分到稳定平衡与自由振动的推导顺序。俄语和信息内容另参考本轮用户原教材的实际第20—21页，不把原文的学科观点泛化为唯一科学定义。详见内容增补核对记录。\n';scope.write_text(s,encoding='utf-8')
log=OUT/'更新日志.md';s=log.read_text(encoding='utf-8');s+='\n\n## 2026-10-17 · 每日增补\n\n- 物理第11节补能量积分、方向分支和反正弦主值限制，展开动势能的时间规律、等能时刻、周期平均、相椭圆、竖直及串并联弹簧；带单位教学示例独立给定。\n- 逻辑第8节补二元素模型穷举、统一见证与可变见证、三重量词依赖，明确非空有限论域条件。原图已覆盖部分不重复冒充新知识。\n- 俄语补动词支配、反身形式、路径与方式、科学术语短语、名词化、信息概念段落与提纲表达，按既有语法主线插入。\n- 计算机科学第1节补信号—数据—信息、信源到接收者、采样与量化、认识通信管理功能，校正“看不懂外语就得不到任何信息”的过强说法。\n- 读取6段新增会话的17张原附件，保留32条消息检查点；旧回答正文及逐条消息图片映射缺口如实记录。导出核验进行中。\n';log.write_text(s,encoding='utf-8')
write(W/'daily17_changes.json',{'revision':REV,'items':len(entries),'new_source_items':sum(x['source_kind']!='curriculum_extension' for x in entries),'extension_items':sum(x['source_kind']=='curriculum_extension' for x in entries),'affected_books':['05','07','09','13'],'new_threads':ids})
print(json.dumps(read(W/'daily17_changes.json'),ensure_ascii=False))
