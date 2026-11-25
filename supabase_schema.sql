-- Supabase Schema for nba_api Data
-- Run these SQL commands in the Supabase SQL Editor

-- 1. Create team_stats table
CREATE TABLE IF NOT EXISTS team_stats (
    id BIGSERIAL PRIMARY KEY,
    season TEXT NOT NULL,
    season_type TEXT NOT NULL,
    team_id INTEGER,
    team_name TEXT,
    gp INTEGER,
    w INTEGER,
    l INTEGER,
    w_pct FLOAT,
    min_avg FLOAT,
    fgm INTEGER,
    fga INTEGER,
    fg_pct FLOAT,
    fg3m INTEGER,
    fg3a INTEGER,
    fg3_pct FLOAT,
    ftm INTEGER,
    fta INTEGER,
    ft_pct FLOAT,
    orb INTEGER,
    drb INTEGER,
    reb INTEGER,
    ast INTEGER,
    turnovers INTEGER,
    stl INTEGER,
    blk INTEGER,
    pf INTEGER,
    pfd INTEGER,
    pts INTEGER,
    plus_minus INTEGER,
    pace FLOAT,
    pace_per40 FLOAT,
    off_rtg FLOAT,
    def_rtg FLOAT,
    net_rtg FLOAT,
    ast_pct FLOAT,
    ast_to FLOAT,
    ast_ratio FLOAT,
    oreb_pct FLOAT,
    dreb_pct FLOAT,
    reb_pct FLOAT,
    tov_pct FLOAT,
    efg_pct FLOAT,
    ts_pct FLOAT,
    pie FLOAT,
    poss FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create player_stats table
CREATE TABLE IF NOT EXISTS player_stats (
    id BIGSERIAL PRIMARY KEY,
    season TEXT NOT NULL,
    season_type TEXT NOT NULL,
    player_id INTEGER,
    player_name TEXT,
    team_id INTEGER,
    team_abbreviation TEXT,
    age INTEGER,
    gp INTEGER,
    w INTEGER,
    l INTEGER,
    w_pct FLOAT,
    min_avg FLOAT,
    fgm INTEGER,
    fga INTEGER,
    fg_pct FLOAT,
    fg3m INTEGER,
    fg3a INTEGER,
    fg3_pct FLOAT,
    ftm INTEGER,
    fta INTEGER,
    ft_pct FLOAT,
    orb INTEGER,
    drb INTEGER,
    reb INTEGER,
    ast INTEGER,
    turnovers INTEGER,
    stl INTEGER,
    blk INTEGER,
    pf INTEGER,
    pfd INTEGER,
    pts INTEGER,
    nb_fantasy_pts FLOAT,
    dd2 INTEGER,
    td3 INTEGER,
    plus_minus INTEGER,
    nb_fantasy_pts_rank FLOAT,
    pace FLOAT,
    pace_per40 FLOAT,
    off_rtg FLOAT,
    def_rtg FLOAT,
    net_rtg FLOAT,
    ast_pct FLOAT,
    ast_to FLOAT,
    ast_ratio FLOAT,
    oreb_pct FLOAT,
    dreb_pct FLOAT,
    reb_pct FLOAT,
    tov_pct FLOAT,
    efg_pct FLOAT,
    ts_pct FLOAT,
    pie FLOAT,
    poss FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create game_logs table (player game-by-game data)
CREATE TABLE IF NOT EXISTS game_logs (
    id BIGSERIAL PRIMARY KEY,
    season TEXT NOT NULL,
    player_id INTEGER,
    game_date DATE,
    min FLOAT,
    fgm INTEGER,
    fga INTEGER,
    fg_pct FLOAT,
    fg3m INTEGER,
    fg3a INTEGER,
    fg3_pct FLOAT,
    ftm INTEGER,
    fta INTEGER,
    ft_pct FLOAT,
    orb INTEGER,
    drb INTEGER,
    reb INTEGER,
    ast INTEGER,
    turnovers INTEGER,
    stl INTEGER,
    blk INTEGER,
    pf INTEGER,
    pfd INTEGER,
    pts INTEGER,
    plus_minus FLOAT,
    pace FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_team_stats_season ON team_stats(season);
CREATE INDEX IF NOT EXISTS idx_team_stats_team ON team_stats(team_id);
CREATE INDEX IF NOT EXISTS idx_team_stats_name ON team_stats(team_name);
CREATE INDEX IF NOT EXISTS idx_player_stats_season ON player_stats(season);
CREATE INDEX IF NOT EXISTS idx_player_stats_player ON player_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_team ON player_stats(team_id);
CREATE INDEX IF NOT EXISTS idx_gamelogs_player ON game_logs(player_id);
CREATE INDEX IF NOT EXISTS idx_gamelogs_season ON game_logs(season);

-- 5. Enable realtime for the tables (run in Supabase dashboard or via API)
-- ALTER PUBLICATION supabase_realtime ADD team_stats, player_stats, game_logs;

-- 5. Sample RLS (Row Level Security) policies
-- CREATE POLICY "Allow public read access" ON team_stats FOR SELECT USING (true);
-- CREATE POLICY "Allow public insert" ON team_stats FOR INSERT WITH CHECK (true);
-- CREATE POLICY "Allow public update" ON team_stats FOR UPDATE USING (true);
-- CREATE POLICY "Allow public delete" ON team_stats FOR DELETE USING (true);

-- Comments for documentation
COMMENT ON TABLE team_stats IS 'NBA team statistics with pace metrics, stored from nba_api LeagueDashTeamStats endpoint';
COMMENT ON TABLE player_stats IS 'NBA player statistics with pace metrics, stored from nba_api LeagueDashPlayerStats endpoint';
COMMENT ON TABLE game_logs IS 'NBA player game-by-game logs, stored from nba_api play-by-play or box score data';