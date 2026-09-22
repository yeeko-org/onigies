"""Regenerates `template.docx` from the client's maquetado.

Run from `api/`:  venv/bin/python question/export/make_template.py [SRC]

The template keeps what the builder cannot produce from the DB (page
setup, header band, footer page number, cover, logos, embedded fonts)
and replaces the maquetado's direct formatting with named styles, so the
builder only picks a style per block.
"""
import copy
import re
import sys
from pathlib import Path

from docx import Document
from docx.document import Document as DocxDocument
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.oxml.xmlchemy import BaseOxmlElement

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = (
    HERE.parents[2] / 'docs' / 'records' / 'assets'
    / 'vf-2025-ONIGIES-maquetado.docx')
TARGET = HERE / 'template.docx'

# The cover ends where the maquetado's table of contents starts.
COVER_END_TEXT = 'Contenido'

GREY = '808080'
ORANGE = 'FBAC1D'
FONT = 'Arial'
TITLE_FONT = 'Century Gothic'

MC_ALTERNATE = (
    '{http://schemas.openxmlformats.org/markup-compatibility/2006}'
    'AlternateContent')

BULLET_LIST = 'OnigiesBullet'
LETTER_LIST = 'OnigiesLetter'


def fonts(name: str) -> str:
    return (
        f'<w:rFonts w:ascii="{name}" w:hAnsi="{name}" '
        f'w:eastAsia="{name}" w:cs="{name}"/>')


def size(half_points: int) -> str:
    return f'<w:sz w:val="{half_points}"/><w:szCs w:val="{half_points}"/>'


def paragraph_style(
        style_id: str, name: str, ppr: str = '', rpr: str = '',
        based_on: str | None = 'Normal', outline: int | None = None,
        default: bool = False) -> str:
    outline_xml = (
        f'<w:outlineLvl w:val="{outline}"/>' if outline is not None else '')
    based = f'<w:basedOn w:val="{based_on}"/>' if based_on else ''
    default_attr = ' w:default="1"' if default else ''
    return (
        f'<w:style {nsdecls("w")} w:type="paragraph"{default_attr} '
        f'w:styleId="{style_id}"><w:name w:val="{name}"/>{based}'
        f'<w:next w:val="Normal"/><w:qFormat/>'
        f'<w:pPr>{ppr}{outline_xml}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>')


KEEP = '<w:keepNext/><w:keepLines/>'

