from unittest.mock import patch

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

from apps.exchanges.constants import BTC, USD
from apps.exchanges.exchange_clients import FetchAlphavantageQuotesStory
from apps.exchanges.models import ExchangeRate
from apps.exchanges.tests.fartories import ExchangeRateFactory
from apps.exchanges.api.views import ExchangeRateCreateRetrieveView


class ExchangeRateCreateRetrieveViewTest(APITestCase):
    """Tests for ExchangeRateCreateRetrieve View"""

    @classmethod
    def setUpTestData(cls):
        """Data for tests"""
        ExchangeRateFactory.create_batch(size=10)
        api_key = APIKey.objects.create_key(name="test")
        cls.header = {"HTTP_AUTHORIZATION": "Api-Key " + str(api_key[1])}
        cls.url_reversed = reverse("api:exchanges:rate_create_retrieve")

    def test_retrieve_view_url_is_resolved(self):
        """Test case for correct url resolve for retrieve rate"""
        url = "/api/v1/quotes"
        response = self.client.get(url, **self.header)

        self.assertEqual(url, self.url_reversed)
        self.assertNotIn(
            response.status_code,
            [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_404_NOT_FOUND],
        )

    @patch.object(ExchangeRateCreateRetrieveView, "post", return_value=Response())
    def test_create_view_url_is_resolved(self, view_mock):
        """Test case for correct url resolve for retrieve rate"""
        url = "/api/v1/quotes"
        response = self.client.post(url, **self.header)
        self.assertEqual(url, self.url_reversed)
        self.assertTrue(view_mock.called)
        self.assertNotIn(response.status_code, [status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_404_NOT_FOUND])

    def test_get_rate__success(self):
        """Test case for success getting a rate"""
        response = self.client.get(self.url_reversed, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        last_rate_obj = ExchangeRate.objects.filter(base_asset=BTC, quote_asset=USD).order_by("-last_updated").first()
        self.assertEqual(response.data["rate"], str(last_rate_obj.rate))

    @patch.object(FetchAlphavantageQuotesStory, "main", return_value=ExchangeRateFactory())
    def test_create_rate__success(self, service_mock):
        response = self.client.post(self.url_reversed, **self.header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(service_mock.called)

    def test_get_rate__permission_error(self):
        """Error test case for getting a rate - permission denied"""
        response = self.client.get(self.url_reversed)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_rate__permission_error(self):
        """Error test case for creating a rate - permission denied"""
        response = self.client.post(self.url_reversed)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_rate__not_found_error(self):
        """Error test case for getting a rate - object not found"""
        ExchangeRate.objects.all().delete()
        response = self.client.get(self.url_reversed, **self.header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(FetchAlphavantageQuotesStory, "main", side_effect=APIException)
    def test_create_rate__error(self, service_mock):
        """Error test case for getting a rate - api error"""
        response = self.client.post(self.url_reversed, **self.header)
        self.assertTrue(service_mock.called)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("details", response.data)