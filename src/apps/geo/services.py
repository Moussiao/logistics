import attr
from pycountry import countries
from pycountry.db import Country as CountryInfo

from src.apps.geo.models import Country


class InvalidCountryCodeError(Exception):
    pass


@attr.dataclass(slots=True, frozen=True)
class GetCountryByCode:
    _alpha_2_code: str

    def __call__(self) -> Country:
        try:
            country = Country.objects.get(code=self._alpha_2_code)
        except Country.DoesNotExist:
            country = self._create_country()

        return country

    def _create_country(self) -> Country:
        country_info = self._get_country_info()
        return Country.objects.create(code=country_info.alpha_2, name=country_info.name)

    def _get_country_info(self) -> CountryInfo:
        try:
            country = countries.get(alpha_2=self._alpha_2_code, default=None)
        except (KeyError, LookupError) as exc:
            raise InvalidCountryCodeError(f"{self._alpha_2_code} is invalid") from exc

        if country is None or not isinstance(country, CountryInfo):
            raise InvalidCountryCodeError(f"{self._alpha_2_code} is invalid")

        return country
