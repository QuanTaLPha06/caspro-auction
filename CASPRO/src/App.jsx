// ---------------------------------------------------------------------------
// App.jsx — root router
// src/App.jsx
// ---------------------------------------------------------------------------

import React, { useState, useEffect, useCallback } from 'react';
import { AuctionProvider, useAuction } from './state/AuctionStore';
import LandingGateway from './components/LandingGateway';
import TVDisplay      from './components/TVDisplay';
import AdminPanel     from './components/AdminPanel';
import ResultsPanel   from './components/ResultsPanel';

// Persisted so a refresh — or a TV that reboots mid-auction — does not drop
// back to the login gateway. Wrapped because storage throws in some contexts
// (private windows, blocked site data).
const VIEW_STORAGE_KEY = 'caspro.view';
const VALID_VIEWS = ['display', 'admin'];

function readStoredView() {
  try {
    const stored = window.localStorage.getItem(VIEW_STORAGE_KEY);
    return VALID_VIEWS.includes(stored) ? stored : 'landing';
  } catch {
    return 'landing';
  }
}

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
  const [view, setView] = useState(readStoredView); // 'landing' | 'display' | 'admin'

  useEffect(() => {
    try {
      if (view === 'landing') window.localStorage.removeItem(VIEW_STORAGE_KEY);
      else window.localStorage.setItem(VIEW_STORAGE_KEY, view);
    } catch {
      // Session simply will not persist — the app still works.
    }
  }, [view]);

  const exit = useCallback(() => setView('landing'), []);

  if (view === 'landing') {
    return (
      <AuctionProvider>
        <LandingGateway onEnter={setView} />
      </AuctionProvider>
    );
  }

  return (
    <AuctionProvider>
      <Shell view={view} />
      {/* Discreet sign-out. Sessions persist across refresh, so there has to be
          a deliberate way back to the gateway. */}
      <button
        onClick={exit}
        title="Sign out"
        className="fixed bottom-2 left-2 z-50 px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider
                   bg-slate-900/70 text-slate-500 border border-white/10 backdrop-blur
                   opacity-20 hover:opacity-100 hover:text-white transition-opacity duration-200"
      >
        Sign out
      </button>
    </AuctionProvider>
  );
}
