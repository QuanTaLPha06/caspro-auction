import zipfile, xml.etree.ElementTree as ET, re, json, random

# 1. Extract DOCX questions
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

print(f"Parsed {len(docx_qs)} questions from DOCX.")

easy_docx = [q for q in docx_qs if q['difficulty'] == 'Easy']
medium_docx = [q for q in docx_qs if q['difficulty'] == 'Medium']
hard_docx = [q for q in docx_qs if q['difficulty'] == 'Hard']

print(f"DOCX Breakdown - Easy: {len(easy_docx)}, Medium: {len(medium_docx)}, Hard: {len(hard_docx)}")
