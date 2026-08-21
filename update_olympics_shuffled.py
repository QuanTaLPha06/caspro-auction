import json
import re
import random

easy_txt = """1. Which swimmer holds the record for most total Olympic medals of all time, with 28?
A) Michael Phelps B) Usain Bolt C) Larisa Latynina D) Simone Biles
**Answer: A**

2. Who holds the record for most Olympic gold medals by any athlete, with 23?
A) Carl Lewis B) Michael Phelps C) Paavo Nurmi D) Mark Spitz
**Answer: B**

3. Which sprinter holds the current world record in the men's 100m at 9.58 seconds?
A) Usain Bolt B) Tyson Gay C) Justin Gatlin D) Yohan Blake
**Answer: A**

4. Who is the most decorated female Olympian in U.S. history?
A) Katie Ledecky B) Missy Franklin C) Dara Torres D) Simone Manuel
**Answer: A**

5. Which Soviet gymnast held the record for most Olympic medals by a female athlete for decades, with 18 total?
A) Larisa Latynina B) Nadia Comaneci C) Simone Biles D) Vera Caslavska
**Answer: A**

6. Which cross-country skier became the most decorated athlete in Winter Olympics history at the 2026 Games?
A) Johannes Høsflot Klæbo B) Marit Bjørgen C) Ole Einar Bjørndalen D) Bjørn Dæhlie
**Answer: A**

7. Which gymnast is famous for scoring the first-ever perfect 10 in Olympic history?
A) Nadia Comaneci B) Simone Biles C) Olga Korbut D) Mary Lou Retton
**Answer: A**

8. Who holds the men's marathon world record?
A) Eliud Kipchoge B) Kelvin Kiptum C) Kenenisa Bekele D) Mo Farah
**Answer: B**

9. Which gymnast became the most decorated U.S. gymnast in Olympic history at Paris 2024?
A) Simone Biles B) Shannon Miller C) Gabby Douglas D) Suni Lee
**Answer: A**

10. Which pole vaulter holds the current Olympic and world record in his event?
A) Sergey Bubka B) Armand Duplantis C) Renaud Lavillenie D) Sam Kendricks
**Answer: B**"""

medium_txt = """1. Who holds the record for most gold medals won by an individual at the Winter Olympics?
A) Johannes Høsflot Klæbo B) Marit Bjørgen C) Ole Einar Bjørndalen D) Bjørn Dæhlie
**Answer: A**

2. Who holds the record for most Olympic medals won by a female Winter Olympian?
A) Marit Bjørgen B) Stefania Belmondo C) Claudia Pechstein D) Arianna Fontana
**Answer: A**

3. Which wrestler went unbeaten for 13 years and won three consecutive Olympic golds, earning the nickname "the Experiment"?
A) Alexander Karelin B) Mijaín López C) Buvaisar Saitiev D) Kaori Icho
**Answer: A**

4. Which Cuban wrestler holds the record for most consecutive Olympic golds in the same individual event, with five?
A) Mijaín López B) Yowlys Bonne C) Reineris Salas D) Filiberto Ascuy
**Answer: A**

5. Which biathlete holds the record for most Olympic gold medals in his sport?
A) Ole Einar Bjørndalen B) Martin Fourcade C) Johannes Thingnes Bø D) Emil Hegle Svendsen
**Answer: A**

6. Who holds the women's marathon world record?
A) Ruth Chepngetich B) Brigid Kosgei C) Paula Radcliffe D) Tigst Assefa
**Answer: A**

7. Which sprinter's world record in the men's 100m has stood unbroken since 2009?
A) Usain Bolt B) Tyson Gay C) Asafa Powell D) Yohan Blake
**Answer: A**

8. Which swimmer holds the record for most Olympic golds by a female swimmer, tying a gymnastics legend?
A) Katie Ledecky B) Missy Franklin C) Dara Torres D) Natalie Coughlin
**Answer: A**

9. Which discus thrower holds the record for winning the same individual Olympic event four times in a row?
A) Al Oerter B) Virgilijus Alekna C) Jürgen Schult D) Fortune Gordien
**Answer: A**

10. Which distance runner holds the record for most Olympic gold medals in track and field by a man, with 9?
A) Paavo Nurmi B) Carl Lewis C) Usain Bolt D) Emil Zátopek
**Answer: A**"""

