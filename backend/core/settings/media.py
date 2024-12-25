from backend.core.settings.environ import env

MEDIA_URL = env("MEDIA_URL", default="/media/")
