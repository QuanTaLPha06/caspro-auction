import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('18 TEAM DRAWS FINAL.xlsx', 'r') as z:
    with z.open('xl/styles.xml') as f:
        content = f.read().decode('utf-8')

root = ET.fromstring(content)
ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

# borders
borders = root.find(f'{{{ns}}}borders')
if borders is not None:
    for i, border in enumerate(borders):
        parts = []
        for side in ['left','right','top','bottom','diagonal']:
            el = border.find(f'{{{ns}}}{side}')
            if el is not None:
                style = el.get('style', 'none')
                color_el = el.find(f'{{{ns}}}color')
                color = color_el.get('rgb', '') if color_el is not None else ''
                parts.append(f'{side}:{style}:{color}')
        print(f'Border [{i}]: {parts}')

# xfs (cell formats)
xfs = root.find(f'{{{ns}}}cellXfs')
if xfs is not None:
    for i, xf in enumerate(xfs):
        border_id = xf.get('borderId', '0')
        fill_id = xf.get('fillId', '0')
        font_id = xf.get('fontId', '0')
        align = xf.find(f'{{{ns}}}alignment')
        h_align = align.get('horizontal', '') if align is not None else ''
        v_align = align.get('vertical', '') if align is not None else ''
        wrap = align.get('wrapText', '') if align is not None else ''
        print(f'XF [{i}]: border={border_id}, fill={fill_id}, font={font_id}, align={h_align}/{v_align}, wrap={wrap}')

# fills
fills = root.find(f'{{{ns}}}fills')
if fills is not None:
    for i, fill in enumerate(fills):
        pf = fill.find(f'{{{ns}}}patternFill')
        if pf is not None:
            ptype = pf.get('patternType', '')
            fgc = pf.find(f'{{{ns}}}fgColor')
            bg_c = pf.find(f'{{{ns}}}bgColor')
            fg = fgc.get('rgb', '') if fgc is not None else ''
            bg = bg_c.get('rgb', '') if bg_c is not None else ''
            print(f'Fill [{i}]: type={ptype}, fg={fg}, bg={bg}')
