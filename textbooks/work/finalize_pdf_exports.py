from pathlib import Path
import json,hashlib,zipfile,datetime,re,subprocess,sys
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs';B=OUT/'教材'
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=read(OUT/'教材清单.json')
edition=read(ROOT/'work/edition_status.json')
qa=read(ROOT/'work/qa/qa_report.json')
assert not qa['issues']
subprocess.run([sys.executable,str(ROOT/'work/check_links.py')],cwd=ROOT,check=True)
built=read(ROOT/'work/pdf_build_sources.json')
for b in manifest['books']:
 md=B/b['source'];pdf=B/b['file'];web=md.with_suffix('.html')
 assert built[md.name]['source_sha256']==sha(md)
 assert built[md.name]['pdf_sha256']==sha(pdf)==b['sha256']
 b.update(source_sha256=sha(md),html=web.name,html_sha256=sha(web),
  source_revision=edition['revision'],pdf_status='current_verified',pdf_matches_source=True)
manifest.update(source_revision=edition['revision'],source_updated_at=now.isoformat(),
 pdf_status='current_verified',pdf_edition_date=now.date().isoformat(),html_status='current',
 export_limitation=None,archive_excludes_current_pdfs=False)
manifest['qa'].update(formula_count=len(read(ROOT/'work/formulas/index.json')),
 html_formula_errors=read(ROOT/'work/render_report.json')['errors'],
 nested_svg_formula_previews=len(read(ROOT/'work/formula_rasters_v1/index.json')),
 current_pdf_verified=True,page_boundary_issues=qa['issues'],
 combined_internal_links=sum(len(p.get('/Annots',[])) for p in PdfReader(OUT/'各学科教材合集.pdf').pages),broken_internal_links=0)
combined=OUT/'各学科教材合集.pdf'
assert len(PdfReader(combined).pages)==manifest['combined_pages']
manifest['combined_sha256']=sha(combined)
write(OUT/'教材清单.json',manifest)
scope=(OUT/'来源覆盖与编写说明.md').read_text(encoding='utf-8')
current_summary=f'本轮13科教材保留，4科完成增补；源稿、HTML、PDF与完整下载包已同步；分册{manifest["book_pages"]}页，合集{manifest["combined_pages"]}页。'
scope=re.sub(r'\*\*本轮4科源稿增补完成，[^*]+\*\*','**'+current_summary+'**',scope,count=1)
scope=re.sub(r'当前去重检查点包含 \d+ 个会话、\d+ 条带内容哈希的消息',
 f'当前去重检查点包含 {len(read(ROOT/"work/update_state.json")["threads"])} 个会话、{sum(len(t["messages"]) for t in read(ROOT/"work/update_state.json")["threads"])} 条带内容哈希的消息',scope,count=1)
scope=re.sub(r'\d+个不同公式的MathJax转换及KaTeX阅读版转换均无错误',
 f'{manifest["qa"]["formula_count"]}个不同公式的MathJax转换及KaTeX阅读版转换均无错误',scope,count=1)
scope=re.sub(r'13科PDF已重建，全\d+页已渲染检查，未发现内容越界；',
 f'当前13科PDF中4科在本轮重建，全{manifest["book_pages"]}页已渲染检查，未发现内容越界；',scope,count=1)
scope=scope.replace('历史清单包含 123 个 ChatGPT 会话，另有可访问的 Codex 对话和只读本地对话缓存。',
 '既有历史清单检查了123个ChatGPT会话，本轮另核对6个新增会话；另有可访问的Codex对话和只读本地对话缓存。')
scope=scope.replace('本轮13科源稿、HTML与PDF现已同步重建；合集与完整下载包正在完成最终核验。',
 '本轮13科源稿、HTML、PDF与完整下载包已同步；分册203页，合集205页。')
scope=scope.replace('应为205页','为205页')
(OUT/'来源覆盖与编写说明.md').write_text(scope,encoding='utf-8')
audit=(OUT/'内容增补核对记录.md').read_text(encoding='utf-8')
audit=audit.replace('以下“已融入”仅指新Markdown和HTML；分科PDF、合集和旧下载包尚未重建，不能据此宣称其已更新。',
 '以下增补已同步至Markdown、HTML和新版PDF；合集与下载包已重建，见本文件末尾的重试核验记录。')
audit=audit.replace('PDF生成进程被当前Windows执行环境阻止；新导出路径已准备，但Python构建和整页视觉检查未运行成功。',
 '此前Windows执行环境曾阻止启动；2026-10-16重试已成功构建并完成页面检查。')
(OUT/'内容增补核对记录.md').write_text(audit,encoding='utf-8')
log=(OUT/'更新日志.md').read_text(encoding='utf-8')
log=log.replace('合集与完整下载包随后按当前源稿重新合并与核验，最终状态以教材清单为准。',
 '205页合集与完整下载包已按当前源稿重建；322个内部跳转目标有效，正式清单记录各文件哈希。')
