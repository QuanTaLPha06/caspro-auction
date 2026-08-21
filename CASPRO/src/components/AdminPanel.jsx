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

function Btn({ children, onClick, tone = 'slate', disabled = false, loading = false, className = '' }) {
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
      disabled={disabled || loading}
      className={`px-5 py-2.5 rounded-xl font-bold text-sm transition-all duration-200 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 ${tones[tone]} ${className}`}
    >
      {loading ? (
        <>
          <svg className="animate-spin h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Processing...</span>
        </>
      ) : (
        children
      )}
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
  const [banner, setBanner]                 = useState(null); // { type: 'error' | 'success', message: string }

  // Sync manual sale selection whenever current lot or live bid values update
  useEffect(() => {
    if (currentBidTeamId) {
      setOverrideTeamId(currentBidTeamId);
    } else if (teams.length > 0) {
      setOverrideTeamId(teams[0].id);
    }

    if (currentBidLakhs != null) {
      setOverridePrice(String(currentBidLakhs));
    } else if (currentPlayer?.base_price_lakhs != null) {
      setOverridePrice(String(currentPlayer.base_price_lakhs));
    }
  }, [currentIndex, currentBidTeamId, currentBidLakhs, currentPlayer?.id]);

  // Helper function to trigger non-blocking UI notifications
  function notify(message, type = 'success') {
    setBanner({ message, type });
    if (type === 'success') {
      setTimeout(() => {
        setBanner(prev => (prev?.message === message ? null : prev));
      }, 5000);
    }
  }

  async function wrap(fn, successMsg = null) {
    if (busy) return;
    setBusy(true);
    try { 
      await fn(); 
      if (successMsg) notify(successMsg, 'success');
    }
    catch (e) { 
      notify(`Error: ${e.message || 'Operation failed'}`, 'error');
    }
    finally { 
      setBusy(false); 
    }
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
        onForce: () => wrap(() => placeBid(teamId, amt), `Bid of ${fmt(amt)} placed for ${teamId}`),
      });
      return;
    }
    await wrap(() => placeBid(teamId, amt), `Bid of ${fmt(amt)} placed for ${teamId}`);
  }

  async function handleDirectSold(force = false) {
    const targetTeamId = overrideTeamId || currentBidTeamId;
    const targetPrice  = isOverridePriceValid ? parsedOverridePrice : (currentBidLakhs ?? currentPlayer?.base_price_lakhs);

    if (!targetTeamId) { notify('Please select a winning team.', 'error'); return; }
    if (!targetPrice || isNaN(targetPrice) || targetPrice <= 0) { notify('Please enter a valid price in Lakhs.', 'error'); return; }

    const team = teams.find(t => t.id === targetTeamId);
    if (!team) { notify('Invalid team selected.', 'error'); return; }

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
          await nextLot();
        }, `FORCE SOLD: ${currentPlayer.name} to ${targetTeamId} for ${fmt(targetPrice)}`),
      });
      return;
    }

    await wrap(async () => {
      await markSold(targetTeamId, targetPrice);
      await nextLot();
    }, `SOLD: ${currentPlayer.name} to ${team.name} (${targetTeamId}) for ${fmt(targetPrice)}`);
  }

  async function handleJump(targetIndex) {
    const idx = targetIndex !== undefined ? targetIndex : parseInt(jumpIndex, 10) - 1;
    if (!isNaN(idx) && idx >= 0 && idx < auctionOrder.length) {
      await wrap(() => jumpToLot(idx), `Jumped to Lot ${idx + 1}`);
      setJumpIndex('');
    }
  }

  async function handleReset() {
    if (!confirm('Reset the entire auction? This will clear all sales and restore team purses.')) return;
    await wrap(reset, 'Auction reset successfully');
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

        {/* SYSTEM NOTIFICATION BANNER */}
        {banner && (
          <div className={`px-4 py-2.5 text-xs font-bold flex items-center justify-between transition-all duration-300 shrink-0 z-20 ${
            banner.type === 'error'
              ? 'bg-rose-950/90 text-rose-200 border-b border-rose-500/40 shadow-lg shadow-rose-950/50'
              : 'bg-emerald-950/90 text-emerald-200 border-b border-emerald-500/40 shadow-lg shadow-emerald-950/50'
          }`}>
            <div className="flex items-center gap-2">
              <span className="text-sm">{banner.type === 'error' ? '🚨' : '✅'}</span>
              <span>{banner.message}</span>
            </div>
            <button onClick={() => setBanner(null)} className="text-slate-400 hover:text-white px-2 py-0.5 rounded hover:bg-white/10 transition">✕</button>
          </div>
        )}

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
                      <Btn tone="amber" onClick={() => handleDirectSold(false)} disabled={busy} loading={busy} className="!py-2 !px-4 !text-xs">
                        🔨 Mark SOLD ({currentBidTeamId} @ {fmt(currentBidLakhs)})
                      </Btn>
                    )}

                    {status !== 'finished' && (
                      <Btn tone="red" onClick={() => wrap(async () => { await markUnsold(); await nextLot(); }, `Marked ${currentPlayer.name} UNSOLD`)} disabled={busy} loading={busy} className="!py-2 !px-4 !text-xs">
                        ✖ Mark UNSOLD
                      </Btn>
                    )}

                    {currentIndex > 0 && (
                      <Btn tone="slate" onClick={() => handleJump(currentIndex - 1)} disabled={busy} loading={busy} className="!py-2 !px-3 !text-xs">
                        ← Prev Lot
                      </Btn>
                    )}
                    <Btn tone="indigo" onClick={() => wrap(nextLot, `Advanced to Lot ${currentIndex + 2}`)} disabled={busy} loading={busy} className="!py-2 !px-4 !text-xs">
                      Skip / Next Lot →
                    </Btn>
                    <Btn
                      tone="ghost"
                      onClick={() => {
                        if (window.confirm('End auction now? This will set status to finished across all screens (Admin, TV, Leaderboards) and export rosters.json.')) {
                          wrap(async () => {
                            await endAuction();
                            exportRostersJSON(teams);
                          }, 'Auction ended successfully');
                        }
                      }}
                      disabled={busy || status === 'finished'}
                      loading={busy}
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
                        onClick={() => setWarningModal({ team: selectedTeam, bidLakhs: parsedOverridePrice, player: currentPlayer, math: selectedTeamMath, action: 'direct_sold', onForce: () => wrap(async () => { await markSold(overrideTeamId, parsedOverridePrice); await nextLot(); }) })}
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
                        onClick={() => setWarningModal({ team: selectedTeam, bidLakhs: parsedOverridePrice, player: currentPlayer, math: selectedTeamMath, action: 'direct_sold', onForce: () => wrap(async () => { await markSold(overrideTeamId, parsedOverridePrice); await nextLot(); }) })}
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
