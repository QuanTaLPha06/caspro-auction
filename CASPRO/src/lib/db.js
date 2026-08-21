// ---------------------------------------------------------------------------
// db.js  →  src/lib/db.js
// All Supabase read/write operations — pure async functions, no React deps
// ---------------------------------------------------------------------------

import { supabase }  from './supabase';
import { TEAMS }     from './constants';

// ── Helpers ──────────────────────────────────────────────────────────────────

function assertOk({ error, data }, label) {
  if (error) {
    console.error(`[db] ${label}:`, error);
    throw error;
  }
  return data;
}

// ── Hydration ─────────────────────────────────────────────────────────────────

/**
 * Fetch everything needed to reconstruct auction state on mount.
 * Returns { auctionState, purses, sales }
 */
export async function hydrate() {
  const [
    { data: auctionState, error: e1 },
    { data: purses,       error: e2 },
    { data: sales,        error: e3 },
    { data: logs,         error: e4 },
  ] = await Promise.all([
    supabase.from('auction_state').select('*').eq('id', 1).single(),
    supabase.from('team_purses').select('*'),
    supabase.from('player_sales').select('*'),
    supabase.from('bid_log').select('*').eq('type', 'UNSOLD').order('created_at', { ascending: true }),
  ]);

  if (e1) throw e1;
  if (e2) throw e2;
  if (e3) throw e3;

  // Normalize purses: [{ team_id, purse_lakhs }] → Map
  const purseMap = Object.fromEntries(purses.map(r => [r.team_id, r.purse_lakhs]));

  // Normalize sales: [{ player_id, team_id, sold_price_lakhs }] → Map keyed by player_id
  const salesMap = Object.fromEntries(
    sales.map(r => [r.player_id, { teamId: r.team_id, soldPriceLakhs: Number(r.sold_price_lakhs) }])
  );

  const unsoldPlayerIds = (logs || [])
    .map(l => l.player_id)
    .filter(pid => pid && !salesMap[pid]);

  return {
    auctionState: {
      currentIndex:     auctionState.current_index,
      currentBidLakhs:  auctionState.current_bid_lakhs != null ? Number(auctionState.current_bid_lakhs) : null,
      currentBidTeamId: auctionState.current_bid_team_id,
      status:           auctionState.status,
    },
    purseMap,
    salesMap,
    unsoldPlayerIds,
  };
}

// ── Auction control ───────────────────────────────────────────────────────────

export async function dbStartLot() {
  assertOk(
    await supabase.from('auction_state').update({
      status:              'live',
      current_bid_lakhs:   null,
      current_bid_team_id: null,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    'dbStartLot'
  );
}

export async function dbPlaceBid(playerId, teamId, bidLakhs) {
  await Promise.all([
    supabase.from('auction_state').update({
      current_bid_lakhs:   bidLakhs,
      current_bid_team_id: teamId,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    supabase.from('bid_log').insert({
      type: 'BID', player_id: playerId, team_id: teamId, price_lakhs: bidLakhs,
    }),
  ]);
}

export async function dbMarkSold(playerId, teamId, soldPriceLakhs, newPurseLakhs) {
  await Promise.all([
    // 1. Record the sale
    supabase.from('player_sales').upsert({
      player_id: playerId, team_id: teamId, sold_price_lakhs: soldPriceLakhs,
    }),
    // 2. Deduct purse
    supabase.from('team_purses').update({ purse_lakhs: newPurseLakhs }).eq('team_id', teamId),
    // 3. Update auction_state with winning team, final price and status
    supabase.from('auction_state').update({
      status:              'sold',
      current_bid_lakhs:   soldPriceLakhs,
      current_bid_team_id: teamId,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    // 4. Bid log
    supabase.from('bid_log').insert({
      type: 'SOLD', player_id: playerId, team_id: teamId, price_lakhs: soldPriceLakhs,
    }),
  ]);
}

export async function dbMarkUnsold(playerId) {
  await Promise.all([
    supabase.from('auction_state').update({
      status: 'unsold', updated_at: new Date().toISOString(),
    }).eq('id', 1),
    supabase.from('bid_log').insert({ type: 'UNSOLD', player_id: playerId }),
  ]);
}

export async function dbNextLot(nextIndex, finished) {
  assertOk(
    await supabase.from('auction_state').update({
      current_index:       nextIndex,
      status:              finished ? 'finished' : 'idle',
      current_bid_lakhs:   null,
      current_bid_team_id: null,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    'dbNextLot'
  );
}

export async function dbJumpToLot(index) {
  assertOk(
    await supabase.from('auction_state').update({
      current_index:       index,
      status:              'idle',
      current_bid_lakhs:   null,
      current_bid_team_id: null,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    'dbJumpToLot'
  );
}

/**
 * Full reset: clear all sales, restore purses, reset auction_state.
 */
export async function dbReset() {
  await Promise.all([
    supabase.from('player_sales').delete().gt('created_at', '1970-01-01'),
    supabase.from('bid_log').delete().gt('created_at', '1970-01-01'),
    // Restore purses
    ...TEAMS.map(t =>
      supabase.from('team_purses').update({ purse_lakhs: t.purseLakhs }).eq('team_id', t.id)
    ),
  ]);
  // Reset control row last
  await supabase.from('auction_state').update({
    current_index:       0,
    current_bid_lakhs:   null,
    current_bid_team_id: null,
    status:              'idle',
    updated_at:          new Date().toISOString(),
  }).eq('id', 1);
}

// ── Player slide images ───────────────────────────────────────────────────────

/**
 * Returns the public URL for a player's slide image stored in Supabase Storage.
 * Upload slides as: {player_id}.jpg  (or .png — change ext below)
 */
export function getSlideUrl(playerId, ext = 'jpg') {
  const { data } = supabase.storage
    .from('player-slides')
    .getPublicUrl(`${playerId}.${ext}`);
  return data?.publicUrl ?? null;
}
