"""
Quick Start: nba_api + Supabase Integration

This is a minimal example to get started quickly with storing NBA data in Supabase.

Prerequisites:
1. Supabase project: https://supabase.com
2. Install: pip install supabase nba_api pandas
3. Get your Supabase URL and anon key from Project Settings > API

Usage:
    python supabase_quick_start.py
"""

import os
from supabase import create_client, Client
from nba_api.stats.endpoints import LeagueDashTeamStats, LeagueDashPlayerStats
from nba_api.stats.library.parameters import Season, SeasonTypeAllStar, PaceAdjust
import pandas as pd
from dotenv import load_dotenv

# ============================================================
# 1. Configuration - carrega credenciais do arquivo .env
# ============================================================
load_dotenv()  # le o arquivo .env da raiz do projeto

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-public-key")

# Valida credenciais antes de tentar conectar
PLACEHOLDERS = ("your-project", "your-anon", "seu-projeto", "sua-chave")
if any(p in SUPABASE_URL or p in SUPABASE_KEY for p in PLACEHOLDERS):
    print("[CONFIG] Credenciais do Supabase nao configuradas!")
    print("[CONFIG] Edite o arquivo .env com seus valores reais:")
    print("[CONFIG]   SUPABASE_URL=https://SEU-PROJETO.supabase.co")
    print("[CONFIG]   SUPABASE_KEY=sua-chave-anonima")
    print("[CONFIG] Obtenha em: https://supabase.com/dashboard > Settings > API")
    SUPABASE_OK = False
else:
    SUPABASE_OK = True

# Initialize Supabase client (so com credenciais validas)
supabase: Client = None
if SUPABASE_OK:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"[CONFIG] Supabase conectado: {SUPABASE_URL}")
    except Exception as e:
        print(f"[CONFIG] Erro ao criar cliente Supabase: {e}")

# ============================================================
# 2. Formatacao: API retorna fracoes, site mostra percentuais
# ============================================================
# Colunas que vem como 0.597 na API e devem ser salvas como 59.7
PCT_COLUMNS = (
    "AST_PCT", "OREB_PCT", "DREB_PCT", "REB_PCT",
    "TM_TOV_PCT", "EFG_PCT", "TS_PCT", "PIE",
)


def fmt_pct(row, column: str):
    """Converte fracao (0.597) em percentual (59.7), como no site da NBA."""
    value = row.get(column)
    return float(value) * 100 if pd.notna(value) else None


def fmt_poss(row):
    """Converte POSS de 1803 para 1.803, como no site da NBA."""
    value = row.get("POSS")
    return float(value) / 1000 if pd.notna(value) else None


def fmt_float(row, column: str):
    """Float simples, sem conversao (OffRtg, DefRtg, PACE, etc)."""
    value = row.get(column)
    return float(value) if pd.notna(value) else None


# ============================================================
# 3. Fetch Data from NBA API
# ============================================================
def fetch_team_stats(season: str = None, season_type: str = None) -> pd.DataFrame:
    """Fetch team statistics from NBA API."""
    if season is None:
        season = Season.default  # "2026-27" (automatic based on date)
    if season_type is None:
        season_type = SeasonTypeAllStar.default  # "Regular Season"

    print(f"[NET] Fetching team stats for {season} ({season_type})...")

    data = LeagueDashTeamStats(
        season=season,
        season_type_all_star=season_type,
        pace_adjust=PaceAdjust.default,
        per_mode_detailed="PerGame",  # MEDIA por jogo (evita totais como 1000 pts)
        measure_type_detailed_defense="Advanced",  # OffRtg, DefRtg, PACE, PIE, POSS...
        get_request=True  # Use True for real API, False for offline mode
    )

    # Try to get data frames; handle both online and offline modes
    try:
        if data.data_sets and len(data.data_sets) > 0:
            df = data.league_dash_team_stats.get_data_frame()
            print(f"   [OK] Retrieved {len(df)} team records (online mode)")
        else:
            # Offline mode: return empty DataFrame with expected columns
            print(f"   [OFFLINE] No data available, returning structure")
            import pandas as pd
            df = pd.DataFrame(columns=[
                'TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'PACE', 'PACE_PER40', 'PTS'
            ])
    except Exception as e:
        print(f"   [WARN] Error fetching data: {type(e).__name__}")
        import pandas as pd
        df = pd.DataFrame(columns=[
            'TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'PACE', 'PACE_PER40', 'PTS'
        ])

    # Metricas avancadas (OffRtg, DefRtg, PACE, PIE, POSS) ja vem no endpoint
    if not df.empty and 'PACE' in df.columns:
        print(f"   [OK] Advanced: OffRtg/DefRtg/PACE/PIE/POSS incluidos")

    return df


