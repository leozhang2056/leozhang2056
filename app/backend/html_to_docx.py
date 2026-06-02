from __future__ import annotations

from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, NavigableString, Tag, Comment
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

# --- Constants for Unification ---
BASE_FONT_SIZE = 10.5
BASE_LINE_SPACING = 1.15
BASE_SPACE_AFTER = 4.0
# Spacing constants (use these to tune global rhythm)
SUMMARY_SPACE_AFTER = BASE_SPACE_AFTER * 2.0
SECTION_SPACE_BEFORE = 8.0
SECTION_SPACE_AFTER = BASE_SPACE_AFTER
CONTACT_SPACE_AFTER = BASE_SPACE_AFTER * 2.0
LIST_SPACE_AFTER = 1.5
SKILL_SPACE_AFTER = 1.5
EDU_TAB_SPACE_AFTER = 2.0
EDU_DETAIL_SPACE_AFTER = 3.0
JOB_HEADER_SPACE_AFTER = 2.0
JOB_ROLE_SPACE_AFTER = 1.5
TECH_SPACE_AFTER = 2.0

PDF_TITLE_BLUE = RGBColor(0x1A, 0x4D, 0x96)
PDF_LINK_BLUE = RGBColor(0x1A, 0x4A, 0x8A)
PDF_TEXT = RGBColor(0x11, 0x11, 0x11)
PDF_MUTED = RGBColor(0x44, 0x44, 0x44)
PDF_DATE = RGBColor(0x77, 0x77, 0x77)


def _set_document_defaults(document):
    section = document.sections[0]
    section.top_margin = Inches(0.45)
    section.bottom_margin = Inches(0.45)
    section.left_margin = Inches(0.45)
    section.right_margin = Inches(0.45)

    normal = document.styles['Normal']
    try:
        normal.font.name = 'Roboto'
        normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
    except Exception:
        normal.font.name = 'Arial'
    normal.font.size = Pt(BASE_FONT_SIZE)
    
    fmt = normal.paragraph_format
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(BASE_SPACE_AFTER)
    fmt.line_spacing_rule = WD_LINE_SPACING.SINGLE
    fmt.line_spacing = BASE_LINE_SPACING


def _format_paragraph(paragraph, *, size: float = BASE_FONT_SIZE, bold: bool = False, italic: bool = False,
                      color: Optional[RGBColor] = None,
                      align: Optional[WD_PARAGRAPH_ALIGNMENT] = None, 
                      space_before: float = 0,
                      space_after: float = BASE_SPACE_AFTER):
    if align is not None:
        paragraph.alignment = align
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(space_before)
    fmt.space_after = Pt(space_after)
    fmt.line_spacing_rule = WD_LINE_SPACING.SINGLE
    fmt.line_spacing = BASE_LINE_SPACING
    
    for run in paragraph.runs:
        run.font.size = Pt(size)
        if color is not None:
            run.font.color.rgb = color
        if bold:
            run.bold = True
        if italic:
            run.italic = True
        try:
            run.font.name = 'Roboto'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
        except Exception:
            pass


def _style_paragraph(paragraph, **kwargs):
    # Backward compatibility helper
    _format_paragraph(paragraph, **kwargs)


def _set_paragraph_bottom_border(paragraph, *, color: str = 'D9D9D9', size: str = '6') -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn('w:pBdr'))
    if p_bdr is None:
        p_bdr = OxmlElement('w:pBdr')
        p_pr.append(p_bdr)
    bottom = p_bdr.find(qn('w:bottom'))
    if bottom is None:
        bottom = OxmlElement('w:bottom')
        p_bdr.append(bottom)
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), size)
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color)


def _add_tabbed_line(document, left: str, right: str, *, 
                     left_size: float = BASE_FONT_SIZE, 
                     right_size: float = BASE_FONT_SIZE - 0.5,
                     left_bold: bool = False, right_bold: bool = False,
                     left_italic: bool = False, right_italic: bool = False,
                     left_color: Optional[RGBColor] = None, right_color: Optional[RGBColor] = None,
                     space_after: float = 2.0, tab_pos: float = 6.6):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.tab_stops.add_tab_stop(Inches(tab_pos))
    _format_paragraph(paragraph, size=left_size, space_after=space_after)

    left_run = paragraph.add_run(left)
    left_run.font.size = Pt(left_size)
    left_run.bold = left_bold
    left_run.italic = left_italic
    if left_color is not None:
        left_run.font.color.rgb = left_color
    try:
        left_run.font.name = 'Roboto'
        left_run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
    except Exception:
        pass
        
    paragraph.add_run('\t')
    
    right_run = paragraph.add_run(right)
    right_run.font.size = Pt(right_size)
    right_run.bold = right_bold
    right_run.italic = right_italic
    if right_color is not None:
        right_run.font.color.rgb = right_color
    try:
        right_run.font.name = 'Roboto'
        right_run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
    except Exception:
        pass
    return paragraph


