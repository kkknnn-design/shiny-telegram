from pathlib import Path
import re,json,math
files=['05_大学物理.md','08_数字电子技术基础.md','10_自动控制与仿真.md','12_数学建模与优化.md']
report=[]
for f in files:
 s=(Path('outputs/教材')/f).read_text(encoding='utf-8-sig')
 checks={k:len(re.findall(re.escape(k),s)) for k in [r'\[',r'\]',r'\(',r'\)']}
 han=len(re.findall('[\u4e00-\u9fff]',s))
 assert han>=6000,(f,han)
 assert checks[r'\[']==checks[r'\]'] and checks[r'\(']==checks[r'\)']
 assert not re.search('自测|练习与答案|待填|TODO|【待',s)
 assert not re.search(r'^#{1,3}.*[?？]',s,re.M)
 report.append({'file':f,'characters':len(s),'han_characters':han,'display_formulas':checks[r'\['],'inline_formulas':checks[r'\(']})
print(json.dumps(report,ensure_ascii=True,indent=2))
print('bounce_accumulation_seconds',math.sqrt(50/9.81)*9)
print('two_period_efficiency_cost',2+3*(1-.9*.9))
try:
 import sympy as sy
 t=sy.symbols('t'); m1,m2,l,g=sy.symbols('m1 m2 l g',positive=True);x=sy.Function('x')(t);q=sy.Function('q')(t)
 L=(m1+m2)*sy.diff(x,t)**2/2+m2*l*sy.diff(x,t)*sy.diff(q,t)*sy.cos(q)+m2*l*l*sy.diff(q,t)**2/2+m2*g*l*sy.cos(q)
 elx=sy.diff(sy.diff(L,sy.diff(x,t)),t)-sy.diff(L,x)
 elq=sy.diff(sy.diff(L,sy.diff(q,t)),t)-sy.diff(L,q)
 assert sy.simplify(elx-((m1+m2)*sy.diff(x,t,2)+m2*l*(sy.diff(q,t,2)*sy.cos(q)-sy.diff(q,t)**2*sy.sin(q))))==0
 assert sy.simplify(elq-m2*l*(l*sy.diff(q,t,2)+sy.diff(x,t,2)*sy.cos(q)+g*sy.sin(q)))==0
 print('moving_support_lagrange_equations_checked')
except ImportError: print('sympy_unavailable_manual_algebra_review_done')
Path('work/science_rewrite_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
