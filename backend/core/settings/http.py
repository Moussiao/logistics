from backend.core.settings.environ import env

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", cast=str)

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", cast=str)


if env("DEBUG", cast=bool):
    import socket

    # https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
    # This might fail on some OS
    try:  # pragma: no cover
        INTERNAL_IPS = [
            "{}.1".format(ip[: ip.rfind(".")])
            for ip in socket.gethostbyname_ex(socket.gethostname())[2]
        ]
    except OSError:
        INTERNAL_IPS = []

    INTERNAL_IPS += ["127.0.0.1", "172.21.0.1"]
