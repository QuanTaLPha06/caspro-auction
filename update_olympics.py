import json
import re

easy_txt = """1. Which swimmer holds the record for most total Olympic medals of all time, with 28? A) Michael Phelps B) Usain Bolt C) Larisa Latynina D) Simone Biles Answer: A — Michael Phelps

2. Who holds the record for most Olympic gold medals by any athlete, with 23? A) Carl Lewis B) Michael Phelps C) Paavo Nurmi D) Mark Spitz Answer: B — Michael Phelps

3. Which sprinter set the current world record in the men's 100m at 9.58 seconds? A) Usain Bolt B) Tyson Gay C) Justin Gatlin D) Yohan Blake Answer: A — Usain Bolt

4. Who is the most decorated female Olympian in U.S. history? A) Katie Ledecky B) Missy Franklin C) Dara Torres D) Simone Manuel Answer: A — Katie Ledecky

5. Which Soviet gymnast held the record for most Olympic medals by a female athlete for decades, with 18 total? A) Larisa Latynina B) Nadia Comaneci C) Simone Biles D) Vera Caslavska Answer: A — Larisa Latynina

6. Which country holds the record for most medals ever won at a single Winter Olympics, set in 2026? A) Norway B) United States C) Germany D) Canada Answer: A — Norway

7. Which cross-country skier became the most decorated athlete in Winter Olympics history at the 2026 Games? A) Johannes Høsflot Klæbo B) Marit Bjørgen C) Ole Einar Bjørndalen D) Bjørn Dæhlie Answer: A — Johannes Høsflot Klæbo

8. Which country holds the record for most total Olympic medals (Summer Games) of any nation? A) United States B) Soviet Union C) Germany D) China Answer: A — United States

9. Who holds the men's marathon world record? A) Eliud Kipchoge B) Kelvin Kiptum C) Kenenisa Bekele D) Mo Farah Answer: B — Kelvin Kiptum

10. Which gymnast is famous for scoring the first-ever perfect 10 in Olympic history? A) Nadia Comaneci B) Simone Biles C) Olga Korbut D) Mary Lou Retton Answer: A — Nadia Comaneci"""

medium_txt = """1. Who holds the record for most gold medals won by an individual at the Winter Olympics? A) Johannes Høsflot Klæbo B) Marit Bjørgen C) Ole Einar Bjørndalen D) Bjørn Dæhlie Answer: A — Johannes Høsflot Klæbo

2. Who holds the record for most Olympic medals won by a female Winter Olympian? A) Marit Bjørgen B) Stefania Belmondo C) Claudia Pechstein D) Arianna Fontana Answer: A — Marit Bjørgen

3. Which wrestler went unbeaten for 13 years and won three consecutive Olympic golds, earning the nickname "the Experiment"? A) Alexander Karelin B) Mijaín López C) Buvaisar Saitiev D) Kaori Icho Answer: A — Alexander Karelin

4. Which Cuban wrestler holds the record for most consecutive Olympic golds in the same individual event, with five? A) Mijaín López B) Yowlys Bonne C) Reineris Salas D) Filiberto Ascuy Answer: A — Mijaín López

5. Which biathlete holds the record for most Olympic gold medals in his sport? A) Ole Einar Bjørndalen B) Martin Fourcade C) Johannes Thingnes Bø D) Emil Hegle Svendsen Answer: A — Ole Einar Bjørndalen

6. Which country has led the all-time Winter Olympics medal table for three consecutive Games in a row entering 2026? A) Norway B) Germany C) United States D) Russia Answer: A — Norway

7. Who holds the women's marathon world record? A) Ruth Chepngetich B) Brigid Kosgei C) Paula Radcliffe D) Tigst Assefa Answer: A — Ruth Chepngetich

8. Which sprinter's world record in the 100m has stood since 2009, unbroken for over 15 years? A) Usain Bolt B) Tyson Gay C) Asafa Powell D) Yohan Blake Answer: A — Usain Bolt

9. Which American swimmer holds the record for most Olympic golds by a female swimmer, tying a gymnastics legend? A) Katie Ledecky B) Missy Franklin C) Dara Torres D) Natalie Coughlin Answer: A — Katie Ledecky

10. Which discus thrower holds the record for winning the same individual Olympic event four times in a row? A) Al Oerter B) Virgilijus Alekna C) Jürgen Schult D) Fortune Gordien Answer: A — Al Oerter"""