def fetch_player_stats(season: str = None, season_type: str = None) -> pd.DataFrame:
    """Fetch player statistics from NBA API."""
    if season is None:
        season = Season.default  # "2026-27" (automatic based on date)
    if season_type is None:
        season_type = SeasonTypeAllStar.default  # "Regular Season"

    print(f"[NET] Fetching player stats for {season} ({season_type})...")

    data = LeagueDashPlayerStats(
        season=season,
        season_type_all_star=season_type,
        pace_adjust=PaceAdjust.default,
        per_mode_detailed="PerGame",  # MEDIA por jogo (evita totais como 1000 pts)
        measure_type_detailed_defense="Advanced",  # OffRtg, DefRtg, PACE, PIE, POSS...
        get_request=True  # Use True for real API, False for offline mode
    )

    # Try to get data frames; handle both online and offline modes
    try:
        if data.data_sets and len(data.data_sets) > 0:
            df = data.league_dash_player_stats.get_data_frame()
            print(f"   [OK] Retrieved {len(df)} player records (online mode)")
        else:
            # Offline mode: return empty DataFrame with expected columns
            print(f"   [OFFLINE] No cached data available, returning structure")
            import pandas as pd
            df = pd.DataFrame(columns=[
                'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'PTS', 'PACE', 'AGE'
            ])
    except Exception as e:
        print(f"   [WARN] Error fetching data: {type(e).__name__}")
        import pandas as pd
        df = pd.DataFrame(columns=[
            'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'PTS', 'PACE', 'AGE'
        ])

    # Metricas avancadas (OffRtg, DefRtg, PACE, PIE, POSS) ja vem no endpoint
    if not df.empty and 'PACE' in df.columns:
        print(f"   [OK] Advanced: OffRtg/DefRtg/PACE/PIE/POSS incluidos")

    return df

