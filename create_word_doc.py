import zipfile
import xml.sax.saxutils as saxutils
import re
import os

def create_docx_from_md(md_path, docx_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.splitlines()

    document_body_xml = []

    # Helper XML generators
    def escape(t):
        return saxutils.escape(t)

    def make_paragraph(text_runs, p_style=None, space_after=120, bg_color=None):
        # text_runs: list of tuples (text, is_bold, is_italic, color, font_size)
        pPr = f'<w:pPr>'
        if p_style:
            pPr += f'<w:pStyle w:val="{p_style}"/>'
        if space_after is not None:
            pPr += f'<w:spacing w:after="{space_after}"/>'
        if bg_color:
            pPr += f'<w:shd w:val="clear" w:color="auto" w:fill="{bg_color}"/>'
        pPr += f'</w:pPr>'

        r_xmls = []
        for item in text_runs:
            txt, bold, italic, color, sz = item
            txt_esc = escape(txt)
            rPr = '<w:rPr>'
            if bold:
                rPr += '<w:b/>'
            if italic:
                rPr += '<w:i/>'
            if color:
                rPr += f'<w:color w:val="{color}"/>'
            if sz:
                rPr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
            rPr += '</w:rPr>'
            r_xmls.append(f'<w:r>{rPr}<w:t xml:space="preserve">{txt_esc}</w:t></w:r>')

        return f'<w:p>{pPr}{"".join(r_xmls)}</w:p>'

    def parse_inline(line_text, default_sz=22, default_color=None):
        # Parses **bold**, *italic*, and plain text into text_runs
        # Tokenize by bold ** and italic *
        # Simplified regex parser for markdown inline formatting
        tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*)', line_text)
        runs = []
        for tok in tokens:
            if not tok:
                continue
            if tok.startswith('**') and tok.endswith('**'):
                content = tok[2:-2]
                runs.append((content, True, False, default_color or "000000", default_sz))
            elif tok.startswith('*') and tok.endswith('*'):
                content = tok[1:-1]
                runs.append((content, False, True, default_color or "555555", default_sz))
            else:
                runs.append((tok, False, False, default_color, default_sz))
        return runs

    i = 0
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return ""
        # Build table XML
        tbl_xml = ['<w:tbl>',
                   '<w:tblPr>',
                   '<w:tblStyle w:val="TableGrid"/>',
                   '<w:tblW w:w="0" w:type="auto"/>',
                   '<w:tblBorders>',
                   '<w:top w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>',
                   '<w:left w:val="none"/>',
                   '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="1F4E78"/>',
                   '<w:right w:val="none"/>',
                   '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>',
                   '<w:insideV w:val="none"/>',
                   '</w:tblBorders>',
                   '</w:tblPr>']

        for r_idx, row in enumerate(table_rows):
            tbl_xml.append('<w:tr>')
            is_header = (r_idx == 0)
            for c_idx, cell in enumerate(row):
                bg = "1F4E78" if is_header else ("F2F4F8" if r_idx % 2 == 1 else "FFFFFF")
                txt_color = "FFFFFF" if is_header else "000000"
                runs = [(cell.strip(), is_header, False, txt_color, 22)]
                p_xml = make_paragraph(runs, space_after=60)
                tc_xml = f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{bg}"/><w:tcMar><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="180" w:type="dxa"/><w:right w:w="180" w:type="dxa"/></w:tcMar></w:tcPr>{p_xml}</w:tc>'
                tbl_xml.append(tc_xml)
            tbl_xml.append('</w:tr>')
        tbl_xml.append('</w:tbl>')
        tbl_xml.append(make_paragraph([], space_after=180)) # spacer
        table_rows = []
        return "".join(tbl_xml)

    while i < len(lines):
        line = lines[i].strip()

        # Handle Markdown Table
        if line.startswith('|') and line.endswith('|'):
            # check if separator line
            if '---' in line:
                i += 1
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            table_rows.append(cells)
            i += 1
            continue
        elif table_rows:
            document_body_xml.append(flush_table())

        if not line:
            i += 1
            continue

        # Headers
        if line.startswith('# '):
            title_text = line[2:].strip()
            document_body_xml.append(make_paragraph([(title_text, True, False, "1F4E78", 36)], space_after=240))
        elif line.startswith('## '):
            h2_text = line[3:].strip()
            document_body_xml.append(make_paragraph([(h2_text, True, False, "1F4E78", 28)], space_after=180))
        elif line.startswith('### '):
            h3_text = line[4:].strip()
            document_body_xml.append(make_paragraph([(h3_text, True, False, "2E75B6", 24)], space_after=140))
        elif line.startswith('#### '):
            h4_text = line[5:].strip()
            document_body_xml.append(make_paragraph([(h4_text, True, False, "333333", 22)], space_after=100))
        elif line == '---':
            # Horizontal rule
            document_body_xml.append(make_paragraph([], space_after=180))
        else:
            # Regular text line or Question/Answer line
            if line.startswith('*Answer:*') or line.startswith('_Answer:_') or 'Answer:' in line:
                runs = parse_inline(line, default_sz=22, default_color="1F4E78")
                document_body_xml.append(make_paragraph(runs, space_after=140, bg_color="F2F4F7"))
            else:
                runs = parse_inline(line, default_sz=22, default_color="1A1A1A")
                document_body_xml.append(make_paragraph(runs, space_after=100))

        i += 1

    if table_rows:
        document_body_xml.append(flush_table())

    # Build full document.xml content
    document_xml_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {"".join(document_body_xml)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

    rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    doc_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>'''

    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', content_types_xml)
        docx.writestr('_rels/.rels', rels_xml)
        docx.writestr('word/_rels/document.xml.rels', doc_rels_xml)
        docx.writestr('word/styles.xml', styles_xml)
        docx.writestr('word/document.xml', document_xml_content)

    print(f"Docx successfully written to {docx_path}")

if __name__ == "__main__":
    create_docx_from_md("Categorized_Sports_Quiz.md", "Categorized_Sports_Quiz.docx")
