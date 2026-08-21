// ---------------------------------------------------------------------------
// AuctionStore.jsx  →  src/state/AuctionStore.jsx
// Supabase-backed state: real-time sync across Admin + TV tabs/devices
// ---------------------------------------------------------------------------

import React, {
  createContext, useContext, useReducer,
  useEffect, useCallback, useRef,
} from 'react';

import players            from '../../players.json';
import { TEAMS, TEAM_NAME_MAX, TEAM_SHORT_MAX } from '../lib/constants';
import { finalizeSale }   from '../lib/auctionEngine';
import { supabase }       from '../lib/supabase';
import {
  hydrate,
  dbStartLot, dbPlaceBid, dbMarkSold,
  dbMarkUnsold, dbEndAuction, dbNextLot, dbJumpToLot, dbReset, dbSetTeamName,
} from '../lib/db';

// ── Static data ───────────────────────────────────────────────────────────────

const ALL_PLAYERS   = players;
const AUCTION_ORDER = players.map(p => p.id);

// How often to re-check the DB when Realtime is unavailable or drops out.
const POLL_INTERVAL_MS = 1500;

// Stable fingerprint of a DB snapshot, used to skip no-op re-renders while polling.
function snapshotSignature(snap) {
  const stable = obj => Object.keys(obj).sort().map(k => `${k}:${JSON.stringify(obj[k])}`).join('|');
  return [
    JSON.stringify(snap.auctionState),
    stable(snap.purseMap),
    stable(snap.salesMap),
    stable(snap.teamMetaMap ?? {}),
    snap.unsoldPlayerIds.join(','),
  ].join('#');
}

// ── Build fresh local state from DB snapshot ──────────────────────────────────

function buildStateFromSnapshot(auctionStateRow, purseMap, salesMap, unsoldPlayerIds = [], teamMetaMap = {}) {
  // Rebuild teams with DB purses + sold squads + admin-set display names
  const teams = TEAMS.map(t => {
    const purseLakhs = purseMap[t.id] ?? t.purseLakhs;
    const squad = ALL_PLAYERS
      .filter(p => salesMap[p.id]?.teamId === t.id)
      .map(p => ({ ...p, sold_price_lakhs: salesMap[p.id].soldPriceLakhs }));
    const meta = teamMetaMap[t.id];
    return {
      ...t,
      name:  meta?.name  || t.name,
      short: meta?.short || t.short,
      purseLakhs,
      squad,
    };
  });

  const auctionOrder = [...AUCTION_ORDER, ...unsoldPlayerIds];

  return {
    players:         ALL_PLAYERS,
    teams,
    auctionOrder,
    salesMap,
    currentIndex:    auctionStateRow.currentIndex,
    currentBidLakhs: auctionStateRow.currentBidLakhs,
    currentBidTeamId:auctionStateRow.currentBidTeamId,
    status:          auctionStateRow.status,
    loading:         false,
    error:           null,
  };
}

// ── Initial (loading) state ───────────────────────────────────────────────────

const loadingState = {
  players:          ALL_PLAYERS,
  teams:            TEAMS.map(t => ({ ...t, squad: [] })),
  auctionOrder:     AUCTION_ORDER,
  salesMap:         {},
  currentIndex:     0,
  currentBidLakhs:  null,
  currentBidTeamId: null,
  status:           'idle',
  loading:          true,
  error:            null,
};

// ── Reducer (local-only — mirrors DB writes already dispatched) ───────────────

function currentPlayerFrom(state) {
  const pid = state.auctionOrder[state.currentIndex];
  return state.players.find(p => p.id === pid) ?? null;
}

