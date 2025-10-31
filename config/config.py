import os
import json
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent

    ENV = os.getenv("TEST_ENV", "e2e")

    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    DEVICE_TYPE = os.getenv("DEVICE_TYPE", "desktop")

    PAGE_LOAD_TIMEOUT = 10

    @classmethod
    def load_environment_config(cls):
        env_file = cls.BASE_DIR / "config" / "environments.json"
        with open(env_file) as f:
            environments = json.load(f)
        return environments.get(cls.ENV, {})
