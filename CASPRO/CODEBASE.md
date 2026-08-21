# CASPRO - Full Codebase Documentation

## File: package.json

```json
{
  "name": "mock-ipl-auction",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "upload-slides": "node scripts/upload-slides.mjs",
    "upload-slides:auto": "node scripts/upload-slides.mjs --auto",
    "upload-slides:local": "node scripts/upload-slides.mjs --auto --local"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.112.3",
    "pdf2pic": "^3.2.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.20",
    "mupdf": "^1.28.0",
    "postcss": "^8.4.47",
    "tailwindcss": "^3.4.14",
    "vite": "^5.4.10"
  }
}

```

## File: vite.config.js

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Expose players.json from the project root so it can be imported in src/
  resolve: {
    alias: {},
  },
});

```

## File: tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
};

```

## File: src/main.jsx

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

```

## File: src/App.jsx

```javascript
// ---------------------------------------------------------------------------
// App.jsx — root router
// src/App.jsx
// ---------------------------------------------------------------------------

import React, { useState } from 'react';
import { AuctionProvider, useAuction } from './state/AuctionStore';
import LandingGateway from './components/LandingGateway';
import TVDisplay      from './components/TVDisplay';
import AdminPanel     from './components/AdminPanel';
import ResultsPanel   from './components/ResultsPanel';

// ── Inner shell — reads auction status to decide when to show ResultsPanel ──
function Shell({ view }) {
  const { state } = useAuction();

  if (view === 'display') {
    return state.status === 'finished' ? <ResultsPanel /> : <TVDisplay />;
  }
  if (view === 'admin') {
    return state.status === 'finished' ? <ResultsPanel /> : <AdminPanel />;
  }
  return null;
}

// ── Root ─────────────────────────────────────────────────────────────────────
export default function App() {
  const [view, setView] = useState('landing'); // 'landing' | 'display' | 'admin'

  return (
    <AuctionProvider>
      {view === 'landing' ? (
        <LandingGateway onEnter={setView} />
      ) : (
        <Shell view={view} />
      )}
    </AuctionProvider>
  );
}

```

## File: src/index.css

```css
/* ── Tailwind directives ─────────────────────────────────────────── */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ── JNAA Cascade 31st Edition Theme Design Tokens ───────────────── */
@layer base {
  *, *::before, *::after {
    box-sizing: border-box;
  }

  html {
    font-family: 'Plus Jakarta Sans', 'Outfit', 'Inter', system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #08091a;
    color: #f8fafc;
  }

  body {
    margin: 0;
    padding: 0;
    background: #08091a;
    background-image: 
      radial-gradient(circle at 15% 15%, rgba(67, 24, 255, 0.25) 0%, transparent 45%),
      radial-gradient(circle at 85% 85%, rgba(147, 51, 234, 0.22) 0%, transparent 45%),
      radial-gradient(circle at 50% 30%, rgba(30, 27, 75, 0.6) 0%, transparent 60%),
      linear-gradient(to bottom, rgba(8, 9, 26, 0.95), rgba(11, 12, 30, 0.98));
    background-attachment: fixed;
    color: #f8fafc;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Elegant Purple Scrollbar */
  ::-webkit-scrollbar {
    width: 7px;
    height: 7px;
  }
  ::-webkit-scrollbar-track {
    background: #08091a;
  }
  ::-webkit-scrollbar-thumb {
    background: rgba(147, 51, 234, 0.4);
    border-radius: 9999px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: rgba(168, 85, 247, 0.8);
    box-shadow: 0 0 12px rgba(168, 85, 247, 0.5);
  }
}

/* ── JNAA Cascade Utility Classes ────────────────────────────────── */
@layer utilities {
  .no-scrollbar::-webkit-scrollbar {
    display: none;
  }
  .no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  /* Glassmorphism Card with Purple Glow border */
  .nb-card {
    background: rgba(15, 17, 43, 0.82);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(147, 51, 234, 0.25);
    box-shadow: 0 20px 50px -10px rgba(4, 5, 15, 0.9), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    border-radius: 1.25rem;
    position: relative;
  }

  .nb-card-hover {
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .nb-card-hover:hover {
    transform: translateY(-3px) scale(1.01);
    border-color: rgba(168, 85, 247, 0.6);
    box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.95), 0 0 30px rgba(147, 51, 234, 0.35);
  }

  /* Cascade Glow Effects */
  .nb-glow-blue {
    box-shadow: 0 0 30px rgba(59, 130, 246, 0.45), inset 0 0 15px rgba(59, 130, 246, 0.2);
  }
  .nb-glow-cyan {
    box-shadow: 0 0 30px rgba(6, 182, 212, 0.45), inset 0 0 15px rgba(6, 182, 212, 0.2);
  }
  .nb-glow-purple {
    box-shadow: 0 0 35px rgba(168, 85, 247, 0.55), inset 0 0 15px rgba(168, 85, 247, 0.25);
  }
  .nb-glow-amber {
    box-shadow: 0 0 30px rgba(245, 158, 11, 0.45), inset 0 0 15px rgba(245, 158, 11, 0.2);
  }

  /* Pill & Tag Badges */
  .nb-pill {
    display: inline-flex;
    items-center: center;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border: 1px solid rgba(255, 255, 255, 0.15);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
  }

  /* Text Gradients */
  .nb-gradient-purple {
    background: linear-gradient(135deg, #a855f7 0%, #c084fc 50%, #e9d5ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .nb-gradient-gold {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  /* Custom Animations */
  @keyframes floatSlow {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-8px) rotate(1deg); }
  }
  .animate-float {
    animation: floatSlow 6s ease-in-out infinite;
  }

  @keyframes pulseGlow {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 0.8; }
  }
  .animate-glow {
    animation: pulseGlow 4s ease-in-out infinite;
  }
}

```

## File: src/lib/constants.js

```javascript
// ---------------------------------------------------------------------------
// constants.js  →  src/lib/constants.js
// ---------------------------------------------------------------------------

export const TEAMS = [
  { id: 'MI',   name: 'Mumbai Indians',             color: '#004BA0', purseLakhs: 12000 },
  { id: 'CSK',  name: 'Chennai Super Kings',         color: '#FFCC00', purseLakhs: 12000 },
  { id: 'RCB',  name: 'Royal Challengers Bengaluru', color: '#EC1C24', purseLakhs: 12000 },
  { id: 'KKR',  name: 'Kolkata Knight Riders',       color: '#3A225D', purseLakhs: 12000 },
  { id: 'DC',   name: 'Delhi Capitals',              color: '#17479E', purseLakhs: 12000 },
  { id: 'PBKS', name: 'Punjab Kings',                color: '#DD1F2D', purseLakhs: 12000 },
  { id: 'RR',   name: 'Rajasthan Royals',            color: '#254AA5', purseLakhs: 12000 },
  { id: 'SRH',  name: 'Sunrisers Hyderabad',         color: '#F26522', purseLakhs: 12000 },
  { id: 'LSG',  name: 'Lucknow Super Giants',        color: '#00B2A9', purseLakhs: 12000 },
  { id: 'GT',   name: 'Gujarat Titans',              color: '#1B2133', purseLakhs: 12000 },
];

export const SQUAD_RULES = {
  MIN_SQUAD_SIZE:     15,
  MAX_SQUAD_SIZE:     25,
  MAX_OVERSEAS:        8,
  MIN_WICKET_KEEPERS:  2,
};

export const ROLES = ['Batsman', 'Wicket-Keeper', 'All-Rounder', 'Pacer', 'Spinner'];

export const BID_INCREMENTS = [
  { upToLakhs: 100,      step: 5  },  // < 1 Cr  → steps of 5L
  { upToLakhs: 200,      step: 10 },  // 1–2 Cr  → steps of 10L
  { upToLakhs: 500,      step: 20 },  // 2–5 Cr  → steps of 20L
  { upToLakhs: Infinity, step: 25 },  // > 5 Cr  → steps of 25L
];

export function nextBidLakhs(currentLakhs) {
  const step = BID_INCREMENTS.find(b => currentLakhs < b.upToLakhs)?.step ?? 25;
  return currentLakhs + step;
}

export const AUTH = {
  DISPLAY_PIN:    'TVMODE',      // read-only display gateway
  ADMIN_PASSWORD: 'caspro',      // auctioneer control room
};

```

## File: src/lib/supabase.js

```javascript
// ---------------------------------------------------------------------------
// supabase.js  →  src/lib/supabase.js
// Singleton Supabase client — import this everywhere you need DB access
// ---------------------------------------------------------------------------

import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL      = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
  throw new Error(
    'Missing Supabase env vars. Copy .env.example → .env and fill in your project credentials.'
  );
}

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  realtime: { params: { eventsPerSecond: 10 } },
});

```

## File: src/lib/db.js

```javascript
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

```

## File: src/lib/scoringEngine.js

```javascript
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

```

## File: src/lib/auctionEngine.js

```javascript
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

```

## File: src/lib/exportUtils.js

```javascript
// src/lib/exportUtils.js
// Utility helper to export auction sales & team rosters as JSON or CSV format

/**
 * Helper to download a string of data as a file in the browser
 */
