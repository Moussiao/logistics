from src.core.settings.environ import env

BOT_TOKEN = env("BOT_TOKEN", cast=str)

TG_ORDERS_URL = env("TG_ORDERS_URL", cast=str)
