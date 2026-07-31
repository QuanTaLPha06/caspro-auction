"""
Tournament Draw Generator
=========================
Generates draw Excel files by cloning reference files (13-19 teams).
For 11 & 12 teams, builds from scratch with rightBrace shapes, Century Gothic font,
zoomScale=42, and full cell formatting injected.

Outputs files in both naming conventions:
- "DODGEBALL 11 TEAM DRAWS FINAL.xlsx", etc.
- "Dodgeball 11 draws.xlsx", etc.
"""

import shutil, os, zipfile, io

REFERENCE_DIR = r"d:\Case"
OUTPUT_DIR    = r"d:\Case"

REFERENCE_FILES = {
    13: "13 TEAM DRAWS FINAL.xlsx",
    14: "14 TEAM DRAWS FINAL.xlsx",
    15: "15 TEAM DRAWS FINAL.xlsx",
    16: "16 TEAM DRAWS FINAL.xlsx",
    17: "17 TEAM DRAWS FINAL.xlsx",
    18: "18 TEAM DRAWS FINAL.xlsx",
    19: "19 TEAM DRAWS FINAL.xlsx",
}

JOBS = [
    ("DODGEBALL", 11),
    ("DODGEBALL", 12),
    ("DODGEBALL", 13),
    ("DODGEBALL", 14),
    ("DODGEBALL", 15),
    ("DODGEBALL", 16),
    ("KHO KHO",   14),
    ("KHO KHO",   15),
    ("KHO KHO",   16),
    ("KHO KHO",   17),
    ("KHO KHO",   18),
    ("KHO KHO",   19),
]


DRAW_NS = (
    'xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
)

def _anchor(idx, fc, fr, fco, fro, tc, tr, tco, tro):
    return f"""  <xdr:twoCellAnchor editAs="twoCell">
    <xdr:from><xdr:col>{fc}</xdr:col><xdr:colOff>{fco}</xdr:colOff><xdr:row>{fr}</xdr:row><xdr:rowOff>{fro}</xdr:rowOff></xdr:from>
    <xdr:to><xdr:col>{tc}</xdr:col><xdr:colOff>{tco}</xdr:colOff><xdr:row>{tr}</xdr:row><xdr:rowOff>{tro}</xdr:rowOff></xdr:to>
    <xdr:sp macro="" textlink="">
      <xdr:nvSpPr>
        <xdr:cNvPr id="{idx+1}" name="Right Brace {idx+1}"/>
        <xdr:cNvSpPr><a:spLocks noGrp="1"/></xdr:cNvSpPr>
      </xdr:nvSpPr>
      <xdr:spPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></a:xfrm>
        <a:prstGeom prst="rightBrace"><a:avLst/></a:prstGeom>
        <a:noFill/>
        <a:ln><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:ln>
      </xdr:spPr>
      <xdr:style>
        <a:lnRef idx="2"><a:schemeClr clr="accent1"><a:shade val="50000"/></a:schemeClr></a:lnRef>
        <a:fillRef idx="1"><a:schemeClr clr="accent1"/></a:fillRef>
        <a:effectRef idx="0"><a:schemeClr clr="accent1"/></a:effectRef>
        <a:fontRef idx="minor"><a:schemeClr clr="lt1"/></a:fontRef>
      </xdr:style>
      <xdr:txBody><a:bodyPr/><a:lstStyle/><a:p/></xdr:txBody>
    </xdr:sp>
    <xdr:clientData/>
  </xdr:twoCellAnchor>"""


def make_drawing_xml(shapes):
    anchors = "\n".join(_anchor(i, *s) for i, s in enumerate(shapes))
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<xdr:wsDr {DRAW_NS}>\n'
        f'{anchors}\n'
        '</xdr:wsDr>'
    )


WS_NS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'

def num_to_col(n):
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result