function downloadFile(content, fileName, contentType) {
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * Format lakhs to display string (e.g. 150 -> "1.50 Cr", 50 -> "50 Lakhs")
 */
function formatLakhs(lakhs) {
  if (lakhs == null || isNaN(lakhs)) return '0 Lakhs';
  if (lakhs >= 100) return `${(lakhs / 100).toFixed(2)} Cr`;
  return `${lakhs} Lakhs`;
}

/**
 * Export full auction roster data per team in JSON format
 * Creates an object indexed by Team Name / ID with squad details and purse stats.
 */
export function exportRostersJSON(teams, playerSales = {}) {
  const exportData = {
    exportDate: new Date().toISOString(),
    system: "CASPRO Mock IPL Auction System",
    teams: teams.map(t => {
      const squad = (t.squad || []).map(p => ({
        id: p.id,
        name: p.name,
        role: p.role,
        isOverseas: !!p.is_overseas,
        isRookie: !!p.is_rookie,
        rating: p.rating || null,
        basePriceLakhs: p.base_price_lakhs,
        basePriceFormatted: formatLakhs(p.base_price_lakhs),
        soldPriceLakhs: p.sold_price_lakhs,
        soldPriceFormatted: formatLakhs(p.sold_price_lakhs),
      }));

      return {
        teamId: t.id,
        teamName: t.name,
        shortName: t.shortName,
        purseInitialLakhs: t.initialPurseLakhs || 12000,
        purseRemainingLakhs: t.purseLakhs,
        purseSpentLakhs: (t.initialPurseLakhs || 12000) - t.purseLakhs,
        purseRemainingFormatted: formatLakhs(t.purseLakhs),
        purseSpentFormatted: formatLakhs((t.initialPurseLakhs || 12000) - t.purseLakhs),
        totalPlayers: squad.length,
        overseasPlayers: squad.filter(p => p.isOverseas).length,
        squad: squad,
      };
    })
  };

  const jsonStr = JSON.stringify(exportData, null, 2);
  const fileName = `IPL_Auction_Team_Rosters_${new Date().toISOString().slice(0, 10)}.json`;
  downloadFile(jsonStr, fileName, 'application/json');
}

/**
 * Export full auction roster data as CSV format
 * Generates a clean tabular CSV sheet readable by Microsoft Excel, Google Sheets, etc.
 */
export function exportRostersCSV(teams) {
  const headers = [
    'Team ID',
    'Team Name',
    'Player ID',
    'Player Name',
    'Role',
    'Overseas',
    'Rookie',
    'Rating',
    'Base Price (Lakhs)',
    'Sold Price (Lakhs)',
    'Sold Price (Formatted)',
    'Team Remaining Purse (Lakhs)',
  ];

  const rows = [];

  teams.forEach(t => {
    const squad = t.squad || [];
    if (squad.length === 0) {
      // Add entry even if team bought 0 players
      rows.push([
        `"${t.id}"`,
        `"${t.name}"`,
        '""',
        '"No Players Bought"',
        '""',
        '""',
        '""',
        '""',
        '""',
        '""',
        '""',
        t.purseLakhs,
      ]);
    } else {
      squad.forEach(p => {
        rows.push([
          `"${t.id}"`,
          `"${t.name}"`,
          `"${p.id}"`,
          `"${p.name.replace(/"/g, '""')}"`,
          `"${p.role || ''}"`,
          p.is_overseas ? 'Yes' : 'No',
          p.is_rookie ? 'Yes' : 'No',
          p.rating ?? '',
          p.base_price_lakhs ?? '',
          p.sold_price_lakhs ?? '',
          `"${formatLakhs(p.sold_price_lakhs)}"`,
          t.purseLakhs,
        ]);
      });
    }
  });

  const csvContent = [
    headers.join(','),
    ...rows.map(r => r.join(','))
  ].join('\n');

  const fileName = `IPL_Auction_Team_Rosters_${new Date().toISOString().slice(0, 10)}.csv`;
  downloadFile(csvContent, fileName, 'text/csv;charset=utf-8;');
}

```

## File: src/state/AuctionStore.jsx

```javascript
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
  dbMarkUnsold, dbEndAuction, dbNextLot, dbJumpToLot, dbReset,
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
        event: 'DELETE', schema: 'public', table: 'player_sales',
      }, () => {
        // When sales are cleared (reset), re-hydrate full state
        hydrate().then(({ auctionState, purseMap, salesMap, unsoldPlayerIds }) => {
          dispatch({
            type: 'HYDRATE',
            state: buildStateFromSnapshot(auctionState, purseMap, salesMap, unsoldPlayerIds),
          });
        });
      })

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

  const endAuction = useCallback(async () => {
    await dbEndAuction();
  }, []);

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

```

## File: src/components/LandingGateway.jsx

```javascript
// ---------------------------------------------------------------------------
// LandingGateway.jsx  →  src/components/LandingGateway.jsx
// Dual-gateway login with NeuroBank Glassmorphism UI
// ---------------------------------------------------------------------------

import React, { useState } from 'react';
import { AUTH } from '../lib/constants';

export default function LandingGateway({ onEnter }) {
  const [mode,  setMode]  = useState(null); // 'display' | 'admin' | null
  const [code,  setCode]  = useState('');
  const [error, setError] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (mode === 'display') {
      code === AUTH.DISPLAY_PIN ? onEnter('display') : setError('Wrong PIN for the TV display.');
    } else if (mode === 'admin') {
      code === AUTH.ADMIN_PASSWORD ? onEnter('admin') : setError('Wrong auctioneer password.');
    }
  }

  function reset() { setMode(null); setCode(''); setError(''); }

  return (
    <div className="min-h-screen text-slate-100 flex flex-col items-center justify-center px-4 py-12 relative overflow-hidden bg-[#08091a]">
      
      {/* Background ambient glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-purple-600/20 rounded-full blur-[180px] pointer-events-none animate-pulse" />
      <div className="absolute bottom-10 right-10 w-[500px] h-[500px] bg-indigo-600/15 rounded-full blur-[160px] pointer-events-none" />
      <div className="absolute top-10 left-10 w-[450px] h-[450px] bg-blue-600/15 rounded-full blur-[160px] pointer-events-none" />

      <div className="w-full max-w-md relative z-10">

        {/* Brand Header */}
        <div className="text-center mb-8 flex flex-col items-center">
          {/* Logo container */}
          <div className="w-48 h-48 mb-2 flex items-center justify-center p-2 rounded-3xl bg-white/5 border border-purple-500/20 backdrop-blur-xl shadow-[0_0_40px_rgba(168,85,247,0.25)] transition-all hover:scale-105">
            <img src="/logo.png" alt="Cascade Logo" className="w-full h-full object-contain filter drop-shadow-[0_0_15px_rgba(168,85,247,0.4)]" />
          </div>

          <div className="inline-flex items-center gap-2 mb-3 px-4 py-1.5 rounded-full bg-purple-950/80 border border-purple-500/40 text-purple-300 text-xs font-black tracking-widest uppercase shadow-[0_0_20px_rgba(168,85,247,0.3)]">
            <span>✨</span> CASCADE
          </div>
          <h1 className="text-3xl lg:text-4xl font-black tracking-tight mb-2 uppercase font-mono">
            MOCK IPL <span className="nb-gradient-purple">AUCTION</span>
          </h1>
          <p className="text-purple-400/90 text-sm font-black tracking-widest uppercase font-mono drop-shadow-[0_0_10px_rgba(168,85,247,0.5)]">
            3, 2, 1... SOLD
          </p>
        </div>

        {/* Gateway selection */}
        {!mode && (
          <div className="grid grid-cols-1 gap-5">
            <button
              onClick={() => setMode('display')}
              className="nb-card p-6 text-left transition-all duration-300 group hover:border-purple-400/60 hover:shadow-[0_0_35px_rgba(168,85,247,0.35)] relative overflow-hidden border-purple-500/20 bg-slate-950/80"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="w-12 h-12 rounded-2xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform shadow-[0_0_15px_rgba(168,85,247,0.3)]">
                  📺
                </div>
                <span className="nb-pill border-purple-500/40 text-purple-300 text-[10px] tracking-widest bg-purple-950/50">ARENA FEED</span>
              </div>
              <div className="text-xl font-black text-white group-hover:text-purple-300 transition-colors uppercase tracking-wide font-mono">
                TV Display Gateway
              </div>
              <div className="text-xs text-slate-400 mt-1 leading-relaxed font-medium">
                High-impact auditorium live broadcast display tuned for audience viewing.
              </div>
            </button>

            <button
              onClick={() => setMode('admin')}
              className="nb-card p-6 text-left transition-all duration-300 group hover:border-indigo-400/60 hover:shadow-[0_0_35px_rgba(99,102,241,0.35)] relative overflow-hidden border-indigo-500/20 bg-slate-950/80"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="w-12 h-12 rounded-2xl bg-indigo-500/15 border border-indigo-500/30 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform shadow-[0_0_15px_rgba(99,102,241,0.3)]">
                  🎙️
                </div>
                <span className="nb-pill border-indigo-500/40 text-indigo-300 text-[10px] tracking-widest bg-indigo-950/50">COMMAND DECK</span>
              </div>
              <div className="text-xl font-black text-white group-hover:text-indigo-300 transition-colors uppercase tracking-wide font-mono">
                Auctioneer Control Room
              </div>
              <div className="text-xs text-slate-400 mt-1 leading-relaxed font-medium">
                Master command dashboard for real-time player bids & squad roster allocations.
              </div>
            </button>
          </div>
        )}

        {/* Auth form */}
        {mode && (
          <form onSubmit={handleSubmit} className="nb-card p-8 space-y-6 relative border-purple-500/40 shadow-[0_0_50px_rgba(0,0,0,0.9)] bg-slate-950/90">
            <div className="flex items-center justify-between pb-4 border-b border-purple-500/20">
              <div>
                <h3 className="text-xl font-black text-white uppercase font-mono tracking-wider">
                  {mode === 'display' ? 'Display Access' : 'Control Room Auth'}
                </h3>
                <p className="text-xs text-purple-400 mt-0.5 font-bold uppercase tracking-wide">
                  {mode === 'display' ? 'ENTER TV DISPLAY ACCESS PIN' : 'ENTER AUCTIONEER CREDENTIALS'}
                </p>
              </div>
              <button
                type="button"
                onClick={reset}
                className="text-xs text-slate-400 hover:text-white transition-colors border border-slate-700 rounded-lg px-2.5 py-1"
              >
                Back
              </button>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 font-mono">
                {mode === 'display' ? 'TV DISPLAY PIN' : 'COMMAND PASSWORD'}
              </label>
              <input
                type="password"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder={mode === 'display' ? `Enter PIN (Default: ${AUTH.DISPLAY_PIN})` : `Enter Password (Default: ${AUTH.ADMIN_PASSWORD})`}
                className="w-full px-4 py-3 rounded-xl bg-slate-900/90 border border-purple-500/30 text-white placeholder-slate-500 text-sm font-mono focus:outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-400 transition-all"
                autoFocus
              />
            </div>

            {error && (
              <div className="p-3.5 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs font-bold flex items-center gap-2 shadow-[0_0_15px_rgba(239,68,68,0.2)]">
                <span>⚠️</span> {error}
              </div>
            )}

            <div className="flex gap-3 pt-2">
              <button
                type="submit"
                className="flex-1 py-3.5 px-5 rounded-xl bg-gradient-to-r from-red-600 via-rose-600 to-red-700 text-white font-black text-sm tracking-wider uppercase hover:from-red-500 hover:to-rose-500 transition-all duration-200 shadow-[0_0_20px_rgba(239,68,68,0.4)]"
              >
                ACCESS PORTAL
              </button>
              <button
                type="button"
                onClick={reset}
                className="py-3.5 px-5 rounded-xl border border-slate-700 text-slate-300 font-bold text-sm hover:bg-slate-800 transition-all uppercase font-mono"
              >
                ABORT
              </button>
            </div>
          </form>
        )}

      </div>
    </div>
  );
}


```

## File: src/components/TVDisplay.jsx

```javascript
// ---------------------------------------------------------------------------
// TVDisplay.jsx  →  src/components/TVDisplay.jsx
// Read-only big-screen dashboard — Supabase Realtime auto-updates live
// NeuroBank Glassmorphism aesthetic
// ---------------------------------------------------------------------------

import React, { useState, useEffect } from 'react';
import { useAuction }     from '../state/AuctionStore';
import { nextBidLakhs }   from '../lib/constants';
import { getSlideUrl }    from '../lib/db';

function formatLakhs(l) {
  if (l == null) return '—';
  if (l >= 100)  return `₹${(l / 100).toFixed(2)} Cr`;
  return `₹${l} L`;
}

function Badge({ children, tone = 'slate' }) {
  const tones = {
    slate: 'bg-slate-800/80 text-slate-200 border-slate-700/60',
    amber: 'bg-amber-400/10 text-amber-300 border-amber-400/30',
    green: 'bg-emerald-400/10 text-emerald-300 border-emerald-400/30',
    rose:  'bg-rose-400/10 text-rose-300 border-rose-400/30',
    purple:'bg-purple-400/10 text-purple-300 border-purple-400/30',
    cyan:  'bg-indigo-400/10 text-indigo-300 border-indigo-400/30',
  };
  return (
    <span className={`px-3 py-1 rounded-full border text-xs font-semibold tracking-wide ${tones[tone]}`}>
      {children}
    </span>
  );
}

