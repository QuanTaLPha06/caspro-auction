import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('18 TEAM DRAWS FINAL.xlsx', 'r') as z:
    with z.open('xl/worksheets/sheet1.xml') as f:
        ws_content = f.read().decode('utf-8')

root = ET.fromstring(ws_content)
ns_uri = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

# Print all cells with their styles
print("--- All cells ---")
for row in root.iter(f'{{{ns_uri}}}row'):
    r = row.get('r')
    for cell in row:
        ref = cell.get('r', '')
        t = cell.get('t', '')
        s = cell.get('s', '0')
        v_el = cell.find(f'{{{ns_uri}}}v')
        v = v_el.text if v_el is not None else ''
        print(f"  {ref}: s={s}, t={t}, v={v}")
