import allure
import pytest
from http import HTTPStatus
from config.constants import TEST_COMPETITIONS


@allure.story("Competitions")
@allure.title("Verify major competitions presence")
@allure.severity(allure.severity_level.NORMAL)
def test_verify_major_competitions(api_client):
    """
    Test that all expected major competitions from constants are present.
    """
    with allure.step("Retrieve competitions"):
        if hasattr(pytest, "competitions_list"):
            competitions = pytest.competitions_list
            allure.attach(
                "Using cached competitions from previous test",
                name="Data Source",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            response = api_client.get_competitions()
            assert response.status_code == HTTPStatus.OK

            response_text = response.text.strip()
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")
            competitions_str = response_text[start_idx + 1 : end_idx]
            competitions = [
                comp.strip() for comp in competitions_str.split(",") if comp.strip()
            ]

    with allure.step("Prepare competition data for matching"):
        # Convert to lowercase for case-insensitive comparison
        competitions_normalized = {}
        for comp in competitions:
            # Store multiple normalized versions for better matching
            normalized = comp.lower().replace("_", "").replace(" ", "").replace("-", "")
            competitions_normalized[normalized] = comp

    with allure.step("Validate major leagues presence"):
        # Define expected patterns for major leagues
        major_leagues = {
            "premier_league": ["premierleague", "epl", "englishpremierleague"],
            "bundesliga": ["bundesliga", "germanleague"],
            "la_liga": ["laliga", "primeradivision", "spanishleague"],
            "serie_a": ["seriea", "italianleague"],
            "ligue_1": ["ligue1", "frenchleague", "championnatdefrance"],
        }

        found_leagues = {}
        missing_leagues = []

        for league_key, patterns in major_leagues.items():
            found = False
            for pattern in patterns:
                for normalized, original in competitions_normalized.items():
                    if pattern in normalized:
                        found_leagues[league_key] = {
                            "id": TEST_COMPETITIONS.get(league_key),
                            "actual_name": original,
                            "matched_pattern": pattern,
                        }
                        found = True
                        break
                if found:
                    break

            if not found:
                missing_leagues.append(league_key)

        # All major leagues should be present
        assert len(missing_leagues) == 0, f"Missing major leagues: {missing_leagues}"

        allure.attach(
            "Major Leagues Found:\n"
            + "\n".join(
                f"- {key}: '{data['actual_name']}' (ID: {data['id']})"
                for key, data in found_leagues.items()
            ),
            name="Major Leagues Verification",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Validate tournament competitions"):
        # Check for cup/tournament competitions
        tournaments = {
            "champions_league": ["championsleague", "ucl", "uefachampionsleague"],
            "europa_league": ["europaleague", "uefaeuropaleague", "uel"],
            "world_cup": ["worldcup", "fifaworldcup", "wc"],
        }

        found_tournaments = {}
        missing_tournaments = []

        for tournament_key, patterns in tournaments.items():
            found = False
            for pattern in patterns:
                for normalized, original in competitions_normalized.items():
                    if pattern in normalized:
                        found_tournaments[tournament_key] = {
                            "id": TEST_COMPETITIONS.get(tournament_key),
                            "actual_name": original,
                            "matched_pattern": pattern,
                        }
                        found = True
                        break
                if found:
                    break

            if not found:
                missing_tournaments.append(tournament_key)

        # At least 2 out of 3 tournaments should be present
        assert (
            len(found_tournaments) >= 2
        ), f"Expected at least 2 tournaments, found {len(found_tournaments)}: {list(found_tournaments.keys())}"

        allure.attach(
            "Tournaments Found:\n"
            + "\n".join(
                f"- {key}: '{data['actual_name']}' (ID: {data['id']})"
                for key, data in found_tournaments.items()
            )
            + (f"\n\nMissing: {missing_tournaments}" if missing_tournaments else ""),
            name="Tournament Competitions Verification",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Create competition ID mapping"):
        # Combine all found competitions for mapping
        all_found_competitions = {**found_leagues, **found_tournaments}

        competition_id_mapping = {}
        for key, data in all_found_competitions.items():
            if data["id"]:  # Only add if ID exists in constants
                competition_id_mapping[data["actual_name"]] = data["id"]

        allure.attach(
            f"Created mapping for {len(competition_id_mapping)} competitions with IDs",
            name="ID Mapping Created",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Competition coverage analysis"):
        total_expected = len(TEST_COMPETITIONS)
        total_found = len(all_found_competitions)
        coverage_percentage = (total_found / total_expected) * 100

        summary = f"""
           Competition Coverage Analysis:
           =====================================
           Expected from constants: {total_expected}
           Successfully matched: {total_found}
           Coverage: {coverage_percentage:.1f}%

           Leagues found: {len(found_leagues)}/5
           Tournaments found: {len(found_tournaments)}/3

           Total competitions in API: {len(competitions)}
           Competitions with IDs mapped: {len(competition_id_mapping)}
           """

        allure.attach(
            summary,
            name="Coverage Analysis",
            attachment_type=allure.attachment_type.TEXT,
        )

        # Ensure we have good coverage
        assert (
            coverage_percentage >= 75
        ), f"Competition coverage too low: {coverage_percentage:.1f}% (expected >= 75%)"
