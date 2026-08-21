-- =============================================================================
-- Enable Supabase Realtime for the auction tables.
--
-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor → New query).
-- It requires a privileged role, which is why these statements are separated
-- out of schema.sql — they are silently skipped when that file is run by a
-- non-superuser, which leaves Admin and TV out of sync.
--
-- Safe to run more than once.
-- =============================================================================

ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS auction_state;
ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS team_purses;
ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS player_sales;
ALTER PUBLICATION supabase_realtime DROP TABLE IF EXISTS bid_log;

ALTER PUBLICATION supabase_realtime ADD TABLE auction_state;
ALTER PUBLICATION supabase_realtime ADD TABLE team_purses;
ALTER PUBLICATION supabase_realtime ADD TABLE player_sales;
ALTER PUBLICATION supabase_realtime ADD TABLE bid_log;

-- Verify: should return all four table names.
SELECT tablename
FROM   pg_publication_tables
WHERE  pubname = 'supabase_realtime'
ORDER  BY tablename;
