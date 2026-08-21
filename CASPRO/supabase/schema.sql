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
-- NOTE: these must be run by a privileged role (the Supabase SQL Editor works).
-- If they are skipped, the app still syncs via its polling fallback, but the
-- instant (<100ms) push updates will not work.
-- Re-runnable: drop first, then re-add, so this file is safe to run twice.
ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS auction_state;
ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS team_purses;
ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS player_sales;
ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS bid_log;

ALTER PUBLICATION supabase_realtime ADD TABLE auction_state;
ALTER PUBLICATION supabase_realtime ADD TABLE team_purses;
ALTER PUBLICATION supabase_realtime ADD TABLE player_sales;
-- bid_log was missing: AuctionStore subscribes to its INSERTs to requeue
-- unsold players, so without it the TV's lot order drifts from the Admin's.
ALTER PUBLICATION supabase_realtime ADD TABLE bid_log;

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


-- =============================================================================
-- Editable team display names (added later)
-- Team IDs are permanent keys; these two columns are what the UI renders.
-- =============================================================================
ALTER TABLE team_purses ADD COLUMN IF NOT EXISTS team_name  TEXT;
ALTER TABLE team_purses ADD COLUMN IF NOT EXISTS team_short TEXT;
