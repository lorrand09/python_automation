# QA Automation Python Framework

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create .env file inside root

4. Install Dependencies
```bash
pip install -r requirements.txt
```
5. Generate your RAPID_API key from [rapidapi football URL](https://rapidapi.com/GiulianoCrescimbeni/api/football98/) and save it under a new `.env` file

6. Update .env file:
```
API_KEY=your_actual_api_key_here
```
6. Set environment variables (optional):
```
export TEST_ENV=e2e
export BROWSER=chrome
export DEVICE_TYPE=desktop
export HEADLESS=false
```

## Running Tests

### All tests:
```bash
pytest
```

### Frontend tests only:
```bash
pytest tests/e2e/
```

### API tests only:
```bash
pytest tests/api/ -m api
```

### Smoke tests:
```bash
pytest -m smoke
```

### Mobile web tests:
```bash
DEVICE_TYPE=mobile pytest tests/e2e/
```

### Headless mode:
```bash
HEADLESS=true pytest
```

## Viewing Reports

### Generate and view Allure report:
```bash
allure serve reports/allure-results
```
### Pass argument after pytest run tests command: 
```
--alluredir=reports/allure-results
```

### Generate static report:
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

## Project Structure

- `config/` - Configuration files and environment settings
- `drivers/` - Browsers related drivers
- `pages/` - Page Object Model classes and selectors
- `tests/` - Test cases
- `utils/` - Utility functions and helpers
- `test_data/` - Test data files
- `reports/` - Test execution reports

## Short overview

1. Use Page Object Model for UI tests
2. Use Allure for reporting
3. Use fixtures for test setup/teardown
4. Keep tests independent 
5. Update test data files instead of hardcoding values

## Notes

Never commit your .env file to version control (it's in .gitignore) !

#### Common errors
OSError (on Mac OS with M-chip processor):
```bash
# Clear the cache
rm -rf ~/.wdm/

# Reinstall webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager --upgrade
```
#### Run tests
In order to be able to run the tests maybe chromedriver should be installed via homebrew also (MacOS: `brew install chromedriver`)
#### Reporting
In order to be able to run allure reporting you've to also install allure cli (MacOS: `brew install allure`)

## Test Cases

| Test ID | Test Name | Type | File | Priority | Description |
|---------|-----------|------|------|----------|-------------|
| TC-001 | test_get_competitions_list | API | test_competitions.py | Critical | Validates competitions endpoint response structure and data quality |
| TC-002 | test_verify_major_competitions | API | test_competitions.py | Normal | Verifies presence of major leagues and tournaments in response |
| TC-003 | test_search_streamer | E2E | test_basic_search.py | Critical | Verifies search functionality for streamers while logged out |

### Coverage Summary

| Feature | API Tests | E2E Tests | Total |
|--------|-----------|-----------|-------|
| Football Competitions | 2 | 0 | 2 |
| Search | 0 | 1 | 1 |
| **Total** | **2** | **1** | **3** |

## Test Validations

### TC-001: test_get_competitions_list
**Validations Used:**
- **Status Code (200)** - Ensures API is accessible and responding correctly
- **Response Format (curly braces)** - Validates expected data structure `{comp1,comp2,comp3}`
- **Minimum Count (≥50)** - Confirms sufficient data is returned for meaningful testing
- **Name Format Check** - Data integrity - alphanumeric characters required
- **Duplicate Detection (<10%)** - Identifies data quality issues while allowing minor duplicates (the API has issues on duplicates)

**Why:** These validations ensure the API is functional and returns properly formatted data.

### TC-002: test_verify_major_competitions
**Validations Used:**
- **Pattern Matching** - Uses multiple patterns per competition for robust detection
- **Required Leagues (5/5)** - All major European leagues must be present
- **Minimum Tournaments (≥2/3)** - Flexible validation allowing for seasonal availability
- **Coverage Check (≥75%)** - Ensures most expected competitions are found
- **ID Mapping Creation** - Validates that competitions can be mapped to their IDs for future use

**Why:** Confirms that critical competitions are available and properly identifiable, ensuring the API meets minimum content requirements.

### TC-003: test_search_streamer
**Validations Used:**
- **Page Load Waits** - Ensures elements are ready before interaction (prevents flaky tests)
- **UI Element Interactions** - Validates browse button, search input, and suggestion clicks work
- **Scroll Validation**
- **Navigation Flow** - Verifies complete user journey from home → search → streamer page
- **Screenshot Capture** - Visual proof of successful test completion

**Why:** Validates the critical user flow for content discovery, ensuring users can find and access streamer content without authentication.