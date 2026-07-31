import json

with open('final_sports_words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print(f"Total: {len(words)}")
for i, w in enumerate(words[:50]):
    print(f"{i+1}. [{w['cat']}] {w['word']}")
