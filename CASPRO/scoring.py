"""
Role-based player scoring, following the framework:

  - Top-order batters (BAT):      judged mainly on Runs + consistency
  - Wicketkeepers (WK):           keeping baseline + Strike Rate + Runs
  - Middle-order / Finishers/AR:  Strike Rate + Sixes + all-round utility
  - Pace bowlers (PACE):          Wickets (Purple Cap race) + Economy
  - Spinners (SPIN):              Economy + Wickets + utility

Where a note has no cited number, the pool-tier baseline score is used so
every player still gets a fair, non-zero value reflecting their pool tier.
"""

def score_player(p: dict) -> float:
    role = p["role"]
    baseline = p.get("baseline_score", 30)

    runs = p.get("runs")
    wkts = p.get("wickets")
    econ = p.get("economy")
    sr = p.get("strike_rate")
    sixes = p.get("sixes")
    price = p.get("price_cr")

    score = 0.0
    matched_any = False

    if role == "BAT":
        if runs is not None:
            score += runs * 0.10          # ~65-75 runs -> 6.5-7.5 pts scale
            matched_any = True
        if sr is not None:
            score += sr * 0.05
            matched_any = True

    elif role == "WK":
        score += 8  # fixed keeping-utility baseline (every WK offers this)
        if runs is not None:
            score += runs * 0.08
            matched_any = True
        if sr is not None:
            score += sr * 0.08
            matched_any = True

    elif role == "AR":
        score += 4  # multi-dimensional utility baseline
        if runs is not None:
            score += runs * 0.06
            matched_any = True
        if wkts is not None:
            score += wkts * 1.5
            matched_any = True
        if sr is not None:
            score += sr * 0.04
            matched_any = True
        if sixes is not None:
            score += sixes * 0.6
            matched_any = True
        if econ is not None:
            score += max(0, (9.5 - econ)) * 2
            matched_any = True

    elif role == "PACE":
        if wkts is not None:
            score += wkts * 2.2           # Purple Cap race weighting
            matched_any = True
        if econ is not None:
            score += max(0, (9.5 - econ)) * 2.5
            matched_any = True

    elif role == "SPIN":
        if econ is not None:
            score += max(0, (9.0 - econ)) * 3.5   # economy is the premium spinner metric
            matched_any = True
        if wkts is not None:
            score += wkts * 1.8
            matched_any = True

    if sixes is not None and role in ("BAT", "WK"):
        score += sixes * 0.4
        matched_any = True

    if price is not None:
        # small "star power" / big-auction-value bump, capped
        score += min(price, 20) * 0.15

    if not matched_any:
        score = baseline
    else:
        # blend a little bit of pool baseline so tier context isn't lost
        score = 0.85 * score + 0.15 * baseline

    return round(score, 2)
