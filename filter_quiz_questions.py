import json

with open('questions_db.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

allowed_sports = {
    'football': 'Football',
    'tennis': 'Tennis',
    'cricket': 'Cricket',
    'f1': 'Formula 1',
    'formula 1': 'Formula 1',
    'basketball': 'Basketball',
    'olympics': 'Olympics',
    'athletics': 'Olympics',
    'swimming': 'Olympics',
    'marathon': 'Olympics'
}

filtered_questions = []
for q in questions:
    sport_raw = q.get('sport', '').lower()
    matched_sport = None
    for key, canonical in allowed_sports.items():
        if key in sport_raw:
            matched_sport = canonical
            break
    if matched_sport:
        q['sport'] = matched_sport
        filtered_questions.append(q)

print(f"Original questions: {len(questions)}")
print(f"Filtered questions: {len(filtered_questions)}")

with open('questions_db.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_questions, f, indent=2, ensure_ascii=False)

print("Updated questions_db.json successfully!")
