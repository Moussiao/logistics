from ninja import NinjaAPI
from ninja.security import django_auth

from apps.orders.api import router as orders_router

api = NinjaAPI(auth=django_auth, title="Logistic API", urls_namespace="api")

api.add_router("/", orders_router)
