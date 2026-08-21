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

        {/* Build stamp — compare between Admin and TV to catch a stale deploy */}
        <div className="text-center mb-4 text-[10px] font-mono text-slate-600 tracking-wider">
          BUILD {typeof __BUILD_STAMP__ === 'string' ? __BUILD_STAMP__ : 'dev'}
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
                placeholder={mode === 'display' ? 'Enter PIN' : 'Enter Password'}
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

