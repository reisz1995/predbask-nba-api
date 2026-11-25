-- ============================================================
-- MIGRACAO: adiciona colunas avancadas as tabelas existentes
-- (OffRtg, DefRtg, NetRtg, AST%, PIE, POSS, etc)
-- Execute no Supabase SQL Editor (SQL Editor > New Query > Run)
-- ============================================================

-- 1. team_stats
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS off_rtg FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS def_rtg FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS net_rtg FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS ast_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS ast_to FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS ast_ratio FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS oreb_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS dreb_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS reb_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS tov_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS efg_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS ts_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS pie FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS poss FLOAT;

-- 2. player_stats
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS off_rtg FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS def_rtg FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS net_rtg FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS ast_pct FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS ast_to FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS ast_ratio FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS oreb_pct FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS dreb_pct FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS reb_pct FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS tov_pct FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS efg_pct FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS ts_pct FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS pie FLOAT;
ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS poss FLOAT;

-- 3. Confirmar colunas criadas
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_name IN ('team_stats', 'player_stats')
  AND column_name IN ('off_rtg','def_rtg','net_rtg','ast_pct','pie','poss')
ORDER BY table_name, column_name;
