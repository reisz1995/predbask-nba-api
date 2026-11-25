-- ============================================================
-- LIMPEZA DE DUPLICATAS + CONSTRAINT UNICA (UPSERT)
-- Execute no Supabase SQL Editor antes de rodar o script
-- ============================================================

-- 1. Remover duplicatas mantendo apenas o registro MAIS RECENTE (maior id)
DELETE FROM team_stats a USING team_stats b
WHERE a.id < b.id
  AND a.season = b.season
  AND a.season_type = b.season_type
  AND a.team_id = b.team_id;

DELETE FROM player_stats a USING player_stats b
WHERE a.id < b.id
  AND a.season = b.season
  AND a.season_type = b.season_type
  AND a.player_id = b.player_id;

-- 2. Adicionar constraint UNICA para permitir UPSERT
ALTER TABLE team_stats
  ADD CONSTRAINT team_stats_unique_season_team
  UNIQUE (season, season_type, team_id);

ALTER TABLE player_stats
  ADD CONSTRAINT player_stats_unique_season_player
  UNIQUE (season, season_type, player_id);

-- 3. Verificar resultado (deve mostrar 30 times e 481 jogadores)
SELECT season, season_type, COUNT(*) AS total
FROM team_stats GROUP BY season, season_type;

SELECT season, season_type, COUNT(*) AS total
FROM player_stats GROUP BY season, season_type;

-- 4. Conferir pace preenchido
SELECT team_name, pace, gp, pts
FROM team_stats
WHERE season = '2026-27'
ORDER BY pace DESC
LIMIT 10;
