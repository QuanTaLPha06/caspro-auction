import json, re

with open('questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Auditing {len(questions)} questions...")

issues = []

for idx, q in enumerate(questions):
    q_id = q.get('id', f'Q{idx+1}')
    text = q.get('question', '')
    opts = q.get('options', [])
    corr = q.get('correct', 0)
    sport = q.get('sport', '')
    diff = q.get('difficulty', '')

    # Check length of options
    if len(opts) != 4:
        issues.append((idx+1, q_id, text, f"Invalid options count: {len(opts)}"))
        continue

    # Check correct index
    if not (0 <= corr < 4):
        issues.append((idx+1, q_id, text, f"Invalid correct index: {corr}"))
        continue

    ans = opts[corr]

    # Check character replacement issues (like )
    for op_idx, op in enumerate(opts):
        if '' in op or '\ufffd' in op:
            issues.append((idx+1, q_id, text, f"Option {op_idx} contains corrupted char: {op}"))
    if '' in text or '\ufffd' in text:
        issues.append((idx+1, q_id, text, f"Question text contains corrupted char: {text}"))

    # Heuristic category matching check
    text_lower = text.lower()

    # Rule 1: asks for country / nation / national team
    if any(k in text_lower for k in ['which country', 'which nation', 'which national team', 'national side']):
        # answer and options should look like countries
        pass

    # Rule 2: asks for player / who / batter / bowler / superstar / footballer / legend
    if any(k in text_lower for k in ['who is', 'who won', 'who holds', 'which player', 'which batter', 'which bowler', 'which superstar', 'who was', 'which manager', 'who scored']):
        # If options contain club names or numbers instead of people names
        pass

    # Rule 3: asks for club / team
    if any(k in text_lower for k in ['which club', 'which team', 'which franchise']):
        # Check if options are clubs
        pass

print(f"Total basic issues found: {len(issues)}")
for iss in issues:
    print(iss)