PARAGRAPH_STYLES = [
    paragraph_style(
        'Normal', 'Normal', based_on=None, default=True,
        ppr='<w:spacing w:after="120" w:line="276" w:lineRule="auto"/>'
            '<w:jc w:val="both"/>',
        rpr=fonts(FONT) + size(24) + '<w:lang w:val="es-MX"/>'),
    # Part title: sits alone on its page, as in the maquetado.
    paragraph_style(
        'Heading1', 'heading 1', outline=0,
        ppr=KEEP + '<w:pageBreakBefore/>'
            '<w:spacing w:before="4320" w:after="240"/>'
            '<w:jc w:val="right"/>',
        rpr=fonts(TITLE_FONT) + f'<w:color w:val="{GREY}"/>' + size(116)),
    # Materia.
    paragraph_style(
        'Heading2', 'heading 2', outline=1,
        ppr=KEEP + '<w:pageBreakBefore/>'
            '<w:spacing w:before="3600" w:after="480"/>'
            '<w:jc w:val="right"/>',
        rpr=fonts(FONT) + f'<w:color w:val="{GREY}"/>' + size(72)),
    # Componente, and the subsections of «Información de base».
    paragraph_style(
        'Heading3', 'heading 3', outline=2,
        ppr=KEEP + '<w:spacing w:before="360" w:after="120"/>'
            '<w:jc w:val="left"/>',
        rpr=fonts(FONT) + f'<w:color w:val="{ORANGE}"/>' + size(28)),
    # Observable.
    paragraph_style(
        'Heading4', 'heading 4', outline=3,
        ppr=KEEP + '<w:spacing w:before="240" w:after="240"/>'
            '<w:jc w:val="left"/>',
        rpr=fonts(FONT) + '<w:b/><w:bCs/>' + size(24)),
    paragraph_style(
        'TocTitle', 'TOC Title',
        ppr='<w:spacing w:after="480"/><w:jc w:val="right"/>',
        rpr=fonts(TITLE_FONT) + f'<w:b/><w:color w:val="{GREY}"/>'
            + size(116)),
    paragraph_style(
        'SectionTitle', 'Section Title',
        ppr=KEEP + '<w:spacing w:after="240"/><w:jc w:val="center"/>',
        rpr=fonts(TITLE_FONT) + f'<w:b/><w:color w:val="{GREY}"/>'
            + size(48)),
    paragraph_style(
        'PartLogo', 'Part Logo',
        ppr='<w:spacing w:before="1440"/><w:jc w:val="center"/>'),
    paragraph_style(
        'AxisDescription', 'Axis Description',
        ppr='<w:spacing w:before="480" w:after="240"/><w:jc w:val="right"/>',
        rpr=f'<w:b/><w:color w:val="{GREY}"/>' + size(32)),
    paragraph_style(
        'QuestionLabel', 'Question Label',
        ppr=KEEP + '<w:spacing w:before="240"/>'),
    paragraph_style(
        'Question', 'Question',
        ppr=KEEP + '<w:spacing w:before="240"/>', rpr='<w:b/><w:bCs/>'),
    paragraph_style(
        'QuestionHint', 'Question Hint', ppr=KEEP),
    paragraph_style(
        'AnswerOption', 'Answer Option',
        ppr='<w:spacing w:after="0"/><w:ind w:left="720" w:hanging="360"/>'
            '<w:jc w:val="left"/>'),
    paragraph_style(
        'ListItem', 'List Item',
        ppr='<w:spacing w:after="0"/><w:ind w:left="720" w:hanging="360"/>'
            '<w:jc w:val="left"/>'),
    paragraph_style(
        'AnswerLine', 'Answer Line',
        ppr='<w:spacing w:after="0"/><w:ind w:left="720"/>'
            '<w:jc w:val="left"/>'),
    paragraph_style(
        'CrossReference', 'Cross Reference',
        ppr='<w:spacing w:before="240"/>',
        rpr='<w:i/><w:iCs/><w:color w:val="595959"/>'),
    paragraph_style(
        'TableText', 'Table Text',
        ppr='<w:spacing w:after="0"/><w:jc w:val="left"/>'),
] + [
    paragraph_style(
        f'TOC{level}', f'toc {level}',
        ppr='<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="10070"/>'
            '</w:tabs><w:spacing w:after="60"/>'
            f'<w:ind w:left="{220 * (level - 1)}"/><w:jc w:val="left"/>',
        rpr=size(22))
    for level in range(1, 5)
]

