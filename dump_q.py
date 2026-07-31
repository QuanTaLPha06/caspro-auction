import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    qs = json.load(f)

for i, q in enumerate(qs):
    print(f"{i:3d} | {q['id']} | {q['sport']} | {q['difficulty']} | {q['question']}")