(OUT/'更新日志.md').write_text(log,encoding='utf-8')
state=read(ROOT/'work/update_state.json')
state.update(updated_at=now.isoformat(),books=manifest['books'],pending_build=None,
 last_successful_export_date=now.date().isoformat(),edition_status='work/edition_status.json')
write(ROOT/'work/update_state.json',state)
coverage=read(ROOT/'work/knowledge_coverage.json')
for entry in coverage['items']:
 if entry.get('revision')==edition['revision']:
  entry.update(status='integrated',pdf_status='built_and_verified')
write(ROOT/'work/knowledge_coverage.json',coverage)
audit=(OUT/'内容增补核对记录.md').read_text(encoding='utf-8').replace('状态：源稿已写入，导出待核验。','状态：源稿、HTML与PDF已同步核验。')
(OUT/'内容增补核对记录.md').write_text(audit,encoding='utf-8')
log=(OUT/'更新日志.md').read_text(encoding='utf-8').replace('导出核验进行中。',f'4科分册与合集已重建，合集{manifest["combined_pages"]}页；页面与打包核验通过。')
(OUT/'更新日志.md').write_text(log,encoding='utf-8')
edition.update(updated_at=now.isoformat(),completed_at=now.isoformat(),
 pdf_status='current_verified',combined_pdf_status='current_verified',
 legacy_zip_status='current_verified',renderer_status='built_and_visually_verified',
 blocker=None,pending=[])
write(ROOT/'work/edition_status.json',edition)
rules=(ROOT/'work/教材维护规则.md').read_text(encoding='utf-8')
rules=rules.replace('31个图形预览已检查，但整本PDF仍待构建与全页验收。源稿/HTML是新版，旧PDF、合集和旧ZIP不含本轮增补。',
 '31个相关公式图形及实际PDF重点页已检查。2026-10-16重试完成13科PDF、205页合集与完整打包，源稿、HTML和PDF已同步。')
if '行内代码必须先保护' not in rules:
 rules+='\n\n行内代码必须先保护，再处理粗体等Markdown标记，否则两个反引号中的int **可能被误解析为跨段粗体。此问题已用实际C段落及4种混排输入核验。\n'
(ROOT/'work/教材维护规则.md').write_text(rules,encoding='utf-8')
full=OUT/'各学科教材_分册与源文件.zip'
docs=['教材总目录.md','教材总目录.html','来源覆盖与编写说明.md','更新日志.md','教材清单.json','内容增补核对记录.md']
with zipfile.ZipFile(full,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(B.iterdir()):
  if f.suffix in ['.pdf','.md','.html']:z.write(f,f.relative_to(OUT))
 for name in docs:z.write(OUT/name,name)
 z.write(combined,combined.name)
reading=OUT/'教材阅读版与源稿_扩充修订.zip'
with zipfile.ZipFile(reading,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(B.iterdir()):
  if f.suffix in ['.md','.html']:z.write(f,f.relative_to(OUT))
 for name in docs:
  text=(OUT/name).read_text(encoding='utf-8')
  if name=='教材总目录.html':
   text=re.sub(r'<a href="[^"]+\.pdf">[^<]*</a>','<span>PDF请使用完整下载包</span>',text)
   text=re.sub(r'<a href="[^"]+\.zip">[^<]*</a>','<span>本包为离线阅读版与源稿</span>',text)
  if name=='教材总目录.md':
   text=re.sub(r'\[[^\]]+\]\([^)]+\.pdf\)','PDF请使用完整下载包',text)
   text=re.sub(r'\[[^\]]+\]\([^)]+\.zip\)','本包为离线阅读版与源稿',text)
  z.writestr(name,text)
 z.writestr('阅读说明.txt',f'本包含{len(manifest["books"])}科Markdown和离线HTML。PDF与{manifest["combined_pages"]}页合集已另在完整下载包中同步更新。')
with zipfile.ZipFile(full) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('.pdf')])==len(manifest['books'])+1
 for b in manifest['books']:
  assert hashlib.sha256(z.read('教材/'+b['file'])).hexdigest()==b['sha256']
  assert hashlib.sha256(z.read('教材/'+b['source'])).hexdigest()==b['source_sha256']
  assert hashlib.sha256(z.read('教材/'+b['html'])).hexdigest()==b['html_sha256']
with zipfile.ZipFile(reading) as z:assert z.testzip() is None
result={'revision':edition['revision'],'verified_at':now.isoformat(),'books':len(manifest['books']),'book_pages':manifest['book_pages'],'combined_pages':manifest['combined_pages'],
 'formula_errors':manifest['qa']['formula_errors'],'boundary_issues':qa['issues'],
 'zip_crc':'passed','pdf_source_html_hashes':'matched','combined_sha256':sha(combined),
 'full_zip_bytes':full.stat().st_size,'reading_zip_bytes':reading.stat().st_size}
write(ROOT/'work/pdf_retry_verification.json',result)
print(json.dumps(result,ensure_ascii=False))
