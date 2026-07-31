import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('18 TEAM DRAWS FINAL.xlsx', 'r') as z:
    with z.open('xl/sharedStrings.xml') as f:
        ss_content = f.read().decode('utf-8')

root = ET.fromstring(ss_content)
for i, si in enumerate(root):
    texts = []
    for t in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
        if t.text:
            texts.append(t.text)
    print(f"  [{i}]: {''.join(texts)!r}")
