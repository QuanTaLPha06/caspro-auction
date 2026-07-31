import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open('all_180_review.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total questions: {len(questions)}\n\n")
    for i, q in enumerate(questions):
        opts = q['options']
        corr = q['correct']
        ans = opts[corr]
        q_text = q['question']
        out.write(f"[{i+1}] {q_text}\n")
        out.write(f"    Options: {opts}\n")
        out.write(f"    Correct ({corr}): {ans}\n\n")

print("Done writing to all_180_review.txt")
