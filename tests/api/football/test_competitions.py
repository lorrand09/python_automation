import allure
import pytest
from http import HTTPStatus
from config.constants import TEST_COMPETITIONS, COMPETITION_TYPES


@allure.feature("Football Data API")
class TestCompetitions:
    """Test suite for Football API competitions endpoint."""

    # Class variable to store shared data
    _competitions_data = None
    _competition_mapping = None

    @classmethod
    def _fetch_and_parse_competitions(cls, api_client):
        """
        Helper method to fetch and parse competitions.
        Results are cached at class level to avoid repeated API calls.
        """
        if cls._competitions_data is not None:
            return cls._competitions_data

        # Fetch competitions
        response = api_client.get_competitions()
        assert (
            response.status_code == HTTPStatus.OK
        ), f"Expected {HTTPStatus.OK}, got {response.status_code}"

        # Parse response
        response_text = response.text.strip()

        # Remove the enclosing braces
        if "{" not in response_text or "}" not in response_text:
            pytest.fail(f"Response doesn't contain curly braces: {response_text[:200]}")

        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}")
        competitions_str = response_text[start_idx + 1 : end_idx]

        # Split by comma and clean up
        competitions = [
            comp.strip() for comp in competitions_str.split(",") if comp.strip()
        ]

        # Cache the data
        cls._competitions_data = {
            "raw_list": competitions,
            "response_text": response_text[:1000]
            if len(response_text) > 1000
            else response_text,
            "count": len(competitions),
        }

        return cls._competitions_data

    @classmethod
    def _normalize_competitions(cls, competitions):
        """
        Normalize competition names for matching.
        Returns a dictionary of the original names.
        """
        competitions_normalized = {}
        for comp in competitions:
            normalized = comp.lower().replace("_", "").replace(" ", "").replace("-", "")
            competitions_normalized[normalized] = comp
        return competitions_normalized

    @classmethod
    def _find_competitions_by_patterns(cls, competitions_normalized, patterns_dict):
        """
        Find competitions matching given patterns.

        Args:
            competitions_normalized: normalized original names
            patterns_dict: list of patterns to search

        Returns:
            Tuple of (found_dict, missing_list)
        """
        found = {}
        missing = []

        for key, patterns in patterns_dict.items():
            matched = False
            for pattern in patterns:
                for normalized, original in competitions_normalized.items():
                    if pattern in normalized:
                        found[key] = {
                            "id": TEST_COMPETITIONS.get(key),
                            "actual_name": original,
                            "matched_pattern": pattern,
                        }
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                missing.append(key)

        return found, missing

    @allure.story("Competitions")
    @allure.title("Retrieve and validate competitions list structure")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_competitions_list(self, api_client):
        """
        Test retrieving all available competitions and validating structure.
        This test focuses on API response structure and data quality.
        """
        with allure.step("Fetch and parse competitions"):
            data = self._fetch_and_parse_competitions(api_client)
            competitions = data["raw_list"]

            allure.attach(
                data["response_text"],
                name="Raw Response",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Validate competitions list structure"):
            # Basic validations
            assert len(competitions) > 0, "Should return at least one competition"
            assert (
                len(competitions) >= 50
            ), f"Expected at least 50 competitions, got {len(competitions)}"

            allure.attach(
                f"Found {len(competitions)} competitions",
                name="Competition Count",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Validate competition name format"):
            invalid_competitions = []

            for i, comp in enumerate(competitions[:20]):  # Check first 20
                if len(comp) == 0:
                    invalid_competitions.append(f"Index {i}: Empty string")
                elif not any(c.isalnum() for c in comp):
                    invalid_competitions.append(
                        f"Index {i}: No alphanumeric chars - '{comp}'"
                    )
                elif len(comp) > 100:
                    invalid_competitions.append(
                        f"Index {i}: Too long ({len(comp)} chars)"
                    )

            assert (
                len(invalid_competitions) == 0
            ), f"Found invalid competition formats:\n" + "\n".join(invalid_competitions)

            allure.attach(
                "✅ Competition name format validation passed",
                name="Format Validation",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Check for duplicates"):
            # Find all duplicates
            from collections import Counter

            competition_counts = Counter(competitions)
            duplicates = {
                comp: count for comp, count in competition_counts.items() if count > 1
            }

            if duplicates:
                # Log duplicates as warning
                duplicate_summary = "\n".join(
                    f"- '{comp}': appears {count} times"
                    for comp, count in list(duplicates.items())[:10]  # Show first 10
                )

                total_duplicate_entries = sum(duplicates.values()) - len(duplicates)
                duplicate_percentage = (
                    total_duplicate_entries / len(competitions)
                ) * 100

                allure.attach(
                    f"⚠️ Found {len(duplicates)} competitions with duplicates:\n{duplicate_summary}\n\n"
                    + f"Total duplicate entries: {total_duplicate_entries} ({duplicate_percentage:.1f}% of total)\n"
                    + f"Unique competitions: {len(competition_counts)}",
                    name="Duplicate Analysis",
                    attachment_type=allure.attachment_type.TEXT,
                )

                # Allow some duplicates but fail if too many (more than 10% of total)
                assert (
                    duplicate_percentage < 10
                ), f"Too many duplicates: {duplicate_percentage:.1f}% of competitions are duplicates (threshold: 10%)"

                # Store unique list for further processing
                competitions = list(competition_counts.keys())
                self._competitions_data["raw_list"] = competitions
                self._competitions_data["has_duplicates"] = True
                self._competitions_data["duplicate_count"] = len(duplicates)
            else:
                allure.attach(
                    f"✅ No duplicates found in {len(competitions)} competitions",
                    name="Duplicate Check",
                    attachment_type=allure.attachment_type.TEXT,
                )

        with allure.step("Display sample competitions"):
            sample_size = min(15, len(competitions))
            sample_comps = competitions[:sample_size]

            allure.attach(
                "Sample competitions:\n"
                + "\n".join(f"{i + 1}. {comp}" for i, comp in enumerate(sample_comps)),
                name="Sample Competitions",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Create initial competition mapping"):
            # Quick check for major competitions and create basic mapping
            competitions_normalized = self._normalize_competitions(competitions)

            # Store basic mapping for use in next test
            quick_patterns = {
                "premierleague": TEST_COMPETITIONS.get("premier_league"),
                "bundesliga": TEST_COMPETITIONS.get("bundesliga"),
                "laliga": TEST_COMPETITIONS.get("la_liga"),
                "seriea": TEST_COMPETITIONS.get("serie_a"),
            }

            quick_mapping = {}
            for pattern, comp_id in quick_patterns.items():
                for normalized, original in competitions_normalized.items():
                    if pattern in normalized:
                        quick_mapping[original] = comp_id
                        break

            # Store in class variable for next test
            self.__class__._competition_mapping = quick_mapping

            allure.attach(
                f"Created initial mapping for {len(quick_mapping)} competitions",
                name="Initial Mapping",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.story("Competitions")
    @allure.title("Verify major competitions presence and coverage")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verify_major_competitions(self, api_client):
        """
        Test that all expected major competitions from constants are present.
        This test focuses on business logic validation and data completeness.
        """
        with allure.step("Retrieve competitions (from cache if available)"):
            data = self._fetch_and_parse_competitions(api_client)
            competitions = data["raw_list"]

            allure.attach(
                f"Using {'cached' if self._competitions_data else 'fresh'} competitions data",
                name="Data Source",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Prepare competition data for matching"):
            competitions_normalized = self._normalize_competitions(competitions)

        with allure.step("Validate major leagues presence"):
            major_leagues = {
                "premier_league": ["premierleague", "epl", "englishpremierleague"],
                "bundesliga": ["bundesliga", "germanleague"],
                "la_liga": ["laliga", "primeradivision", "spanishleague"],
                "serie_a": ["seriea", "italianleague"],
                "ligue_1": ["ligue1", "frenchleague", "championnatdefrance"],
            }

            found_leagues, missing_leagues = self._find_competitions_by_patterns(
                competitions_normalized, major_leagues
            )

            # All major leagues should be present
            assert (
                len(missing_leagues) == 0
            ), f"Missing major leagues: {missing_leagues}"

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
            tournaments = {
                "champions_league": ["championsleague", "ucl", "uefachampionsleague"],
                "europa_league": ["europaleague", "uefaeuropaleague", "uel"],
                "world_cup": ["worldcup", "fifaworldcup", "wc"],
            }

            (
                found_tournaments,
                missing_tournaments,
            ) = self._find_competitions_by_patterns(
                competitions_normalized, tournaments
            )

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
                + (
                    f"\n\nMissing: {missing_tournaments}" if missing_tournaments else ""
                ),
                name="Tournament Competitions Verification",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Create comprehensive competition ID mapping"):
            # Combine all found competitions for mapping
            all_found_competitions = {**found_leagues, **found_tournaments}

            # Create a comprehensive mapping
            competition_id_mapping = {}
            for key, data in all_found_competitions.items():
                if data["id"]:  # Only add if ID exists in constants
                    competition_id_mapping[data["actual_name"]] = data["id"]

            # Update class variable with comprehensive mapping
            if self.__class__._competition_mapping:
                self.__class__._competition_mapping.update(competition_id_mapping)
            else:
                self.__class__._competition_mapping = competition_id_mapping

            allure.attach(
                f"Created comprehensive mapping for {len(competition_id_mapping)} competitions with IDs",
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
            Competitions with IDs mapped: {len(self._competition_mapping)}
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

    @allure.story("Competitions")
    @allure.title("Validate competitions endpoint with query parameters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_competitions_endpoint_with_params(self, api_client):
        """
        Test that competitions endpoint accepts query parameters.
        """
        with allure.step("Test competitions endpoint with ID parameter"):
            competition_id = TEST_COMPETITIONS["premier_league"]

            # This endpoint accepts the parameter but may not filter
            response = api_client._make_request(
                "GET", f"/competitions?id={competition_id}"
            )

            assert (
                response.status_code == HTTPStatus.OK
            ), f"Expected {HTTPStatus.OK}, got {response.status_code}"

            allure.attach(
                response.text[:1000],
                name="Response with ID parameter",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Verify response structure"):
            response_text = response.text.strip()

            # Should be in the same format as the main competitions list
            assert (
                "{" in response_text and "}" in response_text
            ), "Response should contain competition list in braces"

            # Parse the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")
            competitions_str = response_text[start_idx + 1 : end_idx]
            competitions = [
                comp.strip() for comp in competitions_str.split(",") if comp.strip()
            ]

            assert len(competitions) > 0, "Should return competitions"

            allure.attach(
                f"Returned {len(competitions)} competitions\n"
                f"First 10: {', '.join(competitions[:10])}",
                name="Query Parameter Result",
                attachment_type=allure.attachment_type.TEXT,
            )
