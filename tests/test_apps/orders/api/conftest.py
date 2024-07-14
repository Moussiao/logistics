from phonenumbers import (
    SUPPORTED_REGIONS,
    PhoneNumberFormat,
    example_number,
    format_number,
)
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from apps.orders.api.schemas import CustomerAddressInput, CustomerInput, OrderInput


class CustomerInputFactory(ModelFactory[CustomerInput]):
    SAFE_PHONE_NUMBER = "+79999999999"

    @classmethod
    def phone(cls) -> str:
        """
        Значение, которое будет проставлено в поле CustomerInput.phone.

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


class CustomerAddressInputFactory(ModelFactory[CustomerAddressInput]):
    @classmethod
    def country_code(cls) -> str:
        return cls.__faker__.country_code()


class OrderInputFactory(ModelFactory[OrderInput]):
    customer = Use(CustomerInputFactory.build)
    customer_address = Use(CustomerAddressInputFactory.build)


customer_input_factory = register_fixture(CustomerInputFactory)
customer_address_factory = register_fixture(CustomerAddressInputFactory)
order_input_factory = register_fixture(OrderInputFactory)
