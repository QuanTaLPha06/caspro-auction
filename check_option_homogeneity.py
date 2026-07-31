import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions")

# Let's inspect every question and its 4 options line by line
with open('question_options_audit.txt', 'w', encoding='utf-8') as f:
    for i, q in enumerate(questions):
        f.write(f"Q{i+1:03d} [{q['sport']}|{q['difficulty']}] {q['question']}\n")
        f.write(f"      Options: {q['options']}\n")
        f.write(f"      Correct: Index {q['correct']} -> '{q['options'][q['correct']]}'\n\n")

print("Wrote full audit to question_options_audit.txt")
