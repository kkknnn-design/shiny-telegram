const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {createRequire}=require('module');const r=createRequire(path.join(__dirname,'math/package.json'));
const {mathjax}=r('mathjax-full/js/mathjax.js');
const {TeX}=r('mathjax-full/js/input/tex.js');const {SVG}=r('mathjax-full/js/output/svg.js');
const {liteAdaptor}=r('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler}=r('mathjax-full/js/handlers/html.js');
const {AllPackages}=r('mathjax-full/js/input/tex/AllPackages.js');
const a=liteAdaptor();RegisterHTMLHandler(a);
const doc=mathjax.document('',{InputJax:new TeX({packages:AllPackages}),OutputJax:new SVG({fontCache:'none'})});
const dest=path.join(__dirname,'formulas');fs.mkdirSync(dest,{recursive:true});
const files=fs.readdirSync(path.join(__dirname,'../outputs/教材')).filter(f=>f.endsWith('.md'));
const formulas={},errors=[];
for(const file of files){let t=fs.readFileSync(path.join(__dirname,'../outputs/教材',file),'utf8').replace(/\r\n?/g,'\n').replace(/```[\s\S]*?```|`[^`\n]+`/g,'');for(const m of t.matchAll(/\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|\$\$([\s\S]*?)\$\$/g)){const tex=(m[1]??m[2]??m[3]).trim();if(formulas[tex])continue;let s=a.outerHTML(doc.convert(tex,{display:!m[2]}));if(s.includes('data-mml-node="merror"')){errors.push({file,tex});continue;}s=s.slice(s.indexOf('<svg'),s.lastIndexOf('</svg>')+6);let name=crypto.createHash('sha256').update(tex).digest('hex').slice(0,20)+'.svg';fs.writeFileSync(path.join(dest,name),s);formulas[tex]=name;}}
fs.writeFileSync(path.join(dest,'index.json'),JSON.stringify(formulas,null,2));fs.writeFileSync(path.join(dest,'errors.json'),JSON.stringify(errors,null,2));console.log(JSON.stringify({formulas:Object.keys(formulas).length,errors}));if(errors.length)process.exitCode=1;
