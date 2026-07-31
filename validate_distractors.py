import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

suspect_questions = []

for i, q in enumerate(questions):
    text = q['question'].lower()
    opts = q['options']
    corr = q['correct']

    # 1. Ask for club/team
    if 'which club' in text or 'which team' in text or 'which franchise' in text:
        # Check if options contain person names like 'messi', 'ronaldo', 'jordan', etc.
        people_keywords = ['messi', 'ronaldo', 'jordan', 'tendulkar', 'dhoni', 'salah', 'federer', 'nadal', 'djokovic', 'curry', 'james', 'pelé', 'pélé', 'pele']
        for op in opts:
            if any(pk in op.lower() for pk in people_keywords):
                suspect_questions.append((i+1, "Asking for club but option is a person", q))
                break

    # 2. Ask for person / who
    if 'who ' in text or 'which player' in text or 'which batter' in text or 'which bowler' in text or 'which manager' in text:
        # Check if options contain club names or numbers or countries when asking for a player
        clubs_keywords = ['real madrid', 'barcelona', 'bayern', 'manchester', 'liverpool', 'psg', 'juventus', 'milan', 'inter', 'chelsea', 'arsenal']
        for op in opts:
            if any(ck in op.lower() for ck in clubs_keywords):
                suspect_questions.append((i+1, "Asking for person but option is a club", q))
                break

    # 3. Ask for country / nation
    if 'which country' in text or 'which nation' in text or 'which national team' in text:
        clubs_people = ['real madrid', 'barcelona', 'messi', 'ronaldo', 'psg', 'milan', 'lakers', 'celtics']
        for op in opts:
            if any(cp in op.lower() for cp in clubs_people):
                suspect_questions.append((i+1, "Asking for country but option is club/person", q))
                break

print(f"Found {len(suspect_questions)} suspect questions out of {len(questions)}")
for sq in suspect_questions:
    print(f"Q{sq[0]}: {sq[1]}")
    print(f"   Q: {sq[2]['question']}")
    print(f"   Opts: {sq[2]['options']}\n")
