import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for b, (start, end) in enumerate([(0, 60), (60, 120), (120, 180)]):
    filename = f"batch_{b+1}.txt"
    with open(filename, 'w', encoding='utf-8') as out:
        for i in range(start, end):
            item = questions[i]
            q_str = item['question']
            opts = item['options']
            corr = opts[item['correct']]
            out.write(f"Q{i+1:03d}: {q_str}\n")
            out.write(f"     Options: {opts}\n")
            out.write(f"     Correct: {corr}\n\n")
    print(f"Wrote {filename}")