hard_txt = """1. Who holds the record for the youngest individual Olympic gold medalist in the modern era?
A) Marjorie Gestring B) Nadia Comaneci C) Fu Mingxia D) Kim Yun-mi
**Answer: A**

2. Which shooter holds the record for oldest individual Olympic gold medalist in history?
A) Oscar Swahn B) Ian Millar C) Hubert Raudaschl D) Durward Knowles
**Answer: A**

3. Which cross-country skier broke the previous three-way tie for most Winter Olympics gold medals in 2026?
A) Johannes Høsflot Klæbo B) Marit Bjørgen C) Ole Einar Bjørndalen D) Bjørn Dæhlie
**Answer: A**

4. Which archer holds the record for most Olympic gold medals in archery?
A) Kim Soo-nyung B) Ki Bo-bae C) Jang Hye-jin D) An San
**Answer: A**

5. Which fencer holds the record for most Olympic gold medals in fencing?
A) Valentina Vezzali B) Aladár Gerevich C) Edoardo Mangiarotti D) Nedo Nadi
**Answer: A**

6. Which Hungarian fencer holds the record for longest span between first and last Olympic gold medals, at 28 years?
A) Aladár Gerevich B) Rudolf Kárpáti C) Pál Kovács D) Endre Kabos
**Answer: A**

7. Which canoeist holds the record for most gold medals won in Olympic canoeing events?
A) Lisa Carrington B) Birgit Fischer C) Katie Vincent D) Jessica Fox
**Answer: A**

8. Which dressage rider holds the record for most wins in a single Olympic Games?
A) Isabell Werth B) Charlotte Dujardin C) Anky van Grunsven D) Reiner Klimke
**Answer: A**

9. Which table tennis player holds the record for most Olympic gold medals in the sport?
A) Ma Long B) Wang Liqin C) Zhang Jike D) Fan Zhendong
**Answer: A**

10. Which triathlete became the first athlete to win four total Olympic medals in the sport?
A) Alex Yee B) Hayden Wilde C) Léo Bergère D) Kristian Blummenfelt
**Answer: A**"""

def parse_and_shuffle(text, diff, seed_offset=0):
    blocks = [b.strip() for b in text.strip().split('\n\n') if b.strip()]
    parsed = []
    mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    for i, b in enumerate(blocks):
        lines = [line.strip() for line in b.split('\n') if line.strip()]
        q_text = lines[0]
        # remove leading "1. "
        q_text = re.sub(r'^\d+\.\s*', '', q_text)
        
        opts_line = lines[1]
        ans_line = lines[2]
        
        m_opts = re.match(r'^A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*)$', opts_line)
        if not m_opts:
            print("FAILED OPTS MATCH:", opts_line)
            continue
        orig_opts = list(m_opts.groups())
        
        m_ans = re.search(r'\*\*Answer:\s*([A-D])\*\*', ans_line)
        if not m_ans:
            print("FAILED ANS MATCH:", ans_line)
            continue
        correct_letter = m_ans.group(1)
        correct_answer_text = orig_opts[mapping[correct_letter]]
        
        # Shuffle options reproducibly/randomly so correct index varies
        random.seed(42 + seed_offset + i)
        shuffled_opts = orig_opts.copy()
        random.shuffle(shuffled_opts)
        
        new_correct_index = shuffled_opts.index(correct_answer_text)
        
        parsed.append({
            'sport': 'Olympics',
            'difficulty': diff,
            'question': q_text,
            'options': shuffled_opts,
            'correct': new_correct_index
        })
    return parsed

new_easy = parse_and_shuffle(easy_txt, 'Easy', 0)
new_med = parse_and_shuffle(medium_txt, 'Medium', 10)
new_hard = parse_and_shuffle(hard_txt, 'Hard', 20)

print(f"Parsed: Easy={len(new_easy)}, Med={len(new_med)}, Hard={len(new_hard)}")

with open('questions_180.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

easy_ids = [q['id'] for q in data if q.get('sport') == 'Olympics' and q.get('difficulty') == 'Easy']
med_ids = [q['id'] for q in data if q.get('sport') == 'Olympics' and q.get('difficulty') == 'Medium']
hard_ids = [q['id'] for q in data if q.get('sport') == 'Olympics' and q.get('difficulty') == 'Hard']

for obj, q_id in zip(new_easy, easy_ids):
    obj['id'] = q_id

for obj, q_id in zip(new_med, med_ids):
    obj['id'] = q_id

for obj, q_id in zip(new_hard, hard_ids):
    obj['id'] = q_id

oly_indices = [i for i, q in enumerate(data) if q.get('sport') == 'Olympics']
new_all_oly = new_easy + new_med + new_hard

for idx, new_q in zip(oly_indices, new_all_oly):
    data[idx] = new_q

with open('questions_180.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("questions_180.json successfully updated with shuffled options!")