OPTION_TABLE_STYLE = (
    f'<w:style {nsdecls("w")} w:type="table" w:styleId="OptionTable">'
    '<w:name w:val="Option Table"/><w:basedOn w:val="TableNormal"/>'
    '<w:qFormat/><w:pPr><w:spacing w:after="0"/><w:jc w:val="left"/>'
    '</w:pPr><w:tblPr><w:tblBorders>'
    + ''.join(
        f'<w:{side} w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    + '</w:tblBorders><w:tblCellMar>'
    '<w:top w:w="100" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
    '<w:bottom w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/>'
    '</w:tblCellMar></w:tblPr></w:style>')


def abstract_num(
        abstract_id: int, name: str, fmt: str, text: str,
        font: str | None = None) -> str:
    rfonts = (
        f'<w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" '
        f'w:hint="default"/></w:rPr>' if font else '')
    return (
        f'<w:abstractNum {nsdecls("w")} w:abstractNumId="{abstract_id}">'
        f'<w:multiLevelType w:val="singleLevel"/><w:name w:val="{name}"/>'
        f'<w:lvl w:ilvl="0"><w:start w:val="1"/>'
        f'<w:numFmt w:val="{fmt}"/><w:lvlText w:val="{text}"/>'
        f'<w:lvlJc w:val="left"/>'
        f'<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
        f'{rfonts}</w:lvl></w:abstractNum>')


# CT_Settings is a strict sequence: updateFields must precede these.
SETTINGS_AFTER_UPDATE_FIELDS = (
    'hdrShapeDefaults', 'footnotePr', 'endnotePr', 'compat', 'docVars',
    'rsids', 'mathPr', 'attachedSchema', 'themeFontLang',
    'clrSchemeMapping', 'doNotIncludeSubdocsInStats',
    'doNotAutoCompressPictures', 'forceUpgrade', 'captions',
    'readModeInkLockDown', 'smartTagType', 'schemaLibrary',
    'shapeDefaults', 'doNotEmbedSmartTags', 'decimalSymbol',
    'listSeparator')


def paragraph_text(element: BaseOxmlElement) -> str:
    return ''.join(t.text or '' for t in element.iter(qn('w:t'))).strip()


def is_blank(element: BaseOxmlElement) -> bool:
    return (
        element.tag == qn('w:p') and not paragraph_text(element)
        and next(element.iter(qn('w:drawing')), None) is None
        and next(element.iter(MC_ALTERNATE), None) is None)


def strip_body(document: DocxDocument) -> None:
    body = document.element.body
    children = list(body.iterchildren())
    cover_end = next(
        i for i, el in enumerate(children)
        if el.tag == qn('w:p') and paragraph_text(el) == COVER_END_TEXT)
    cover = children[:cover_end]
    while cover and is_blank(cover[-1]):
        cover.pop()
    # One section: the maquetado's first sectPr carries the header and
    # footer references; its last one only restarts page numbering.
    first_sect = next(body.iter(qn('w:sectPr')))
    final_sect = copy.deepcopy(first_sect)
    for el in children:
        if el not in cover:
            body.remove(el)
    body.append(final_sect)


def replace_styles(document: DocxDocument) -> None:
    styles = document.styles.element
    defaults = styles.find(qn('w:docDefaults'))
    rpr = defaults.find(qn('w:rPrDefault')).find(qn('w:rPr'))
    rpr.find(qn('w:rFonts')).getparent().replace(
        rpr.find(qn('w:rFonts')), parse_xml(
            f'<w:rFonts {nsdecls("w")} w:ascii="{FONT}" w:hAnsi="{FONT}" '
            f'w:eastAsia="{FONT}" w:cs="{FONT}"/>'))
    for xml in PARAGRAPH_STYLES + [OPTION_TABLE_STYLE]:
        new = parse_xml(xml)
        style_id = new.get(qn('w:styleId'))
        old = styles.xpath(f'w:style[@w:styleId="{style_id}"]')
        if old:
            styles.replace(old[0], new)
        else:
            styles.append(new)
    # The maquetado's anonymous table styles (a1, a5, af0…) only served
    # the dropped answer tables.
    for style in styles.xpath('w:style[@w:type="table"]'):
        if re.fullmatch(r'a[0-9a-f]*', style.get(qn('w:styleId'))):
            styles.remove(style)


def add_numbering(document: DocxDocument) -> None:
    numbering = document.part.numbering_part.element
    abstracts = numbering.findall(qn('w:abstractNum'))
    next_id = max(int(a.get(qn('w:abstractNumId'))) for a in abstracts) + 1
    bullet = parse_xml(abstract_num(
        next_id, BULLET_LIST, 'bullet', '•', font='Arial'))
    letter = parse_xml(abstract_num(
        next_id + 1, LETTER_LIST, 'lowerLetter', '%1.'))
    abstracts[-1].addnext(letter)
    abstracts[-1].addnext(bullet)
    bullet_num = numbering.add_num(next_id)
    list_item = document.styles.element.xpath(
        'w:style[@w:styleId="ListItem"]')[0]
    list_item.find(qn('w:pPr')).insert(0, parse_xml(
        f'<w:numPr {nsdecls("w")}><w:ilvl w:val="0"/>'
        f'<w:numId w:val="{bullet_num.numId}"/></w:numPr>'))


def request_field_update(document: DocxDocument) -> None:
    settings = document.settings.element
    update = parse_xml(f'<w:updateFields {nsdecls("w")} w:val="true"/>')
    anchor = next(
        (child for child in settings
         if child.tag.split('}')[1] in SETTINGS_AFTER_UPDATE_FIELDS), None)
    if anchor is None:
        settings.append(update)
    else:
        anchor.addprevious(update)


def main(src: Path = DEFAULT_SRC, target: Path = TARGET) -> None:
    document = Document(str(src))
    strip_body(document)
    replace_styles(document)
    add_numbering(document)
    request_field_update(document)
    document.save(str(target))
    print(f'{target} written from {src}')


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC)
