import factory
from django.utils import timezone
from factory import fuzzy
from factory.django import DjangoModelFactory

from apps.exchanges.constants import BTC, USD
from apps.exchanges.models import ExchangeRate


class ExchangeRateFactory(DjangoModelFactory):
    """
    Describes factory for ExchangeRate objects to quickly generate test
    """

    rate = fuzzy.FuzzyDecimal(0, 1000000)
    base_asset = BTC
    quote_asset = USD
    last_updated = factory.Faker(
        "past_datetime", tzinfo=timezone.get_current_timezone()
    )

    class Meta:
        model = ExchangeRate