# ============================================================
# 3. Store Data in Supabase
# ============================================================
def store_team_stats(df: pd.DataFrame, season: str = None, season_type: str = None) -> None:
    """Store team stats in Supabase."""
    if supabase is None:
        print("[SKIP] Supabase nao configurado - pulando insercao")
        return
    if season is None:
        season = Season.default
    if season_type is None:
        season_type = SeasonTypeAllStar.default

    if df.empty:
        print("[WARN] No data to store")
        return

    # Prepare records - select relevant columns
    records = []
    for _, row in df.iterrows():
        record = {
            "season": season,
            "season_type": season_type,
            "team_id": int(row.get("TEAM_ID", 0)) if pd.notna(row.get("TEAM_ID")) else None,
            "team_name": str(row.get("TEAM_NAME", "")) if pd.notna(row.get("TEAM_NAME")) else None,
            "gp": int(row.get("GP", 0)) if pd.notna(row.get("GP")) else None,
            "w": int(row.get("W", 0)) if pd.notna(row.get("W")) else None,
            "l": int(row.get("L", 0)) if pd.notna(row.get("L")) else None,
            "w_pct": float(row.get("W_PCT", 0)) if pd.notna(row.get("W_PCT")) else None,
            "min_avg": float(row.get("MIN", 0)) if pd.notna(row.get("MIN")) else None,
            "fgm": int(row.get("FGM", 0)) if pd.notna(row.get("FGM")) else None,
            "fga": int(row.get("FGA", 0)) if pd.notna(row.get("FGA")) else None,
            "fg_pct": float(row.get("FG_PCT", 0)) if pd.notna(row.get("FG_PCT")) else None,
            "fg3m": int(row.get("FG3M", 0)) if pd.notna(row.get("FG3M")) else None,
            "fg3a": int(row.get("FG3A", 0)) if pd.notna(row.get("FG3A")) else None,
            "fg3_pct": float(row.get("FG3_PCT", 0)) if pd.notna(row.get("FG3_PCT")) else None,
            "ftm": int(row.get("FTM", 0)) if pd.notna(row.get("FTM")) else None,
            "fta": int(row.get("FTA", 0)) if pd.notna(row.get("FTA")) else None,
            "ft_pct": float(row.get("FT_PCT", 0)) if pd.notna(row.get("FT_PCT")) else None,
            "orb": int(row.get("OREB", 0)) if pd.notna(row.get("OREB")) else None,
            "drb": int(row.get("DREB", 0)) if pd.notna(row.get("DREB")) else None,
            "reb": int(row.get("REB", 0)) if pd.notna(row.get("REB")) else None,
            "ast": int(row.get("AST", 0)) if pd.notna(row.get("AST")) else None,
            "turnovers": int(row.get("TOV", 0)) if pd.notna(row.get("TOV")) else None,
            "stl": int(row.get("STL", 0)) if pd.notna(row.get("STL")) else None,
            "blk": int(row.get("BLK", 0)) if pd.notna(row.get("BLK")) else None,
            "pf": int(row.get("PF", 0)) if pd.notna(row.get("PF")) else None,
            "pfd": int(row.get("PFD", 0)) if pd.notna(row.get("PFD")) else None,
            "pts": int(row.get("PTS", 0)) if pd.notna(row.get("PTS")) else None,
            "plus_minus": int(row.get("PLUS_MINUS", 0)) if pd.notna(row.get("PLUS_MINUS")) else None,
            "pace": float(row.get("PACE", 0)) if pd.notna(row.get("PACE")) else None,
            "pace_per40": float(row.get("PACE_PER40", 0)) if pd.notna(row.get("PACE_PER40")) else None,
            # Metricas avancadas (mesmas colunas do site NBA.com/Glossary)
            "off_rtg": float(row.get("OFF_RATING", 0)) if pd.notna(row.get("OFF_RATING")) else None,
            "def_rtg": float(row.get("DEF_RATING", 0)) if pd.notna(row.get("DEF_RATING")) else None,
            "net_rtg": float(row.get("NET_RATING", 0)) if pd.notna(row.get("NET_RATING")) else None,
            "ast_pct": fmt_pct(row, "AST_PCT"),      # 0.597 -> 59.7
            "ast_to": fmt_float(row, "AST_TO"),       # 1.49 (sem conversao)
            "ast_ratio": fmt_float(row, "AST_RATIO"), # 17.4 (sem conversao)
            "oreb_pct": fmt_pct(row, "OREB_PCT"),     # 0.338 -> 33.8
            "dreb_pct": fmt_pct(row, "DREB_PCT"),     # 0.645 -> 64.5
            "reb_pct": fmt_pct(row, "REB_PCT"),       # 0.496 -> 49.6
            "tov_pct": fmt_pct(row, "TM_TOV_PCT"),    # 0.164 -> 16.4
            "efg_pct": fmt_pct(row, "EFG_PCT"),       # 0.568 -> 56.8
            "ts_pct": fmt_pct(row, "TS_PCT"),         # 0.612 -> 61.2
            "pie": fmt_pct(row, "PIE"),               # 0.534 -> 53.4
            "poss": fmt_poss(row),                    # 1803 -> 1.803
        }
        records.append(record)

    # Limpar registros anteriores da mesma temporada (evita duplicatas)
    try:
        supabase.table("team_stats").delete().eq("season", season).eq(
            "season_type", season_type
        ).execute()
    except Exception:
        pass

    # Insert into Supabase
    try:
        result = supabase.table("team_stats").insert(records).execute()
        print(f"[OK] Stored {len(records)} team stat records in Supabase")
        if result.data:
            print(f"   First record ID: {result.data[0].get('id')}")
    except Exception as e:
        print(f"[ERR] Error storing team stats: {e}")


