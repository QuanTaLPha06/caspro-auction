import json

with open('questions_180.json', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('éé', 'é')

with open('questions_180.json', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned double accents in questions_180.json")
