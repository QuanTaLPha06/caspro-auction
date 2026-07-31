import zipfile, xml.etree.ElementTree as ET, re, json, random

def get_docx_lines(path):
    with zipfile.ZipFile(path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        return [''.join([node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]).strip()
                for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
                if ''.join([node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]).strip()]

docx_path = r'C:\Users\Kevin Gandhi\Downloads\Sports_Quiz_Exam_Ready.docx'
lines = get_docx_lines(docx_path)

answer_key = {}
ak_started = False
for l in lines:
    if l == 'Answer Key':
        ak_started = True
        continue
    if ak_started:
        matches = re.findall(r'(\d+):\s*([A-D])', l)
        for num, ans in matches:
            answer_key[int(num)] = ans

current_sport = 'Football'
current_diff = 'Easy'

docx_qs = []
i = 0
while i < len(lines):
    l = lines[i]
    if l == 'Answer Key':
        break
    
    if l in ['Football (Soccer)', 'Football']:
        current_sport = 'Football'
    elif l in ['Basketball']:
        current_sport = 'Basketball'
    elif l in ['Tennis']:
        current_sport = 'Tennis'
    elif l.startswith('Easy'):
        current_diff = 'Easy'
    elif l.startswith('Medium'):
        current_diff = 'Medium'
    elif l.startswith('Hard'):
        current_diff = 'Hard'
        
    m = re.match(r'^(\d+)\.\s+(.*)', l)
    if m:
        q_num = int(m.group(1))
        q_text = m.group(2)
        options = []
        j = i + 1
        while j < len(lines) and len(options) < 4:
            opt_line = lines[j]
            opt_m = re.match(r'^([A-D])\.\s+(.*)', opt_line)
            if opt_m:
                options.append(opt_m.group(2))
                j += 1
            else:
                break
        if len(options) == 4 and q_num in answer_key:
            ans_letter = answer_key[q_num]
            ans_idx = ord(ans_letter) - ord('A')
            docx_qs.append({
                'id': f'DOCX_{q_num}',
                'sport': current_sport,
                'difficulty': current_diff,
                'question': q_text,
                'options': options,
                'correct': ans_idx
            })
            i = j - 1
    i += 1

# Define parsed Cricket questions from Prompt
cricket_qs_data = [
    # EASY
    {"difficulty": "Easy", "question": "Which country won the first Cricket World Cup in 1975?", "options": ["Australia", "West Indies", "England", "India"], "correct": 1},
    {"difficulty": "Easy", "question": "How many players are on a cricket team on the field?", "options": ["10", "11", "12", "9"], "correct": 1},
    {"difficulty": "Easy", "question": "How many runs is a hit over the boundary without bouncing worth?", "options": ["4", "6", "8", "5"], "correct": 1},
    {"difficulty": "Easy", "question": "How many runs is a hit that bounces before crossing the boundary worth?", "options": ["2", "4", "6", "3"], "correct": 1},
    {"difficulty": "Easy", "question": "Which country is historically known as the birthplace of cricket?", "options": ["Australia", "India", "England", "South Africa"], "correct": 2},
    {"difficulty": "Easy", "question": "Which country has won the most Men’s ODI World Cup titles?", "options": ["India", "West Indies", "Australia", "England"], "correct": 2},
    {"difficulty": "Easy", "question": "What color ball is traditionally used in daytime Test cricket?", "options": ["White", "Red", "Pink", "Yellow"], "correct": 1},
    {"difficulty": "Easy", "question": "What color ball is commonly used in ODI day-night matches?", "options": ["Red", "White", "Pink", "Orange"], "correct": 1},
    {"difficulty": "Easy", "question": "How many wooden stumps make up the wicket at one end of the pitch?", "options": ["2", "3", "4", "5"], "correct": 1},
    {"difficulty": "Easy", "question": "In cricket, what is a batter dismissed for zero runs called?", "options": ["A score of 50", "A duck", "A wide ball", "A catch drop"], "correct": 1},
    {"difficulty": "Easy", "question": "What is taking three wickets in three consecutive deliveries called?", "options": ["Super Over", "Triple Strike", "Hat-trick", "Clean Sweep"], "correct": 2},
    {"difficulty": "Easy", "question": "What is the maximum number of overs per innings in a T20 match?", "options": ["15", "20", "50", "10"], "correct": 1},
    {"difficulty": "Easy", "question": "What is the maximum number of overs per innings in a standard ODI match?", "options": ["20", "40", "50", "60"], "correct": 2},
    {"difficulty": "Easy", "question": "Which country hosted the 2023 ICC Men's Cricket World Cup?", "options": ["Australia", "England", "India", "South Africa"], "correct": 2},
    {"difficulty": "Easy", "question": "Which national team won the 2023 ICC Men's Cricket World Cup?", "options": ["India", "Australia", "South Africa", "New Zealand"], "correct": 1},
    {"difficulty": "Easy", "question": "Which country won the 2024 ICC Men’s T20 World Cup?", "options": ["South Africa", "England", "India", "Australia"], "correct": 2},
    {"difficulty": "Easy", "question": "Which Indian cricketer is famously nicknamed 'Hitman'?", "options": ["Virat Kohli", "MS Dhoni", "Rohit Sharma", "KL Rahul"], "correct": 2},
    {"difficulty": "Easy", "question": "Which Indian cricketer is famously nicknamed 'King Kohli'?", "options": ["Rohit Sharma", "Virat Kohli", "Shubman Gill", "Yuvraj Singh"], "correct": 1},
    {"difficulty": "Easy", "question": "Which legendary captain is fondly known as 'Captain Cool' in India?", "options": ["Kapil Dev", "Sourav Ganguly", "MS Dhoni", "Rahul Dravid"], "correct": 2},
    {"difficulty": "Easy", "question": "Which Indian batter is world-famous for inventing the 'helicopter shot'?", "options": ["Sachin Tendulkar", "MS Dhoni", "Virender Sehwag", "AB de Villiers"], "correct": 1},

    # MEDIUM
    {"difficulty": "Medium", "question": "Who was named Player of the Match in the 2011 ODI World Cup final?", "options": ["Gautam Gambhir", "MS Dhoni", "Yuvraj Singh", "Zaheer Khan"], "correct": 1},
    {"difficulty": "Medium", "question": "Which player hit the winning six and scored 91* in the 2011 World Cup final?", "options": ["Gautam Gambhir", "MS Dhoni", "Sachin Tendulkar", "Virat Kohli"], "correct": 1},
    {"difficulty": "Medium", "question": "Against which country did Sachin Tendulkar make his international debut in 1989?", "options": ["England", "Australia", "Pakistan", "West Indies"], "correct": 2},
    {"difficulty": "Medium", "question": "Which bowler took the first-ever hat-trick in Cricket World Cup history?", "options": ["Wasim Akram", "Chetan Sharma", "Saqlain Mushtaq", "Kapil Dev"], "correct": 1},
    {"difficulty": "Medium", "question": "Who was the first male cricketer to score a double century in ODI cricket?", "options": ["Virender Sehwag", "Rohit Sharma", "Sachin Tendulkar", "Chris Gayle"], "correct": 2},
    {"difficulty": "Medium", "question": "Against which team did Sachin Tendulkar score his iconic 200* in ODIs?", "options": ["Australia", "South Africa", "Sri Lanka", "Bangladesh"], "correct": 1},
    {"difficulty": "Medium", "question": "Who was the first male cricketer to score a century in T20 Internationals?", "options": ["Brendon McCullum", "Chris Gayle", "Suresh Raina", "Rohit Sharma"], "correct": 1},
    {"difficulty": "Medium", "question": "Who holds the record for the highest individual score in Men’s Test cricket (400*)?", "options": ["Matthew Hayden", "Brian Lara", "Sir Donald Bradman", "Virender Sehwag"], "correct": 1},
    {"difficulty": "Medium", "question": "Which bowler has taken the most wickets in Test cricket history (800 wickets)?", "options": ["Shane Warne", "James Anderson", "Muttiah Muralitharan", "Anil Kumble"], "correct": 2},
    {"difficulty": "Medium", "question": "Which fast bowler holds the record for most wickets in Test match history?", "options": ["Glenn McGrath", "Stuart Broad", "James Anderson", "Wasim Akram"], "correct": 2},
    {"difficulty": "Medium", "question": "Which spinner holds the record for most wickets in ODI cricket history?", "options": ["Wasim Akram", "Muttiah Muralitharan", "Waqar Younis", "Chaminda Vaas"], "correct": 1},
    {"difficulty": "Medium", "question": "Against which team did Anil Kumble take all 10 wickets in a Test innings (1999)?", "options": ["Australia", "England", "Pakistan", "Sri Lanka"], "correct": 2},
    {"difficulty": "Medium", "question": "Who captained Australia to back-to-back undefeated ODI World Cup wins in 2003 and 2007?", "options": ["Allan Border", "Steve Waugh", "Ricky Ponting", "Michael Clarke"], "correct": 2},
    {"difficulty": "Medium", "question": "Which country won the 2013 ICC Champions Trophy under MS Dhoni?", "options": ["England", "Sri Lanka", "India", "South Africa"], "correct": 2},
    {"difficulty": "Medium", "question": "Which batter holds the record for most centuries in ODI cricket history?", "options": ["Sachin Tendulkar", "Virat Kohli", "Rohit Sharma", "Ricky Ponting"], "correct": 1},
    {"difficulty": "Medium", "question": "Which player holds the record for the most total centuries in Test cricket (51 centuries)?", "options": ["Jacques Kallis", "Ricky Ponting", "Sachin Tendulkar", "Steve Smith"], "correct": 2},
    {"difficulty": "Medium", "question": "Which wicketkeeper has the most total dismissals across all international formats?", "options": ["MS Dhoni", "Adam Gilchrist", "Mark Boucher", "Kumar Sangakkara"], "correct": 2},
    {"difficulty": "Medium", "question": "Which cricketer played an extraordinary 200 Test matches during his career?", "options": ["James Anderson", "Ricky Ponting", "Sachin Tendulkar", "Steve Waugh"], "correct": 2},
    {"difficulty": "Medium", "question": "Who scored the fastest century in ODI cricket history (off just 31 balls)?", "options": ["Shahid Afridi", "AB de Villiers", "Corey Anderson", "Chris Gayle"], "correct": 1},
    {"difficulty": "Medium", "question": "Which Indian stadium has the highest seating capacity in the world?", "options": ["Eden Gardens", "Wankhede Stadium", "Narendra Modi Stadium", "M. Chinnaswamy Stadium"], "correct": 2},

    # HARD
    {"difficulty": "Hard", "question": "Who was the first player given out by a third umpire (TV replay) in international cricket?", "options": ["Rahul Dravid", "Sachin Tendulkar", "Brian Lara", "Hansie Cronje"], "correct": 1},
    {"difficulty": "Hard", "question": "Which two teams played the first official Men’s T20 International in 2005?", "options": ["England and Australia", "Australia and New Zealand", "South Africa and New Zealand", "India and Pakistan"], "correct": 1},
    {"difficulty": "Hard", "question": "Who was the first cricketer in history to reach 10,000 runs in ODI cricket?", "options": ["Desmond Haynes", "Sunil Gavaskar", "Sachin Tendulkar", "Inzamam-ul-Haq"], "correct": 2},
    {"difficulty": "Hard", "question": "Who was the first bowler in cricket history to reach 500 Test wickets?", "options": ["Shane Warne", "Muttiah Muralitharan", "Courtney Walsh", "Kapil Dev"], "correct": 2},
    {"difficulty": "Hard", "question": "What is Sir Donald Bradman's famous career Test batting average?", "options": ["95.14", "99.94", "101.20", "88.60"], "correct": 1},
    {"difficulty": "Hard", "question": "Who was the first cricketer in history to reach 10,000 Test runs?", "options": ["Allan Border", "Sachin Tendulkar", "Sunil Gavaskar", "Brian Lara"], "correct": 2},
    {"difficulty": "Hard", "question": "Which non-wicketkeeper holds the record for most catches in Test history (210 catches)?", "options": ["Mahela Jayawardene", "Ricky Ponting", "Rahul Dravid", "Jacques Kallis"], "correct": 2},
    {"difficulty": "Hard", "question": "Who was the first spin bowler to reach 600 Test wickets?", "options": ["Muttiah Muralitharan", "Shane Warne", "Anil Kumble", "James Anderson"], "correct": 1},
    {"difficulty": "Hard", "question": "Which player holds the record for most stumpings in international cricket history?", "options": ["Kumar Sangakkara", "Romesh Kaluwitharana", "MS Dhoni", "Moin Khan"], "correct": 2},
    {"difficulty": "Hard", "question": "Who was the first Indian cricketer to score centuries in all three international formats?", "options": ["Rohit Sharma", "Virat Kohli", "Suresh Raina", "KL Rahul"], "correct": 2},
    {"difficulty": "Hard", "question": "Who was awarded Player of the Tournament at the 2003 ODI World Cup?", "options": ["Ricky Ponting", "Sachin Tendulkar", "Chaminda Vaas", "Adam Gilchrist"], "correct": 1},
    {"difficulty": "Hard", "question": "Which player scored the fastest ODI fifty in men's cricket history (16 balls)?", "options": ["Sanath Jayasuriya", "AB de Villiers", "Shahid Afridi", "Kusal Perera"], "correct": 1},
    {"difficulty": "Hard", "question": "Which player scored the fastest double century in Test history (off 153 balls)?", "options": ["Virender Sehwag", "Nathan Astle", "Brendon McCullum", "Adam Gilchrist"], "correct": 1},
    {"difficulty": "Hard", "question": "Who was the first player in Test cricket history to score a triple century (325 runs)?", "options": ["Don Bradman", "Andy Sandham", "Wally Hammond", "Hanif Mohammad"], "correct": 1},
    {"difficulty": "Hard", "question": "Which bowler holds the best bowling figures in a Men's ODI innings (8/19)?", "options": ["Muttiah Muralitharan", "Chaminda Vaas", "Shahid Afridi", "Glenn McGrath"], "correct": 1},
    {"difficulty": "Hard", "question": "Who scored the most runs in a single edition of an ODI World Cup (765 runs in 2023)?", "options": ["Sachin Tendulkar", "Matthew Hayden", "Virat Kohli", "Rohit Sharma"], "correct": 2},
    {"difficulty": "Hard", "question": "Which batter has hit the most total sixes in ODI World Cup history?", "options": ["Chris Gayle", "AB de Villiers", "Rohit Sharma", "Ricky Ponting"], "correct": 2},
    {"difficulty": "Hard", "question": "Which player has scored the most total centuries in ODI World Cup history (7 centuries)?", "options": ["Sachin Tendulkar", "Ricky Ponting", "Rohit Sharma", "David Warner"], "correct": 2},
    {"difficulty": "Hard", "question": "Which bowler has taken the most overall wickets in ODI World Cup history (71 wickets)?", "options": ["Wasim Akram", "Lasith Malinga", "Glenn McGrath", "Mitchell Starc"], "correct": 2},
    {"difficulty": "Hard", "question": "Which player hit an extraordinary 175* off 66 balls in an IPL match for RCB in 2013?", "options": ["Brendon McCullum", "Chris Gayle", "AB de Villiers", "KL Rahul"], "correct": 1}
]

for q in cricket_qs_data:
    q['sport'] = 'Cricket'

random.seed(100)

def balance_select(diff_name, docx_items, cricket_items, total=60):
    # Select ~20 Cricket, rest from docx (Football, Tennis, Basketball)
    cricket_avail = [q for q in cricket_items if q['difficulty'] == diff_name]
    docx_avail = [q for q in docx_items if q['difficulty'] == diff_name]
    
    random.shuffle(cricket_avail)
    random.shuffle(docx_avail)
    
    num_cricket = min(20, len(cricket_avail))
    num_docx = total - num_cricket
    
    res = cricket_avail[:num_cricket] + docx_avail[:num_docx]
    random.shuffle(res)
    return res

easy_selected = balance_select('Easy', docx_qs, cricket_qs_data, 60)
medium_selected = balance_select('Medium', docx_qs, cricket_qs_data, 60)
hard_selected = balance_select('Hard', docx_qs, cricket_qs_data, 60)

final_180 = []
qid = 1
for diff, pool in [('Easy', easy_selected), ('Medium', medium_selected), ('Hard', hard_selected)]:
    for item in pool:
        final_180.append({
            "id": f"Q{qid:03d}",
            "sport": item["sport"],
            "difficulty": diff,
            "question": item["question"],
            "options": item["options"],
            "correct": item["correct"]
        })
        qid += 1

with open(r'd:\Case\questions_180.json', 'w', encoding='utf-8') as f:
    json.dump(final_180, f, indent=2, ensure_ascii=False)

print("Saved balanced questions_180.json successfully!")
