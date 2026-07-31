import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Fix map for known corrupted strings
fix_map = {
    'Mbapp': 'Mbappé',
    'Mourinho': 'Mourinho',
    'Jos': 'José',
    'Bjrn': 'Björn',
    'Amrica': 'América',
    'Pel': 'Pelé',
    'Ronaldo Nazrio': 'Ronaldo Nazário',
    'Sadio Man': 'Sadio Mané',
    'Luka Modri': 'Luka Modrić',
    'Nemanja Vidi': 'Nemanja Vidić',
    'Nemanja Vidic': 'Nemanja Vidić',
    'Modric': 'Modrić',
    '': '', # strip any leftover replacement chars
}

def clean_str(s):
    if not isinstance(s, str):
        return s
    for k, v in fix_map.items():
        s = s.replace(k, v)
    return s

cleaned = []
for q in questions:
    q['question'] = clean_str(q['question'])
    q['options'] = [clean_str(op) for op in q['options']]
    cleaned.append(q)

with open('questions_180.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print("Cleaned corrupted characters in questions_180.json!")
