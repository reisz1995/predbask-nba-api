-- ============================================================
-- CORRECAO: adiciona as 20 colunas faltantes em team_stats
-- Execute no Supabase SQL Editor (SQL Editor > New Query > Run)
-- ============================================================
-- Diagnostico: a tabela team_stats tem apenas 19 colunas.
-- Faltam: fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct,
--         orb, drb, reb, ast, turnovers, stl, blk, pf, pfd, pts, plus_minus
-- ============================================================

ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS fgm INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS fga INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS fg_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS fg3m INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS fg3a INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS fg3_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS ftm INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS fta INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS ft_pct FLOAT;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS orb INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS drb INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS reb INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS ast INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS turnovers INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS stl INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS blk INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS pf INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS pfd INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS pts INTEGER;
ALTER TABLE team_stats ADD COLUMN IF NOT EXISTS plus_minus INTEGER;

-- Recarrega o schema cache do PostgREST apos o ALTER TABLE
NOTIFY pgrst, 'reload schema';

-- Conferir resultado (deve listar 39 colunas)
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'team_stats'
ORDER BY ordinal_position;