def make_worksheet_xml(cc_cells, text_cells, row_count=50, max_col=14):
    from collections import defaultdict
    import re
    rows_data = defaultdict(dict)

    for ref in cc_cells:
        m = re.match(r'([A-Z]+)(\d+)', ref)
        col, row = m.group(1), int(m.group(2))
        rows_data[row][col] = ('cc', '2', 's')   # value, style, type

    for ref, val in text_cells:
        m = re.match(r'([A-Z]+)(\d+)', ref)
        col, row = m.group(1), int(m.group(2))
        rows_data[row][col] = (val, '1', 'str')

    ss_map = {'cc': '0', 'best loser': '1'}

    row_xmls = []
    for r in range(1, row_count + 1):
        cells_in_row = rows_data.get(r, {})
        cell_xmls = []
        for col_idx in range(1, max_col + 1):
            col_letter = num_to_col(col_idx)
            ref = f"{col_letter}{r}"
            if col_letter in cells_in_row:
                val, style, vtype = cells_in_row[col_letter]
                if vtype == 's':
                    ss_idx = ss_map.get(val, '0')
                    cell_xmls.append(f'<c r="{ref}" s="{style}" t="s"><v>{ss_idx}</v></c>')
                else:
                    cell_xmls.append(f'<c r="{ref}" s="{style}" t="str"><v>{val}</v></c>')
            else:
                cell_xmls.append(f'<c r="{ref}" s="1"/>')

        row_xmls.append(f'<row r="{r}" ht="15.6" customHeight="1">{"".join(cell_xmls)}</row>')

    rows_xml = "\n".join(row_xmls)
    dim_ref = f"A1:{num_to_col(max_col)}{row_count}"

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet {WS_NS} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac" xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac">
  <dimension ref="{dim_ref}"/>
  <sheetViews>
    <sheetView tabSelected="1" zoomScale="42" workbookViewId="0">
      <selection activeCell="A1" sqref="A1"/>
    </sheetView>
  </sheetViews>
  <sheetFormatPr defaultColWidth="11.19921875" defaultRowHeight="15.6" x14ac:dyDescent="0.3"/>
  <sheetData>
{rows_xml}
  </sheetData>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
  <drawing r:id="rId1"/>
</worksheet>"""


STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac" xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac">
  <fonts count="2" x14ac:knownFonts="1">
    <font><sz val="12"/><color theme="1"/><name val="Calibri"/><family val="2"/><scheme val="minor"/></font>
    <font><sz val="12"/><color theme="1"/><name val="Century Gothic"/><family val="1"/></font>
  </fonts>
  <fills count="2">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="medium"><color indexed="64"/></left>
      <right style="medium"><color indexed="64"/></right>
      <top style="medium"><color indexed="64"/></top>
      <bottom style="medium"><color indexed="64"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1"/>
  </cellXfs>
  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>
</styleSheet>"""

SHARED_STRINGS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="2" uniqueCount="2">
  <si><t>cc</t></si>
  <si><t>best loser</t></si>
</sst>"""

WORKBOOK_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""

WORKBOOK_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

SHEET_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="../drawings/drawing1.xml"/>
</Relationships>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml"            ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml"   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml"              ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/xl/sharedStrings.xml"       ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
  <Override PartName="/xl/drawings/drawing1.xml"   ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>
</Types>"""


def write_xlsx(out_path, ws_xml, drawing_xml):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml',              CONTENT_TYPES)
        zf.writestr('_rels/.rels',                      ROOT_RELS)
        zf.writestr('xl/workbook.xml',                  WORKBOOK_XML)
        zf.writestr('xl/_rels/workbook.xml.rels',       WORKBOOK_RELS)
        zf.writestr('xl/styles.xml',                    STYLES_XML)
        zf.writestr('xl/sharedStrings.xml',             SHARED_STRINGS_XML)
        zf.writestr('xl/worksheets/sheet1.xml',         ws_xml)
        zf.writestr('xl/worksheets/_rels/sheet1.xml.rels', SHEET_RELS)
        zf.writestr('xl/drawings/drawing1.xml',         drawing_xml)
    try:
        with open(out_path, 'wb') as f:
            f.write(buf.getvalue())
    except PermissionError:
        print(f"  [WARN] PermissionError writing to {os.path.basename(out_path)} (file may be open in Excel)")


