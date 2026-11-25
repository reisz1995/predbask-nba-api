"""
Supabase Backend for nba_api

This module provides a bridge between the nba_api Python client and Supabase,
allowing you to:
1. Fetch NBA statistics from stats.nba.com
2. Store them in Supabase tables
3. Query the data via Supabase's REST API or Realtime features

Typical usage:
    from supabase_backend import NBADataBackend
    
    backend = NBADataBackend(
        supabase_url="https://your-project.supabase.co",
        supabase_key="your-anon-key"
    )
    
    # Fetch and store team stats for 2024-25 season
    backend.store_team_stats(season="2024-25")
    
    # Query stored data
    teams = backend.get_team_stats(season="2024-25")
"""

from supabase import create_client, Client
from nba_api.stats.endpoints import LeagueDashTeamStats, LeagueDashPlayerStats
from nba_api.stats.library.parameters import Season, SeasonTypeAllStar, PaceAdjust
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NBADataBackend:
    """
    Backend class that connects nba_api with Supabase.
    
    Handles:
    - Supabase client initialization
    - Data fetching from NBA API
    - Data storage in Supabase
    - Data querying and retrieval
    """
    
    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Initialize the Supabase client.
        
        Args:
            supabase_url: Your Supabase project URL (e.g., https://abc123.supabase.co)
            supabase_key: Your Supabase anonymous key (public API key)
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self._ensure_tables()
    
    def _ensure_tables(self) -> None:
        """
        Create necessary tables if they don't exist.
        This runs Supabase SQL to set up the schema.
        """
        # SQL to create tables for NBA data
        sql_commands = [
            """
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
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
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
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
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
                plus_minus INTEGER,
                pace FLOAT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
        ]
        
        for sql in sql_commands:
            try:
                self.supabase.rpc("exec", {"sql": sql}).execute()
                logger.info("Table ensured successfully")
            except Exception as e:
                logger.warning(f"Could not execute SQL directly: {e}")
                # Try alternative approach using rest
                pass
    
    def fetch_team_stats(self, season: str = None, season_type: str = None) -> pd.DataFrame:
        """
        Fetch team statistics from NBA API.
        
        Args:
            season: Season in format "2024-25" or None (uses default)
            season_type: "Regular Season" or "Playoffs" or None (uses default)
            
        Returns:
            DataFrame with team statistics including pace metrics
        """
        if season is None:
            season = Season.default
        if season_type is None:
            season_type = SeasonTypeAllStar.default
        
        logger.info(f"Fetching team stats for {season} ({season_type})")
        
        team_data = LeagueDashTeamStats(
            season=season,
            season_type_all_star=season_type,
            pace_adjust=PaceAdjust.default,
            get_request=True
        )
        
        # Get the data frame from the first dataset
        df = team_data.league_dash_team_stats.get_data_frames()[0]
        return df
    
    def fetch_player_stats(self, season: str = None, season_type: str = None) -> pd.DataFrame:
        """
        Fetch player statistics from NBA API.
        
        Args:
            season: Season in format "2024-25" or None (uses default)
            season_type: "Regular Season" or "Playoffs" or None (uses default)
            
        Returns:
            DataFrame with player statistics including pace metrics
        """
        if season is None:
            season = Season.default
        if season_type is None:
            season_type = SeasonTypeAllStar.default
        
        logger.info(f"Fetching player stats for {season} ({season_type})")
        
        player_data = LeagueDashPlayerStats(
            season=season,
            season_type_all_star=season_type,
            pace_adjust=PaceAdjust.default,
            get_request=True
        )
        
        df = player_data.league_dash_player_stats.get_data_frames()[0]
        return df
    
    def store_team_stats(self, season: str = None, season_type: str = None) -> dict:
        """
        Fetch team stats and store in Supabase.
        
        Args:
            season: Season in format "2024-25" or None (uses default)
            season_type: "Regular Season" or "Playoffs" or None (uses default)
            
        Returns:
            Dict with storage results
        """
        if season is None:
            season = Season.default
        if season_type is None:
            season_type = SeasonTypeAllStar.default
        
        df = self.fetch_team_stats(season, season_type)
        
        if df.empty:
            logger.warning("No data returned from NBA API")
            return {"stored": 0, "error": "No data"}
        
        # Prepare records for insertion
        # Select only the columns we need for the team_stats table
        columns_to_store = [
            'TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT',
            'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
            'TOV', 'STL', 'BLK', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'PACE', 'PACE_PER40'
        ]
        
        # Filter and rename columns to match Supabase table
        records = []
        for _, row in df.iterrows():
            record = {}
            for col in columns_to_store:
                if col in row.index:
                    record[col] = row[col]
                else:
                    record[col] = None
            
            # Add season info
            record['season'] = season
            record['season_type'] = season_type
            
            records.append(record)
        
        # Insert into Supabase
        try:
            result = self.supabase.table("team_stats").insert(records).execute()
            logger.info(f"Stored {len(records)} team stat records for {season}")
            return {
                "stored": len(records),
                "season": season,
                "data": result.data if result.data else []
            }
        except Exception as e:
            logger.error(f"Error storing team stats: {e}")
            return {"stored": 0, "error": str(e)}
    
    def store_player_stats(self, season: str = None, season_type: str = None) -> dict:
        """
        Fetch player stats and store in Supabase.
        
        Args:
            season: Season in format "2024-25" or None (uses default)
            season_type: "Regular Season" or "Playoffs" or None (uses default)
            
        Returns:
            Dict with storage results
        """
        if season is None:
            season = Season.default
        if season_type is None:
            season_type = SeasonTypeAllStar.default
        
        df = self.fetch_player_stats(season, season_type)
        
        if df.empty:
            logger.warning("No data returned from NBA API")
            return {"stored": 0, "error": "No data"}
        
        # Select columns for player_stats table
        columns_to_store = [
            'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'W', 'L',
            'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
            'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'PFD', 'PTS',
            'NBA_FANTASY_PTS', 'DD2', 'TD3', 'PLUS_MINUS', 'NBA_FANTASY_PTS_RANK', 'PACE', 'PACE_PER40'
        ]
        
        records = []
        for _, row in df.iterrows():
            record = {}
            for col in columns_to_store:
                if col in row.index:
                    record[col] = row[col]
                else:
                    record[col] = None
            
            record['season'] = season
            record['season_type'] = season_type
            records.append(record)
        
        try:
            result = self.supabase.table("player_stats").insert(records).execute()
            logger.info(f"Stored {len(records)} player stat records for {season}")
            return {
                "stored": len(records),
                "season": season,
                "data": result.data if result.data else []
            }
        except Exception as e:
            logger.error(f"Error storing player stats: {e}")
            return {"stored": 0, "error": str(e)}
    
    def get_team_stats(self, season: str = None, team_id: int = None) -> list:
        """
        Query stored team stats from Supabase.
        
        Args:
            season: Filter by season (e.g., "2024-25")
            team_id: Filter by team ID
            
        Returns:
            List of records matching the query
        """
        query = self.supabase.table("team_stats").select("*")
        
        if season:
            query = query.eq("season", season)
        if team_id:
            query = query.eq("team_id", team_id)
        
        result = query.execute()
        return result.data
    
    def get_player_stats(self, season: str = None, player_id: int = None) -> list:
        """
        Query stored player stats from Supabase.
        
        Args:
            season: Filter by season (e.g., "2024-25")
            player_id: Filter by player ID
            
        Returns:
            List of records matching the query
        """
        query = self.supabase.table("player_stats").select("*")
        
        if season:
            query = query.eq("season", season)
        if player_id:
            query = query.eq("player_id", player_id)
        
        result = query.execute()
        return result.data
    
    def get_team_by_name(self, team_name: str, season: str = None) -> list:
        """
        Get team stats by team name.
        
        Args:
            team_name: Name of the team
            season: Season to filter by
            
        Returns:
            List of matching records
        """
        query = self.supabase.table("team_stats").select("*").eq("team_name", team_name)
        
        if season:
            query = query.eq("season", season)
        
        result = query.execute()
        return result.data
    
    def realtime_subscribe(self, table_name: str, callback):
        """
        Subscribe to realtime updates on a table.
        
        Args:
            table_name: Name of the table to subscribe to ("team_stats" or "player_stats")
            callback: Function to call when data changes
        """
        try:
            channel = self.supabase.channel(f"nba_{table_name}_changes")
            channel.on("*", event_type="post_changes", callback=callback)
            channel.subscribe()
            logger.info(f"Subscribed to realtime updates on {table_name}")
        except Exception as e:
            logger.error(f"Error subscribing to realtime: {e}")


# Example usage
if __name__ == "__main__":
    # Example configuration - replace with your actual Supabase credentials
    SUPABASE_URL = "https://your-project.supabase.co"
    SUPABASE_KEY = "your-anon-public-key"
    
    # Initialize backend
    backend = NBADataBackend(
        supabase_url=SUPABASE_URL,
        supabase_key=SUPABASE_KEY
    )
    
    # Store team stats for current season
    result = backend.store_team_stats(season="2024-25", season_type="Regular Season")
    print(f"Team stats storage result: {result}")
    
    # Store player stats for current season
    result = backend.store_player_stats(season="2024-25", season_type="Regular Season")
    print(f"Player stats storage result: {result}")
    
    # Query stored data
    teams = backend.get_team_stats(season="2024-25")
    print(f"Found {len(teams)} team records for 2024-25")
    
    # Example: Get a specific team
    if teams:
        lakers = backend.get_team_by_name("Los Angeles Lakers", "2024-25")
        print(f"Lakers 2024-25 stats: {lakers}")