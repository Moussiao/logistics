from django.conf import settings
from ninja import NinjaAPI, Redoc

from src.apps.delivery.api import router as delivery_router
from src.apps.security.api import router as security_router
from src.apps.security.auth import AccessTokenAuth
from src.apps.users.api import router as users_router

api_auth = (AccessTokenAuth(),)
if settings.DEBUG:
    from ninja.security import django_auth

    api_auth = (*api_auth, django_auth)


api = NinjaAPI(auth=api_auth, title="Logistic API", urls_namespace="api", docs=Redoc())

api.add_router("/auth", security_router)
api.add_router("/delivery", delivery_router)
api.add_router("/users", users_router)
