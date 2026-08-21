-- =============================================================================
-- Editable team names
--
-- Run this in the Supabase SQL Editor (Dashboard -> SQL Editor -> New query)
-- before using the Teams tab in the Admin panel.
--
-- Team IDs (MI, CSK, ...) are permanent internal keys stored on every sale and
-- purse row — they are deliberately NOT changed here. These two columns hold
-- the display name and short badge the admin edits at runtime.
--
-- Safe to run more than once.
-- =============================================================================

ALTER TABLE team_purses ADD COLUMN IF NOT EXISTS team_name  TEXT;
ALTER TABLE team_purses ADD COLUMN IF NOT EXISTS team_short TEXT;

-- Seed generic defaults for any team that has no name yet.
UPDATE team_purses SET team_name = 'Team 1',  team_short = 'T1'  WHERE team_id = 'MI'   AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 2',  team_short = 'T2'  WHERE team_id = 'CSK'  AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 3',  team_short = 'T3'  WHERE team_id = 'RCB'  AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 4',  team_short = 'T4'  WHERE team_id = 'KKR'  AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 5',  team_short = 'T5'  WHERE team_id = 'DC'   AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 6',  team_short = 'T6'  WHERE team_id = 'PBKS' AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 7',  team_short = 'T7'  WHERE team_id = 'RR'   AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 8',  team_short = 'T8'  WHERE team_id = 'SRH'  AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 9',  team_short = 'T9'  WHERE team_id = 'LSG'  AND team_name IS NULL;
UPDATE team_purses SET team_name = 'Team 10', team_short = 'T10' WHERE team_id = 'GT'   AND team_name IS NULL;

-- Verify
SELECT team_id, team_short, team_name, purse_lakhs FROM team_purses ORDER BY team_id;
