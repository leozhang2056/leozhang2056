from pathlib import Path
import sys
import re
import statistics
from docx import Document
import yaml
from bs4 import BeautifulSoup

# find latest outputs folder with CV_*.docx and html
out_root = Path(__file__).parent.parent / 'outputs'
if not out_root.exists():
    print('outputs folder missing')
    sys.exit(1)

# pick latest date folder
date_dirs = sorted([d for d in out_root.iterdir() if d.is_dir()], reverse=True)
if not date_dirs:
    print('no output date dirs')
    sys.exit(1)

latest = date_dirs[0]
print('Using outputs dir:', latest)

docx_files = list(latest.glob('*.docx'))
html_files = list(latest.glob('*.html'))
if not docx_files:
    print('no docx found in', latest)
    sys.exit(1)

if not html_files:
    print('no html found in', latest)

# choose first docx and html
docx_path = docx_files[0]
html_path = html_files[0] if html_files else None
print('Docx:', docx_path)
print('Html:', html_path)

# load style config
cfg_path = Path(__file__).parent / 'app' / 'backend' / 'docx_style.yaml'
# fall back to app/backend path
cfg_path = Path(__file__).parent.parent / 'app' / 'backend' / 'docx_style.yaml'
if not cfg_path.exists():
    print('style config not found at', cfg_path)
    cfg = {}
else:
    cfg = yaml.safe_load(cfg_path.read_text(encoding='utf-8')) or {}

# open docx and inspect runs and paragraphs
doc = Document(str(docx_path))
font_names = []
font_sizes = []
line_spacings = []
for p in doc.paragraphs:
    fmt = p.paragraph_format
    try:
        ls = fmt.line_spacing
        if ls:
            line_spacings.append(float(ls))
    except Exception:
        pass
    for r in p.runs:
        try:
            name = r.font.name
            if name:
                font_names.append(name)
        except Exception:
            pass
        try:
            sz = r.font.size.pt if r.font.size else None
            if sz:
                font_sizes.append(float(sz))
        except Exception:
            pass

print('\nDOCX stats:')
from collections import Counter
if font_names:
    common_name = Counter(font_names).most_common(5)
    print('Top font names:', common_name[:5])
else:
    print('No font names found')

if font_sizes:
    print('Font size median/mean:', statistics.median(font_sizes), statistics.mean(font_sizes))
else:
    print('No font sizes found')

if line_spacings:
    print('Line spacing median/mean:', statistics.median(line_spacings), statistics.mean(line_spacings))
else:
    print('No line spacing values found')

# parse html css for body font-size and line-height
if html_path and html_path.exists():
    txt = html_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(txt, 'html.parser')
    body = soup.find('body')
    style_block = ''.join([s.get_text() for s in soup.find_all('style')])
    # look for body { font-size: Xpt; line-height: Y; }
    m_font = re.search(r'body\s*{[^}]*font-size:\s*([0-9.\.]+)pt', style_block)
    m_line = re.search(r'body\s*{[^}]*line-height:\s*([0-9\.]+)', style_block)
    print('\nHTML/CSS stats:')
    if m_font:
        print('body font-size (pt):', m_font.group(1))
    else:
        print('body font-size not found in style blocks')
    if m_line:
        print('body line-height:', m_line.group(1))
    else:
        print('body line-height not found in style blocks')

# compare to YAML
print('\nConfig (docx_style.yaml):')
for k in ['font_name', 'base_font_size', 'base_line_spacing', 'tab_pos']:
    print(k, ':', cfg.get(k))

# Simple pass/fail checks
print('\nChecks:')
if cfg.get('font_name'):
    if font_names and cfg.get('font_name') in font_names:
        print('Font name matches config')
    else:
        print('Font name MISMATCH: config', cfg.get('font_name'), 'docx top names', Counter(font_names).most_common(3))

if cfg.get('base_font_size'):
    try:
        cfg_sz = float(cfg.get('base_font_size'))
        med = statistics.median(font_sizes) if font_sizes else None
        if med and abs(med - cfg_sz) < 0.6:
            print('Font size close to config')
        else:
            print('Font size MISMATCH: config', cfg_sz, 'docx median', med)
    except Exception:
        pass

print('\nDone')
