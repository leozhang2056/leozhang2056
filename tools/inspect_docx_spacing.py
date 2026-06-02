from docx import Document
from docx.shared import Pt
p='outputs/2026-06-02/CV_Leo_Zhang_20260602_android.docx'
doc=Document(p)
for i,pobj in enumerate(doc.paragraphs[:40]):
    f=pobj.paragraph_format
    sb = getattr(f,'space_before',None)
    sa = getattr(f,'space_after',None)
    ls = getattr(f,'line_spacing',None)
    def val(x):
        try:
            return x.pt
        except Exception:
            return x
    print(i, repr(pobj.text.strip())[:80], ' space_before=', val(sb), ' space_after=', val(sa), ' line_spacing=', ls)
