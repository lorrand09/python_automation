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