import json, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open('final_sports_words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


print(f"Total words: {len(data)}")
cats = Counter(x.get('cat', 'Uncategorized') for x in data)
for cat, count in cats.items():
    print(f"Category: {cat} -> {count} items")

print("\nSample items per category:")
by_cat = {}
for item in data:
    c = item.get('cat', 'Uncategorized')
    by_cat.setdefault(c, []).append(item['word'])

for c, words in by_cat.items():
    print(f"\n--- {c} ({len(words)}) ---")
    print(", ".join(words[:15]))
