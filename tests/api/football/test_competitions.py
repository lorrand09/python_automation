import allure
import pytest
from http import HTTPStatus
from config.constants import TEST_COMPETITIONS


@allure.feature("Football Data API")
@allure.story("Competitions")
@allure.title("Get all available competitions")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_competitions(api_client):
    """
    Test retrieving all available competitions
    API returns a string of comma-separated competition names in curly braces
    """
    with allure.step("Send GET request to competitions endpoint"):
        response = api_client.get_competitions()

    with allure.step("Validate response status code"):
        assert (
            response.status_code == HTTPStatus.OK
        ), f"Expected {HTTPStatus.OK}, got {response.status_code}"

    with allure.step("Parse response data"):
        # API returns string like: "{comp1,comp2,comp3}"
        response_text = response.text.strip()

        allure.attach(
            response_text[:1000] if len(response_text) > 1000 else response_text,
            name="Raw Response",
            attachment_type=allure.attachment_type.TEXT,
        )

        # Simple robust parsing - just remove first and last character
        try:
            # Remove the enclosing braces
            if "{" in response_text and "}" in response_text:
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}")
                competitions_str = response_text[start_idx + 1 : end_idx]

                # Split by comma and clean up
                competitions = [
                    comp.strip() for comp in competitions_str.split(",") if comp.strip()
                ]
            else:
                pytest.fail(
                    f"Response doesn't contain curly braces: {response_text[:200]}"
                )

        except Exception as e:
            pytest.fail(f"Failed to parse response: {str(e)}")

    with allure.step("Validate competitions list"):
        # Validate we got competitions
        assert len(competitions) > 0, "Should return at least one competition"

        allure.attach(
            f"Found {len(competitions)} competitions",
            name="Competition Count",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Display sample competitions"):
        # Show first 15 competitions
        sample_size = min(15, len(competitions))
        sample_comps = competitions[:sample_size]

        allure.attach(
            "Sample competitions:\n"
            + "\n".join(f"{i + 1}. {comp}" for i, comp in enumerate(sample_comps)),
            name="Sample Competitions",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Validate presence of major competitions"):
        # Use competition names from constants - map IDs to expected name patterns
        expected_competition_patterns = {
            "premierleague": TEST_COMPETITIONS["premier_league"],
            "bundesliga": TEST_COMPETITIONS["bundesliga"],
            "laliga": TEST_COMPETITIONS["la_liga"],
            "seriea": TEST_COMPETITIONS["serie_a"],
            "ligue1": TEST_COMPETITIONS["ligue_1"],
            "championsleague": TEST_COMPETITIONS["champions_league"],
            "europaleague": TEST_COMPETITIONS["europa_league"],
            "worldcup": TEST_COMPETITIONS["world_cup"],
        }

        found_competitions = {}
        for pattern, comp_id in expected_competition_patterns.items():
            # Check if any competition contains the pattern
            matching_comps = [
                comp
                for comp in competitions
                if pattern in comp.lower().replace("_", "").replace(" ", "")
            ]
            if matching_comps:
                found_competitions[pattern] = {
                    "id": comp_id,
                    "found_names": matching_comps,
                }

        # Ensure at least half of the expected competitions are found
        min_required = len(expected_competition_patterns) // 2
        assert (
            len(found_competitions) >= min_required
        ), f"Should find at least {min_required} major competitions. Found: {list(found_competitions.keys())}"

        allure.attach(
            f"Major competitions found ({len(found_competitions)}/{len(expected_competition_patterns)}):\n"
            + "\n".join(
                f"- {key}: {value['found_names'][0]}"
                for key, value in found_competitions.items()
            ),
            name="Major Competitions Verification",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Validate competition name format"):
        # Validate first 10 competitions are not empty
        for i, comp in enumerate(competitions[:10]):
            assert len(comp) > 0, f"Competition at index {i} is empty"
            # Most competition names should be alphanumeric (allowing apostrophes and underscores)
            assert any(
                c.isalnum() for c in comp
            ), f"Competition name '{comp}' doesn't contain alphanumeric characters"

        allure.attach(
            "✅ Competition name format validation passed",
            name="Format Validation",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Store competition mapping for future use"):
        competition_mapping = {}
        for pattern, data in found_competitions.items():
            competition_mapping[pattern] = {
                "id": data["id"],
                "actual_name": data["found_names"][0],
            }

        allure.attach(
            f"Stored mapping for {len(competition_mapping)} competitions",
            name="Competition Mapping",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Final validation summary"):
        summary = f"""
        Test Summary:
        ✅ Response status: {response.status_code}
        ✅ Total competitions: {len(competitions)}
        ✅ Major competitions found: {len(found_competitions)}/{len(expected_competition_patterns)}
        ✅ Sample competitions: {', '.join(competitions[:5])}
        ✅ Competition IDs from constants: {list(TEST_COMPETITIONS.keys())}
        """

        allure.attach(
            summary,
            name="Test Summary",
            attachment_type=allure.attachment_type.TEXT,
        )
