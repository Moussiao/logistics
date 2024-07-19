from .customer import CustomerInput, CustomerOutput
from .customer_address import CustomerAddressInput, CustomerAddressOutput
from .order import (
    CreateOrderOutput,
    DetailOrderOutput,
    OrderInput,
    OrderOutput,
    OrdersFilters,
    OrdersOutput,
)
from .partner import PartnerOutput, PartnersFilters, PartnersOutput
from .product import ProductInput

__all__ = (
    "CustomerInput",
    "CustomerOutput",
    "CustomerAddressInput",
    "CustomerAddressOutput",
    "CreateOrderOutput",
    "DetailOrderOutput",
    "OrderInput",
    "OrderOutput",
    "OrdersFilters",
    "OrdersOutput",
    "PartnerOutput",
    "PartnersFilters",
    "PartnersOutput",
    "ProductInput",
)