def _add_text_paragraph(document, text: str, **kwargs):
    text = (text or '').strip()
    if not text:
        return
    paragraph = document.add_paragraph()
    paragraph.add_run(text)
    _format_paragraph(paragraph, **kwargs)


def _append_inline(node, paragraph, size: float = BASE_FONT_SIZE, color: Optional[RGBColor] = PDF_TEXT):
    if isinstance(node, Comment):
        return
    if isinstance(node, NavigableString):
        text = str(node)
        if text:
            run = paragraph.add_run(text)
            run.font.size = Pt(size)
            run.font.color.rgb = color
            try:
                run.font.name = 'Roboto'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
            except Exception:
                pass
        return

    if not isinstance(node, Tag):
        return

    name = node.name.lower()
    if name == 'br':
        paragraph.add_run().add_break()
        return

    if name in {'strong', 'b'}:
        for child in node.children:
            if isinstance(child, NavigableString):
                if str(child):
                    run = paragraph.add_run(str(child))
                    run.bold = True
                    run.font.size = Pt(size)
                    run.font.color.rgb = color
                    try:
                        run.font.name = 'Roboto'
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
                    except Exception:
                        pass
            else:
                _append_inline(child, paragraph, size=size, color=color)
        return

    if name in {'em', 'i'}:
        for child in node.children:
            if isinstance(child, NavigableString):
                if str(child):
                    run = paragraph.add_run(str(child))
                    run.italic = True
                    run.font.size = Pt(size)
                    try:
                        run.font.name = 'Roboto'
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
                    except Exception:
                        pass
                    run.font.color.rgb = color
            else:
                _append_inline(child, paragraph, size=size, color=color)
        return

    if name == 'a':
        text = node.get_text(' ', strip=False)
        if text:
            run = paragraph.add_run(text)
            run.font.size = Pt(size)
            run.underline = True
            run.font.color.rgb = PDF_LINK_BLUE
            try:
                run.font.name = 'Roboto'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
            except Exception:
                pass
        return

    for child in node.children:
        _append_inline(child, paragraph, size=size, color=color)


def _render_inline_container(document, node: Tag, **kwargs):
    paragraph = document.add_paragraph()
    size = kwargs.get('size', BASE_FONT_SIZE)
    color = kwargs.get('color', PDF_TEXT)
    for child in node.children:
        _append_inline(child, paragraph, size=size, color=color)
    _format_paragraph(paragraph, **kwargs)


def _render_section_title(document, text: str):
    paragraph = document.add_paragraph()
    run = paragraph.add_run(text.strip().upper())
    run.bold = True
    run.font.size = Pt(BASE_FONT_SIZE)
    try:
        run.font.name = 'Roboto'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
    except Exception:
        pass
    _format_paragraph(
        paragraph,
        size=BASE_FONT_SIZE,
        bold=True,
        color=PDF_TITLE_BLUE,
        align=WD_PARAGRAPH_ALIGNMENT.LEFT,
        space_before=SECTION_SPACE_BEFORE,
        space_after=SECTION_SPACE_AFTER,
    )
    _set_paragraph_bottom_border(paragraph)


def _render_header(document, node: Tag):
    name_node = node.select_one('.cv-name')
    contact_node = node.select_one('.cv-contact')

    if name_node:
        _add_text_paragraph(
            document,
            name_node.get_text(' ', strip=True),
            size=21,
            bold=True,
            color=PDF_TEXT,
            align=WD_PARAGRAPH_ALIGNMENT.CENTER,
            space_after=CONTACT_SPACE_AFTER,
        )
    if contact_node:
        _render_inline_container(
            document,
            contact_node,
            align=WD_PARAGRAPH_ALIGNMENT.CENTER,
            size=9,
            color=PDF_LINK_BLUE,
            space_after=CONTACT_SPACE_AFTER,
        )


def _render_list(document, node: Tag):
    for li in node.find_all('li', recursive=False):
        paragraph = document.add_paragraph(style='List Bullet')
        _append_inline(li, paragraph, size=BASE_FONT_SIZE)
        paragraph.paragraph_format.left_indent = Inches(0.2)
        paragraph.paragraph_format.first_line_indent = Inches(-0.14)
        _format_paragraph(paragraph, size=BASE_FONT_SIZE, space_after=LIST_SPACE_AFTER, color=PDF_TEXT)


def _render_skill_row(document, node: Tag):
    paragraph = document.add_paragraph()
    label = node.select_one('.skill-label')
    if label:
        run = paragraph.add_run(label.get_text(' ', strip=True))
        run.bold = True
        run.font.size = Pt(BASE_FONT_SIZE)
        run.font.color.rgb = PDF_TEXT
        text = node.get_text(' ', strip=True)
        label_text = label.get_text(' ', strip=True)
        remainder = text.replace(label_text, '', 1).strip()
        if remainder:
            paragraph.add_run(' ' + remainder)
    else:
        _append_inline(node, paragraph, size=BASE_FONT_SIZE)
    _format_paragraph(paragraph, size=BASE_FONT_SIZE, space_after=SKILL_SPACE_AFTER, color=PDF_TEXT)