LAYOUTS = {
    11: {
        'cc': ['A2','A4','A7','A9','A12','A14','A17','A19','A22','A24','A27',
               'C3','C8','C13','C18','C23','C28',
               'E5','E15','E25',
               'G10','G20',
               'I15'],
        'text': [('A29', 'best loser')],
        'shapes': [
            (1,1,63500,38100,  1,3, 596900,165100),
            (1,6,63500,63500,  1,8, 774700,190500),
            (1,11,76200,63500, 1,13,762000,203200),
            (1,16,63500,63500, 1,18,800100,139700),
            (1,21,76200,38100, 1,23,749300,165100),
            (3,2,114300,152400,3,7, 812800, 88900),
            (3,12,76200,101600,3,17,787400,101600),
            (3,22,114300,101600,3,27,800100,127000),
            (5,4,165100,101600,6,14, 12700, 88900),
            (5,24,114300,101600,6,34, 12700,101600),
            (7,9,165100,88900, 8,29,546100,127000),
        ],
        'rows': 50,
    },
    12: {
        'cc': ['A2','A4','A7','A9','A12','A14','A17','A19',
               'A22','A24','A27','A29','A32','A34','A37','A39',
               'C3','C8','C13','C18','C23','C28','C33','C38',
               'E5','E15','E25','E35',
               'G10','G30',
               'I20'],
        'text': [],
        'shapes': [
            (1,1,63500,38100,  1,3, 596900,165100),
            (1,6,63500,63500,  1,8, 774700,190500),
            (1,11,76200,63500, 1,13,762000,203200),
            (1,16,63500,63500, 1,18,800100,139700),
            (1,21,76200,38100, 1,23,749300,165100),
            (1,26,63500,50800, 1,28,774700,177800),
            (1,31,0,88900,     1,33,787400,127000),
            (1,36,0,88900,     1,38,787400,127000),
            (3,2,114300,152400,3,7, 812800, 88900),
            (3,12,76200,101600,3,17,787400,101600),
            (3,22,114300,101600,3,27,800100,127000),
            (3,32,114300,88900,3,37,787400,127000),
            (5,4,165100,101600,6,14, 12700, 88900),
            (5,24,114300,101600,6,34, 12700,101600),
            (7,9,165100,88900, 8,29,546100,127000),
        ],
        'rows': 55,
    },
}


def safe_copy(src, dst):
    try:
        shutil.copy2(src, dst)
    except PermissionError:
        print(f"  [WARN] PermissionError copying to {os.path.basename(dst)} (file may be open in Excel)")


def build_from_scratch(teams, out_path):
    layout = LAYOUTS[teams]
    ws_xml      = make_worksheet_xml(layout['cc'], layout['text'], layout['rows'])
    drawing_xml = make_drawing_xml(layout['shapes'])
    write_xlsx(out_path, ws_xml, drawing_xml)


def generate(sport, teams):
    name1 = os.path.join(OUTPUT_DIR, f"{sport.upper()} {teams} TEAM DRAWS FINAL.xlsx")
    name2 = os.path.join(OUTPUT_DIR, f"{sport.title()} {teams} draws.xlsx")

    print(f"Generating for {sport} ({teams} teams)...")

    ref_file = REFERENCE_FILES.get(teams)
    if ref_file:
        ref_path = os.path.join(REFERENCE_DIR, ref_file)
        if os.path.exists(ref_path):
            safe_copy(ref_path, name1)
            safe_copy(ref_path, name2)
            print(f"  Cloned from {ref_file} -> {os.path.basename(name1)} & {os.path.basename(name2)}")
            return

    # Build from scratch for 11 & 12 teams
    print(f"  Building {teams}-team from scratch...")
    build_from_scratch(teams, name1)
    safe_copy(name1, name2)
    print(f"  Saved -> {os.path.basename(name1)} & {os.path.basename(name2)}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output Directory: {OUTPUT_DIR}\nGenerating draw files...\n")
    for sport, teams in JOBS:
        generate(sport, teams)
    print(f"\nDone! All files successfully generated.")


if __name__ == "__main__":
    main()