function StatusBanner({ status, leadingTeam, nextBid }) {
  if (status === 'sold') {
    return (
      <div className="text-4xl lg:text-5xl font-black font-mono tracking-tight animate-bounce drop-shadow-[0_0_30px_rgba(34,197,94,0.6)] text-emerald-400 border border-emerald-500/40 bg-emerald-950/60 px-6 py-3 rounded-2xl inline-block">
        ✨ SOLD {leadingTeam ? `to ${leadingTeam.name}` : ''} 🎉
      </div>
    );
  }
  if (status === 'unsold') {
    return <div className="text-4xl font-extrabold text-slate-500 tracking-wider">UNSOLD</div>;
  }
  if (status === 'live' && leadingTeam) {
    return (
      <div className="text-2xl font-medium text-slate-200">
        Leading:{' '}
        <span className="font-bold drop-shadow-md" style={{ color: leadingTeam.color }}>{leadingTeam.name}</span>
        <span className="text-slate-400 text-lg"> · next bid <span className="text-purple-400 font-mono font-bold">{formatLakhs(nextBid)}</span></span>
      </div>
    );
  }
  if (status === 'live') {
    return <div className="text-2xl text-purple-400 font-semibold animate-pulse">Bidding open — awaiting first bid…</div>;
  }
  return <div className="text-2xl text-slate-500 font-medium">Up next…</div>;
}

