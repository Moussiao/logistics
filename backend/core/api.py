from django.conf import settings
from ninja import NinjaAPI, Redoc
from ninja.security.base import AuthBase

from backend.apps.delivery.api import router as delivery_router
from backend.apps.security.api import router as security_router
from backend.apps.security.auth import AccessTokenAuth
from backend.apps.users.api import router as users_router

api_auth: tuple[AuthBase, ...] = (AccessTokenAuth(),)
if settings.DEBUG:
    from ninja.security import django_auth

    api_auth = (*api_auth, django_auth)


api = NinjaAPI(auth=api_auth, title="Logistic API", urls_namespace="api", docs=Redoc())

api.add_router("/auth", security_router)
api.add_router("/delivery", delivery_router)
api.add_router("/users", users_router)
