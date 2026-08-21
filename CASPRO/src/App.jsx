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
