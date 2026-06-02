from docx import Document
from docx.oxml.ns import qn
p='outputs/2026-06-02/CV_Leo_Zhang_20260602_android.docx'
d=Document(p)
for i,p in enumerate(d.paragraphs[:10]):
    print('PAR',i,repr(p.text)[:80])
    for r in p.runs:
        name = getattr(r.font,'name',None)
        size = getattr(r.font,'size',None)
        print('   ', repr(r.text)[:30], ' size=', size.pt if size else None, ' name=', name)
