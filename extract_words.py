import json
import re

with open('questions_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

extracted = []

def map_sport_cat(sport_raw):
    s = str(sport_raw).lower()
    if 'cricket' in s: return '🏏 CRICKET'
    if 'football' in s or 'soccer' in s: return '⚽ FOOTBALL'
    if 'tennis' in s: return '🎾 TENNIS'
    if 'basket' in s: return '🏀 BASKETBALL'
    if 'f1' in s or 'formula' in s or 'racing' in s or 'auto' in s: return '🏎️ FORMULA 1'
    if 'olympic' in s or 'athletic' in s or 'track' in s or 'sprint' in s or 'marathon' in s: return '🥇 OLYMPICS'
    if 'badminton' in s: return '🏸 BADMINTON'
    if 'dodgeball' in s: return '🤾 DODGEBALL'
    if 'kho' in s: return '🏃 KHO KHO'
    if 'golf' in s: return '⛳ GOLF'
    if 'swim' in s: return '🏊 SWIMMING'
    if 'chess' in s: return '♟️ CHESS'
    if 'box' in s or 'mma' in s or 'wrestl' in s: return '🥊 BOXING & COMBAT'
    return '🏆 SPORTS'

# Add existing SPORTS_DATA items from Heads_Up_Sports.html
existing_sports_data = [
    { "word": "Red Card", "cat": "⚽ FOOTBALL" },
    { "word": "VAR", "cat": "⚽ FOOTBALL" },
    { "word": "Ballon d'Or", "cat": "⚽ FOOTBALL" },
    { "word": "Nutmeg", "cat": "⚽ FOOTBALL" },
    { "word": "Offside", "cat": "⚽ FOOTBALL" },
    { "word": "Golden Boot", "cat": "⚽ FOOTBALL" },
    { "word": "Header", "cat": "⚽ FOOTBALL" },
    { "word": "Panenka", "cat": "⚽ FOOTBALL" },
    { "word": "Corner Kick", "cat": "⚽ FOOTBALL" },
    { "word": "Step Overs", "cat": "⚽ FOOTBALL" },
    { "word": "Crossbar", "cat": "⚽ FOOTBALL" },
    { "word": "Free Kick", "cat": "⚽ FOOTBALL" },
    { "word": "Backhand", "cat": "🎾 TENNIS" },
    { "word": "Forehand", "cat": "🎾 TENNIS" },
    { "word": "Volley", "cat": "🎾 TENNIS" },
    { "word": "Second Serve", "cat": "🎾 TENNIS" },
    { "word": "Rally", "cat": "🎾 TENNIS" },
    { "word": "Ace", "cat": "🎾 TENNIS" },
    { "word": "Racquet", "cat": "🎾 TENNIS" },
    { "word": "Slice", "cat": "🎾 TENNIS" },
    { "word": "Top Spin", "cat": "🎾 TENNIS" },
    { "word": "Roland Garros", "cat": "🎾 TENNIS" },
    { "word": "Wimbledon", "cat": "🎾 TENNIS" },
    { "word": "Match Point", "cat": "🎾 TENNIS" },
    { "word": "100m Sprint", "cat": "🥇 OLYMPICS" },
    { "word": "Pole Vault", "cat": "🥇 OLYMPICS" },
    { "word": "Freestyle 100m", "cat": "🥇 OLYMPICS" },
    { "word": "Gold Medal", "cat": "🥇 OLYMPICS" },
    { "word": "Olympic Rings", "cat": "🥇 OLYMPICS" },
    { "word": "Relay Race", "cat": "🥇 OLYMPICS" },
    { "word": "High Jump", "cat": "🥇 OLYMPICS" },
    { "word": "Marathon", "cat": "🥇 OLYMPICS" },
    { "word": "Discus Throw", "cat": "🥇 OLYMPICS" },
    { "word": "3 Point Shot", "cat": "🏀 BASKETBALL" },
    { "word": "2 Point Shot", "cat": "🏀 BASKETBALL" },
    { "word": "Technical Foul", "cat": "🏀 BASKETBALL" },
    { "word": "Pick & Roll", "cat": "🏀 BASKETBALL" },
    { "word": "Slam Dunk", "cat": "🏀 BASKETBALL" },
    { "word": "Fast Break", "cat": "🏀 BASKETBALL" },
    { "word": "Stepback", "cat": "🏀 BASKETBALL" },
    { "word": "Time Out", "cat": "🏀 BASKETBALL" },
    { "word": "Alley Oop", "cat": "🏀 BASKETBALL" },
    { "word": "Rebound", "cat": "🏀 BASKETBALL" },
    { "word": "Buzzer Beater", "cat": "🏀 BASKETBALL" },
    { "word": "Pit Stop", "cat": "🏎️ FORMULA 1" },
    { "word": "Yellow Flag", "cat": "🏎️ FORMULA 1" },
    { "word": "Safety Car", "cat": "🏎️ FORMULA 1" },
    { "word": "Team Radio", "cat": "🏎️ FORMULA 1" },
    { "word": "Overtake", "cat": "🏎️ FORMULA 1" },
    { "word": "DRS Zone", "cat": "🏎️ FORMULA 1" },
    { "word": "Podium", "cat": "🏎️ FORMULA 1" },
    { "word": "Pole Position", "cat": "🏎️ FORMULA 1" },
    { "word": "Sprint Race", "cat": "🏎️ FORMULA 1" },
    { "word": "Checkered Flag", "cat": "🏎️ FORMULA 1" },
    { "word": "Reverse Sweep", "cat": "🏏 CRICKET" },
    { "word": "Powerplay", "cat": "🏏 CRICKET" },
    { "word": "Strategic Timeout", "cat": "🏏 CRICKET" },
    { "word": "Sixer", "cat": "🏏 CRICKET" },
    { "word": "LBW", "cat": "🏏 CRICKET" },
    { "word": "Hat Trick", "cat": "🏏 CRICKET" },
    { "word": "Yorker", "cat": "🏏 CRICKET" },
    { "word": "Free Hit", "cat": "🏏 CRICKET" },
    { "word": "Super Over", "cat": "🏏 CRICKET" },
    { "word": "Bouncer", "cat": "🏏 CRICKET" }
]

extracted.extend(existing_sports_data)

for q in db:
    sport_cat = map_sport_cat(q.get('sport', ''))
    clues = q.get('clues', [])
    for c in clues:
        clean_c = re.sub(r'^Clue\s*\d+\s*:\s*', '', c).strip()
        clean_c = re.sub(r'\s*\([^)]*\)', '', clean_c).strip()
        if 2 <= len(clean_c) <= 35:
            extracted.append({'word': clean_c, 'cat': sport_cat})

with open('Categorized_Sports_Quiz.md', 'r', encoding='utf-8') as f:
    md = f.read()

ans_matches = re.findall(r'\*\*Answer:\*\*\s*(.+)', md)
for a in ans_matches:
    clean_a = re.sub(r'\([^)]*\)', '', a).strip()
    clean_a = re.sub(r'[*_`]', '', clean_a).strip()
    if 2 <= len(clean_a) <= 35 and not clean_a.startswith('http'):
        extracted.append({'word': clean_a, 'cat': '🏆 SPORTS'})

seen = set()
final_words = []
ignore_terms = {'all of the above', 'none of the above', 'true', 'false', 'both a and b'}

for item in extracted:
    w = item['word'].strip()
    w_lower = w.lower()
    if (w_lower not in seen and 
        len(w) >= 2 and 
        w_lower not in ignore_terms and 
        not any(w_lower.startswith(p) for p in ['http', 'www', 'see ', 'note:'])):
        seen.add(w_lower)
        final_words.append({'word': w, 'cat': item['cat']})

print(f"Total extracted unique sports words: {len(final_words)}")

with open('final_sports_words.json', 'w', encoding='utf-8') as f:
    json.dump(final_words, f, indent=2, ensure_ascii=False)
