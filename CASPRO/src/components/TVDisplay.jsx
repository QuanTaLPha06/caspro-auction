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
  if (status === 'sold' && leadingTeam) {
    return (
      <div
        className="text-4xl font-extrabold animate-pulse drop-shadow-[0_0_20px_rgba(255,255,255,0.2)]"
        style={{ color: leadingTeam.color }}
      >
        SOLD to {leadingTeam.name} 🎉
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

// Player slide image — falls back to /player_images/{id}.png/jpg, local /slides/{id}.jpg, then to initials avatar
function PlayerSlide({ player }) {
  const [src, setSrc]         = useState(null);
  const [attempt, setAttempt] = useState('manifest'); // 'manifest' | 'supabase' | 'local' | 'avatar'

  useEffect(() => {
    setAttempt('manifest');
    setSrc(`/player_images/${player.id}.png`);
  }, [player.id]);

  const handleError = () => {
    if (attempt === 'manifest') {
      setAttempt('manifest_jpg');
      setSrc(`/player_images/${player.id}.jpg`);
    } else if (attempt === 'manifest_jpg') {
      setAttempt('supabase');
      setSrc(getSlideUrl(player.id));
    } else if (attempt === 'supabase') {
      setAttempt('local');
      setSrc(`/slides/${player.id}.jpg`);
    } else if (attempt === 'local') {
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
    <div className="relative rounded-3xl overflow-hidden border border-slate-700/60 shadow-2xl group">
      <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent z-10 opacity-60" />
      <img
        src={src}
        alt={player.name}
        onError={handleError}
        className="aspect-[3/4] w-full object-cover object-top rounded-3xl transition-transform duration-700 group-hover:scale-105"
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
          <div className="w-10 h-10 rounded-xl bg-red-600/20 border border-red-500/50 flex items-center justify-center text-red-400 text-lg font-black shadow-[0_0_15px_rgba(239,68,68,0.4)]">
            🔥
          </div>
          <div>
            <div className="text-xl font-black tracking-widest text-white uppercase font-mono drop-shadow-[0_0_10px_rgba(239,68,68,0.5)]">
              DEADLY IPL <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-400 to-red-600">AUCTION 2026</span>
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

