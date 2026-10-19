import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const root=path.resolve(import.meta.dirname,'..');
const req=createRequire(path.join(root,'work/math/package.json'));
const katex=req('katex');
const {marked}=await import(pathToFileURL(path.join(root,'work/math/node_modules/marked/lib/marked.esm.js')));
const out=path.join(root,'outputs/教材');
const edition=JSON.parse(fs.readFileSync(path.join(root,'work/edition_status.json'),'utf8'));
const args=[];
const all=fs.readdirSync(out).filter(f=>f.endsWith('.md')).sort();
const files=args.length?all.filter(f=>args.some(a=>f.startsWith(a))):all;
const dist=path.dirname(req.resolve('katex/package.json'));
let mathCSS=fs.readFileSync(path.join(dist,'dist/katex.min.css'),'utf8');
mathCSS=mathCSS.replace(/url\(([^)]+)\)/g,(m,p)=>{p=p.replace(/["']/g,'');if(!p.startsWith('fonts/'))return m;let b=fs.readFileSync(path.join(dist,'dist',p));return `url(data:font/${p.endsWith('.woff2')?'woff2':'woff'};base64,${b.toString('base64')})`});
const css=`${mathCSS}
@page{size:A4;margin:19mm 18mm 20mm}
*{box-sizing:border-box}html{font-size:12pt;color:#171b22}body{font-family:'Times New Roman',SimSun,serif;line-height:1.8;margin:0;background:white}
h1,h2,h3{font-family:SimSun,serif;color:#172a3c;line-height:1.45;break-after:avoid}h1{font-size:25pt;margin:0 0 13mm}h2{text-align:center;font-size:17pt;margin:10mm 0 4mm;padding-bottom:2mm;border-bottom:0.4pt solid #b9c4cc}h3{font-size:13pt;margin:6mm 0 2mm}p{text-align:justify;text-indent:2em;margin:2.6mm 0;orphans:3;widows:3}a{color:#254e6d;text-decoration:none;overflow-wrap:anywhere}ul,ol{padding-left:6mm;margin:3mm 0}li{margin:1mm 0}blockquote{margin:4mm 0;padding:3mm 4mm;border-left:2pt solid #8d9ca8;background:#f4f6f7;font-size:10.5pt}
code,pre{font-family:Consolas,'Courier New',monospace}code{font-size:.88em}pre{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-size:9.2pt;line-height:1.5;background:#f5f6f7;border:0.4pt solid #d7dce0;padding:3mm;margin:4mm 0;tab-size:4}pre code{font-size:inherit}table{border-collapse:collapse;width:100%;font-size:10pt;margin:4mm 0;break-inside:auto}th,td{padding:2mm 2.2mm;border:0.5pt solid #b9c4cc;text-align:left;vertical-align:top}th{background:#edf1f4}tr{break-inside:avoid}thead{display:table-header-group}img{max-width:100%}hr{border:0;border-top:0.5pt solid #c7d0d7;margin:7mm 0}
.cover{text-align:center;min-height:238mm;break-after:page;display:flex;flex-direction:column;justify-content:center}.cover .eyebrow{font-size:11pt;letter-spacing:2px;color:#546a7c}.cover h1{margin-top:12mm}.cover .subtitle{font-size:16pt;line-height:1.8;color:#425a6c}.cover .note{font-size:10.5pt;margin-top:22mm;border-top:1pt solid #aebbc5;padding-top:5mm}.toc{break-after:page}.toc h2{text-align:center;margin-top:0}.toc ul{list-style:none;padding:0}.toc li{font-size:11pt;border-bottom:.3pt solid #e0e5e8;padding:1.6mm 0}.meta{font-size:10pt;color:#596b79}.katex{font-size:1.08em}.katex-display{margin:4mm 0;break-inside:avoid;overflow:visible}.math-block{break-inside:avoid;padding:0 0.5mm}.ref-list{font-size:10pt}.chapter-start{break-before:page}
@media screen{body{max-width:820px;margin:auto;padding:40px}.cover{text-align:center;min-height:780px}.katex-display{overflow-x:auto}}
`;
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
const errors=[];const stats=[];
for(const file of files){
 let source=fs.readFileSync(path.join(out,file),'utf8');
 let title=(source.match(/^# (.+)$/m)||[])[1]||file;
 let parts=source.split(/\n## /);let intro=parts.shift().replace(/^# .+\n/,'').trim();
 let subtitle=intro.split('\n')[0]||'个人学习教材';
 let tokens=[];
 // Protect fenced and inline code before converting math.
 let code=[];source=source.replace(/```[^\n]*\n[\s\S]*?```|`[^`\n]+`/g,m=>{code.push(m);return `CODEPLACEHOLDER${code.length-1}END`});
 const renderMath=(tex,display)=>{try{return katex.renderToString(tex.trim(),{displayMode:display,throwOnError:true,strict:'ignore',trust:false,output:'htmlAndMathml'});}catch(e){errors.push({file,tex,error:e.message});return `<span style="color:red">公式排版错误</span>`;}};
 source=source.replace(/\\\[([\s\S]*?)\\\]|\$\$([\s\S]*?)\$\$/g,(_,a,b)=>{tokens.push(`<div class="math-block">${renderMath(a??b,true)}</div>`);return `\n\nMATHTOKEN${tokens.length-1}END\n\n`;});
 source=source.replace(/\\\(([\s\S]*?)\\\)/g,(_,a)=>{tokens.push(renderMath(a,false));return `MATHTOKEN${tokens.length-1}END`;});
 source=source.replace(/CODEPLACEHOLDER(\d+)END/g,(_,i)=>code[+i]);
 source=source.replace(/^# .+\n/, '');
 // Remove the one-line subtitle from body; it appears on the cover.
 source=source.replace(subtitle,'');
 let html=marked.parse(source,{gfm:true,breaks:false});
 html=html.replace(/<p>MATHTOKEN(\d+)END<\/p>/g,(_,i)=>tokens[+i]);
 html=html.replace(/MATHTOKEN(\d+)END/g,(_,i)=>tokens[+i]);
 let toc=[];let num=0;html=html.replace(/<h2>([\s\S]*?)<\/h2>/g,(_,h)=>{let id='section-'+num++;toc.push({h,id});return `<h2 id="${id}">${h}</h2>`;});
 let cover=`<section class="cover"><div class="eyebrow">个人学科教材 · 持续更新版</div><h1>${esc(title)}</h1><div class="subtitle">${esc(subtitle)}</div><div class="note">中文正文：宋体　数学公式：KaTeX 数学字体<br>按知识依赖重组 · 配有概念、推导与讲解型例题<br>版本：${edition.revision} · 扩充修订阅读版<br>历史图片未重读的细节不作为已核实原题</div></section>`;
 let contents=`<section class="toc"><h2>本册目录</h2><ul>${toc.map(x=>`<li><a href="#${x.id}">${x.h}</a></li>`).join('')}</ul><p class="meta">阅读方法：依目录顺序阅读；每个例题的条件、计算与解释均在正文中展开。</p></section>`;
 let doc=`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>${esc(title)}</title><style>${css}</style><body>${cover}${contents}${html}</body></html>`;
 const htmlPath=path.join(out,file.replace(/\.md$/,'.html'));fs.writeFileSync(htmlPath,doc);
 stats.push({file,title,formulas:tokens.length});console.log(JSON.stringify(stats.at(-1)));
 }
fs.writeFileSync(path.join(root,'work/render_report.json'),JSON.stringify({stats,errors},null,2));
if(errors.length){console.error(JSON.stringify(errors));process.exitCode=1;}
