# E2E Configuration
E2E_BASE_URL = "https://m.twitch.tv/"

# Football API Configuration
FOOTBALL_API_BASE_URL = "https://football98.p.rapidapi.com"
RAPIDAPI_HOST = "football98.p.rapidapi.com"

# API Endpoints
ENDPOINTS = {
    # Competitions
    "competitions": "/competitions",
    "competition_details": "/competitions/{id}",
    # Teams
    "teams": "/competitions/{competition_id}/teams",
    "team_details": "/teams/{id}",
    # Matches
    "matches": "/matches",
    "match_details": "/matches/{id}",
    "head_to_head": "/matches/head2head",
    # Standings
    "standings": "/competitions/{competition_id}/standings",
    # Players (if needed)
    "team_players": "/teams/{id}/players",
    "player_details": "/players/{id}",
    # Scorers (if needed)
    "competition_scorers": "/competitions/{id}/scorers",
}

# ============================================
# Test Data - Competition IDs
# ============================================
TEST_COMPETITIONS = {
    "premier_league": 2021,
    "bundesliga": 2002,
    "la_liga": 2014,
    "serie_a": 2019,
    "ligue_1": 2015,
    "champions_league": 2001,
    "europa_league": 2146,
    "world_cup": 2000,
}

COMPETITION_TYPES = {"league": "LEAGUE", "cup": "CUP"}

# Timeouts
API_TIMEOUT = 30
