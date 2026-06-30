import sys
sys.stdout.reconfigure(encoding='utf-8')
from pypdf import PdfReader
r = PdfReader(r'E:\Coding\leozhang2056\outputs\2026-07-01\CV_Leo_Zhang_20260701_fullstack_Temperzone.pdf')
t = r.pages[0].extract_text() + r.pages[1].extract_text()
idx = t.find('Target role')
if idx >= 0: print(t[idx:idx+60])
for l in t.split('\n'):
    if '| 201' in l: print(l)
