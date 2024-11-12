from phonenumbers import (
    SUPPORTED_REGIONS,
    PhoneNumberFormat,
    example_number,
    format_number,
)
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from src.apps.delivery.api.schemas import (
    CustomerAddressRequest,
    CustomerRequest,
    OrderRequest,
)


class CustomerRequestFactory(ModelFactory[CustomerRequest]):
    SAFE_PHONE_NUMBER = "+79999999999"

    @classmethod
    def phone(cls) -> str:
        """
        Значение, которое будет проставлено в поле CustomerRequest.phone.

        Необходимо, так как происходит валидация номера при создании экземпляра.
        Используется example_number так как Faker может вернуть не валидный номер.
        """

        region_code = cls.__faker__.random_element(SUPPORTED_REGIONS)
        phone_info = example_number(region_code)
        if phone_info is None:
            return cls.SAFE_PHONE_NUMBER

        return format_number(phone_info, num_format=PhoneNumberFormat.E164)

    @classmethod
    def email(cls) -> str:
        return cls.__faker__.email()


class CustomerAddressRequestFactory(ModelFactory[CustomerAddressRequest]):
    @classmethod
    def country_code(cls) -> str:
        return cls.__faker__.country_code()


class OrderRequestFactory(ModelFactory[OrderRequest]):
    customer = Use(CustomerRequestFactory.build)
    customer_address = Use(CustomerAddressRequestFactory.build)


customer_request_factory = register_fixture(CustomerRequestFactory)
customer_address_request_factory = register_fixture(CustomerAddressRequestFactory)
order_request_factory = register_fixture(OrderRequestFactory)
