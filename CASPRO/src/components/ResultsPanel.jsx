// src/components/ResultsPanel.jsx
import React, { useState } from 'react';
import { useAuction } from '../state/AuctionStore';
import { rankTeams }  from '../lib/scoringEngine';

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
        <div className="text-center mb-10">
          <p className="text-red-500 font-mono font-extrabold uppercase tracking-widest text-xs mb-2 shadow-[0_0_10px_rgba(239,68,68,0.5)]">
            AUCTION TERMINATED // FINAL AUDIT
          </p>
          <h1 className="text-5xl font-black mb-3 font-mono tracking-tight text-white">
            DEADLY <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-400 to-red-600">STANDINGS</span>
          </h1>
          <p className="text-slate-400 font-mono text-xs">
            COMPUTED MATRIX (100 PTS MAX) · EFFICIENCY (50) + BALANCE (30) + EXPERIENCE (20)
          </p>
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
