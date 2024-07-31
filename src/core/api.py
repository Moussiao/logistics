from django.conf import settings
from ninja import NinjaAPI

from apps.delivery.api import router as delivery_router
from apps.security.api import router as security_router
from apps.security.auth import AccessTokenAuth

api_auth = (AccessTokenAuth(),)
if settings.DEBUG:
    from ninja.security import django_auth

    api_auth = (django_auth, *api_auth)


api = NinjaAPI(auth=api_auth, title="Logistic API", urls_namespace="api")

api.add_router("/auth", security_router)
api.add_router("/delivery", delivery_router)