// Player slide image — uses player.image from JSON, fallback to /player_images/{id}.jpg/png, then initials avatar
function PlayerSlide({ player }) {
  const [src, setSrc]         = useState(null);
  const [attempt, setAttempt] = useState('manifest'); // 'manifest' | 'jpg' | 'png' | 'avatar'

  useEffect(() => {
    setAttempt('manifest');
    setSrc(player.image || `/player_images/${player.id}.jpg`);
  }, [player.id, player.image]);

  const handleError = () => {
    if (attempt === 'manifest') {
      setAttempt('jpg');
      setSrc(`/player_images/${player.id}.jpg`);
    } else if (attempt === 'jpg') {
      setAttempt('png');
      setSrc(`/player_images/${player.id}.png`);
    } else if (attempt === 'png') {
      setAttempt('avatar');
    }
  };

  if (attempt === 'avatar' || !src) {
    return (
      <div className="aspect-[3/4] rounded-3xl bg-gradient-to-br from-slate-900/90 to-slate-950/90 border border-slate-700/60 flex items-center justify-center shadow-2xl relative overflow-hidden backdrop-blur-xl">
        <div className="absolute inset-0 bg-cyan-500/5 blur-xl pointer-events-none" />
        <span className="text-8xl font-black text-slate-700 select-none tracking-tighter">
          {player.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
        </span>
      </div>
    );
  }

  return (
    <div className="relative rounded-3xl overflow-hidden border border-slate-700/60 shadow-2xl group max-h-[60vh] flex items-center justify-center bg-slate-950/50">
      <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent z-10 opacity-60 pointer-events-none" />
      <img
        src={src}
        alt={player.name}
        onError={handleError}
        className="max-h-[60vh] w-auto object-contain rounded-3xl transition-transform duration-700 group-hover:scale-105"
      />
    </div>
  );
}

export default function TVDisplay() {
  const { state, currentPlayer } = useAuction();
  const { teams, currentBidLakhs, currentBidTeamId, status, currentIndex, auctionOrder, players } = state;

  const leadingTeam = teams.find(t => t.id === currentBidTeamId);
  const nextBid     = currentBidLakhs != null
    ? nextBidLakhs(currentBidLakhs)
    : currentPlayer?.base_price_lakhs;

  const isUnsoldRound = currentIndex >= players.length;

  if (status === 'finished' || !currentPlayer) {
    return (
      <div className="h-screen w-screen text-white flex items-center justify-center relative overflow-hidden bg-[#070a12]">
        <div className="absolute inset-0 bg-cyan-500/5 blur-3xl pointer-events-none" />
        <div className="text-center nb-card p-10 max-w-lg">
          <div className="text-6xl mb-4">🏏</div>
          <div className="text-4xl font-black mb-2">Auction Complete</div>
          <div className="text-slate-400 text-base">All lots have been called.</div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen w-screen text-white flex flex-col select-none relative overflow-hidden bg-[#030712]">

      {/* Cyber Deadly background ambient glow spots */}
      <div className="absolute top-0 right-1/4 w-[600px] h-[600px] bg-red-600/15 rounded-full blur-[180px] pointer-events-none animate-pulse" />
      <div className="absolute bottom-0 left-1/4 w-[600px] h-[600px] bg-purple-600/15 rounded-full blur-[180px] pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-cyan-600/10 rounded-full blur-[200px] pointer-events-none" />

      {/* Top navbar strip - Cyber Metallic */}
      <div className="flex items-center justify-between px-8 py-3.5 border-b border-red-500/30 backdrop-blur-2xl bg-slate-950/90 shrink-0 z-20 shadow-[0_4px_30px_rgba(0,0,0,0.8)]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-600/20 border border-purple-500/50 flex items-center justify-center p-1 shadow-[0_0_15px_rgba(168,85,247,0.4)]">
            <img src="/logo.png" alt="Logo" className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(168,85,247,0.6)]" />
          </div>
          <div>
            <div className="text-xl font-black tracking-widest text-white uppercase font-mono drop-shadow-[0_0_10px_rgba(168,85,247,0.5)]">
              3, 2, 1... <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400">SOLD</span>
            </div>
            <div className="text-[10px] text-red-400/80 font-mono tracking-widest uppercase font-bold">
              LIVE BROADCAST FEED // HIGH STAKES ARENA
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4 text-slate-300 text-xs font-bold tracking-wider">
          {/* Live indicator */}
          <span className="border border-red-500/50 text-red-400 bg-red-950/60 flex items-center gap-2 px-4 py-1.5 rounded-full shadow-[0_0_20px_rgba(239,68,68,0.4)] font-mono font-black tracking-wider">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping" />
            LIVE STAGE
          </span>
          <span className="text-red-900 font-bold">|</span>
          <span className="font-mono text-cyan-300 font-extrabold text-sm border border-cyan-500/30 bg-cyan-950/40 px-3.5 py-1 rounded-lg">
            LOT {currentIndex + 1} / {auctionOrder.length}
          </span>
          {isUnsoldRound && (
            <span className="border border-amber-500/50 text-amber-300 bg-amber-950/60 px-3.5 py-1 rounded-full font-black animate-pulse shadow-[0_0_15px_rgba(245,158,11,0.3)] font-mono">
              ⚡ RE-ACCELERATED ARENA
            </span>
          )}
          {currentPlayer.pool_name && (
            <>
              <span className="text-red-900 font-bold">|</span>
              <span className="text-purple-300 font-mono font-extrabold border border-purple-500/30 bg-purple-950/40 px-3.5 py-1 rounded-lg">
                POOL {currentPlayer.pool} — {currentPlayer.pool_name.toUpperCase()}
              </span>
            </>
          )}
        </div>
      </div>

      {/* Main stage - Viewport fitted */}
      <div className="flex-1 grid grid-cols-12 gap-8 px-10 py-6 items-center overflow-hidden min-h-0 z-10">
        
        {/* Player slide / photo container */}
        <div className="col-span-5 flex items-center justify-center max-h-full overflow-hidden">
          <div className="w-full max-h-[62vh] flex items-center justify-center relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-red-600 via-purple-600 to-cyan-500 rounded-3xl blur-xl opacity-30 group-hover:opacity-60 transition duration-1000 animate-pulse pointer-events-none" />
            <PlayerSlide player={currentPlayer} />
          </div>
        </div>

        {/* Player info & bidding stage */}
        <div className="col-span-7 space-y-5 flex flex-col justify-center max-h-full">
          <div>
            <div className="flex items-center gap-2 mb-2">
              {isUnsoldRound && (
                <span className="px-3 py-1 rounded-md text-xs font-mono font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 shadow-[0_0_10px_rgba(245,158,11,0.2)]">
                  RE-ACCELERATED LOT
                </span>
              )}
            </div>
            <h1 className="text-4xl lg:text-6xl font-black leading-tight tracking-tight text-white font-mono drop-shadow-[0_4px_20px_rgba(0,0,0,0.9)]">
              {currentPlayer.name}
            </h1>
            <div className="flex flex-wrap gap-2.5 mt-3.5">
              <Badge tone="cyan">{currentPlayer.role}</Badge>
              {currentPlayer.style      && <Badge>{currentPlayer.style}</Badge>}
              <Badge>{currentPlayer.nationality}</Badge>
              <Badge>Age {currentPlayer.age}</Badge>
              {currentPlayer.is_rookie   && <Badge tone="amber">Uncapped</Badge>}
              {currentPlayer.is_overseas && <Badge tone="green">✈ Overseas</Badge>}
              {currentPlayer.performance_rating != null && (
                <Badge tone="rose">⭐ {currentPlayer.performance_rating}</Badge>
              )}
            </div>
          </div>

          {currentPlayer.note && (
            <p className="text-slate-200 text-xs lg:text-sm leading-relaxed p-4 rounded-2xl bg-slate-950/80 border border-red-500/30 backdrop-blur-md font-sans shadow-lg">
              "{currentPlayer.note}"
            </p>
          )}

          <div className="grid grid-cols-2 gap-5">
            <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 shadow-[0_4px_20px_rgba(0,0,0,0.5)]">
              <div className="text-slate-400 text-xs font-mono uppercase font-bold tracking-wider mb-1">Base Price</div>
              <div className="text-2xl lg:text-3xl font-black text-slate-100 font-mono">{currentPlayer.base_price_label}</div>
            </div>
            <div className="p-4 rounded-2xl bg-slate-950/90 border border-cyan-500/40 shadow-[0_0_25px_rgba(6,182,212,0.25)]">
              <div className="text-cyan-400/80 text-xs font-mono uppercase font-bold tracking-wider mb-1">
                {status === 'sold' ? 'Final Valuation' : 'Current Standing Bid'}
              </div>
              <div className="text-3xl lg:text-4xl font-black text-cyan-300 font-mono drop-shadow-[0_0_12px_rgba(6,182,212,0.6)]">
                {formatLakhs(currentBidLakhs ?? currentPlayer.base_price_lakhs)}
              </div>
            </div>
          </div>

          <div className="pt-2">
            <StatusBanner status={status} leadingTeam={leadingTeam} nextBid={nextBid} />
          </div>
        </div>
      </div>

      {/* Team purse ticker */}
      <div className="border-t border-red-500/20 bg-slate-950/95 backdrop-blur-xl px-8 py-3 overflow-x-auto shrink-0 z-20 shadow-[0_-4px_30px_rgba(0,0,0,0.8)]">
        <div className="flex gap-4 min-w-max">
          {teams.map(t => (
            <div
              key={t.id}
              className="rounded-xl px-5 py-2.5 border transition-all duration-300 backdrop-blur-md"
              style={{
                borderColor: t.id === currentBidTeamId ? t.color : 'rgba(255, 255, 255, 0.1)',
                background:  t.id === currentBidTeamId ? `${t.color}25` : 'rgba(15, 23, 42, 0.6)',
                boxShadow:   t.id === currentBidTeamId ? `0 0 20px ${t.color}55` : 'none',
              }}
            >
              <div className="text-[11px] text-slate-400 font-mono font-bold tracking-wider uppercase">{t.id}</div>
              <div className="font-black text-base font-mono" style={{ color: t.color }}>{formatLakhs(t.purseLakhs)}</div>
              <div className="text-[10px] text-slate-400 font-medium font-mono">{t.squad.length} / 25 players</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}


```

## File: src/components/AdminPanel.jsx

```javascript
// ---------------------------------------------------------------------------
// AdminPanel.jsx  →  src/components/AdminPanel.jsx
// NeuroBank Online Banking Dashboard Design inspired Auctioneer Control Room
// Real-time Supabase sync + Manual Team & Price Direct Sales + Squad Math Popup
// ---------------------------------------------------------------------------

import React, { useState, useEffect } from 'react';
import { useAuction }                     from '../state/AuctionStore';
import { SQUAD_RULES, nextBidLakhs }      from '../lib/constants';
import { canTeamBid, computeMaxLegalBid } from '../lib/auctionEngine';
import { exportRostersJSON, exportRostersCSV } from '../lib/exportUtils';

function fmt(l) {
  if (l == null || isNaN(l)) return '—';
  if (l >= 100) return `₹${(l / 100).toFixed(2)} Cr`;
  return `₹${l} L`;
}

function computeSquadMath(team, bidLakhs, player) {
  if (!team) return null;
  const squadCount = team.squad ? team.squad.length : 0;
  const minSquad = SQUAD_RULES.MIN_SQUAD_SIZE; // 18
  const maxSquad = SQUAD_RULES.MAX_SQUAD_SIZE; // 25
  const reservePerSlot = 30; // Lakhs (Pool E base price)

  const squadAfterBuy = squadCount + 1;
  const slotsRemainingNeeded = Math.max(0, minSquad - squadAfterBuy);
  const totalReserveRequired = slotsRemainingNeeded * reservePerSlot;
  const purse = team.purseLakhs;
  const maxLegalBid = Math.max(0, purse - totalReserveRequired);

  const overseasCount = team.squad ? team.squad.filter(p => p.is_overseas).length : 0;
  const maxOverseas = SQUAD_RULES.MAX_OVERSEAS; // 8

  const isMaxSquadBreach = squadCount >= maxSquad;
  const isOverseasBreach = player?.is_overseas && (overseasCount >= maxOverseas);
  const isExceedPurse = bidLakhs > purse;
  const isExceedHardCeiling = bidLakhs > maxLegalBid;
  const shortfall = Math.max(0, bidLakhs - maxLegalBid);

  let primaryReason = '';
  if (isMaxSquadBreach) {
    primaryReason = `Squad is already at maximum capacity (${maxSquad} players). No more buys allowed.`;
  } else if (isOverseasBreach) {
    primaryReason = `Overseas limit reached (${overseasCount}/${maxOverseas} overseas players). Cannot buy another overseas player.`;
  } else if (isExceedPurse) {
    primaryReason = `Bid price of ${fmt(bidLakhs)} exceeds total available team purse of ${fmt(purse)}.`;
  } else if (isExceedHardCeiling) {
    primaryReason = `Buying this player for ${fmt(bidLakhs)} leaves only ${fmt(purse - bidLakhs)} purse. ${team.name} still needs ${slotsRemainingNeeded} more player(s) to reach mandatory minimum squad size of ${minSquad}, requiring at least ${fmt(totalReserveRequired)} (at ₹30L reserve price per slot). Max allowed legal bid is ${fmt(maxLegalBid)}.`;
  }

  return {
    squadCount,
    minSquad,
    maxSquad,
    squadAfterBuy,
    slotsRemainingNeeded,
    reservePerSlot,
    totalReserveRequired,
    purse,
    maxLegalBid,
    bidLakhs,
    shortfall,
    overseasCount,
    maxOverseas,
    isMaxSquadBreach,
    isOverseasBreach,
    isExceedPurse,
    isExceedHardCeiling,
    hasWarning: isMaxSquadBreach || isOverseasBreach || isExceedPurse || isExceedHardCeiling,
    primaryReason,
  };
}

function SquadMathModal({ data, onClose }) {
  if (!data) return null;
  const { team, bidLakhs, player, math, onForce } = data;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-2xl flex items-center justify-center p-4 overflow-y-auto animate-fadeIn">
      <div className="nb-card border-2 border-rose-500/50 max-w-2xl w-full p-6 md:p-8 space-y-6 relative overflow-hidden text-slate-100 shadow-2xl">
        
        {/* Background Glow */}
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-rose-500/15 rounded-full blur-3xl pointer-events-none" />

        {/* Top Header */}
        <div className="flex items-start justify-between gap-4 border-b border-white/10 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-2xl shrink-0 shadow-lg shadow-rose-950">
              🚨
            </div>
            <div>
              <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
                <span>Squad Math &amp; Hard Ceiling Warning</span>
              </h2>
              <p className="text-xs text-rose-300/80 font-medium">
                Mandatory Minimum Squad Rule ({math.minSquad} Players) &amp; Budget Reserve Calculation
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="text-slate-400 hover:text-white p-2 rounded-xl bg-slate-800/60 hover:bg-slate-700/60 border border-white/10 transition"
          >
            ✕
          </button>
        </div>

        {/* Team & Player Banner */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-950/90 p-4 rounded-2xl border border-white/10">
          <div className="flex items-center gap-3">
            <span className="text-lg font-black px-3 py-1 rounded-xl bg-slate-900 border border-white/15 font-mono" style={{ color: team.color }}>
              {team.id}
            </span>
            <div>
              <div className="text-sm font-bold text-white">{team.name}</div>
              <div className="text-xs text-slate-400">Target Player: <span className="text-amber-300 font-semibold">{player?.name || 'Current Lot'}</span></div>
            </div>
          </div>
          <div className="text-left sm:text-right border-t sm:border-t-0 border-white/10 pt-2 sm:pt-0">
            <div className="text-[10px] text-slate-400 uppercase font-semibold">Attempted Transaction</div>
            <div className="text-lg font-black text-rose-400 font-mono">{fmt(bidLakhs)}</div>
          </div>
        </div>

        {/* Primary Violation Alert Box */}
        <div className="bg-rose-950/50 border border-rose-500/50 p-4 rounded-2xl text-rose-200 text-xs sm:text-sm font-medium leading-relaxed shadow-inner">
          <div className="font-bold text-rose-300 mb-1 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
            <span>⚠️ Warning Breakdown</span>
          </div>
          {math.primaryReason}
        </div>

        {/* Mathematical Breakdown Cards */}
        <div>
          <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
            <span>🧮 Mathematical Audit Breakdown</span>
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 font-mono text-xs">
            <div className="bg-slate-950/70 p-3.5 rounded-2xl border border-white/10">
              <span className="text-[10px] text-slate-500 uppercase block font-sans font-bold">Current Squad</span>
              <span className="text-base font-black text-slate-200">{math.squadCount} / {math.minSquad}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5 font-sans">Target: Min {math.minSquad}</span>
            </div>

            <div className="bg-slate-950/70 p-3.5 rounded-2xl border border-white/10">
              <span className="text-[10px] text-slate-500 uppercase block font-sans font-bold">Squad After Purchase</span>
              <span className="text-base font-black text-indigo-300">{math.squadAfterBuy} Players</span>
              <span className="text-[10px] text-slate-400 block mt-0.5 font-sans">Needs {math.slotsRemainingNeeded} more slots</span>
            </div>

            <div className="bg-slate-950/70 p-3.5 rounded-2xl border border-white/10">
              <span className="text-[10px] text-slate-500 uppercase block font-sans font-bold">Reserve / Slot</span>
              <span className="text-base font-black text-amber-300">₹30 Lakhs</span>
              <span className="text-[10px] text-slate-400 block mt-0.5 font-sans">Cheapest Base Price</span>
            </div>

            <div className="bg-slate-950/70 p-3.5 rounded-2xl border border-white/10">
              <span className="text-[10px] text-slate-500 uppercase block font-sans font-bold">Total Reserve Required</span>
              <span className="text-base font-black text-amber-400">{fmt(math.totalReserveRequired)}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5 font-sans">{math.slotsRemainingNeeded} slots × ₹30L</span>
            </div>

            <div className="bg-slate-950/70 p-3.5 rounded-2xl border border-white/10">
              <span className="text-[10px] text-slate-500 uppercase block font-sans font-bold">Available Purse</span>
              <span className="text-base font-black text-emerald-400">{fmt(math.purse)}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5 font-sans">Team Purse</span>
            </div>

            <div className="bg-slate-950/70 p-3.5 rounded-2xl border border-white/10">
              <span className="text-[10px] text-slate-500 uppercase block font-sans font-bold">Max Legal Allowed Bid</span>
              <span className="text-base font-black text-indigo-400">{fmt(math.maxLegalBid)}</span>
              <span className="text-[10px] text-slate-400 block mt-0.5 font-sans">Purse - Reserve Needed</span>
            </div>
          </div>
        </div>

        {/* Overseas Quota Status */}
        {player?.is_overseas && (
          <div className="bg-slate-950/70 p-3.5 rounded-2xl border border-white/10 flex items-center justify-between text-xs">
            <span className="text-slate-400 font-medium">✈ Overseas Player Quota:</span>
            <span className={`font-bold font-mono ${math.isOverseasBreach ? 'text-rose-400' : 'text-emerald-400'}`}>
              {math.overseasCount} / {math.maxOverseas} Filled {math.isOverseasBreach ? '❌ (MAX REACHED)' : '✔'}
            </span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="pt-2 flex flex-col sm:flex-row gap-3">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 py-3.5 px-4 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-white font-bold text-sm border border-white/10 transition text-center"
          >
            ← Acknowledge &amp; Re-adjust Price
          </button>

          {onForce && (
            <button
              type="button"
              onClick={() => {
                onClose();
                onForce();
              }}
              className="py-3.5 px-5 rounded-xl bg-gradient-to-r from-rose-600 to-rose-700 hover:from-rose-500 hover:to-rose-600 text-white font-bold text-sm transition text-center shadow-lg shadow-rose-950 flex items-center justify-center gap-2"
            >
              <span>⚡ Admin Force Override</span>
            </button>
          )}
        </div>

      </div>
    </div>
  );
}

function Btn({ children, onClick, tone = 'slate', disabled = false, className = '' }) {
  const tones = {
    slate:   'bg-slate-800/80 text-slate-100 hover:bg-slate-700/80 border border-white/10 shadow-md',
    emerald: 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-500 hover:to-teal-500 shadow-lg shadow-emerald-950/40 border border-emerald-400/30',
    amber:   'bg-gradient-to-r from-amber-600 to-amber-700 text-white hover:from-amber-500 hover:to-amber-600 shadow-lg shadow-amber-950/40 border border-amber-400/30',
    red:     'bg-gradient-to-r from-rose-600 to-rose-700 text-white hover:from-rose-500 hover:to-rose-600 border border-rose-400/30 shadow-lg shadow-rose-950/40',
    indigo:  'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white hover:from-indigo-500 hover:to-cyan-500 shadow-lg shadow-indigo-950/40 border border-indigo-400/30',
    ghost:   'border border-rose-500/40 text-rose-400 hover:bg-rose-500/10 backdrop-blur-md',
  };
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`px-5 py-2.5 rounded-xl font-bold text-sm transition-all duration-200 active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 ${tones[tone]} ${className}`}
    >
      {children}
    </button>
  );
}

export default function AdminPanel() {
  const { state, currentPlayer, startLot, placeBid, markSold, markUnsold, endAuction, nextLot, jumpToLot, reset } = useAuction();
  const { teams, currentBidLakhs, currentBidTeamId, status, currentIndex, auctionOrder, salesMap } = state;

  const [activeTab, setActiveTab]           = useState('auction'); // 'auction' | 'teams' | 'lots'
  const [jumpIndex, setJumpIndex]           = useState('');
  const [overrideTeamId, setOverrideTeamId] = useState('');
  const [overridePrice, setOverridePrice]   = useState('');
  const [busy, setBusy]                     = useState(false);
  const [warningModal, setWarningModal]     = useState(null);
  const [searchQuery, setSearchQuery]       = useState('');

  // Sync manual sale selection whenever lot or live bid updates
  useEffect(() => {
    if (currentBidTeamId) {
      setOverrideTeamId(currentBidTeamId);
    } else if (teams.length > 0 && (!overrideTeamId || !teams.some(t => t.id === overrideTeamId))) {
      setOverrideTeamId(teams[0].id);
    }

    if (currentBidLakhs != null) {
      setOverridePrice(String(currentBidLakhs));
    } else if (currentPlayer?.base_price_lakhs != null) {
      setOverridePrice(String(currentPlayer.base_price_lakhs));
    }
  }, [currentIndex, currentBidTeamId, currentBidLakhs, currentPlayer, teams, overrideTeamId]);

  async function wrap(fn) {
    if (busy) return;
    setBusy(true);
    try { await fn(); }
    catch (e) { alert(`Error: ${e.message}`); }
    finally   { setBusy(false); }
  }

  const nextBid = currentBidLakhs != null
    ? nextBidLakhs(currentBidLakhs)
    : currentPlayer?.base_price_lakhs;

  const selectedTeam = teams.find(t => t.id === overrideTeamId);
  const parsedOverridePrice = Number(overridePrice);
  const isOverridePriceValid = !isNaN(parsedOverridePrice) && parsedOverridePrice > 0;
  const selectedTeamMath = selectedTeam ? computeSquadMath(selectedTeam, parsedOverridePrice, currentPlayer) : null;

  async function handleBid(teamId) {
    const team = teams.find(t => t.id === teamId);
    const amt  = nextBid;
    const math = computeSquadMath(team, amt, currentPlayer);
    
    if (math.hasWarning) {
      setWarningModal({
        team,
        bidLakhs: amt,
        player: currentPlayer,
        math,
        action: 'bid',
        onForce: () => wrap(() => placeBid(teamId, amt)),
      });
      return;
    }
    await wrap(() => placeBid(teamId, amt));
  }

  async function handleDirectSold(force = false) {
    const targetTeamId = overrideTeamId || currentBidTeamId;
    const targetPrice  = isOverridePriceValid ? parsedOverridePrice : (currentBidLakhs ?? currentPlayer?.base_price_lakhs);

    if (!targetTeamId) { alert('Please select a team.'); return; }
    if (!targetPrice || isNaN(targetPrice) || targetPrice <= 0) { alert('Please enter a valid price in Lakhs.'); return; }

    const team = teams.find(t => t.id === targetTeamId);
    if (!team) { alert('Invalid team selected.'); return; }

    const math = computeSquadMath(team, targetPrice, currentPlayer);

    if (!force && math.hasWarning) {
      setWarningModal({
        team,
        bidLakhs: targetPrice,
        player: currentPlayer,
        math,
        action: 'direct_sold',
        onForce: () => wrap(async () => {
          await markSold(targetTeamId, targetPrice);
        }),
      });
      return;
    }

    await wrap(async () => {
      await markSold(targetTeamId, targetPrice);
    });
  }

  async function handleJump(targetIndex) {
    const idx = targetIndex !== undefined ? targetIndex : parseInt(jumpIndex, 10) - 1;
    if (!isNaN(idx) && idx >= 0 && idx < auctionOrder.length) {
      await wrap(() => jumpToLot(idx));
      setJumpIndex('');
    }
  }

  async function handleReset() {
    if (!confirm('Reset the entire auction? This will clear all sales and restore team purses.')) return;
    await wrap(reset);
    setOverrideTeamId('');
    setOverridePrice('');
    setJumpIndex('');
    setSearchQuery('');
  }

  // Calculate global statistics for NeuroBank Top Bar
  const totalPurseAllocated = 12000 * 10; // 120 Cr per team * 10 teams = 1200 Cr = 120,000 Lakhs
  const totalPurseRemaining = teams.reduce((acc, t) => acc + t.purseLakhs, 0);
  const totalSpentLakhs = totalPurseAllocated - totalPurseRemaining;
  const totalPlayersBought = teams.reduce((acc, t) => acc + (t.squad ? t.squad.length : 0), 0);

  if (status === 'finished' || !currentPlayer) {
    return (
      <div className="min-h-screen bg-[#070a12] text-white flex items-center justify-center p-6 relative overflow-hidden">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-amber-500/10 rounded-full blur-[140px] pointer-events-none" />
        
        <div className="nb-card p-10 max-w-lg w-full text-center space-y-6 relative z-10">
          <div className="w-20 h-20 mx-auto rounded-3xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-4xl shadow-xl shadow-amber-950/50">
            🏆
          </div>
          <div>
            <h1 className="text-3xl font-black nb-gradient-amber tracking-tight mb-2">
              Auction Completed
            </h1>
            <p className="text-slate-400 text-sm">All player lots have been processed successfully.</p>
          </div>
          <div className="space-y-3 pt-2">
            <button
              onClick={() => exportRostersJSON(teams)}
              className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm transition shadow-lg border border-indigo-400/30 flex items-center justify-center gap-2"
            >
              <span>📥</span>
              <span>Export Rosters JSON (rank_teams.py)</span>
            </button>
            <button
              onClick={handleReset}
              className="w-full py-3 rounded-2xl bg-slate-800/80 hover:bg-slate-700/80 text-rose-300 font-semibold text-xs transition border border-rose-500/30"
            >
              🔄 Reset &amp; Restart Auction
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen w-screen bg-[#030712] text-slate-100 font-sans flex flex-col md:flex-row relative overflow-hidden">
      
      {/* Cyber Deadly Ambient Background Lights */}
      <div className="absolute top-0 left-64 w-[600px] h-[600px] bg-red-600/15 rounded-full blur-[180px] pointer-events-none animate-pulse" />
      <div className="absolute bottom-0 right-10 w-[600px] h-[600px] bg-purple-600/15 rounded-full blur-[180px] pointer-events-none" />
      <div className="absolute top-1/2 left-1/3 w-[500px] h-[500px] bg-cyan-600/10 rounded-full blur-[180px] pointer-events-none" />

      {/* Squad Math Warning Modal Popup */}
      <SquadMathModal data={warningModal} onClose={() => setWarningModal(null)} />

      {/* ── DEADLY ARENA LEFT SIDEBAR NAVIGATION ───────────────────────────────────── */}
      <aside className="w-full md:w-56 bg-slate-950/90 border-b md:border-b-0 md:border-r border-red-500/20 backdrop-blur-2xl flex flex-col justify-between shrink-0 relative z-20 h-full shadow-[4px_0_30px_rgba(0,0,0,0.8)]">
        <div>
          {/* Brand Header */}
          <div className="p-4 border-b border-white/10 flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-purple-600/20 border border-purple-500/50 flex items-center justify-center p-1 shadow-[0_0_15px_rgba(168,85,247,0.4)]">
              <img src="/logo.png" alt="Logo" className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(168,85,247,0.6)]" />
            </div>
            <div>
              <div className="text-sm font-black text-white tracking-widest leading-none font-mono uppercase">
                3, 2, 1... <span className="nb-gradient-purple">SOLD</span>
              </div>
              <div className="text-[10px] text-slate-400 font-extrabold tracking-widest uppercase mt-1 font-mono">
                COMMAND MATRIX
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="p-3 space-y-1.5">
            <button
              onClick={() => setActiveTab('auction')}
              className={`w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl font-black text-xs uppercase tracking-wider transition-all duration-200 ${
                activeTab === 'auction'
                  ? 'bg-red-950/80 text-red-300 border border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.3)]'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900/60 border border-transparent'
              }`}
            >
              <span className="text-base">📊</span>
              <span>Command Center</span>
            </button>

            <button
              onClick={() => setActiveTab('teams')}
              className={`w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl font-black text-xs uppercase tracking-wider transition-all duration-200 ${
                activeTab === 'teams'
                  ? 'bg-red-950/80 text-red-300 border border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.3)]'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900/60 border border-transparent'
              }`}
            >
              <span className="text-base">💳</span>
              <span>Team Accounts</span>
            </button>

            <button
              onClick={() => setActiveTab('lots')}
              className={`w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl font-black text-xs uppercase tracking-wider transition-all duration-200 ${
                activeTab === 'lots'
                  ? 'bg-red-950/80 text-red-300 border border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.3)]'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900/60 border border-transparent'
              }`}
            >
              <span className="text-base">📋</span>
              <span>Player Catalog</span>
            </button>
          </nav>
        </div>

        {/* Sidebar Footer Stats & System Reset */}
        <div className="p-3 border-t border-slate-800/80 space-y-2">
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-2.5 text-xs space-y-1.5">
            <div className="text-[9px] font-bold uppercase tracking-wider text-slate-400 font-mono px-1">Export Sales &amp; Rosters</div>
            <div className="grid grid-cols-2 gap-1.5">
              <button
                onClick={() => exportRostersJSON(teams)}
                className="py-1.5 px-2 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-500/40 text-indigo-200 font-mono font-bold text-[10px] transition text-center shadow"
              >
                📥 JSON
              </button>
              <button
                onClick={() => exportRostersCSV(teams)}
                className="py-1.5 px-2 rounded-lg bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-500/40 text-emerald-200 font-mono font-bold text-[10px] transition text-center shadow"
              >
                📊 CSV
              </button>
            </div>
          </div>

          <Btn tone="ghost" onClick={handleReset} disabled={busy} className="w-full !py-2 !text-[11px] font-semibold">
            ⚠ Reset Auction
          </Btn>
        </div>
      </aside>

      {/* ── MAIN DASHBOARD AREA ─────────────────────────────────────────────────── */}
      <main className="flex-1 flex flex-col min-w-0 h-full overflow-hidden relative z-10">
        
        {/* Top Header Bar */}
        <header className="px-4 py-2.5 border-b border-slate-800/80 bg-slate-950/60 backdrop-blur-xl flex flex-col md:flex-row md:items-center justify-between gap-3 shrink-0 z-20">
          
          {/* Search Lot Bar */}
          <div className="relative flex-1 max-w-md">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs">🔍</span>
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search player lot or team ID..."
              className="w-full bg-slate-900/80 border border-white/10 rounded-xl pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition font-medium"
            />
          </div>

          {/* Quick Metrics Bar */}
          <div className="flex items-center gap-5 text-xs">
            <div className="text-right">
              <div className="text-[9px] text-slate-400 uppercase font-semibold">Lot Progress</div>
              <div className="text-xs font-black text-white font-mono">Lot {currentIndex + 1} / {auctionOrder.length}</div>
            </div>

            <div className="h-6 w-px bg-slate-800" />

            <div className="text-right">
              <div className="text-[9px] text-slate-400 uppercase font-semibold">Total Spent</div>
              <div className="text-xs font-black text-amber-400 font-mono">{fmt(totalSpentLakhs)}</div>
            </div>

            <div className="h-6 w-px bg-slate-800" />

            <div className="text-right">
              <div className="text-[9px] text-slate-400 uppercase font-semibold">Players Sold</div>
              <div className="text-xs font-black text-emerald-400 font-mono">{totalPlayersBought}</div>
            </div>

            <span className={`ml-1 px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider border backdrop-blur-md ${
              status === 'finished' ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40' :
              status === 'live' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 animate-pulse' :
              status === 'sold' ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' :
              status === 'unsold' ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' :
              'bg-slate-800/80 text-slate-300 border-white/10'
            }`}>
              {status}
            </span>

            <button
              onClick={() => {
                if (window.confirm('End auction now? This will set status to finished across all screens (Admin, TV, Leaderboards) and export rosters.json for Python evaluation.')) {
                  wrap(async () => {
                    await endAuction();
                    exportRostersJSON(teams);
                  });
                }
              }}
              disabled={busy || status === 'finished'}
              className="py-1 px-3 rounded-lg bg-gradient-to-r from-purple-900 to-indigo-900 hover:from-purple-800 hover:to-indigo-800 border border-purple-500/50 text-purple-200 font-bold text-xs shadow transition active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5"
            >
              <span>🏁</span>
              <span>End Auction</span>
            </button>
          </div>
        </header>

        {/* Content Body */}
        <div className="flex-1 p-3 md:p-4 overflow-y-auto lg:overflow-hidden min-h-0">

          {/* TAB 1: LIVE AUCTION COMMAND CENTER (2-COLUMN HIGH DENSITY NO-SCROLL LAYOUT) */}
          {activeTab === 'auction' && (
            <div className="h-full grid grid-cols-1 lg:grid-cols-12 gap-3.5 items-stretch overflow-y-auto lg:overflow-hidden">
              
              {/* LEFT COLUMN: Player Hero Card + Actions + Live Bidding Grid */}
              <div className="lg:col-span-6 flex flex-col space-y-3 min-h-0">
                
                {/* CURRENT PLAYER HERO CARD */}
                <div className="nb-card p-4 space-y-3 relative overflow-hidden shrink-0">
                  <div className="flex justify-between items-start gap-3">
                    <div className="space-y-1.5 min-w-0">
                      <div className="flex flex-wrap items-center gap-1.5 text-[11px] font-semibold">
                        <span className="nb-pill text-cyan-300 border-cyan-500/30 bg-cyan-950/60 py-0.5 px-2">
                          Pool {currentPlayer.pool} — {currentPlayer.pool_name}
                        </span>
                        {currentIndex >= state.players.length && (
                          <span className="nb-pill text-amber-300 border-amber-500/40 bg-amber-500/20 py-0.5 px-2 font-bold animate-pulse">
                            🔁 UNSOLD RE-LIST
                          </span>
                        )}
                        {currentPlayer.is_rookie && <span className="nb-pill text-amber-300 border-amber-500/40 bg-amber-500/20 py-0.5 px-2">Uncapped</span>}
                        {currentPlayer.is_overseas && <span className="nb-pill text-emerald-300 border-emerald-500/40 bg-emerald-500/20 py-0.5 px-2">✈ Overseas</span>}
                      </div>

                      <h2 className="text-2xl font-black text-white tracking-tight truncate">{currentPlayer.name}</h2>
                      <p className="text-slate-300 text-xs truncate">
                        {currentPlayer.role} · {currentPlayer.style} · {currentPlayer.nationality} · Age {currentPlayer.age}
                        {currentPlayer.performance_rating != null && ` · ⭐ ${currentPlayer.performance_rating}`}
                      </p>
                    </div>

                    {/* Current Bid / Sold price badge */}
                    <div className="bg-slate-950/80 border border-white/10 p-2.5 rounded-xl text-right shrink-0 min-w-[130px]">
                      <div className="text-[10px] text-slate-400 uppercase font-semibold">
                        {status === 'sold' ? 'Sold Price' : 'Current Bid'}
                      </div>
                      <div className="text-xl font-black text-amber-400 font-mono">
                        {fmt(currentBidLakhs ?? currentPlayer.base_price_lakhs)}
                      </div>
                      <div className="text-[10px] text-slate-400">Base: {currentPlayer.base_price_label}</div>
                    </div>
                  </div>

                  {/* Lot Phase Action Controls */}
                  <div className="pt-2 border-t border-white/10 flex flex-wrap gap-2 items-center">
                    {currentBidTeamId && (
                      <Btn tone="amber" onClick={() => handleDirectSold(false)} disabled={busy} className="!py-2 !px-4 !text-xs">
                        🔨 Mark SOLD ({currentBidTeamId} @ {fmt(currentBidLakhs)})
                      </Btn>
                    )}

                    {status !== 'finished' && (
                      <Btn tone="red" onClick={() => wrap(async () => { await markUnsold(); await nextLot(); })} disabled={busy} className="!py-2 !px-4 !text-xs">
                        ✖ Mark UNSOLD
                      </Btn>
                    )}

                    {currentIndex > 0 && (
                      <Btn tone="slate" onClick={() => handleJump(currentIndex - 1)} disabled={busy} className="!py-2 !px-3 !text-xs">
                        ← Prev Lot
                      </Btn>
                    )}
                    <Btn tone="indigo" onClick={() => wrap(nextLot)} disabled={busy} className="!py-2 !px-4 !text-xs">
                      Skip / Next Lot →
                    </Btn>
                    <Btn
                      tone="ghost"
                      onClick={() => {
                        if (window.confirm('End auction now? This will set status to finished across all screens (Admin, TV, Leaderboards) and export rosters.json.')) {
                          wrap(async () => {
                            await endAuction();
                            exportRostersJSON(teams);
                          });
                        }
                      }}
                      disabled={busy || status === 'finished'}
                      className="!py-2 !px-3 !text-xs border-purple-500/50 text-purple-300 hover:bg-purple-950/50"
                    >
                      🏁 End &amp; Export Rosters
                    </Btn>
                  </div>
                </div>

                {/* LIVE INCREMENTAL BIDDING GRID */}
                <div className="nb-card p-3.5 space-y-2 flex-1 flex flex-col justify-center min-h-0">
                  <div className="flex justify-between items-center shrink-0">
                    <h3 className="text-[11px] font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                      <span>Tap Team to Bid —</span>
                      <span className="text-amber-400 font-mono font-black text-sm">{fmt(nextBid)}</span>
                    </h3>
                    <span className="text-[10px] text-slate-500 font-mono">Increments Auto-Calculated</span>
                  </div>

                  <div className="grid grid-cols-5 gap-2 flex-1 items-stretch min-h-[140px]">
                    {teams.map(t => {
                      const math    = computeSquadMath(t, nextBid, currentPlayer);
                      const leading = t.id === currentBidTeamId;
                      return (
                        <button
                          key={t.id}
                          disabled={leading || busy || status === 'finished'}
                          onClick={() => handleBid(t.id)}
                          title={math.hasWarning ? math.primaryReason : leading ? 'Currently leading bid' : `Place bid for ${fmt(nextBid)}`}
                          className={`rounded-xl border p-2 text-left transition-all flex flex-col justify-between ${
                            leading
                              ? 'border-amber-400 bg-amber-950/50 ring-1 ring-amber-400/50 shadow-md'
                              : !math.hasWarning && status !== 'finished'
                                ? 'border-white/10 bg-slate-950/80 hover:border-white/20 hover:bg-slate-900 cursor-pointer'
                                : 'border-rose-500/40 bg-rose-950/30 opacity-70'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-black text-xs" style={{ color: t.color }}>{t.id}</span>
                            {leading ? (
                              <span className="text-[9px] bg-amber-400 text-slate-950 font-bold px-1 rounded">LEAD</span>
                            ) : math.hasWarning ? (
                              <span className="text-[9px] text-rose-400 font-bold">⚠️</span>
                            ) : null}
                          </div>
                          <div className="text-[11px] font-mono font-bold text-slate-200 mt-1">{fmt(t.purseLakhs)}</div>
                          <div className="text-[9px] text-slate-500 truncate">{t.squad.length} players</div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* RIGHT COLUMN: Direct Sale & Manual Price Override Panel */}
              <div className="lg:col-span-6 flex flex-col space-y-3 min-h-0">
                <div className="nb-card p-4 space-y-3 border-2 border-cyan-500/30 bg-gradient-to-br from-slate-900/90 via-slate-900/80 to-blue-950/40 relative overflow-hidden flex-1 flex flex-col justify-between min-h-0">
                  
                  <div className="flex items-center justify-between border-b border-white/10 pb-2 shrink-0">
                    <div>
                      <h3 className="text-xs font-black text-white flex items-center gap-1.5">
                        <span>🎯 Direct Sale &amp; Manual Price Override</span>
                      </h3>
                      <p className="text-slate-400 text-[10px]">
                        Select team and enter final sold price in Lakhs (e.g. 200 = ₹2.00 Cr).
                      </p>
                    </div>

                    {selectedTeamMath && (
                      <button
                        type="button"
                        onClick={() => setWarningModal({ team: selectedTeam, bidLakhs: parsedOverridePrice, player: currentPlayer, math: selectedTeamMath, action: 'direct_sold', onForce: () => wrap(() => markSold(overrideTeamId, parsedOverridePrice)) })}
                        className={`px-2.5 py-1 rounded-lg text-[10px] font-bold border transition ${
                          selectedTeamMath.hasWarning
                            ? 'bg-rose-500/20 text-rose-300 border-rose-500/40 animate-pulse'
                            : 'bg-slate-800/80 text-slate-300 border-white/10'
                        }`}
                      >
                        {selectedTeamMath.hasWarning ? '🚨 Warning Math' : '🧮 Squad Math'}
                      </button>
                    )}
                  </div>

                  {/* Warning Banner */}
                  {selectedTeamMath && selectedTeamMath.hasWarning && (
                    <div className="bg-rose-950/60 border border-rose-500/50 p-2 rounded-xl flex items-center justify-between text-[10px] text-rose-200 shrink-0">
                      <div className="truncate pr-2">
                        <span className="font-bold text-rose-300">⚠️ Risk: </span>
                        {selectedTeamMath.primaryReason}
                      </div>
                      <button
                        type="button"
                        onClick={() => setWarningModal({ team: selectedTeam, bidLakhs: parsedOverridePrice, player: currentPlayer, math: selectedTeamMath, action: 'direct_sold', onForce: () => wrap(() => markSold(overrideTeamId, parsedOverridePrice)) })}
                        className="px-2 py-0.5 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded shrink-0 text-[9px]"
                      >
                        Inspect 🧮
                      </button>
                    </div>
                  )}

                  {/* Team selection 5x2 grid */}
                  <div className="space-y-1 shrink-0">
                    <label className="block text-[10px] font-bold text-slate-300 uppercase tracking-wider">
                      1. Select Winning Team
                    </label>
                    <div className="grid grid-cols-5 gap-1.5">
                      {teams.map(t => {
                        const isSelected = t.id === overrideTeamId;
                        const tMath = computeSquadMath(t, parsedOverridePrice || 0, currentPlayer);
                        return (
                          <button
                            key={t.id}
                            type="button"
                            onClick={() => setOverrideTeamId(t.id)}
                            className={`p-1.5 rounded-xl border text-left transition-all ${
                              isSelected
                                ? 'border-cyan-400 bg-cyan-950/80 ring-1 ring-cyan-500/50 shadow-md'
                                : 'border-white/10 bg-slate-950/60 hover:bg-slate-900/60'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-black text-xs" style={{ color: t.color }}>{t.id}</span>
                              {tMath?.hasWarning && <span className="text-rose-400 text-[10px]">⚠️</span>}
                            </div>
                            <div className="text-[10px] text-slate-300 font-mono mt-0.5 truncate">{fmt(t.purseLakhs)}</div>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Price input + presets */}
                  <div className="space-y-1.5 shrink-0">
                    <div className="grid grid-cols-12 gap-2 items-center">
                      <div className="col-span-6 space-y-1">
                        <label className="block text-[10px] font-bold text-slate-300 uppercase tracking-wider">
                          2. Price (Lakhs)
                        </label>
                        <div className="relative flex items-center">
                          <input
                            type="number"
                            step="5"
                            min="20"
                            value={overridePrice}
                            onChange={e => setOverridePrice(e.target.value)}
                            placeholder="e.g. 200"
                            className="w-full bg-slate-950/90 border border-cyan-500/50 rounded-xl px-3 py-1.5 text-sm font-mono font-bold text-white focus:outline-none focus:border-cyan-400"
                          />
                          <span className="absolute right-2 font-bold text-amber-400 text-xs font-mono pointer-events-none">
                            {isOverridePriceValid ? fmt(parsedOverridePrice) : 'Invalid'}
                          </span>
                        </div>
                      </div>

                      <div className="col-span-6 space-y-1">
                        <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                          Presets
                        </label>
                        <div className="flex flex-wrap gap-1">
                          <button
                            type="button"
                            onClick={() => setOverridePrice(String(currentPlayer.base_price_lakhs))}
                            className="px-2 py-1 rounded bg-slate-800 text-[10px] font-semibold text-slate-200 border border-white/10"
                          >
                            Base
                          </button>
                          <button
                            type="button"
                            onClick={() => setOverridePrice(prev => String((Number(prev) || 0) + 25))}
                            className="px-2 py-1 rounded bg-slate-800 text-[10px] font-semibold text-cyan-300 border border-white/10"
                          >
                            +25L
                          </button>
                          <button
                            type="button"
                            onClick={() => setOverridePrice(prev => String((Number(prev) || 0) + 50))}
                            className="px-2 py-1 rounded bg-slate-800 text-[10px] font-semibold text-cyan-300 border border-white/10"
                          >
                            +50L
                          </button>
                          <button
                            type="button"
                            onClick={() => setOverridePrice(prev => String((Number(prev) || 0) + 100))}
                            className="px-2 py-1 rounded bg-slate-800 text-[10px] font-semibold text-amber-300 border border-white/10"
                          >
                            +1Cr
                          </button>
                          <button
                            type="button"
                            onClick={() => setOverridePrice(prev => String((Number(prev) || 0) + 500))}
                            className="px-2 py-1 rounded bg-slate-800 text-[10px] font-semibold text-emerald-300 border border-white/10"
                          >
                            +5Cr
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Confirm Direct Sale Button */}
                  <div className="pt-1 shrink-0">
                    <button
                      type="button"
                      onClick={() => handleDirectSold(false)}
                      disabled={busy || !overrideTeamId || !isOverridePriceValid}
                      className={`w-full py-2.5 rounded-xl text-white font-extrabold text-xs tracking-wide transition shadow-md disabled:opacity-40 flex items-center justify-center gap-2 border border-white/20 ${
                        selectedTeamMath?.hasWarning
                          ? 'bg-gradient-to-r from-amber-600 via-rose-600 to-rose-700 hover:from-amber-500 hover:to-rose-600'
                          : 'bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-500 hover:from-emerald-500 hover:to-teal-500'
                      }`}
                    >
                      <span>
                        {selectedTeamMath?.hasWarning
                          ? '⚠️ Confirm Sale (Review Squad Warning Math)'
                          : `✔ Confirm Direct Sale to ${selectedTeam ? selectedTeam.name : 'Selected Team'} for ${isOverridePriceValid ? fmt(parsedOverridePrice) : 'Entered Price'}`}
                      </span>
                    </button>
                  </div>
                </div>
              </div>

            </div>
          )}

          {/* TAB 2: TEAM PURSES & ACCOUNTS (NEUROBANK FINTECH CARDS) */}
          {activeTab === 'teams' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-black text-white tracking-tight">Team Financial Accounts &amp; Squad Roster</h2>
                  <p className="text-xs text-slate-400 mt-0.5">Real-time purse balance, reserve headroom, and player slots across all 10 franchises.</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {teams.map(team => {
                  const purseMax = 12000; // 120 Cr
                  const spent = purseMax - team.purseLakhs;
                  const spentPct = ((spent / purseMax) * 100).toFixed(1);
                  const squadCount = team.squad ? team.squad.length : 0;
                  const overseasCount = team.squad ? team.squad.filter(p => p.is_overseas).length : 0;
                  const math = computeSquadMath(team, 0, currentPlayer);

                  return (
                    <div
                      key={team.id}
                      className="nb-card p-6 border border-white/10 relative overflow-hidden group hover:border-cyan-500/40 transition-all duration-300"
                    >
                      {/* Ambient color light */}
                      <div className="absolute top-0 right-0 w-32 h-32 rounded-full blur-3xl pointer-events-none opacity-20" style={{ background: team.color }} />

                      <div className="flex items-start justify-between border-b border-white/10 pb-4 mb-4">
                        <div className="flex items-center gap-3">
                          <div
                            className="w-12 h-12 rounded-2xl flex items-center justify-center font-black text-xl border border-white/20 shadow-md font-mono"
                            style={{ background: `${team.color}22`, color: team.color }}
                          >
                            {team.id}
                          </div>
                          <div>
                            <h3 className="text-lg font-black text-white">{team.name}</h3>
                            <span className="text-xs text-slate-400 font-mono">Purse Allocated: ₹120.00 Cr</span>
                          </div>
                        </div>
                        <div className="text-right font-mono">
                          <div className="text-xs text-slate-400 uppercase font-semibold">Remaining Purse</div>
                          <div className="text-xl font-black" style={{ color: team.color }}>{fmt(team.purseLakhs)}</div>
                        </div>
                      </div>

                      {/* Purse Spend Bar */}
                      <div className="space-y-1.5 mb-5">
                        <div className="flex justify-between text-xs text-slate-400">
                          <span>Budget Spent: {spentPct}%</span>
                          <span>{fmt(spent)} / ₹120.00 Cr</span>
                        </div>
                        <div className="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden border border-white/10">
                          <div
                            className="h-full rounded-full transition-all duration-500"
                            style={{ width: `${spentPct}%`, background: team.color }}
                          />
                        </div>
                      </div>

                      {/* Stats Grid */}
                      <div className="grid grid-cols-3 gap-3 font-mono text-xs mb-4">
                        <div className="bg-slate-950/60 p-3 rounded-xl border border-white/10">
                          <span className="text-[10px] text-slate-500 block font-sans uppercase">Squad Size</span>
                          <span className="font-bold text-slate-200">{squadCount} / 25</span>
                          <span className="text-[10px] text-slate-400 block font-sans">Min: {SQUAD_RULES.MIN_SQUAD_SIZE}</span>
                        </div>
                        <div className="bg-slate-950/60 p-3 rounded-xl border border-white/10">
                          <span className="text-[10px] text-slate-500 block font-sans uppercase">Overseas</span>
                          <span className="font-bold text-emerald-400">{overseasCount} / 8</span>
                          <span className="text-[10px] text-slate-400 block font-sans">Max allowed</span>
                        </div>
                        <div className="bg-slate-950/60 p-3 rounded-xl border border-white/10">
                          <span className="text-[10px] text-slate-500 block font-sans uppercase">Max Legal Bid</span>
                          <span className="font-bold text-amber-400">{fmt(math?.maxLegalBid)}</span>
                          <span className="text-[10px] text-slate-400 block font-sans">Reserve set</span>
                        </div>
                      </div>

                      {/* Squad Players Preview */}
                      {squadCount > 0 ? (
                        <div className="space-y-2">
                          <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Bought Players ({squadCount})</div>
                          <div className="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto pr-1">
                            {team.squad.map(p => (
                              <span
                                key={p.id}
                                className="px-2.5 py-1 rounded-lg text-xs font-semibold border bg-slate-950/80 border-white/10 text-slate-200 flex items-center gap-1.5"
                              >
                                <span>{p.name}</span>
                                <span className="font-mono text-amber-300">{fmt(p.sold_price_lakhs)}</span>
                              </span>
                            ))}
                          </div>
                        </div>
                      ) : (
                        <div className="text-xs text-slate-500 italic text-center py-2 border border-dashed border-white/10 rounded-xl">
                          No players bought yet.
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 3: PLAYER ORDER & CATALOG */}
          {activeTab === 'lots' && (
            <div className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-black text-white tracking-tight">Full Player Catalog &amp; Auction Order</h2>
                  <p className="text-xs text-slate-400 mt-0.5">Jump to any lot or view pool sets.</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Jump to Lot #</span>
                  <input
                    type="number"
                    min="1"
                    max={auctionOrder.length}
                    value={jumpIndex}
                    onChange={e => setJumpIndex(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleJump()}
                    className="w-24 bg-slate-900 border border-white/10 rounded-xl px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-cyan-500"
                    placeholder={`1-${auctionOrder.length}`}
                  />
                  <Btn tone="slate" onClick={() => handleJump()} disabled={busy} className="!px-4 !py-1.5 !text-xs">
                    Go
                  </Btn>
                </div>
              </div>

              <div className="nb-card p-6 space-y-3">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                  {auctionOrder.map((player, idx) => {
                    const isCurrent = idx === currentIndex;
                    const matchesSearch = !searchQuery || player.name.toLowerCase().includes(searchQuery.toLowerCase()) || String(idx + 1) === searchQuery;

                    if (!matchesSearch) return null;

                    return (
                      <div
                        key={player.id}
                        onClick={() => handleJump(idx)}
                        className={`p-4 rounded-2xl border transition-all cursor-pointer flex items-center justify-between gap-3 ${
                          isCurrent
                            ? 'border-cyan-400 bg-cyan-950/50 ring-2 ring-cyan-500/40 shadow-lg'
                            : 'border-white/10 bg-slate-950/60 hover:bg-slate-900/60 hover:border-white/20'
                        }`}
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <span className={`w-8 h-8 rounded-xl font-mono text-xs font-black flex items-center justify-center shrink-0 ${
                            isCurrent ? 'bg-cyan-500 text-slate-950' : 'bg-slate-900 text-slate-400 border border-white/10'
                          }`}>
                            #{idx + 1}
                          </span>
                          <div className="min-w-0">
                            <div className="text-sm font-bold text-white truncate">{player.name}</div>
                            <div className="text-[10px] text-slate-400 truncate">Pool {player.pool} · {player.role}</div>
                          </div>
                        </div>

                        <div className="text-right shrink-0">
                          <span className="text-xs font-mono font-bold text-amber-300">{player.base_price_label}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

        </div>
      </main>

    </div>
  );
}

```

## File: src/components/ResultsPanel.jsx

```javascript
import React, { useState } from 'react';
import { useAuction } from '../state/AuctionStore';
import { rankTeams }  from '../lib/scoringEngine';
import { exportRostersJSON, exportRostersCSV } from '../lib/exportUtils';

function fmt(l) {
  if (l == null) return '—';
  if (l >= 100)  return `₹${(l / 100).toFixed(2)} Cr`;
  return `₹${l}L`;
}

function ScoreBar({ value, max, color }) {
  return (
    <div className="relative h-2 w-full rounded-full bg-slate-700 overflow-hidden">
      <div className="absolute inset-y-0 left-0 rounded-full transition-all duration-700" style={{ width: `${Math.min(100,(value/max)*100)}%`, background: color }} />
    </div>
  );
}

function RankBadge({ rank }) {
  const m = { 1:'🥇', 2:'🥈', 3:'🥉' };
  if (m[rank]) return <span className="text-2xl">{m[rank]}</span>;
  return <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-slate-700 text-slate-300 font-bold text-sm">{rank}</span>;
}

function SquadDrawer({ team }) {
  const grouped = {};
  for (const p of team.squad) { grouped[p.role] = grouped[p.role] || []; grouped[p.role].push(p); }
  const order = ['Batsman','Wicket-Keeper','All-Rounder','Pacer','Spinner'];
  return (
    <div className="mt-4 border-t border-slate-700 pt-4 space-y-3">
      {order.map(role => !grouped[role] ? null : (
        <div key={role}>
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">{role}</div>
          <div className="flex flex-wrap gap-2">
            {grouped[role].map(p => (
              <span key={p.id} className="px-2 py-1 rounded text-xs border" style={{ borderColor: team.color+'66', color: team.color, background: team.color+'11' }}>
                {p.name}{p.is_rookie && <span className="ml-1 opacity-60">(R)</span>} — {fmt(p.sold_price_lakhs)}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ResultsPanel() {
  const { state } = useAuction();
  const [expanded, setExpanded] = useState(null);
  const ranked  = rankTeams(state.teams);
  const winner  = ranked[0];

  return (
    <div className="min-h-screen bg-[#08091a] text-white p-6 md:p-12 relative overflow-hidden select-none">
      {/* JNAA Cascade ambient glow spots */}
      <div className="absolute top-0 right-1/4 w-[600px] h-[600px] bg-purple-600/20 rounded-full blur-[180px] pointer-events-none animate-pulse" />
      <div className="absolute bottom-0 left-1/4 w-[600px] h-[600px] bg-indigo-600/20 rounded-full blur-[180px] pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-violet-600/10 rounded-full blur-[200px] pointer-events-none" />

      <div className="max-w-4xl mx-auto relative z-10">
        <div className="text-center mb-10 flex flex-col items-center">
          <div className="w-24 h-24 mb-4 flex items-center justify-center p-2 rounded-2xl bg-white/5 border border-purple-500/30 backdrop-blur-xl shadow-[0_0_30px_rgba(168,85,247,0.3)]">
            <img src="/logo.png" alt="Logo" className="w-full h-full object-contain filter drop-shadow-[0_0_10px_rgba(168,85,247,0.5)]" />
          </div>
          <p className="text-purple-400 font-mono font-extrabold uppercase tracking-widest text-xs mb-2 shadow-[0_0_10px_rgba(168,85,247,0.5)]">
            AUCTION TERMINATED // FINAL AUDIT
          </p>
          <h1 className="text-5xl font-black mb-3 font-mono tracking-tight text-white">
            3, 2, 1... <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400">SOLD</span>
          </h1>
          <p className="text-slate-400 font-mono text-xs mb-4">
            COMPUTED MATRIX (100 PTS MAX) · EFFICIENCY (50) + BALANCE (30) + EXPERIENCE (20)
          </p>
          <div className="flex items-center gap-3">
            <button
              onClick={() => exportRostersJSON(state.teams)}
              className="px-4 py-2 rounded-xl bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/50 text-indigo-300 font-mono font-bold text-xs transition flex items-center gap-2 shadow-lg"
            >
              <span>📥 Export Final Roster (JSON)</span>
            </button>
            <button
              onClick={() => exportRostersCSV(state.teams)}
              className="px-4 py-2 rounded-xl bg-emerald-600/30 hover:bg-emerald-600/50 border border-emerald-500/50 text-emerald-300 font-mono font-bold text-xs transition flex items-center gap-2 shadow-lg"
            >
              <span>📊 Export Final Roster (CSV)</span>
            </button>
          </div>
        </div>

        {winner && (
          <div className="rounded-2xl border p-6 mb-8 flex items-center gap-6 backdrop-blur-xl relative overflow-hidden shadow-[0_0_40px_rgba(239,68,68,0.25)]" style={{ borderColor: winner.teamColor, background:`linear-gradient(135deg, ${winner.teamColor}25, rgba(3,7,18,0.9))` }}>
            <div className="absolute inset-0 bg-red-500/5 blur-xl pointer-events-none" />
            <div className="text-6xl filter drop-shadow-[0_0_15px_rgba(255,215,0,0.6)]">🏆</div>
            <div className="flex-1 z-10">
              <div className="text-amber-400 text-xs font-mono font-black uppercase tracking-widest">VICTORIOUS FRANCHISE</div>
              <div className="text-3xl font-black font-mono" style={{ color: winner.teamColor }}>{winner.teamName}</div>
              <div className="text-slate-300 text-xs font-mono mt-1">{winner.squadSize} players · {fmt(winner.purseRemaining)} remaining · avg ⭐ {winner.avgRating}</div>
            </div>
            <div className="text-right z-10">
              <div className="text-6xl font-black font-mono drop-shadow-[0_0_15px_rgba(239,68,68,0.5)]" style={{ color: winner.teamColor }}>{winner.total}</div>
              <div className="text-slate-400 text-xs font-mono">/ 100 PTS</div>
            </div>
          </div>
        )}

        <div className="space-y-4">
          {ranked.map(team => {
            const isOpen   = expanded === team.teamId;
            const srcTeam  = state.teams.find(t => t.id === team.teamId);
            return (
              <div key={team.teamId} className="rounded-xl border border-red-500/20 bg-slate-950/80 backdrop-blur-xl overflow-hidden shadow-lg transition-all duration-300 hover:border-red-500/40">
                <button className="w-full text-left p-5 flex items-center gap-4" onClick={() => setExpanded(isOpen ? null : team.teamId)}>
                  <RankBadge rank={team.rank} />
                  <div className="flex-1 min-w-0">
                    <div className="font-black text-xl font-mono" style={{ color: team.teamColor }}>{team.teamName}</div>
                    <div className="text-slate-400 font-mono text-xs mt-0.5">{team.squadSize} players · {fmt(team.purseRemaining)} remaining · avg ⭐ {team.avgRating}</div>
                    <div className="mt-3 space-y-1.5">
                      {[['Efficiency', team.efficiency, 50],['Balance', team.balance, 30],['Experience', team.experience, 20]].map(([label, val, max]) => (
                        <div key={label} className="flex items-center gap-2 text-xs font-mono text-slate-300">
                          <span className="w-24 font-bold">{label}</span>
                          <ScoreBar value={val} max={max} color={team.teamColor} />
                          <span className="w-12 text-right font-mono font-bold">{val}/{max}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="text-right shrink-0 font-mono">
                    <div className="text-3xl font-black" style={{ color: team.teamColor }}>{team.total}</div>
                    <div className="text-slate-400 text-xs">/ 100</div>
                  </div>
                  <div className={`text-slate-400 transition-transform ${isOpen ? 'rotate-180 text-cyan-400' : ''}`}>▾</div>
                </button>
                {isOpen && srcTeam && (
                  <div className="px-5 pb-5 border-t border-slate-800/80 bg-slate-900/40">
                    <SquadDrawer team={{ ...srcTeam, color: team.teamColor }} />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <p className="text-center text-slate-500 font-mono text-xs mt-10">
          SYSTEM MATRIX TIEBREAKERS: TOTAL POINTS → REMAINING PURSE → AVG PERFORMANCE RATING
        </p>
      </div>
    </div>
  );
}

```

## File: supabase/schema.sql

```sql
-- =============================================================================
-- Mock IPL Auction — Supabase Schema
-- Run this entire file once in your Supabase SQL Editor
-- =============================================================================

-- 1. auction_state (single row, id = 1)
CREATE TABLE IF NOT EXISTS auction_state (
  id                  INTEGER PRIMARY KEY DEFAULT 1,
  current_index       INTEGER     NOT NULL DEFAULT 0,
  current_bid_lakhs   NUMERIC,
  current_bid_team_id TEXT,
  status              TEXT        NOT NULL DEFAULT 'idle',
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (id = 1)                        -- enforce single-row contract
);

-- Seed the single control row
INSERT INTO auction_state (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

-- 2. team_purses
CREATE TABLE IF NOT EXISTS team_purses (
  team_id     TEXT    PRIMARY KEY,
  purse_lakhs NUMERIC NOT NULL
);

-- Seed initial purses (120 Cr each = 12 000 L)
INSERT INTO team_purses (team_id, purse_lakhs) VALUES
  ('MI',   12000),
  ('CSK',  12000),
  ('RCB',  12000),
  ('KKR',  12000),
  ('DC',   12000),
  ('PBKS', 12000),
  ('RR',   12000),
  ('SRH',  12000),
  ('LSG',  12000),
  ('GT',   12000)
ON CONFLICT (team_id) DO NOTHING;

-- 3. player_sales
CREATE TABLE IF NOT EXISTS player_sales (
  player_id         TEXT    PRIMARY KEY,
  team_id           TEXT    NOT NULL,
  sold_price_lakhs  NUMERIC NOT NULL,
  created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- 4. bid_log (audit trail)
CREATE TABLE IF NOT EXISTS bid_log (
  id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  type         TEXT        NOT NULL,   -- BID | SOLD | UNSOLD
  player_id    TEXT,
  team_id      TEXT,
  price_lakhs  NUMERIC,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================================================
-- Enable Realtime (run in SQL editor — must be superuser)
-- =============================================================================
ALTER PUBLICATION supabase_realtime ADD TABLE auction_state;
ALTER PUBLICATION supabase_realtime ADD TABLE team_purses;
ALTER PUBLICATION supabase_realtime ADD TABLE player_sales;

-- =============================================================================
-- Storage bucket for player slides (public reads & uploads)
-- Execute in Supabase SQL Editor if storage policies are needed:
-- =============================================================================
INSERT INTO storage.buckets (id, name, public) 
VALUES ('player-slides', 'player-slides', true)
ON CONFLICT (id) DO UPDATE SET public = true;

CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'player-slides');
CREATE POLICY "Public Upload" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'player-slides');
CREATE POLICY "Public Update" ON storage.objects FOR UPDATE USING (bucket_id = 'player-slides');

-- =============================================================================
-- Row-Level Security — OPEN policies (app auth is frontend PIN-based)
-- =============================================================================
ALTER TABLE auction_state  DISABLE ROW LEVEL SECURITY;
ALTER TABLE team_purses    DISABLE ROW LEVEL SECURITY;
ALTER TABLE player_sales   DISABLE ROW LEVEL SECURITY;
ALTER TABLE bid_log        DISABLE ROW LEVEL SECURITY;


```