function reducer(state, action) {
  switch (action.type) {

    case 'HYDRATE':
      return { ...action.state, loading: false, error: null };

    case 'REALTIME_AUCTION_STATE': {
      const { new: row } = action.payload;
      return {
        ...state,
        currentIndex:     row.current_index,
        currentBidLakhs:  row.current_bid_lakhs != null ? Number(row.current_bid_lakhs) : null,
        currentBidTeamId: row.current_bid_team_id,
        status:           row.status,
      };
    }

    case 'REALTIME_PURSE': {
      const { new: row } = action.payload;
      const teams = state.teams.map(t =>
        t.id === row.team_id ? { ...t, purseLakhs: Number(row.purse_lakhs) } : t
      );
      return { ...state, teams };
    }

    case 'REALTIME_SALE': {
      const { new: row } = action.payload;
      const player = state.players.find(p => p.id === row.player_id);
      if (!player) return state;
      const soldPlayer = { ...player, sold_price_lakhs: Number(row.sold_price_lakhs) };
      const teams = state.teams.map(t =>
        t.id === row.team_id
          ? { ...t, squad: [...t.squad.filter(p => p.id !== player.id), soldPlayer] }
          : t
      );
      const salesMap = { ...state.salesMap, [player.id]: { teamId: row.team_id, soldPriceLakhs: Number(row.sold_price_lakhs) } };
      return { ...state, teams, salesMap };
    }

    case 'REALTIME_BID_LOG': {
      const { new: row } = action.payload;
      if (row.type === 'UNSOLD' && row.player_id) {
        return {
          ...state,
          auctionOrder: [...state.auctionOrder, row.player_id],
        };
      }
      return state;
    }

    case 'LOCAL_REQUEUE_UNSOLD': {
      return {
        ...state,
        auctionOrder: [...state.auctionOrder, action.playerId],
      };
    }

    case 'SET_TEAM_NAME': {
      const teams = state.teams.map(t =>
        t.id === action.teamId ? { ...t, name: action.name, short: action.short } : t
      );
      return { ...state, teams };
    }

    case 'SET_ERROR':
      return { ...state, loading: false, error: action.error };

    default:
      return state;
  }
}

// ── Context ───────────────────────────────────────────────────────────────────

const AuctionContext = createContext(null);

