import environ

from core.settings.common import BASE_DIR

__all__ = ("env",)

env = environ.Env(
    DEBUG=(bool, False),
)

env_path = BASE_DIR / ".env"

if env_path.exists():
    env.read_env(env_path)