def store_player_stats(df: pd.DataFrame, season: str = None, season_type: str = None) -> None:
    """Store player stats in Supabase."""
    if supabase is None:
        print("[SKIP] Supabase nao configurado - pulando insercao")
        return
    if season is None:
        season = Season.default
    if season_type is None:
        season_type = SeasonTypeAllStar.default

    if df.empty:
        print("[WARN] No data to store")
        return

    # Prepare records
    records = []
    for _, row in df.iterrows():
        record = {
            "season": season,
            "season_type": season_type,
            "player_id": int(row.get("PLAYER_ID", 0)) if pd.notna(row.get("PLAYER_ID")) else None,
            "player_name": str(row.get("PLAYER_NAME", "")) if pd.notna(row.get("PLAYER_NAME")) else None,
            "team_id": int(row.get("TEAM_ID", 0)) if pd.notna(row.get("TEAM_ID")) else None,
            "team_abbreviation": str(row.get("TEAM_ABBREVIATION", "")) if pd.notna(row.get("TEAM_ABBREVIATION")) else None,
            "age": int(row.get("AGE", 0)) if pd.notna(row.get("AGE")) else None,
            "gp": int(row.get("GP", 0)) if pd.notna(row.get("GP")) else None,
            "w": int(row.get("W", 0)) if pd.notna(row.get("W")) else None,
            "l": int(row.get("L", 0)) if pd.notna(row.get("L")) else None,
            "w_pct": float(row.get("W_PCT", 0)) if pd.notna(row.get("W_PCT")) else None,
            "min_avg": float(row.get("MIN", 0)) if pd.notna(row.get("MIN")) else None,
            "fgm": int(row.get("FGM", 0)) if pd.notna(row.get("FGM")) else None,
            "fga": int(row.get("FGA", 0)) if pd.notna(row.get("FGA")) else None,
            "fg_pct": float(row.get("FG_PCT", 0)) if pd.notna(row.get("FG_PCT")) else None,
            "fg3m": int(row.get("FG3M", 0)) if pd.notna(row.get("FG3M")) else None,
            "fg3a": int(row.get("FG3A", 0)) if pd.notna(row.get("FG3A")) else None,
            "fg3_pct": float(row.get("FG3_PCT", 0)) if pd.notna(row.get("FG3_PCT")) else None,
            "ftm": int(row.get("FTM", 0)) if pd.notna(row.get("FTM")) else None,
            "fta": int(row.get("FTA", 0)) if pd.notna(row.get("FTA")) else None,
            "ft_pct": float(row.get("FT_PCT", 0)) if pd.notna(row.get("FT_PCT")) else None,
            "orb": int(row.get("OREB", 0)) if pd.notna(row.get("OREB")) else None,
            "drb": int(row.get("DREB", 0)) if pd.notna(row.get("DREB")) else None,
            "reb": int(row.get("REB", 0)) if pd.notna(row.get("REB")) else None,
            "ast": int(row.get("AST", 0)) if pd.notna(row.get("AST")) else None,
            "turnovers": int(row.get("TOV", 0)) if pd.notna(row.get("TOV")) else None,
            "stl": int(row.get("STL", 0)) if pd.notna(row.get("STL")) else None,
            "blk": int(row.get("BLK", 0)) if pd.notna(row.get("BLK")) else None,
            "pf": int(row.get("PF", 0)) if pd.notna(row.get("PF")) else None,
            "pfd": int(row.get("PFD", 0)) if pd.notna(row.get("PFD")) else None,
            "pts": int(row.get("PTS", 0)) if pd.notna(row.get("PTS")) else None,
            "nb_fantasy_pts": float(row.get("NBA_FANTASY_PTS", 0)) if pd.notna(row.get("NBA_FANTASY_PTS")) else None,
            "dd2": int(row.get("DD2", 0)) if pd.notna(row.get("DD2")) else None,
            "td3": int(row.get("TD3", 0)) if pd.notna(row.get("TD3")) else None,
            "plus_minus": int(row.get("PLUS_MINUS", 0)) if pd.notna(row.get("PLUS_MINUS")) else None,
            "nb_fantasy_pts_rank": float(row.get("NBA_FANTASY_PTS_RANK", 0)) if pd.notna(row.get("NBA_FANTASY_PTS_RANK")) else None,
            "pace": float(row.get("PACE", 0)) if pd.notna(row.get("PACE")) else None,
            "pace_per40": float(row.get("PACE_PER40", 0)) if pd.notna(row.get("PACE_PER40")) else None,
            # Metricas avancadas (mesmas colunas do site NBA.com/Glossary)
            "off_rtg": float(row.get("OFF_RATING", 0)) if pd.notna(row.get("OFF_RATING")) else None,
            "def_rtg": float(row.get("DEF_RATING", 0)) if pd.notna(row.get("DEF_RATING")) else None,
            "net_rtg": float(row.get("NET_RATING", 0)) if pd.notna(row.get("NET_RATING")) else None,
            "ast_pct": fmt_pct(row, "AST_PCT"),      # 0.597 -> 59.7
            "ast_to": fmt_float(row, "AST_TO"),       # 1.49 (sem conversao)
            "ast_ratio": fmt_float(row, "AST_RATIO"), # 17.4 (sem conversao)
            "oreb_pct": fmt_pct(row, "OREB_PCT"),     # 0.338 -> 33.8
            "dreb_pct": fmt_pct(row, "DREB_PCT"),     # 0.645 -> 64.5
            "reb_pct": fmt_pct(row, "REB_PCT"),       # 0.496 -> 49.6
            "tov_pct": fmt_pct(row, "TM_TOV_PCT"),    # 0.164 -> 16.4
            "efg_pct": fmt_pct(row, "EFG_PCT"),       # 0.568 -> 56.8
            "ts_pct": fmt_pct(row, "TS_PCT"),         # 0.612 -> 61.2
            "pie": fmt_pct(row, "PIE"),               # 0.534 -> 53.4
            "poss": fmt_poss(row),                    # 1803 -> 1.803
        }
        records.append(record)

    # Limpar registros anteriores da mesma temporada (evita duplicatas)
    try:
        supabase.table("player_stats").delete().eq("season", season).eq(
            "season_type", season_type
        ).execute()
    except Exception:
        pass

    # Insert into Supabase
    try:
        result = supabase.table("player_stats").insert(records).execute()
        print(f"[OK] Stored {len(records)} player stat records in Supabase")
        if result.data:
            print(f"   First record ID: {result.data[0].get('id')}")
    except Exception as e:
        print(f"[ERR] Error storing player stats: {e}")

