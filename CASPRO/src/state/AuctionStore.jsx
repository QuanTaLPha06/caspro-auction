// ---------------------------------------------------------------------------
// AuctionStore.jsx  →  src/state/AuctionStore.jsx
// Supabase-backed state: real-time sync across Admin + TV tabs/devices
// ---------------------------------------------------------------------------

import React, {
  createContext, useContext, useReducer,
  useEffect, useCallback, useRef,
} from 'react';

import players            from '../../players.json';
import { TEAMS }          from '../lib/constants';
import { finalizeSale }   from '../lib/auctionEngine';
import { supabase }       from '../lib/supabase';
import {
  hydrate,
  dbStartLot, dbPlaceBid, dbMarkSold,
  dbMarkUnsold, dbNextLot, dbJumpToLot, dbReset,
} from '../lib/db';

// ── Static data ───────────────────────────────────────────────────────────────

const ALL_PLAYERS   = players;
const AUCTION_ORDER = players.map(p => p.id);

// ── Build fresh local state from DB snapshot ──────────────────────────────────

function buildStateFromSnapshot(auctionStateRow, purseMap, salesMap, unsoldPlayerIds = []) {
  // Rebuild teams with DB purses + sold squads
  const teams = TEAMS.map(t => {
    const purseLakhs = purseMap[t.id] ?? t.purseLakhs;
    const squad = ALL_PLAYERS
      .filter(p => salesMap[p.id]?.teamId === t.id)
      .map(p => ({ ...p, sold_price_lakhs: salesMap[p.id].soldPriceLakhs }));
    return { ...t, purseLakhs, squad };
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

  // ── 1. Hydrate from Supabase on mount ──────────────────────────────────────
  useEffect(() => {
    hydrate()
      .then(({ auctionState, purseMap, salesMap, unsoldPlayerIds }) => {
        dispatch({
          type: 'HYDRATE',
          state: buildStateFromSnapshot(auctionState, purseMap, salesMap, unsoldPlayerIds),
        });
      })
      .catch(err => dispatch({ type: 'SET_ERROR', error: err.message }));
  }, []);

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
        event: 'INSERT', schema: 'public', table: 'bid_log',
      }, payload => dispatch({ type: 'REALTIME_BID_LOG', payload }))

      .subscribe();

    return () => supabase.removeChannel(channel);
  }, []);

  // ── 3. Action helpers (write to DB → Realtime propagates to all clients) ───

  const startLot = useCallback(async () => {
    await dbStartLot();
  }, []);

  const placeBid = useCallback(async (teamId, bidLakhs) => {
    const { currentIndex, auctionOrder } = stateRef.current;
    const pid = auctionOrder[currentIndex];
    await dbPlaceBid(pid, teamId, bidLakhs);
  }, []);

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
    await dbMarkSold(player.id, team.id, targetPrice, newPurse);
  }, []);

  const markUnsold = useCallback(async () => {
    const player = currentPlayerFrom(stateRef.current);
    if (!player) return;
    await dbMarkUnsold(player.id);
    dispatch({ type: 'LOCAL_REQUEUE_UNSOLD', playerId: player.id });
  }, []);

  const nextLot = useCallback(async () => {
    const { currentIndex, auctionOrder } = stateRef.current;
    const nextIndex = currentIndex + 1;
    const finished  = nextIndex >= auctionOrder.length;
    await dbNextLot(nextIndex, finished);
  }, []);

  const jumpToLot = useCallback(async (index) => {
    await dbJumpToLot(index);
  }, []);

  const reset = useCallback(async () => {
    await dbReset();
    const hydrated = await hydrate();
    dispatch({
      type: 'HYDRATE',
      state: buildStateFromSnapshot(
        hydrated.auctionState,
        hydrated.purseMap,
        hydrated.salesMap,
        hydrated.unsoldPlayerIds
      ),
    });
  }, []);

  const value = {
    state,
    currentPlayer: currentPlayerFrom(state),
    startLot,
    placeBid,
    markSold,
    markUnsold,
    nextLot,
    jumpToLot,
    reset,
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
