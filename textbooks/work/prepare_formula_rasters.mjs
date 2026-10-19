import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'..');
const req=createRequire(path.join(root,'work/math/package.json'));
const sharp=req('C:/Users/zheng/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const input=path.join(root,'work/formulas');
const output=path.join(root,'work/formula_rasters_v1');
await fs.mkdir(output,{recursive:true});
const formulas=JSON.parse(await fs.readFile(path.join(input,'index.json'),'utf8'));
const records={};
for (const name of new Set(Object.values(formulas))) {
  const source=await fs.readFile(path.join(input,name),'utf8');
  if ((source.match(/<svg\b/g)||[]).length<2) continue;
  const view=source.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
  const file=name.replace(/\.svg$/,'.png');
  // Eight pixels per point at the nominal 12pt formula size.
  const width=Math.max(1,Math.ceil(view[2]*12/1000*8));
  const result=await sharp(Buffer.from(source)).resize({width}).png().toBuffer({resolveWithObject:true});
  await fs.writeFile(path.join(output,file),result.data);
  records[name]={file,viewbox_width:view[2],viewbox_height:view[3],
    pixel_width:result.info.width,pixel_height:result.info.height,
    svg_sha256:crypto.createHash('sha256').update(source).digest('hex')};
}
await fs.writeFile(path.join(output,'index.json'),JSON.stringify(records,null,2));
console.log(JSON.stringify({nested_formula_rasters:Object.keys(records).length,nominal_dpi:576}));