def _render_education_item(document, node: Tag):
    table = node.select_one('table.edu-header-table')
    if table:
        cells = table.find_all('td')
        if cells:
            degree = cells[0].get_text(' ', strip=True) if len(cells) > 0 else ''
            school = cells[1].get_text(' ', strip=True) if len(cells) > 1 else ''
            date = cells[2].get_text(' ', strip=True) if len(cells) > 2 else ''
            if degree or school or date:
                _add_tabbed_line(
                    document,
                    f'{degree}  {school}'.strip(),
                    date,
                    left_size=BASE_FONT_SIZE,
                    right_size=BASE_FONT_SIZE - 0.5,
                    left_bold=True,
                    left_color=PDF_TEXT,
                    right_color=PDF_DATE,
                    space_after=EDU_TAB_SPACE_AFTER,
                )

    detail = node.select_one('.edu-detail')
    if detail:
        _render_inline_container(document, detail, size=BASE_FONT_SIZE - 0.5, space_after=EDU_DETAIL_SPACE_AFTER)


def _render_job_header(document, node: Tag):
    table = node.select_one('table.job-header-table')
    if not table:
        return
    cells = table.find_all('td')
    if not cells:
        return

    left = cells[0].get_text(' ', strip=True) if len(cells) > 0 else ''
    right = cells[-1].get_text(' ', strip=True) if len(cells) > 1 else ''
    if left or right:
        _add_tabbed_line(
            document,
            left,
            right,
            left_size=BASE_FONT_SIZE,
            right_size=BASE_FONT_SIZE - 0.5,
            left_bold=True,
            left_color=PDF_TEXT,
            right_color=PDF_DATE,
            space_after=JOB_HEADER_SPACE_AFTER,
        )


def _render_node(document, node):
    if isinstance(node, Comment):
        return
    if isinstance(node, NavigableString):
        text = str(node).strip()
        if text:
            _add_text_paragraph(document, text)
        return

    if not isinstance(node, Tag):
        return

    classes = set(node.get('class', []))

    if 'section-title' in classes:
        _render_section_title(document, node.get_text(' ', strip=True))
        return

    if 'cv-header' in classes:
        _render_header(document, node)
        return

    if node.name == 'table' and 'job-header-table' in classes:
        _render_job_header(document, node)
        return

    if 'cv-summary' in classes or 'cv-references' in classes or 'company-alignment' in classes:
        _render_inline_container(
            document,
            node,
            size=BASE_FONT_SIZE,
            italic=('company-alignment' in classes),
            color=PDF_MUTED,
            space_after=8.0,
        )
        return

    if 'cv-skills' in classes:
        for child in node.find_all(recursive=False):
            _render_node(document, child)
        return

    if 'skill-row' in classes:
        _render_skill_row(document, node)
        return

    if 'edu-item' in classes:
        _render_education_item(document, node)
        return

    if node.name in {'ul', 'ol'}:
        _render_list(document, node)
        return

    if any(c in classes for c in {'job', 'career-stage', 'job-employer'}):
        for child in node.find_all(recursive=False):
            _render_node(document, child)
        document.add_paragraph().paragraph_format.space_after = Pt(BASE_SPACE_AFTER)
        return

    if 'job-role' in classes or 'stage-header' in classes:
        paragraph = document.add_paragraph()
        strong = node.find('strong')
        if strong:
            label = strong.get_text(' ', strip=True)
            run = paragraph.add_run(label)
            run.bold = True
            run.font.size = Pt(BASE_FONT_SIZE)
            try:
                run.font.name = 'Roboto'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Roboto')
            except Exception:
                pass
            remainder = node.get_text(' ', strip=True).replace(label, '', 1).strip(' -—|')
            if remainder:
                paragraph.add_run(' ' + remainder)
        else:
            _append_inline(node, paragraph)
        _format_paragraph(paragraph, size=BASE_FONT_SIZE, space_after=JOB_ROLE_SPACE_AFTER, color=PDF_TEXT)
        return

    if 'job-tech' in classes or 'stage-tech' in classes or 'stage-focus' in classes or 'employer-desc' in classes:
        _render_inline_container(
            document,
            node,
            size=BASE_FONT_SIZE,
            italic=('stage-focus' in classes),
            color=PDF_MUTED,
            space_after=TECH_SPACE_AFTER,
        )
        return

    if node.name in {'p', 'div'}:
        if node.get_text(' ', strip=True):
            _render_inline_container(document, node, space_after=BASE_SPACE_AFTER)
        return

    if node.name in {'section', 'article'}:
        for child in node.children:
            _render_node(document, child)


def html_to_docx(html_content: str, output_path: str) -> None:
    soup = BeautifulSoup(html_content, 'html.parser')
    document = Document()
    _set_document_defaults(document)

    body = soup.body or soup
    for child in body.children:
        _render_node(document, child)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output))
