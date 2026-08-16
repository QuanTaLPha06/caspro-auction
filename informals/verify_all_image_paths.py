import json
import os
from pathlib import Path

base_dir = Path("D:/Case/informals")

with open('players_data.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Filter out comment lines
data_lines = [l for l in lines if not l.strip().startswith("//")]
content = "".join(data_lines)
json_str = content.replace("const PLAYERS_DATABASE = ", "").strip().rstrip(";")
players = json.loads(json_str)

print(f"Total players in database: {len(players)}")

missing_count = 0
for p in players:
    name = p['name']
    flag = p['flagImg']
    club_img = p['clubImg']
    league_img = p['leagueImg']
    card_img = p['cardImg']

    flag_exists = (base_dir / flag).exists()
    club_exists = (base_dir / club_img).exists()
    league_exists = (base_dir / league_img).exists()
    card_exists = (base_dir / card_img).exists()

    if not (flag_exists and club_exists and league_exists and card_exists):
        missing_count += 1
        print(f"FAILED: {name}")
        if not flag_exists: print(f"  - Flag missing: {flag}")
        if not club_exists: print(f"  - Club img missing: {club_img}")
        if not league_exists: print(f"  - League img missing: {league_img}")
        if not card_exists: print(f"  - Card img missing: {card_img}")

if missing_count == 0:
    print("ALL 99 PLAYERS HAVE 100% VALID EXISTING ASSET PATHS!")
else:
    print(f"Total players with missing assets: {missing_count}")
