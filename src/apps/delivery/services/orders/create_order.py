from typing import TYPE_CHECKING, final

import attr
from django.db import transaction

from apps.delivery.models import Customer, CustomerAddress, Order, OrderProduct, Partner, Product
from apps.delivery.services.orders.exceptions import (
    DuplicateExternalIdOrderError,
    InvalidCountryCodeOrderError,
    PartnerNotExistsOrderError,
)
from apps.geo.models import City, Region
from apps.geo.services import GetCountryByCode, InvalidCountryCodeError

if TYPE_CHECKING:
    from apps.delivery.api.schemas import OrderRequest
    from apps.geo.models import Country


@final
@attr.dataclass(slots=True, frozen=True)
class CreateOrder:
    _order_schema: "OrderRequest"

    def __call__(self) -> Order:
        if Order.objects.filter(external_id=self._order_schema.external_id).exists():
            raise DuplicateExternalIdOrderError

        partner = self._get_partner()
        with transaction.atomic():
            country = self._get_or_create_country()
            customer = self._get_or_create_customer()
            customer_address = self._create_customer_address(country=country, customer=customer)

            order = self._create_order(
                partner=partner, customer=customer, customer_address=customer_address
            )
            self._set_products(order)

        return order

    def _get_partner(self) -> Partner:
        try:
            partner = Partner.objects.get(name=self._order_schema.partner)
        except Partner.DoesNotExist as exc:
            raise PartnerNotExistsOrderError from exc

        return partner

    def _get_or_create_country(self) -> "Country":
        """
        Возвращает страну на основе переданных при инициализации данных.

        Необходим как отдельный метод, так как могут быть переданы не валидные данные.
        Тем самым мы должны прервать логику создания заказа на этапе валидации.
        """

        country_code = self._order_schema.customer_address.country_code

        try:
            country = GetCountryByCode(country_code)()
        except InvalidCountryCodeError as exc:
            raise InvalidCountryCodeOrderError from exc

        return country

    def _get_or_create_customer(self) -> Customer:
        customer_schema = self._order_schema.customer
        customer, _x = Customer.objects.update_or_create(
            phone=customer_schema.phone,
            defaults={
                "name": customer_schema.name,
                "email": customer_schema.email,
                "gender": customer_schema.gender,
            },
        )
        return customer

    def _create_customer_address(
        self,
        country: "Country",
        customer: Customer,
    ) -> CustomerAddress:
        address_schema = self._order_schema.customer_address

        region, _x = Region.objects.get_or_create(country=country, name=address_schema.region_name)
        city, _x = City.objects.get_or_create(region=region, name=address_schema.city_name)

        return CustomerAddress.objects.create(
            customer=customer,
            country=country,
            region=region,
            city=city,
            postcode=address_schema.postcode or "",
            street=address_schema.street,
            house_number=address_schema.house_number,
            flat_number=address_schema.flat_number or "",
            comment=address_schema.comment or "",
        )

    def _create_order(
        self,
        partner: Partner,
        customer: Customer,
        customer_address: CustomerAddress,
    ) -> Order:
        total_price = sum(x.price * x.quantity for x in self._order_schema.products)

        return Order.objects.create(
            partner=partner,
            customer=customer,
            customer_address=customer_address,
            external_id=self._order_schema.external_id,
            external_verbose=self._order_schema.external_verbose or "",
            state=Order.State.NEW,
            expected_delivery_date=self._order_schema.expected_delivery_date,
            total_price=total_price,
            comment=self._order_schema.comment or "",
        )

    def _set_products(self, order: Order) -> None:
        for product_schema in self._order_schema.products:
            product, _x = Product.objects.get_or_create(
                name=product_schema.name, defaults={"price": product_schema.price}
            )

            order_product = OrderProduct(
                product=product,
                order=order,
                quantity=product_schema.quantity,
                total_price=product_schema.quantity * product_schema.price,
            )
            order_product.save()