export function AuctionProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, loadingState);
  const stateRef = useRef(state);
  stateRef.current = state;

  // Number of DB writes currently in flight. The poller pauses while > 0 so it
  // can never roll the UI back to a snapshot taken mid-write.
  const pendingWrites = useRef(0);
  const lastSignature = useRef(null);
  // Bumped on every write. A poll that started before a write must discard its
  // result, otherwise a slow hydrate can land after the write and revert the UI.
  const writeEpoch = useRef(0);

  const runWrite = useCallback(async (fn) => {
    pendingWrites.current += 1;
    writeEpoch.current += 1;
    try {
      return await fn();
    } finally {
      writeEpoch.current += 1;
      pendingWrites.current -= 1;
    }
  }, []);

  const applySnapshot = useCallback((snap) => {
    lastSignature.current = snapshotSignature(snap);
    dispatch({
      type: 'HYDRATE',
      state: buildStateFromSnapshot(
        snap.auctionState, snap.purseMap, snap.salesMap, snap.unsoldPlayerIds, snap.teamMetaMap
      ),
    });
  }, []);

  // ── 1. Hydrate from Supabase on mount ──────────────────────────────────────
  useEffect(() => {
    hydrate()
      .then(applySnapshot)
      .catch(err => dispatch({ type: 'SET_ERROR', error: err.message }));
  }, [applySnapshot]);

  // ── 2. Supabase Realtime subscriptions ─────────────────────────────────────
  useEffect(() => {
    const channel = supabase
      .channel('auction-live')

      .on('postgres_changes', {
        event: 'UPDATE', schema: 'public', table: 'auction_state',
      }, payload => dispatch({ type: 'REALTIME_AUCTION_STATE', payload }))

      .on('postgres_changes', {
        event: 'UPDATE', schema: 'public', table: 'team_purses',
      }, payload => dispatch({ type: 'REALTIME_PURSE', payload }))

      .on('postgres_changes', {
        event: 'INSERT', schema: 'public', table: 'player_sales',
      }, payload => dispatch({ type: 'REALTIME_SALE', payload }))

      .on('postgres_changes', {
        event: 'DELETE', schema: 'public', table: 'player_sales',
      }, () => {
        // When sales are cleared (reset), re-hydrate full state
        hydrate().then(applySnapshot).catch(() => {});
      })

      .on('postgres_changes', {
        event: 'INSERT', schema: 'public', table: 'bid_log',
      }, payload => dispatch({ type: 'REALTIME_BID_LOG', payload }))

      .subscribe(status => {
        if (status !== 'SUBSCRIBED') {
          console.warn(
            `[auction] Realtime channel status: ${status}. ` +
            'Falling back to polling. Run supabase/enable-realtime.sql ' +
            'in the Supabase SQL Editor to enable instant sync.'
          );
        }
      });

    return () => supabase.removeChannel(channel);
  }, [applySnapshot]);

  // ── 2b. Polling fallback ───────────────────────────────────────────────────
  // Realtime only fires if the tables are in the supabase_realtime publication.
  // Polling keeps Admin and TV in sync regardless, and also covers dropped
  // websockets on unreliable venue wifi.
  useEffect(() => {
    let cancelled = false;

    const tick = async () => {
      if (cancelled || pendingWrites.current > 0) return;
      const epoch = writeEpoch.current;
      try {
        const snap = await hydrate();
        // Discard if anything was written while this hydrate was in flight —
        // the snapshot predates that write and would roll the UI backwards.
        if (cancelled || writeEpoch.current !== epoch || pendingWrites.current > 0) return;
        // Only re-render when the DB actually changed.
        if (snapshotSignature(snap) === lastSignature.current) return;
        applySnapshot(snap);
      } catch {
        // Transient network failure — the next tick retries.
      }
    };

    const id = setInterval(tick, POLL_INTERVAL_MS);
    return () => { cancelled = true; clearInterval(id); };
  }, [applySnapshot]);

  // ── 3. Action helpers (write to DB → Realtime propagates to all clients) ───

  const startLot = useCallback(async () => {
    await runWrite(() => dbStartLot());
  }, [runWrite]);

  const placeBid = useCallback(async (teamId, bidLakhs) => {
    const { currentIndex, auctionOrder } = stateRef.current;
    const pid = auctionOrder[currentIndex];
    dispatch({
      type: 'REALTIME_AUCTION_STATE',
      payload: { new: { current_index: currentIndex, current_bid_lakhs: bidLakhs, current_bid_team_id: teamId, status: 'live' } }
    });
    await runWrite(() => dbPlaceBid(pid, teamId, bidLakhs));
  }, [runWrite]);

  const markSold = useCallback(async (customTeamId = null, customPriceLakhs = null) => {
    const s = stateRef.current;
    const player = currentPlayerFrom(s);
    const targetTeamId = customTeamId || s.currentBidTeamId;
    const targetPrice = customPriceLakhs != null ? Number(customPriceLakhs) : s.currentBidLakhs;
    const team = s.teams.find(t => t.id === targetTeamId);

    if (!player) throw new Error('No active player selected.');
    if (!team) throw new Error('Please select a team.');
    if (targetPrice == null || isNaN(targetPrice) || targetPrice <= 0) {
      throw new Error('Please enter a valid price.');
    }

    if (targetPrice > team.purseLakhs) {
      throw new Error(`${team.name} does not have enough purse (${targetPrice} L > ${team.purseLakhs} L).`);
    }

    const newPurse = team.purseLakhs - targetPrice;
    
    // Optimistic local updates
    dispatch({
      type: 'REALTIME_SALE',
      payload: { new: { player_id: player.id, team_id: team.id, sold_price_lakhs: targetPrice } }
    });
    dispatch({
      type: 'REALTIME_PURSE',
      payload: { new: { team_id: team.id, purse_lakhs: newPurse } }
    });
    dispatch({
      type: 'REALTIME_AUCTION_STATE',
      payload: { new: { current_index: s.currentIndex, current_bid_lakhs: targetPrice, current_bid_team_id: team.id, status: 'sold' } }
    });

    await runWrite(() => dbMarkSold(player.id, team.id, targetPrice, newPurse));
  }, [runWrite]);

  const markUnsold = useCallback(async () => {
    const player = currentPlayerFrom(stateRef.current);
    if (!player) return;
    dispatch({
      type: 'REALTIME_AUCTION_STATE',
      payload: { new: { current_index: stateRef.current.currentIndex, current_bid_lakhs: null, current_bid_team_id: null, status: 'unsold' } }
    });
    dispatch({ type: 'LOCAL_REQUEUE_UNSOLD', playerId: player.id });
    await runWrite(() => dbMarkUnsold(player.id));
  }, [runWrite]);

  const nextLot = useCallback(async () => {
    const { currentIndex, auctionOrder } = stateRef.current;
    const nextIndex = currentIndex + 1;
    const finished  = nextIndex >= auctionOrder.length;
    dispatch({
      type: 'REALTIME_AUCTION_STATE',
      // Must match dbNextLot's write ('live'), otherwise the display falls through
      // to the "Up next…" placeholder and stays there.
      payload: { new: { current_index: nextIndex, current_bid_lakhs: null, current_bid_team_id: null, status: finished ? 'finished' : 'live' } }
    });
    await runWrite(() => dbNextLot(nextIndex, finished));
  }, [runWrite]);

  const jumpToLot = useCallback(async (index) => {
    dispatch({
      type: 'REALTIME_AUCTION_STATE',
      // Matches dbJumpToLot's write ('live') — see nextLot.
      payload: { new: { current_index: index, current_bid_lakhs: null, current_bid_team_id: null, status: 'live' } }
    });
    await runWrite(() => dbJumpToLot(index));
  }, [runWrite]);

  const reset = useCallback(async () => {
    await runWrite(async () => {
      await dbReset();
      applySnapshot(await hydrate());
    });
  }, [runWrite, applySnapshot]);

  const setTeamName = useCallback(async (teamId, name, short) => {
    const cleanName  = String(name  ?? '').trim().slice(0, TEAM_NAME_MAX);
    const cleanShort = String(short ?? '').trim().slice(0, TEAM_SHORT_MAX);
    if (!cleanName)  throw new Error('Team name cannot be empty.');
    if (!cleanShort) throw new Error('Short code cannot be empty.');

    // Optimistic local rename so the admin sees it instantly.
    dispatch({ type: 'SET_TEAM_NAME', teamId, name: cleanName, short: cleanShort });
    await runWrite(() => dbSetTeamName(teamId, cleanName, cleanShort));
  }, [runWrite]);

  const endAuction = useCallback(async () => {
    await runWrite(() => dbEndAuction());
  }, [runWrite]);

  const value = {
    state,
    currentPlayer: currentPlayerFrom(state),
    startLot,
    placeBid,
    markSold,
    markUnsold,
    endAuction,
    nextLot,
    jumpToLot,
    reset,
    setTeamName,
  };

  if (state.loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-white text-2xl animate-pulse">Connecting to Supabase…</div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-center">
          <div className="text-4xl mb-4">⚠️</div>
          <div className="text-xl font-bold mb-2">Database connection failed</div>
          <div className="text-sm text-slate-400">{state.error}</div>
          <div className="mt-4 text-sm text-slate-500">Check your .env file and Supabase credentials.</div>
        </div>
      </div>
    );
  }

  return (
    <AuctionContext.Provider value={value}>
      {children}
    </AuctionContext.Provider>
  );
}

export function useAuction() {
  const ctx = useContext(AuctionContext);
  if (!ctx) throw new Error('useAuction must be inside <AuctionProvider>');
  return ctx;
}
