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

## Short overview

1. Used Page Object Model for UI tests

## Notes

#### Common errors
1. OSError - run the command `rm -rf ~/.wdm` which clears the WebDriver cache and rerun the test.

