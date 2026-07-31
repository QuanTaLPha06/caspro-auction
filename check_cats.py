import json, re

for filename in ['index.html', 'Heads_Up_Sports.html', 'Sports_Connection_Quiz.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"=== {filename} ===")
    if 'cat' in content:
        cats = set(re.findall(r'"cat": "([^"]+)"', content))
        for c in sorted(cats):
            print(" -", c.encode('ascii', 'backslashreplace').decode('ascii'))
    if 'sport' in content:
        sports = set(re.findall(r'"sport": "([^"]+)"', content))
        for s in sorted(sports):
            print(" - [sport]", s.encode('ascii', 'backslashreplace').decode('ascii'))
