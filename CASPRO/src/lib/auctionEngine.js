// ---------------------------------------------------------------------------
// auctionEngine.js  →  src/lib/auctionEngine.js
// Hard-ceiling budget engine: a team can never bid past the point where
// they couldn't fill the minimum squad size with their remaining purse.
// ---------------------------------------------------------------------------

import { SQUAD_RULES } from './constants';

const RESERVE_PER_SLOT_LAKHS = 30; // cheapest pool base price (Pool E)

/**
 * Maximum amount this team is legally allowed to bid right now.
 */
export function computeMaxLegalBid(team) {
  const slotsRemainingAfterBuy = Math.max(
    0,
    SQUAD_RULES.MIN_SQUAD_SIZE - (team.squad.length + 1)
  );
  const reserveNeeded = slotsRemainingAfterBuy * RESERVE_PER_SLOT_LAKHS;
  return Math.max(0, team.purseLakhs - reserveNeeded);
}

/**
 * Returns { ok, reason } — whether this team can legally place this bid.
 */
export function canTeamBid(team, bidLakhs, player) {
  if (team.squad.length >= SQUAD_RULES.MAX_SQUAD_SIZE)
    return { ok: false, reason: 'Squad full' };
  if (bidLakhs > computeMaxLegalBid(team))
    return { ok: false, reason: 'Exceeds hard ceiling for remaining slots' };
  if (player.is_overseas) {
    const overseasCount = team.squad.filter(p => p.is_overseas).length;
    if (overseasCount >= SQUAD_RULES.MAX_OVERSEAS)
      return { ok: false, reason: 'Overseas cap reached' };
  }
  return { ok: true };
}

/**
 * Filters teams to those still eligible to raise the bid.
 */
export function eligibleBidders(teams, currentBidLakhs, player) {
  return teams.filter(t => canTeamBid(t, currentBidLakhs, player).ok);
}

/**
 * Marks player sold: returns updated copies of team + player (no mutation).
 */
export function finalizeSale(team, player, soldPriceLakhs) {
  const updatedTeam = {
    ...team,
    purseLakhs: team.purseLakhs - soldPriceLakhs,
    squad: [
      ...team.squad,
      { ...player, sold: true, sold_to: team.id, sold_price_lakhs: soldPriceLakhs },
    ],
  };
  const updatedPlayer = {
    ...player,
    sold: true,
    sold_to: team.id,
    sold_price_lakhs: soldPriceLakhs,
  };
  return { updatedTeam, updatedPlayer };
}
