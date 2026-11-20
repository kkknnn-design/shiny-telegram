"""列出教材正文各段开头，便于选插图锚点。用法：py work/outline.py 02 [起始行] [每段字数]"""
import sys
import re
from pathlib import Path

books = Path(__file__).resolve().parents[1] / 'outputs/教材'
md = next(books.glob(sys.argv[1] + '_*.md'))
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
width = int(sys.argv[3]) if len(sys.argv) > 3 else 22
lines = md.read_text(encoding='utf-8').split('\n')
code = False
for i, l in enumerate(lines, 1):
    s = l.strip()
    if s.startswith('```'):
        code = not code
        continue
    if code or i < start or not s:
        continue
    if s[0] in '\\$|-!&{}' or s[0].isascii() and not s.startswith(('**', '#')):
        continue
    if re.match(r'\d+\. ', s):
        continue
    print(i, s[:width])
