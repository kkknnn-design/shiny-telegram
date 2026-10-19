from pathlib import Path
import json,datetime,hashlib
root=Path.cwd();now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
qa=json.loads((root/'work/qa/qa_report.json').read_text(encoding='utf-8'))
review={'revision':'2026-10-17-daily-01','reviewed_at':now,'all_book_pages_rendered':209,'boundary_issues':qa['issues'],'visual_contact_sheets':['05_contact.jpg','07_contact.jpg','09_contact.jpg','13_contact.jpg'],'detail_pages_reviewed':{'05':[13,14,15],'07':[10,11],'09':[6,7,14,15,16,17],'13':[3,4]},'result':'新增页公式分支、上下标、分式、积分、俄文、中文断行及页码可读，无黑条、重叠或内容越界；未修改的9科沿用已核验PDF。','book_hashes':{x['file']:x['sha256'] for x in qa['stats']}}
(root/'work/qa/daily17/visual_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
p=root/'work/update_state.json';s=json.loads(p.read_text(encoding='utf-8'));s.update(curriculum_extension_revision='2026-10-17-daily-01',curriculum_extension_items=14,new_source_items=30,latest_knowledge_audit={'revision':'2026-10-17-daily-01','items':44,'verified_existing':2,'expanded_or_clarified':42,'extension_items':14,'source_related_items':30,'assistant_body_gap_count':16,'message_attachment_mapping':'unavailable','original_attachment_count':17});p.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
p=root/'outputs/内容增补核对记录.md';s=p.read_text(encoding='utf-8');s+='\n### 本轮导出检查\n\n本轮44项核对中，2项为已有正文的覆盖确认，42项作实质增补或澄清。物理18页、逻辑12页、俄语18页、计算机科学12页；全套13科分册共209页，合并后含2页总封面与目录为211页。2240个不同公式转换无错误，31个嵌套SVG使用既定高分辨率路径；209页边界检查无错误，已目视检查4科全页缩略图及13张重点页。其余9科源稿与PDF保持上次已核验版本。\n\n原附件已核读不等于旧回答正文恢复：16条旧回答仍是引用占位，逐条消息与附件映射仍不可得。这些来源缺口继续保留，未提升为全文已读。\n';p.write_text(s,encoding='utf-8')
print('visual review and current audit persisted')
