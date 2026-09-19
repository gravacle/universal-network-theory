#!/usr/bin/env python3
"""Build a publication-facing UNT Word document from Markdown.

The Markdown file is the content authority. This builder applies a deterministic
publication layout, creates a static clickable contents list, preserves inline
formatting and hyperlinks, and marks table header rows for accessibility.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, Sequence

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL, WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


NAVY = "20364A"
MID_BLUE = "365F7D"
PALE_BLUE = "EEF4F8"
PALE_GRAY = "F6F7F8"
BORDER = "D9D9D9"
TEXT = RGBColor(0x1F, 0x25, 0x2B)
MUTED = RGBColor(0x55, 0x5F, 0x69)
LINK = RGBColor(0x1D, 0x5D, 0x88)
CODE_BG = "F1F3F5"
BODY_FONT = "Aptos"
MONO_FONT = "Aptos Mono"


def set_run_font(run, name: str, size: float | None = None) -> None:
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=85, start=105, bottom=85, end=105) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table) -> None:
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        el = borders.find(tag)
        if el is None:
            el = OxmlElement(f"w:{edge}")
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), BORDER)


def set_table_fixed_layout(table) -> None:
    tbl_pr = table._tbl.tblPr
    layout = tbl_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")


def mark_header_row(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    header = tr_pr.find(qn("w:tblHeader"))
    if header is None:
        header = OxmlElement("w:tblHeader")
        tr_pr.append(header)
    header.set(qn("w:val"), "true")


def prevent_row_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = tr_pr.find(qn("w:cantSplit"))
    if cant_split is None:
        cant_split = OxmlElement("w:cantSplit")
        tr_pr.append(cant_split)


def set_cell_width(cell, width_inches: float) -> None:
    cell.width = Inches(width_inches)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(width_inches * 1440)))
    tc_w.set(qn("w:type"), "dxa")


def add_page_field(paragraph) -> None:
    run = paragraph.add_run()
    set_run_font(run, BODY_FONT, 9)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, text, end])


def add_external_hyperlink(
    paragraph,
    text: str,
    target: str,
    *,
    code=False,
    bold=False,
    italic=False,
    size: float | None = None,
):
    rid = paragraph.part.relate_to(target, RT.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), rid)
    link.set(qn("w:history"), "1")
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "%02X%02X%02X" % tuple(LINK))
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.extend([color, underline])
    if bold:
        rpr.append(OxmlElement("w:b"))
    if italic:
        rpr.append(OxmlElement("w:i"))
    fonts = OxmlElement("w:rFonts")
    font_name = MONO_FONT if code else BODY_FONT
    for attr in ("ascii", "hAnsi", "eastAsia"):
        fonts.set(qn(f"w:{attr}"), font_name)
    rpr.append(fonts)
    sz = OxmlElement("w:sz")
    point_size = size or (9.5 if code else 10.5)
    sz.set(qn("w:val"), str(int(point_size * 2)))
    rpr.append(sz)
    run.append(rpr)
    t = OxmlElement("w:t")
    if text.startswith(" ") or text.endswith(" "):
        t.set(qn("xml:space"), "preserve")
    t.text = text
    run.append(t)
    link.append(run)
    paragraph._p.append(link)
    return link


def add_internal_hyperlink(paragraph, text: str, anchor: str, *, size=10.5, bold=False):
    link = OxmlElement("w:hyperlink")
    link.set(qn("w:anchor"), anchor)
    link.set(qn("w:history"), "1")
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "%02X%02X%02X" % tuple(LINK))
    rpr.append(color)
    if bold:
        rpr.append(OxmlElement("w:b"))
    fonts = OxmlElement("w:rFonts")
    for attr in ("ascii", "hAnsi", "eastAsia"):
        fonts.set(qn(f"w:{attr}"), BODY_FONT)
    rpr.append(fonts)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    rpr.append(sz)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def add_bookmark(paragraph, name: str, bookmark_id: int) -> None:
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:id"), str(bookmark_id))
    start.set(qn("w:name"), name)
    end = OxmlElement("w:bookmarkEnd")
    end.set(qn("w:id"), str(bookmark_id))
    paragraph._p.insert(0, start)
    paragraph._p.append(end)


def add_run(paragraph, text: str, *, bold=False, italic=False, code=False, size=None, color=None):
    if not text:
        return None
    run = paragraph.add_run(text)
    set_run_font(run, MONO_FONT if code else BODY_FONT, size or (9.5 if code else 10.7))
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color or TEXT
    if code:
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), CODE_BG)
        run._element.get_or_add_rPr().append(shd)
    return run


TOKEN_PATTERNS = [
    ("link", re.compile(r"\[([^\]]+)\]\(([^)]+)\)")),
    ("code", re.compile(r"`([^`]+)`")),
    ("bold", re.compile(r"\*\*(.+?)\*\*")),
    ("italic", re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")),
]


def add_inline(paragraph, text: str, *, bold=False, italic=False, size=None) -> None:
    """Add common Markdown inline constructs while preserving human-readable text."""
    pos = 0
    while pos < len(text):
        candidates = []
        for kind, pattern in TOKEN_PATTERNS:
            match = pattern.search(text, pos)
            if match:
                candidates.append((match.start(), kind, match))
        if not candidates:
            add_run(paragraph, text[pos:], bold=bold, italic=italic, size=size)
            break
        start, kind, match = min(candidates, key=lambda item: item[0])
        if start > pos:
            add_run(paragraph, text[pos:start], bold=bold, italic=italic, size=size)
        if kind == "link":
            label, target = match.group(1), match.group(2)
            is_code = label.startswith("`") and label.endswith("`")
            clean = label[1:-1] if is_code else re.sub(r"[*`]", "", label)
            add_external_hyperlink(
                paragraph,
                clean,
                target,
                code=is_code,
                bold=bold,
                italic=italic,
                size=size,
            )
        elif kind == "code":
            add_run(paragraph, match.group(1), bold=bold, italic=italic, code=True, size=size or 9.5)
        elif kind == "bold":
            add_inline(paragraph, match.group(1), bold=True, italic=italic, size=size)
        elif kind == "italic":
            add_inline(paragraph, match.group(1), bold=bold, italic=True, size=size)
        pos = match.end()


def clear_paragraph(paragraph) -> None:
    for child in list(paragraph._p):
        paragraph._p.remove(child)


def configure_section(section, *, landscape=False) -> None:
    section.orientation = WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
    if landscape:
        section.page_width = Inches(11)
        section.page_height = Inches(8.5)
        section.left_margin = Inches(0.56)
        section.right_margin = Inches(0.56)
        section.top_margin = Inches(0.58)
        section.bottom_margin = Inches(0.62)
    else:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        section.left_margin = Inches(0.76)
        section.right_margin = Inches(0.76)
        section.top_margin = Inches(0.68)
        section.bottom_margin = Inches(0.7)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)


def configure_header_footer(section, document_title: str) -> None:
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    header = section.header
    hp = header.paragraphs[0]
    clear_paragraph(hp)
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.paragraph_format.space_after = Pt(0)
    run = hp.add_run(document_title)
    set_run_font(run, BODY_FONT, 8.4)
    run.font.color.rgb = MUTED

    footer = section.footer
    fp = footer.paragraphs[0]
    clear_paragraph(fp)
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    run = fp.add_run("Page ")
    set_run_font(run, BODY_FONT, 8.8)
    run.font.color.rgb = MUTED
    add_page_field(fp)


def get_or_add_style(doc, name: str, style_type=WD_STYLE_TYPE.PARAGRAPH):
    try:
        return doc.styles[name]
    except KeyError:
        return doc.styles.add_style(name, style_type)


def configure_styles(doc) -> None:
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = BODY_FONT
    normal._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    normal.font.size = Pt(10.7)
    normal.font.color.rgb = TEXT
    normal.paragraph_format.space_after = Pt(5.5)
    normal.paragraph_format.line_spacing = 1.14
    normal.paragraph_format.widow_control = True

    title = styles["Title"]
    title.font.name = BODY_FONT
    title._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    title._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    title.font.size = Pt(25)
    title.font.bold = True
    title.font.color.rgb = RGBColor(0, 0, 0)
    title.paragraph_format.space_before = Pt(20)
    title.paragraph_format.space_after = Pt(13)
    title.paragraph_format.keep_with_next = True
    title_ppr = title._element.get_or_add_pPr()
    title_border = title_ppr.find(qn("w:pBdr"))
    if title_border is not None:
        title_ppr.remove(title_border)

    h1 = styles["Heading 1"]
    h1.font.name = BODY_FONT
    h1._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    h1._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0, 0, 0)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    h1.paragraph_format.keep_with_next = True
    h1.paragraph_format.widow_control = True

    h2 = styles["Heading 2"]
    h2.font.name = BODY_FONT
    h2._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    h2._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    h2.font.size = Pt(12.6)
    h2.font.bold = True
    h2.font.color.rgb = RGBColor(0, 0, 0)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(4.5)
    h2.paragraph_format.keep_with_next = True
    h2.paragraph_format.widow_control = True

    contents = get_or_add_style(doc, "Contents Title")
    contents.font.name = BODY_FONT
    contents._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    contents._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    contents.font.size = Pt(16)
    contents.font.bold = True
    contents.font.color.rgb = RGBColor(0, 0, 0)
    contents.paragraph_format.space_before = Pt(13)
    contents.paragraph_format.space_after = Pt(7)

    code_style = get_or_add_style(doc, "Code Block")
    code_style.font.name = MONO_FONT
    code_style._element.rPr.rFonts.set(qn("w:ascii"), MONO_FONT)
    code_style._element.rPr.rFonts.set(qn("w:hAnsi"), MONO_FONT)
    code_style.font.size = Pt(9.1)
    code_style.font.color.rgb = TEXT
    code_style.paragraph_format.left_indent = Inches(0.18)
    code_style.paragraph_format.right_indent = Inches(0.12)
    code_style.paragraph_format.space_before = Pt(4)
    code_style.paragraph_format.space_after = Pt(7)
    code_style.paragraph_format.line_spacing = 1.04

    toc1 = get_or_add_style(doc, "UNT TOC 1")
    toc1.font.name = BODY_FONT
    toc1._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    toc1._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    toc1.font.size = Pt(10.6)
    toc1.paragraph_format.space_after = Pt(3.5)
    toc1.paragraph_format.keep_together = True

    toc2 = get_or_add_style(doc, "UNT TOC 2")
    toc2.font.name = BODY_FONT
    toc2._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    toc2._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    toc2.font.size = Pt(9.7)
    toc2.paragraph_format.left_indent = Inches(0.24)
    toc2.paragraph_format.space_after = Pt(2.8)
    toc2.paragraph_format.keep_together = True

    # Ensure the entire document has an English language declaration.
    for style in (normal, title, h1, h2, contents, code_style, toc1, toc2):
        rpr = style._element.get_or_add_rPr()
        lang = rpr.find(qn("w:lang"))
        if lang is None:
            lang = OxmlElement("w:lang")
            rpr.append(lang)
        lang.set(qn("w:val"), "en-US")


def strip_inline_markup(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.replace("**", "").replace("`", "").replace("*", "")


def parse_table_row(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [part.strip() for part in raw.split("|")]


def is_table_separator(line: str) -> bool:
    cells = parse_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def preferred_widths(headers: Sequence[str], landscape: bool) -> list[float]:
    n = len(headers)
    usable = 9.75 if landscape else 6.98
    cleaned = [strip_inline_markup(h).lower() for h in headers]
    if n == 2:
        weights = [1.35, 3.65]
    elif n == 3:
        if any("urm surface" in h for h in cleaned):
            weights = [1.35, 2.35, 2.3]
        elif any(h == "l" for h in cleaned):
            weights = [0.65, 1.15, 2.2]
        else:
            weights = [1.25, 1.6, 2.8]
    elif n == 4:
        weights = [0.65, 1.8, 1.8, 1.8]
    elif n == 5:
        if cleaned and cleaned[0] in {"scale", "l"}:
            weights = [0.65, 1.35, 1.35, 1.55, 4.2]
        else:
            weights = [2.6, 1.25, 2.3, 1.75, 2.25]
    else:
        weights = [1.0] * n
    total = sum(weights)
    return [usable * w / total for w in weights]


def add_table(doc, rows: Sequence[Sequence[str]], aligns: Sequence[str], *, landscape: bool):
    headers = rows[0]
    table = doc.add_table(rows=len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_fixed_layout(table)
    set_table_borders(table)
    widths = preferred_widths(headers, landscape)
    font_size = 8.9 if len(headers) <= 3 else 8.4 if len(headers) == 4 else 8.2

    for ridx, source_row in enumerate(rows):
        row = table.rows[ridx]
        prevent_row_split(row)
        if ridx == 0:
            mark_header_row(row)
        for cidx, value in enumerate(source_row):
            cell = row.cells[cidx]
            set_cell_width(cell, widths[cidx])
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            clear_paragraph(p)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            align = aligns[cidx] if cidx < len(aligns) else "left"
            p.alignment = {
                "left": WD_ALIGN_PARAGRAPH.LEFT,
                "center": WD_ALIGN_PARAGRAPH.CENTER,
                "right": WD_ALIGN_PARAGRAPH.RIGHT,
            }[align]
            add_inline(p, value, bold=(ridx == 0), size=font_size)
            if ridx == 0:
                set_cell_shading(cell, NAVY)
                # Header cells can contain inline-code and hyperlink runs.  Those
                # runs are not all exposed through ``Paragraph.runs`` and inline
                # code carries its own pale shading, so normalize the underlying
                # run properties to keep every header label high-contrast.
                for run_elm in p._p.iter(qn("w:r")):
                    r_pr = run_elm.find(qn("w:rPr"))
                    if r_pr is None:
                        r_pr = OxmlElement("w:rPr")
                        run_elm.insert(0, r_pr)
                    for run_shading in list(r_pr.findall(qn("w:shd"))):
                        r_pr.remove(run_shading)
                    color = r_pr.find(qn("w:color"))
                    if color is None:
                        color = OxmlElement("w:color")
                        r_pr.append(color)
                    color.set(qn("w:val"), "FFFFFF")
            elif ridx % 2 == 0:
                set_cell_shading(cell, PALE_BLUE)
            else:
                set_cell_shading(cell, "FFFFFF")

    after = doc.add_paragraph()
    after.paragraph_format.space_after = Pt(2)
    return table


def add_code_block(doc, lines: Sequence[str]) -> None:
    p = doc.add_paragraph(style="Code Block")
    p.paragraph_format.keep_together = len(lines) <= 12
    p_pr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), CODE_BG)
    p_pr.append(shd)
    for index, line in enumerate(lines):
        run = p.add_run(line)
        set_run_font(run, MONO_FONT, 9.1)
        run.font.color.rgb = TEXT
        if index != len(lines) - 1:
            run.add_break(WD_BREAK.LINE)


def add_paragraph(doc, text: str, *, style=None, left_indent=0.0, first_line=0.0, keep_next=False):
    p = doc.add_paragraph(style=style)
    if left_indent:
        p.paragraph_format.left_indent = Inches(left_indent)
    if first_line:
        p.paragraph_format.first_line_indent = Inches(first_line)
    p.paragraph_format.keep_with_next = keep_next
    add_inline(p, text)
    return p


def collect_headings(lines: Sequence[str]):
    headings = []
    counter = 1
    for line in lines:
        m = re.match(r"^(##|###)\s+(.+)$", line)
        if not m:
            continue
        level = 1 if m.group(1) == "##" else 2
        text = strip_inline_markup(m.group(2)).strip()
        anchor = f"UNT_Heading_{counter:03d}"
        headings.append((level, text, anchor, counter + 10))
        counter += 1
    return headings


def add_contents(doc, headings) -> None:
    p = doc.add_paragraph(style="Contents Title")
    p.add_run("Contents")
    add_bookmark(p, "UNT_Contents", 2)
    intro = doc.add_paragraph()
    intro.paragraph_format.space_after = Pt(8)
    run = intro.add_run("Select a section title to jump to it.")
    set_run_font(run, BODY_FONT, 9.5)
    run.font.color.rgb = MUTED
    for level, text, anchor, _bookmark_id in headings:
        p = doc.add_paragraph(style="UNT TOC 1" if level == 1 else "UNT TOC 2")
        add_internal_hyperlink(p, text, anchor, size=10.4 if level == 1 else 9.6, bold=(level == 1))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_landscape_section(doc, landscape: bool, document_title: str):
    section = doc.add_section(WD_SECTION.NEW_PAGE)
    configure_section(section, landscape=landscape)
    # Headers/footers remain linked; configure explicitly for compatibility.
    configure_header_footer(section, document_title)
    return section


def build(source: Path, output: Path) -> None:
    lines = source.read_text(encoding="utf-8").splitlines()
    title_lines = [
        strip_inline_markup(line[2:].strip())
        for line in lines
        if line.startswith("# ")
    ]
    if not title_lines:
        raise ValueError("Markdown source must contain one H1 document title")
    document_title = title_lines[0]
    headings = collect_headings(lines)
    heading_iter = iter(headings)
    next_heading = next(heading_iter, None)

    doc = Document()
    configure_styles(doc)
    configure_section(doc.sections[0], landscape=False)
    configure_header_footer(doc.sections[0], document_title)
    doc.core_properties.title = document_title
    doc.core_properties.subject = "Universal Network Theory proof and publication document"
    doc.core_properties.author = "Universal Network Theory"
    doc.core_properties.keywords = "Universal Network Theory, proof index, URM, ARGER, gravity formation"

    current_landscape = False
    toc_inserted = False
    i = 0
    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if line.startswith("# "):
            p = doc.add_paragraph(style="Title")
            p.add_run(strip_inline_markup(line[2:].strip()))
            ppr = p._p.get_or_add_pPr()
            border = ppr.find(qn("w:pBdr"))
            if border is not None:
                ppr.remove(border)
            add_bookmark(p, "UNT_Top", 1)
            i += 1
            continue

        hmatch = re.match(r"^(##|###)\s+(.+)$", line)
        if hmatch:
            level = 1 if hmatch.group(1) == "##" else 2
            text = strip_inline_markup(hmatch.group(2)).strip()
            if level == 1 and text.startswith("3.") and not current_landscape:
                add_landscape_section(doc, True, document_title)
                current_landscape = True
            elif level == 1 and text.startswith("4. Gravity") and current_landscape:
                add_landscape_section(doc, False, document_title)
                current_landscape = False
            if not toc_inserted and level == 1 and text.startswith("1."):
                add_contents(doc, headings)
                toc_inserted = True
            p = doc.add_paragraph(style=f"Heading {level}")
            p.add_run(text)
            if next_heading is not None:
                _lvl, _text, anchor, bookmark_id = next_heading
                add_bookmark(p, anchor, bookmark_id)
                next_heading = next(heading_iter, None)
            i += 1
            continue

        if line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1 if i < len(lines) else 0
            add_code_block(doc, code_lines)
            continue

        if line.startswith("> "):
            quote_lines = [line[2:].strip()]
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:].strip())
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.24)
            p.paragraph_format.right_indent = Inches(0.08)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(7)
            p.paragraph_format.line_spacing = 1.12
            ppr = p._p.get_or_add_pPr()
            pbdr = OxmlElement("w:pBdr")
            left = OxmlElement("w:left")
            left.set(qn("w:val"), "single")
            left.set(qn("w:sz"), "14")
            left.set(qn("w:space"), "8")
            left.set(qn("w:color"), "29465F")
            pbdr.append(left)
            ppr.append(pbdr)
            add_inline(p, " ".join(quote_lines))
            continue

        if line.lstrip().startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            table_rows = [parse_table_row(line)]
            sep = parse_table_row(lines[i + 1])
            aligns = []
            for marker in sep:
                if marker.startswith(":") and marker.endswith(":"):
                    aligns.append("center")
                elif marker.endswith(":"):
                    aligns.append("right")
                else:
                    aligns.append("left")
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row = parse_table_row(lines[i])
                if len(row) < len(table_rows[0]):
                    row.extend([""] * (len(table_rows[0]) - len(row)))
                table_rows.append(row[: len(table_rows[0])])
                i += 1
            add_table(doc, table_rows, aligns, landscape=current_landscape)
            continue

        list_match = re.match(r"^(\s*)([-*]|\d+\.)\s+(.+)$", line)
        if list_match:
            indent_spaces, marker, item_text = list_match.groups()
            continuation = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    break
                if re.match(r"^(\s*)([-*]|\d+\.)\s+", nxt) or nxt.startswith("#") or nxt.startswith("```") or nxt.lstrip().startswith("|"):
                    break
                if len(nxt) - len(nxt.lstrip()) >= 2:
                    continuation.append(nxt.strip())
                    i += 1
                else:
                    break
            if continuation:
                item_text += " " + " ".join(continuation)
            p = doc.add_paragraph(style="List Paragraph")
            p.paragraph_format.left_indent = Inches(0.27 + min(len(indent_spaces) / 4, 2) * 0.22)
            p.paragraph_format.first_line_indent = Inches(-0.18)
            p.paragraph_format.space_after = Pt(3.2)
            p.paragraph_format.line_spacing = 1.1
            lead = marker if marker[0].isdigit() else "•"
            marker_run = p.add_run(f"{lead} ")
            set_run_font(marker_run, BODY_FONT, 10.7)
            add_inline(p, item_text)
            continue

        # A prose paragraph can span multiple source lines. Join wrapped lines
        # while stopping at block boundaries.
        paragraph_lines = [line.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if not nxt.strip():
                break
            if nxt.startswith("#") or nxt.startswith("```"):
                break
            if nxt.lstrip().startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
                break
            if re.match(r"^(\s*)([-*]|\d+\.)\s+", nxt):
                break
            paragraph_lines.append(nxt.strip())
            i += 1
        text = " ".join(paragraph_lines)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5.5)
        p.paragraph_format.line_spacing = 1.14
        add_inline(p, text)

    if not toc_inserted:
        add_contents(doc, headings)

    # Attach the final navigation bookmark to existing content.  A dedicated
    # empty paragraph can spill onto a blank last page in tightly laid-out
    # documents.
    add_bookmark(doc.paragraphs[-1], "UNT_Bottom", 3)

    # Mark fields for update in Word; LibreOffice also honors the page field.
    settings = doc.settings._element
    update_fields = settings.find(qn("w:updateFields"))
    if update_fields is None:
        update_fields = OxmlElement("w:updateFields")
        settings.append(update_fields)
    update_fields.set(qn("w:val"), "true")

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
