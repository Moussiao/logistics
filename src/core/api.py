from ninja import NinjaAPI

from apps.orders.api import router as orders_router

api = NinjaAPI(title="Logistic API", urls_namespace="api")

api.add_router("/", orders_router)
