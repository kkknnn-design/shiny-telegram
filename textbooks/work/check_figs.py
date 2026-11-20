"""检查插图行：不在代码块/公式块内，前后为空行，引用的文件存在。"""
from pathlib import Path
import re
B = Path(__file__).resolve().parents[1] / 'outputs/教材'
bad = 0
for md in sorted(B.glob('*.md')):
    L = md.read_text(encoding='utf-8').replace('\r\n', '\n').split('\n')
    code = math = False
    for i, l in enumerate(L):
        s = l.strip()
        if s.startswith('```'):
            code = not code
        elif not code and s.startswith(r'\[') and not s.endswith(r'\]'):
            math = True
        elif math and s.endswith(r'\]'):
            math = False
        if re.match(r'!\[', s):
            m = re.match(r'!\[(.*?)\]\((.+?)\)', s)
            probs = []
            if code or math: probs.append('在块内')
            if L[i - 1].strip() or (i + 1 < len(L) and L[i + 1].strip()): probs.append('未独立成段')
            if not (B / m.group(2)).exists(): probs.append('文件缺失')
            if probs:
                bad += 1; print(md.name, i + 1, probs, s[:50])
print('问题数', bad)
