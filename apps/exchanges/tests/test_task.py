from unittest.mock import patch

from django.test import TestCase

from apps.exchanges.constants import BTC, USD
from apps.exchanges.exchange_clients import FetchAlphavantageQuotesStory
from apps.exchanges.tasks import get_exchange_rates


class GetExchangeRatesTaskTest(TestCase):
    """Tests for task get_exchange_rates"""

    @patch.object(FetchAlphavantageQuotesStory, "main")
    def test_get_exchange_rates_task__success(self, service_mock):
        """Test case for success running exchange rate"""
        get_exchange_rates(BTC, USD)
        service_mock.assert_called_once()
