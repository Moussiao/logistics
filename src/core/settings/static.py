from core.settings.environ import env

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = env("STATIC_URL", cast=str, default="/static/")
