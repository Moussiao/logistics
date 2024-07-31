from ninja import Router

from apps.delivery.api.endpoints.orders import router as orders_router
from apps.delivery.api.endpoints.partners import router as partners_router

router = Router()

router.add_router("/orders", orders_router)
router.add_router("/partners", partners_router)


__all__ = ("router",)
