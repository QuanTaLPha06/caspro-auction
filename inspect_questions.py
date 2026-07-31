import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Total questions in questions_180.json: {len(questions)}")

weird_questions = []

for i, q in enumerate(questions):
    opts = q.get('options', [])
    corr = q.get('correct', 0)
    ans = opts[corr] if 0 <= corr < len(opts) else "ERR"
    
    # Check if options are homogeneous or if there's any weird options
    # Output to stdout safely
    line = f"Q{i+1}: {q['question']} | Ans: {ans} | Opts: {opts}"
    try:
        print(line)
    except Exception:
        print(line.encode('ascii', errors='replace').decode('ascii'))

