from pypdf import PdfReader
path = 'templates/CV_Leo_Zhang_android_1.pdf'
reader = PdfReader(path)
text = []
for i, page in enumerate(reader.pages):
    txt = page.extract_text()
    text.append(f'---PAGE {i+1}---')
    text.append(txt or '')
out = '\n'.join(text)
with open('outputs/target_pdf_text.txt','w',encoding='utf-8') as f:
    f.write(out)
print('WROTE outputs/target_pdf_text.txt')
print('Pages:', len(reader.pages))
