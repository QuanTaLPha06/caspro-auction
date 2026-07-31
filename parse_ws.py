import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('18 TEAM DRAWS FINAL.xlsx', 'r') as z:
    names = z.namelist()
    print("Files:", [n for n in names if 'drawing' in n or 'sheet' in n.lower()])
    
    # Read sheet1 to understand cc layout
    sheet_name = 'xl/worksheets/sheet1.xml'
    with z.open(sheet_name) as f:
        ws_content = f.read().decode('utf-8')

root = ET.fromstring(ws_content)
ns = {'': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

# Print all cells with values
print("\n--- Cells with values ---")
for row in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
    r = row.get('r')
    for cell in row:
        ref = cell.get('r', '')
        t = cell.get('t', '')
        v_el = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
        v = v_el.text if v_el is not None else ''
        f_el = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}f')
        if v or f_el is not None:
            print(f"  {ref}: t={t} v={v}")

# Print row heights
print("\n--- Row dimensions ---")
for row in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
    r = row.get('r')
    ht = row.get('ht', '')
    if ht:
        print(f"  Row {r}: ht={ht}")

# Print col widths
print("\n--- Column dimensions ---")
for col in root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}col'):
    mn = col.get('min', '')
    mx = col.get('max', '')
    w = col.get('width', '')
    print(f"  Col {mn}-{mx}: width={w}")
