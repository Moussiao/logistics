import os

from backend.core.settings.common import ROOT_DIR
from backend.core.settings.environ import env

MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = os.path.join(ROOT_DIR, "www/media")
