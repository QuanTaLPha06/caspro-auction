import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('18 TEAM DRAWS FINAL.xlsx', 'r') as z:
    with z.open('xl/drawings/drawing1.xml') as f:
        content = f.read().decode('utf-8')

count = content.count('rightBrace')
print(f'Number of rightBrace shapes: {count}')

root = ET.fromstring(content)
ns = {
    'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
}
anchors = root.findall('xdr:twoCellAnchor', ns)
print(f'Total anchors: {len(anchors)}')

for i, anchor in enumerate(anchors):
    frm = anchor.find('xdr:from', ns)
    to  = anchor.find('xdr:to',   ns)
    sp  = anchor.find('xdr:sp',   ns)
    pic = anchor.find('xdr:pic',  ns)

    if frm is not None and to is not None:
        fc = frm.find('xdr:col', ns)
        fr = frm.find('xdr:row', ns)
        fo_col = frm.find('xdr:colOff', ns)
        fo_row = frm.find('xdr:rowOff', ns)
        tc = to.find('xdr:col', ns)
        tr = to.find('xdr:row', ns)
        to_col_off = to.find('xdr:colOff', ns)
        to_row_off = to.find('xdr:rowOff', ns)

        name = ''
        prst = ''
        if sp is not None:
            nvpr = sp.find('.//xdr:cNvPr', ns)
            if nvpr is not None:
                name = nvpr.get('name', '')
            geom = sp.find('.//a:prstGeom', ns)
            prst = geom.get('prst') if geom is not None else ''
            # Get position
            xfrm = sp.find('.//a:xfrm', ns)
            if xfrm is not None:
                off = xfrm.find('a:off', ns)
                ext = xfrm.find('a:ext', ns)
                if off is not None and ext is not None:
                    x = int(off.get('x', 0))
                    y = int(off.get('y', 0))
                    cx = int(ext.get('cx', 0))
                    cy = int(ext.get('cy', 0))
                    print(f'  [{i:02d}] {name} ({prst})')
                    print(f'        from: col={fc.text}, row={fr.text}, colOff={fo_col.text}, rowOff={fo_row.text}')
                    print(f'        to:   col={tc.text}, row={tr.text}, colOff={to_col_off.text}, rowOff={to_row_off.text}')
                    print(f'        pos:  x={x}, y={y}, cx={cx}, cy={cy}')
        elif pic is not None:
            nvpr = pic.find('.//xdr:cNvPr', ns)
            if nvpr is not None:
                name = nvpr.get('name', '')
            print(f'  [{i:02d}] IMAGE: {name}')
            print(f'        from: col={fc.text}, row={fr.text}')
            print(f'        to:   col={tc.text}, row={tr.text}')
