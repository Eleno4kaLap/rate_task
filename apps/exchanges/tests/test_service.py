from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from requests import Session
from rest_framework.exceptions import APIException

from apps.exchanges.constants import BTC, USD
from apps.exchanges.exchange_clients import FetchAlphavantageQuotesStory, AlphavantageClient
from apps.exchanges.models import ExchangeRate
from apps.exchanges.tests.fartories import ExchangeRateFactory


class FetchAlphavantageQuotesStoryTest(TestCase):
    """Tests for FetchAlphavantageQuotesStory"""

    @classmethod
    def setUpTestData(cls):
        """Data for tests"""
        cls.service_class = FetchAlphavantageQuotesStory

    @patch.object(AlphavantageClient, "make_request")
    def test_fetch_quotes__success(self, make_request_mock):
        """Test case for success getting a rate"""
        rate_obj = ExchangeRateFactory.build()
        self.assertFalse(ExchangeRate.objects.filter(rate=rate_obj.rate, last_updated=rate_obj.last_updated))
        make_request_mock.return_value = {
            "Realtime Currency Exchange Rate": {
                "1. From_Currency Code": "BTC",
                "2. From_Currency Name": "Bitcoin",
                "3. To_Currency Code": "USD",
                "4. To_Currency Name": "United States Dollar",
                "5. Exchange Rate": rate_obj.rate,
                "6. Last Refreshed": datetime.strftime(rate_obj.last_updated, '%Y-%m-%d %H:%M:%S'),
                "7. Time Zone": "UTC",
                "8. Bid Price": "40575.00000000",
                "9. Ask Price": "40575.01000000"
            }
        }
        rate_db = self.service_class(base_asset=BTC, quote_asset=USD).main()
        self.assertEqual(rate_db.rate, rate_obj.rate)
        self.assertEqual(rate_db.last_updated, rate_obj.last_updated)

    @patch.object(Session, "get", side_effect=ConnectionError)
    def test_fetch_quotes__api_error(self, request_mock):
        """Error test case for getting a rate - API error"""
        self.assertRaises(APIException, self.service_class(base_asset=BTC, quote_asset=USD).main)
        self.assertTrue(request_mock.called)

    @patch.object(Session, "get")
    def test_fetch_quotes__error_status_code(self, request_mock):
        """Error test case for getting a rate - API returned status code != 200"""
        request_mock.status_code = 400
        self.assertRaises(APIException, self.service_class(base_asset=BTC, quote_asset=USD).main)
        self.assertTrue(request_mock.called)
