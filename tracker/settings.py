from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "local-classroom-demo"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ROOT_URLCONF = "tracker.urls"
INSTALLED_APPS = ["tracker"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "issues.sqlite3"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
