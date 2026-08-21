// ---------------------------------------------------------------------------
// scoringEngine.js  →  src/lib/scoringEngine.js
// Score out of 100: Efficiency (50) + Team Balance (30) + Experience Mix (20)
// ---------------------------------------------------------------------------

import { ROLES, SQUAD_RULES } from './constants';

const TOTAL_PURSE_LAKHS = 12000; // keep in sync with TEAMS[*].purseLakhs

// ── Efficiency (max 50) ───────────────────────────────────────────────────────
function scoreEfficiency(team) {
  if (team.squad.length === 0) return 0;

  let valueScore = 0;
  for (const p of team.squad) {
    const rating = p.performance_rating ?? 60;
    const paid   = p.sold_price_lakhs   ?? p.base_price_lakhs;
    const base   = p.base_price_lakhs   || 1;
    const priceEfficiency = Math.min(1, base / paid);
    valueScore += (rating / 100) * 0.7 + priceEfficiency * 0.3;
  }
  const avgValueScore = valueScore / team.squad.length;

  const unspentRatio   = Math.max(0, team.purseLakhs) / TOTAL_PURSE_LAKHS;
  const unspentPenalty = unspentRatio > 0.1 ? (unspentRatio - 0.1) * 40 : 0;

  return Math.max(0, Math.min(50, avgValueScore * 50 - unspentPenalty));
}

// ── Team Balance (max 30) ─────────────────────────────────────────────────────
function scoreBalance(team) {
  if (team.squad.length === 0) return 0;

  const counts = Object.fromEntries(ROLES.map(r => [r, 0]));
  for (const p of team.squad) counts[p.role] = (counts[p.role] || 0) + 1;

  const total = team.squad.length;
  const ideal = {
    'Batsman':       0.25,
    'Wicket-Keeper': 0.10,
    'All-Rounder':   0.25,
    'Pacer':         0.25,
    'Spinner':       0.15,
  };

  let deviation = 0;
  for (const role of ROLES) {
    deviation += Math.abs(counts[role] / total - ideal[role]);
  }
  let score = Math.max(0, 30 - deviation * 15);
  if (counts['Wicket-Keeper'] < SQUAD_RULES.MIN_WICKET_KEEPERS) score -= 8;

  return Math.max(0, Math.min(30, score));
}

// ── Experience Mix (max 20) ───────────────────────────────────────────────────
function scoreExperience(team) {
  if (team.squad.length === 0) return 0;

  const rookieRatio = team.squad.filter(p => p.is_rookie).length / team.squad.length;
  const idealMin = 0.30, idealMax = 0.40;
  let distance = 0;
  if      (rookieRatio < idealMin) distance = idealMin - rookieRatio;
  else if (rookieRatio > idealMax) distance = rookieRatio - idealMax;

  return Math.max(0, Math.min(20, 20 - distance * 50));
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function avgPerformanceRating(team) {
  if (team.squad.length === 0) return 0;
  return team.squad.reduce((s, p) => s + (p.performance_rating ?? 60), 0) / team.squad.length;
}

function round1(n) { return Math.round(n * 10) / 10; }

// ── Public API ────────────────────────────────────────────────────────────────
export function scoreTeam(team) {
  const efficiency = scoreEfficiency(team);
  const balance    = scoreBalance(team);
  const experience = scoreExperience(team);
  return {
    teamId:         team.id,
    teamName:       team.name,
    teamColor:      team.color,
    efficiency:     round1(efficiency),
    balance:        round1(balance),
    experience:     round1(experience),
    total:          round1(efficiency + balance + experience),
    purseRemaining: team.purseLakhs,
    avgRating:      round1(avgPerformanceRating(team)),
    squadSize:      team.squad.length,
  };
}

export function rankTeams(teams) {
  const scored = teams.map(scoreTeam);
  scored.sort((a, b) => {
    if (b.total          !== a.total)          return b.total          - a.total;
    if (b.purseRemaining !== a.purseRemaining) return b.purseRemaining - a.purseRemaining;
    return b.avgRating - a.avgRating;
  });
  return scored.map((s, i) => ({ ...s, rank: i + 1 }));
}
