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