# ============================================================
# 4. Query Data from Supabase
# ============================================================
def query_team_stats(season: str = None, team_name: str = None) -> list:
    """Query team stats from Supabase."""
    if supabase is None:
        return []
    query = supabase.table("team_stats").select("*")

    if season:
        query = query.eq("season", season)
    if team_name:
        query = query.eq("team_name", team_name)

    result = query.order("id", desc=True).limit(30).execute()
    return result.data


def query_player_stats(season: str = None, min_points: float = None) -> list:
    """Query player stats from Supabase."""
    if supabase is None:
        return []
    query = supabase.table("player_stats").select("*")

    if season:
        query = query.eq("season", season)
    if min_points:
        query = query.gt("pts", min_points)

    result = query.order("id", desc=True).limit(500).execute()
    return result.data


def get_team_by_name(team_name: str, season: str = None) -> list:
    """Get team stats by team name."""
    if supabase is None:
        return []
    query = supabase.table("team_stats").select("*").eq("team_name", team_name)

    if season:
        query = query.eq("season", season)

    result = query.execute()
    return result.data

# ============================================================
# 5. Main Execution
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("nba_api + Supabase Quick Start")
    print("=" * 60)
    print()

    # 1. Fetch team data (usará Season.default = "2026-27")
    print("[NET] Stage 1: Fetching team statistics...")
    team_df = fetch_team_stats()

    # 2. Fetch player data
    print("[NET] Stage 2: Fetching player statistics...")
    player_df = fetch_player_stats()

    # 3. Store in Supabase
    print()
    print("[STORE] Storing data in Supabase...")
    store_team_stats(team_df, season=Season.default, season_type=SeasonTypeAllStar.default)
    store_player_stats(player_df, season=Season.default, season_type=SeasonTypeAllStar.default)

    # 4. Query stored data
    print()
    print("[QUERY] Stage 3: Querying stored data...")

    # Check if we have data fetched from API
    if not team_df.empty or not player_df.empty:
        # Get all teams for the default season
        teams = query_team_stats(season=Season.default)
        print(f"   [DATA] Found {len(teams)} team records for {Season.default}")

        # Get top players by points from the default season
        top_scorers = query_player_stats(season=Season.default, min_points=0)
        print(f"   [STAR] Found {len(top_scorers)} player records for {Season.default}")

        # Example: Get specific team
        if teams:
            first_team = teams[0]
            print(f"   [BASKET] First team: {first_team.get('team_name', 'N/A')} (PACE: {first_team.get('pace', 'N/A')})")
    else:
        print("   [SKIP] No data fetched - skipping queries (use get_request=True for real data)")

    print()
    print("=" * 60)
    print("[DONE] Quick start complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Set valid SUPABASE_URL and SUPABASE_KEY environment variables")
    print("  2. Run SQL schema in Supabase dashboard")
    print("  3. Data will be stored and queryable for season 2026-27")