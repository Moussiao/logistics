import os

from backend.core.settings.common import ROOT_DIR
from backend.core.settings.environ import env

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = env("STATIC_URL", cast=str, default="/static/")
STATIC_ROOT = os.path.join(ROOT_DIR, "www/static")
