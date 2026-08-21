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

  // Display names. Columns are absent until supabase/add-team-names.sql is run,
  // in which case this map is empty and the defaults in constants.js are used.
  const teamMetaMap = Object.fromEntries(
    purses
      .filter(r => r.team_name != null || r.team_short != null)
      .map(r => [r.team_id, { name: r.team_name ?? null, short: r.team_short ?? null }])
  );

  // Normalize sales: [{ player_id, team_id, sold_price_lakhs }] → Map keyed by player_id
  const salesMap = Object.fromEntries(
    sales.map(r => [r.player_id, { teamId: r.team_id, soldPriceLakhs: Number(r.sold_price_lakhs) }])
  );

  const unsoldPlayerIds = (logs || [])
    .map(l => l.player_id)
    .filter(pid => pid && !salesMap[pid]);

  return {
    teamMetaMap,
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
  const [r1, r2] = await Promise.all([
    supabase.from('auction_state').update({
      status:              'live',
      current_bid_lakhs:   bidLakhs,
      current_bid_team_id: teamId,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    supabase.from('bid_log').insert({
      type: 'BID', player_id: playerId, team_id: teamId, price_lakhs: bidLakhs,
    }),
  ]);
  assertOk(r1, 'dbPlaceBid auction_state');
  assertOk(r2, 'dbPlaceBid bid_log');
}

export async function dbMarkSold(playerId, teamId, soldPriceLakhs, newPurseLakhs) {
  const [r1, r2, r3, r4] = await Promise.all([
    supabase.from('player_sales').upsert({
      player_id: playerId, team_id: teamId, sold_price_lakhs: soldPriceLakhs,
    }),
    supabase.from('team_purses').update({ purse_lakhs: newPurseLakhs }).eq('team_id', teamId),
    supabase.from('auction_state').update({
      status:              'sold',
      current_bid_lakhs:   soldPriceLakhs,
      current_bid_team_id: teamId,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    supabase.from('bid_log').insert({
      type: 'SOLD', player_id: playerId, team_id: teamId, price_lakhs: soldPriceLakhs,
    }),
  ]);
  assertOk(r1, 'dbMarkSold player_sales');
  assertOk(r2, 'dbMarkSold team_purses');
  assertOk(r3, 'dbMarkSold auction_state');
  assertOk(r4, 'dbMarkSold bid_log');
}

export async function dbMarkUnsold(playerId) {
  const [r1, r2] = await Promise.all([
    supabase.from('auction_state').update({
      status: 'unsold', updated_at: new Date().toISOString(),
    }).eq('id', 1),
    supabase.from('bid_log').insert({ type: 'UNSOLD', player_id: playerId }),
  ]);
  assertOk(r1, 'dbMarkUnsold auction_state');
  assertOk(r2, 'dbMarkUnsold bid_log');
}

export async function dbEndAuction() {
  assertOk(
    await supabase.from('auction_state').update({
      status:              'finished',
      current_bid_lakhs:   null,
      current_bid_team_id: null,
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    'dbEndAuction'
  );
}

export async function dbNextLot(nextIndex, finished) {
  assertOk(
    await supabase.from('auction_state').update({
      current_index:       nextIndex,
      status:              finished ? 'finished' : 'live',
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
      status:              'live',
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
  const res1 = await supabase.from('player_sales').delete().neq('player_id', '___none___');
  assertOk(res1, 'dbReset player_sales');

  const res2 = await supabase.from('bid_log').delete().neq('type', '___none___');
  assertOk(res2, 'dbReset bid_log');

  const purseResults = await Promise.all(
    TEAMS.map(t =>
      supabase.from('team_purses').update({ purse_lakhs: t.purseLakhs }).eq('team_id', t.id)
    )
  );
  purseResults.forEach((r, idx) => assertOk(r, `dbReset team_purse ${TEAMS[idx].id}`));

  // Reset control row last
  assertOk(
    await supabase.from('auction_state').update({
      current_index:       0,
      current_bid_lakhs:   null,
      current_bid_team_id: null,
      status:              'idle',
      updated_at:          new Date().toISOString(),
    }).eq('id', 1),
    'dbReset auction_state'
  );
}

/**
 * Persist a team's display name + short badge. Team IDs are never changed.
 * Throws a helpful error if the migration has not been run yet.
 */
export async function dbSetTeamName(teamId, name, short) {
  const res = await supabase
    .from('team_purses')
    .update({ team_name: name, team_short: short })
    .eq('team_id', teamId)
    .select();

  if (res.error) {
    if (/team_name|team_short|schema cache/i.test(res.error.message)) {
      throw new Error(
        'Team name columns are missing. Run supabase/add-team-names.sql in the ' +
        'Supabase SQL Editor, then try again.'
      );
    }
    throw res.error;
  }
  return res.data;
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
