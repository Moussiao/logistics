import django_stubs_ext
from split_settings.tools import include, optional

from core.settings.environ import env

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool)

# Application definition
_settings_modules_paths: tuple[str, ...] = (
    "auth.py",
    "celery.py",
    "common.py",
    "db.py",
    "environ.py",
    "http.py",
    "installed_apps.py",
    "middleware.py",
    "static.py",
    # Переопределение дефолтных настроек
    optional("local.py"),
)

# Внедряет указанный настройки из других Python-модулей
include(*_settings_modules_paths)