hard_txt = """1. Who holds the record for the youngest individual Olympic gold medalist in the modern era? A) Marjorie Gestring B) Nadia Comaneci C) Fu Mingxia D) Kim Yun-mi Answer: A — Marjorie Gestring

2. Which shooter holds the record for oldest individual Olympic gold medalist in history? A) Oscar Swahn B) Ian Millar C) Hubert Raudaschl D) Durward Knowles Answer: A — Oscar Swahn

3. How many total gold medals did Norway win at the 2026 Milan Cortina Winter Olympics, setting a new single-Games record? A) 18 B) 16 C) 14 D) 20 Answer: A — 18

4. Which biathlete/cross-country skier trio previously shared the Winter Olympics gold medal record before it was broken in 2026? A) Marit Bjørgen, Ole Einar Bjørndalen, and Bjørn Dæhlie B) Kjetil André Aamodt, Björn Ferry, and Vegard Ulvang C) Stein Eriksen, Hjalmar Andersen, and Johan Grøttumsbråten D) Thomas Alsgaard, Vegard Ulvang, and Gunde Svan Answer: A — Marit Bjørgen, Ole Einar Bjørndalen, and Bjørn Dæhlie

5. Which country has amassed the most all-time Winter Olympics medals, surpassing 400 total? A) Norway B) United States C) Germany D) Austria Answer: A — Norway

6. Which sport's discus record is held by Al Oerter, who won it at four consecutive Olympics from 1956-1968? A) Discus throw B) Javelin throw C) Hammer throw D) Shot put Answer: A — Discus throw

7. Which archer holds the record for most Olympic gold medals in archery? A) Kim Soo-nyung B) Ki Bo-bae C) Jang Hye-jin D) An San Answer: A — Kim Soo-nyung

8. Which fencer holds the record for most Olympic gold medals in fencing? A) Valentina Vezzali B) Aladár Gerevich C) Edoardo Mangiarotti D) Nedo Nadi Answer: A — Valentina Vezzali

9. Which Hungarian fencer holds the record for the longest span between first and last Olympic gold medals, at 28 years? A) Aladár Gerevich B) Rudolf Kárpáti C) Pál Kovács D) Endre Kabos Answer: A — Aladár Gerevich

10. Which country became the first tropical, Latin American, and South American nation to win a Winter Olympics medal, doing so in 2026? A) Brazil B) Mexico C) Colombia D) Argentina Answer: A — Brazil"""

def parse_section(text, diff):
    blocks = [b.strip() for b in text.strip().split('\n\n') if b.strip()]
    parsed = []
    mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    for b in blocks:
        m = re.match(r'^\d+\.\s*(.*?)\s*A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*?)\s*Answer:\s*([A-D])\s*[—\-]\s*(.*)$', b, re.DOTALL)
        if not m:
            print('FAILED TO MATCH:', b)
            continue
        q, a, b, c, d, ans_let, ans_text = m.groups()
        parsed.append({
            'sport': 'Olympics',
            'difficulty': diff,
            'question': q.strip(),
            'options': [a.strip(), b.strip(), c.strip(), d.strip()],
            'correct': mapping[ans_let.strip()]
        })
    return parsed

new_easy = parse_section(easy_txt, 'Easy')
new_med = parse_section(medium_txt, 'Medium')
new_hard = parse_section(hard_txt, 'Hard')

print(f"Parsed counts: Easy={len(new_easy)}, Medium={len(new_med)}, Hard={len(new_hard)}")

with open('questions_180.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect existing IDs for easy/medium/hard olympics
easy_ids = [q['id'] for q in data if q.get('sport') == 'Olympics' and q.get('difficulty') == 'Easy']
med_ids = [q['id'] for q in data if q.get('sport') == 'Olympics' and q.get('difficulty') == 'Medium']
hard_ids = [q['id'] for q in data if q.get('sport') == 'Olympics' and q.get('difficulty') == 'Hard']

print("Easy IDs:", easy_ids)
print("Med IDs:", med_ids)
print("Hard IDs:", hard_ids)

for obj, q_id in zip(new_easy, easy_ids):
    obj['id'] = q_id

for obj, q_id in zip(new_med, med_ids):
    obj['id'] = q_id

for obj, q_id in zip(new_hard, hard_ids):
    obj['id'] = q_id

# Replace in main list preserving order
oly_indices = [i for i, q in enumerate(data) if q.get('sport') == 'Olympics']
new_all_oly = new_easy + new_med + new_hard

assert len(oly_indices) == len(new_all_oly) == 30

for idx, new_q in zip(oly_indices, new_all_oly):
    data[idx] = new_q

with open('questions_180.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("questions_180.json updated successfully!")
