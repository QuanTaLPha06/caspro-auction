#!/usr/bin/env python3
"""
Extracts a stats profile for every player directly from the scouting notes
in Mock_IPL_Auction_2026_Player_Pool.pdf (the user's own player pool document).

Each note sentence often already contains real 2025/26 numbers, e.g.:
    "...scored 657-675 runs, leading RCB to their title."
    "...took 18 wickets at an elite 6.67 economy rate."
    "...retained for Rs 18 Cr..."
    "...elite international T20 strike rate over 161."

This script regex-extracts those numbers into a structured stats record.
Where a note has no cited number (common for domestic/associate players in
the lower pools), a pool-tier baseline is used instead so scoring never
breaks -- this is clearly flagged per player via "stats_source".

Usage:
    pip install pdfplumber --break-system-packages
    python3 extract_stats.py Mock_IPL_Auction_2026_Player_Pool.pdf

Output:
    player_stats.json
"""

import sys
import re
import json
import pdfplumber

from players import PLAYERS
from role_ranges import get_role

# Pool-tier baseline scores, used only when a stat can't be found in the note.
# Roughly reflects the auction pool's own quality tiering (A best -> E entry).
POOL_BASELINE = {"A": 70, "B": 55, "C": 42, "D": 30, "E": 20}


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def find_player_line(full_text: str, lot: int) -> str:
    """Locate the raw text line(s) for a given lot number in the PDF text.
    Matches purely on the leading lot number (unique per row) rather than
    the player name, since some names wrap onto a second physical line
    before the age/style columns even begin (e.g. 'Mohammed\\nAzharuddeen')."""
    lines = full_text.splitlines()
    pattern = re.compile(r"^\s*" + str(lot) + r"\s+(.+)")
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if not m:
            continue
        combined = line
        # Pull in a wrapped continuation line if it doesn't look like a new
        # lot row, a section header, or the running footer.
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            if not re.match(r"^\s*\d+\s+[A-Z]", nxt) and not re.match(
                r"^(MOCK IPL|POOL |BATSMEN|WICKET|ALL-ROUNDERS|PACERS|SPINNERS|#)", nxt
            ):
                combined += " " + nxt
        return clean_line(combined)
    return ""


def extract_numbers(line: str) -> dict:
    stats = {}

    nat = re.search(r"Overseas \(([^)]+)\)", line)
    stats["nationality"] = f"Overseas ({nat.group(1)})" if nat else "Indian"

    runs = re.findall(r"(\d{2,4})(?:[-\u2013]\d{2,4})?\s+runs", line)
    if runs:
        stats["runs"] = max(int(r) for r in runs)

    wkts = re.findall(r"(\d{1,2})\s+wickets", line)
    if wkts:
        stats["wickets"] = max(int(w) for w in wkts)

    econ = re.search(r"(\d\.\d{1,2})\s*(?:economy|econ)", line, re.I)
    if not econ:
        econ = re.search(r"economy(?: rate)? of (\d\.\d{1,2})", line, re.I)
    if econ:
        stats["economy"] = float(econ.group(1))

    sr = re.search(r"strike rate[^\d]{0,10}(\d{2,3}(?:\.\d+)?)", line, re.I)
    if sr:
        stats["strike_rate"] = float(sr.group(1))

    sixes = re.search(r"(\d{1,2})\s+sixes", line)
    if sixes:
        stats["sixes"] = int(sixes.group(1))

    price = re.search(r"[₹Rr]s?\.?\s*([\d.]+)\s*Cr", line)
    if price:
        stats["price_cr"] = float(price.group(1))

    return stats


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "Mock_IPL_Auction_2026_Player_Pool.pdf"

    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(p.extract_text() or "" for p in pdf.pages)

    records = {}
    unmatched = []

    for lot, name, pool in PLAYERS:
        line = find_player_line(full_text, lot)
        role = get_role(lot)
        base = {
            "lot": lot,
            "name": name,
            "pool": pool,
            "role": role,
            "nationality": "Indian",
            "stats_source": "baseline",
        }

        if not line:
            unmatched.append(name)
            base["baseline_score"] = POOL_BASELINE[pool]
            records[str(lot)] = base
            continue

        extracted = extract_numbers(line)
        base.update(extracted)
        has_real_stat = any(k in extracted for k in ("runs", "wickets", "economy", "strike_rate", "sixes"))
        base["stats_source"] = "note" if has_real_stat else "baseline"
        base["baseline_score"] = POOL_BASELINE[pool]
        records[str(lot)] = base

    with open("player_stats.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    with_stats = sum(1 for r in records.values() if r["stats_source"] == "note")
    print(f"Parsed {len(records)} players.")
    print(f"  -> {with_stats} have a real cited stat from their scouting note")
    print(f"  -> {len(records) - with_stats} fall back to pool-tier baseline score")
    if unmatched:
        print(f"  -> {len(unmatched)} lines could not be located at all: {unmatched[:10]}")
    print("Saved to player_stats.json")


if __name__ == "__main__":
    main()
