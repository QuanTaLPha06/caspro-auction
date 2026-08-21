// ---------------------------------------------------------------------------
// constants.js  →  src/lib/constants.js
// ---------------------------------------------------------------------------

// `id` is an internal, permanent key. It is stored on every sale and purse row,
// so it must never change. `name` and `short` are display-only defaults — the
// admin overrides them at runtime (Teams tab) and the values live in the DB so
// Admin and TV always show the same thing.
export const TEAMS = [
  { id: 'MI',   name: 'Team 1',  short: 'T1',  color: '#004BA0', purseLakhs: 12000 },
  { id: 'CSK',  name: 'Team 2',  short: 'T2',  color: '#FFCC00', purseLakhs: 12000 },
  { id: 'RCB',  name: 'Team 3',  short: 'T3',  color: '#EC1C24', purseLakhs: 12000 },
  { id: 'KKR',  name: 'Team 4',  short: 'T4',  color: '#3A225D', purseLakhs: 12000 },
  { id: 'DC',   name: 'Team 5',  short: 'T5',  color: '#17479E', purseLakhs: 12000 },
  { id: 'PBKS', name: 'Team 6',  short: 'T6',  color: '#DD1F2D', purseLakhs: 12000 },
  { id: 'RR',   name: 'Team 7',  short: 'T7',  color: '#254AA5', purseLakhs: 12000 },
  { id: 'SRH',  name: 'Team 8',  short: 'T8',  color: '#F26522', purseLakhs: 12000 },
  { id: 'LSG',  name: 'Team 9',  short: 'T9',  color: '#00B2A9', purseLakhs: 12000 },
  { id: 'GT',   name: 'Team 10', short: 'T10', color: '#1B2133', purseLakhs: 12000 },
];

// Max lengths enforced by the team-name editor.
export const TEAM_NAME_MAX  = 28;
export const TEAM_SHORT_MAX = 4;

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
