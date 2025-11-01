# QA Automation Python Framework

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (optional):
```bash
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
DEVICE_TYPE=mweb pytest tests/e2e/
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

#### Common errors
1. OSError - run the command `rm -rf ~/.wdm` which clears the WebDriver cache and rerun the test.
#### Run tests
In order to be able to run the tests maybe chromedriver should be installed via homebrew also (MacOS: `brew install chromedriver`)
#### Reporting
In order to be able to run allure reporting you've to also install allure cli (MacOS: `brew install allure`)