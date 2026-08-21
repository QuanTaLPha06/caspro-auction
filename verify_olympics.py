import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

oly = [q for q in data if q.get('sport') == 'Olympics']
print('Total Olympics questions:', len(oly))
for diff in ['Easy', 'Medium', 'Hard']:
    sub = [q for q in oly if q['difficulty'] == diff]
    print(f"=== {diff} ({len(sub)}) ===")
    for q in sub:
        print(f"{q['id']}: {q['question']}")
        print(f"   Options: {q['options']}")
        print(f"   Correct Index: {q['correct']} -> {q['options'][q['correct']]}\n")
