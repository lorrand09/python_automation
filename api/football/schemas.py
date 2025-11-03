"""
API Response Schemas for validation

Note: Some endpoints return strings instead of JSON objects.
This file handles both formats.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime


# ============================================
# Helper Functions for String Responses
# ============================================
def parse_competitions_string(response_text: str) -> List[str]:
    """
    Parse competitions from string format: "{comp1,comp2,comp3}"

    Args:
        response_text: String response from API

    Returns:
        List of competition names
    """
    if response_text.startswith("{") and response_text.endswith("}"):
        competitions_str = response_text.strip("{}")
        return competitions_str.split(",")
    else:
        raise ValueError(f"Invalid competitions string format: {response_text[:100]}")


def validate_competitions_string(response_text: str) -> bool:
    """
    Validate competitions string response

    Args:
        response_text: String response from API

    Returns:
        True if valid

    Raises:
        ValueError if invalid
    """
    try:
        competitions = parse_competitions_string(response_text)
        if len(competitions) == 0:
            raise ValueError("No competitions found in response")
        return True
    except Exception as e:
        raise ValueError(f"Invalid competitions response: {str(e)}")


# ============================================
# Competition Schemas (for JSON responses)
# ============================================
class Competition(BaseModel):
    """Schema for a single competition"""

    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    code: Optional[str] = None
    type: Optional[str] = None
    emblem: Optional[str] = None


class CompetitionsResponse(BaseModel):
    """Schema for competitions list response (JSON format)"""

    count: int
    competitions: List[Competition]

    @field_validator("count")
    @classmethod
    def validate_count(cls, v, info):
        """Validate count matches number of competitions"""
        if "competitions" in info.data and v != len(info.data["competitions"]):
            raise ValueError("Count doesn't match number of competitions")
        return v


# ============================================
# Team Schemas
# ============================================
class Team(BaseModel):
    """Schema for a single team"""

    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    shortName: Optional[str] = None
    tla: Optional[str] = None
    crest: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    founded: Optional[int] = None
    clubColors: Optional[str] = None
    venue: Optional[str] = None


class TeamsResponse(BaseModel):
    """Schema for teams list response"""

    count: int
    competition: Optional[Dict[str, Any]] = None
    season: Optional[Dict[str, Any]] = None
    teams: List[Team]


# ============================================
# Match/Fixture Schemas
# ============================================
class Score(BaseModel):
    """Schema for match score"""

    home: Optional[int] = None
    away: Optional[int] = None


class MatchScore(BaseModel):
    """Schema for detailed match score"""

    winner: Optional[str] = None
    duration: Optional[str] = None
    fullTime: Optional[Score] = None
    halfTime: Optional[Score] = None


class Match(BaseModel):
    """Schema for a single match/fixture"""

    model_config = ConfigDict(extra="allow")

    id: int
    utcDate: str
    status: str
    matchday: Optional[int] = None
    stage: Optional[str] = None
    homeTeam: Dict[str, Any]
    awayTeam: Dict[str, Any]
    score: Optional[MatchScore] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Validate match status"""
        valid_statuses = [
            "SCHEDULED",
            "LIVE",
            "IN_PLAY",
            "PAUSED",
            "FINISHED",
            "POSTPONED",
            "SUSPENDED",
            "CANCELLED",
        ]
        if v not in valid_statuses:
            raise ValueError(f"Invalid match status: {v}")
        return v


class MatchesResponse(BaseModel):
    """Schema for matches list response"""

    count: int
    matches: List[Match]


# ============================================
# Standings Schemas
# ============================================
class TeamStanding(BaseModel):
    """Schema for team standing in table"""

    position: int
    team: Dict[str, Any]
    playedGames: int
    won: int
    draw: int
    lost: int
    points: int
    goalsFor: int
    goalsAgainst: int
    goalDifference: int

    @field_validator("goalDifference")
    @classmethod
    def validate_goal_difference(cls, v, info):
        """Validate goal difference calculation"""
        data = info.data
        if "goalsFor" in data and "goalsAgainst" in data:
            expected = data["goalsFor"] - data["goalsAgainst"]
            if v != expected:
                raise ValueError(f"Goal difference mismatch: {v} != {expected}")
        return v


class Standing(BaseModel):
    """Schema for competition standing"""

    stage: str
    type: str
    group: Optional[str] = None
    table: List[TeamStanding]


class StandingsResponse(BaseModel):
    """Schema for standings response"""

    competition: Dict[str, Any]
    season: Dict[str, Any]
    standings: List[Standing]


# ============================================
# Error Response Schema
# ============================================
class ErrorResponse(BaseModel):
    """Schema for API error responses"""

    model_config = ConfigDict(extra="allow")

    message: str
    errorCode: Optional[int] = None


# ============================================
# Schema Validation Helper Functions
# ============================================
def validate_response_schema(response_data: dict, schema: BaseModel) -> bool:
    """
    Validate response data against a Pydantic schema

    Args:
        response_data: Dictionary containing API response
        schema: Pydantic BaseModel schema class

    Returns:
        True if validation passes

    Raises:
        ValidationError if validation fails
    """
    try:
        schema(**response_data)
        return True
    except Exception as e:
        raise ValueError(f"Schema validation failed: {str(e)}")


def get_validation_errors(response_data: dict, schema: BaseModel) -> List[str]:
    """
    Get list of validation errors without raising exception

    Args:
        response_data: Dictionary containing API response
        schema: Pydantic BaseModel schema class

    Returns:
        List of validation error messages
    """
    try:
        schema(**response_data)
        return []
    except Exception as e:
        return [str(e)]
