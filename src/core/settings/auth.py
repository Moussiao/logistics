from src.core.settings.environ import env


AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    "axes.backends.AxesBackend",
    # Django ModelBackend is the default authentication backend.
    "django.contrib.auth.backends.ModelBackend",
]

# JWT
JWT_ALGORITHM = "HS256"
JWT_SECRET = env("JWT_SECRET", cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# django-axes
# https://django-axes.readthedocs.io/

AXES_LOCKOUT_PARAMETERS = ["username", "user_agent"]
AXES_RESET_ON_SUCCESS = True
AXES_FAILURE_LIMIT = 5
