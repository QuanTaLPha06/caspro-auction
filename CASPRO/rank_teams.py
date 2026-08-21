#!/usr/bin/env python3
"""
Ranks IPL auction teams and picks each team's best valid Playing XI, applying:

  1. Max 4 overseas players in the XI
  2. At least 1 wicketkeeper in the XI
  3. At least 5 specialist/part-time bowling options (PACE + SPIN + AR)
  4. 11 players total, rest go to bench (squad depth also factored in lightly)

Player values come from player_stats.json (built by extract_stats.py from
your Player Pool PDF's scouting notes -- real 2025/26 runs, wickets, economy,
strike rate, sixes where cited; pool-tier baseline otherwise).

INPUT (rosters.json), produced by your auction site, one file, structured as:
{
  "Mumbai Marauders": ["Virat Kohli", "Jasprit Bumrah", "Ishan Kishan", ...],
  "Chennai Chargers": ["MS Dhoni", "Ravindra Jadeja", ...],
  ...
}
Player names must match the names in players.py (case-insensitive match is
attempted automatically).

Usage:
    python3 rank_teams.py rosters.json

Output:
    team_rankings.json   -- full breakdown for every team
    Console summary of the Top 3 teams with their best XI
"""

import sys
import json
from scoring import score_player

STATS_PATH = "player_stats.json"

MIN_BOWLERS = 5
MAX_OVERSEAS = 4
XI_SIZE = 11


def load_stats():
    with open(STATS_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    by_lot = {int(k): v for k, v in raw.items()}
    by_name = {}
    for rec in by_lot.values():
        by_name.setdefault(rec["name"].lower(), rec)
    return by_lot, by_name


def resolve_roster(names, by_name):
    resolved, not_found = [], []
    for n in names:
        rec = by_name.get(n.strip().lower())
        if rec:
            resolved.append(rec)
        else:
            not_found.append(n)
    return resolved, not_found


def is_bowler(rec):
    return rec["role"] in ("PACE", "SPIN", "AR")


def is_overseas(rec):
    return rec["nationality"].startswith("Overseas")


def pick_best_xi(squad):
    """Greedy constrained selection: maximize total score while satisfying
    overseas cap, WK minimum, and bowling-depth minimum."""
    scored = sorted(squad, key=lambda r: r["_score"], reverse=True)

    xi = []
    overseas_count = 0
    wk_count = 0
    bowler_count = 0

    def can_add(rec):
        if is_overseas(rec) and overseas_count >= MAX_OVERSEAS:
            return False
        return True

    # Pass 1: greedily take the highest scorers respecting the overseas cap
    for rec in scored:
        if len(xi) >= XI_SIZE:
            break
        if can_add(rec):
            xi.append(rec)
            if is_overseas(rec):
                overseas_count += 1
            if rec["role"] == "WK":
                wk_count += 1
            if is_bowler(rec):
                bowler_count += 1

    # Pass 2: enforce at least 1 WK -- swap out the weakest non-WK if missing
    if wk_count == 0:
        best_wk = next((r for r in scored if r["role"] == "WK" and can_add(r)), None)
        if best_wk:
            xi.sort(key=lambda r: r["_score"])
            for i, weak in enumerate(xi):
                if weak["role"] != "WK":
                    xi[i] = best_wk
                    wk_count += 1
                    bowler_count = sum(1 for r in xi if is_bowler(r))
                    overseas_count = sum(1 for r in xi if is_overseas(r))
                    break
            xi.sort(key=lambda r: r["_score"], reverse=True)

    # Pass 3: enforce minimum bowling depth -- swap in best available bowlers
    while bowler_count < MIN_BOWLERS:
        current_names = {r["name"] for r in xi}
        candidate = next(
            (r for r in scored if r["name"] not in current_names and is_bowler(r) and can_add(r)),
            None,
        )
        if not candidate:
            break
        xi.sort(key=lambda r: r["_score"])
        replaced = False
        for i, weak in enumerate(xi):
            if not is_bowler(weak) and weak["role"] != "WK":
                xi[i] = candidate
                replaced = True
                break
        if not replaced:
            break
        bowler_count = sum(1 for r in xi if is_bowler(r))
        overseas_count = sum(1 for r in xi if is_overseas(r))
        xi.sort(key=lambda r: r["_score"], reverse=True)

    bench = [r for r in scored if r not in xi][:4]
    return xi, bench


def evaluate_team(team_name, squad):
    for rec in squad:
        rec["_score"] = score_player(rec)

    xi, bench = pick_best_xi(squad)
    xi_score = sum(r["_score"] for r in xi)
    bench_score = sum(r["_score"] for r in bench) * 0.15  # light depth bonus
    total_score = round(xi_score + bench_score, 2)

    return {
        "team": team_name,
        "squad_size": len(squad),
        "total_score": total_score,
        "best_xi_score": round(xi_score, 2),
        "overseas_in_xi": sum(1 for r in xi if is_overseas(r)),
        "wicketkeepers_in_xi": sum(1 for r in xi if r["role"] == "WK"),
        "bowling_options_in_xi": sum(1 for r in xi if is_bowler(r)),
        "best_xi": [
            {"name": r["name"], "role": r["role"], "nationality": r["nationality"], "score": r["_score"]}
            for r in xi
        ],
        "bench": [{"name": r["name"], "role": r["role"], "score": r["_score"]} for r in bench],
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 rank_teams.py rosters.json")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        rosters = json.load(f)

    by_lot, by_name = load_stats()

    results = []
    for team_name, names in rosters.items():
        squad, not_found = resolve_roster(names, by_name)
        if not_found:
            print(f"[{team_name}] WARNING - could not match: {not_found}")
        if len(squad) < XI_SIZE:
            print(f"[{team_name}] SKIPPED - only {len(squad)} resolved players, need at least {XI_SIZE}")
            continue
        results.append(evaluate_team(team_name, squad))

    results.sort(key=lambda r: r["total_score"], reverse=True)

    with open("team_rankings.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("TOP 3 TEAMS")
    print("=" * 60)
    for i, r in enumerate(results[:3], start=1):
        print(f"\n#{i}  {r['team']}  -- total score {r['total_score']}")
        print(f"    Overseas in XI: {r['overseas_in_xi']}/4   "
              f"WK in XI: {r['wicketkeepers_in_xi']}   "
              f"Bowling options: {r['bowling_options_in_xi']}")
        print("    Best XI:")
        for p in r["best_xi"]:
            tag = " (O)" if p["nationality"].startswith("Overseas") else ""
            print(f"      - {p['name']:<25} {p['role']:<5} {p['score']:>6}{tag}")

    print(f"\nFull breakdown for all {len(results)} teams saved to team_rankings.json")


if __name__ == "__main__":
    main()
