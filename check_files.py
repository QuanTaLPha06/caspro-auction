import zipfile, os

files = [
    'DODGEBALL 11 TEAM DRAWS FINAL.xlsx',
    'DODGEBALL 12 TEAM DRAWS FINAL.xlsx',
    'DODGEBALL 13 TEAM DRAWS FINAL.xlsx',
    'DODGEBALL 14 TEAM DRAWS FINAL.xlsx',
    'DODGEBALL 15 TEAM DRAWS FINAL.xlsx',
    'DODGEBALL 16 TEAM DRAWS FINAL.xlsx',
    'KHO KHO 14 TEAM DRAWS FINAL.xlsx',
    'KHO KHO 15 TEAM DRAWS FINAL.xlsx',
    'KHO KHO 16 TEAM DRAWS FINAL.xlsx',
    'KHO KHO 17 TEAM DRAWS FINAL.xlsx',
    'KHO KHO 18 TEAM DRAWS FINAL.xlsx',
    'KHO KHO 19 TEAM DRAWS FINAL.xlsx',
]

for fn in files:
    path = os.path.join(r'd:\Case', fn)
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        has_draw = 'xl/drawings/drawing1.xml' in names
        braces = z.read('xl/drawings/drawing1.xml').decode('utf-8').count('rightBrace') if has_draw else 0
        s1 = z.read('xl/worksheets/sheet1.xml').decode('utf-8')
        has_zoom = 'zoomScale="42"' in s1
        st = z.read('xl/styles.xml').decode('utf-8')
        has_cg = 'Century Gothic' in st
        print(f"{fn:<35} | drawing: {str(has_draw):<5} | braces: {braces:<2} | zoom42: {str(has_zoom):<5} | CenturyGothic: {str(has_cg):<5}")
