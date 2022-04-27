import logging
from datetime import datetime
from typing import Dict, Any

import pytz
import requests
from django.conf import settings
from rest_framework.exceptions import APIException

from apps.exchanges.constants import ALPHAVANTAGE_GET_RATE_FUNCTION
from apps.exchanges.models import ExchangeRate

logger = logging.getLogger(__name__)


class AlphavantageClient:
    """Client for Alphavantage requests"""

    base_url = "https://www.alphavantage.co/query"

    def __init__(self) -> None:
        headers = {
            "Accepts": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(headers)

    def make_request(self, parameters: Dict[str, str]) -> Dict[str, Any]:
        """Makes request with the parameters.
        """
        logger.info(
            f"Class={__class__.__name__}, method={self.make_request.__name__}, parameters={parameters}"
        )
        parameters["apikey"] = settings.ALPHAVANTAGE_API_KEY

        try:
            response = self.session.get(self.base_url, params=parameters)
            data = response.json()
            if response.status_code != 200:
                msg = f"An error occurred while try to call {response.request.url}: status_code={response.status_code}," \
                      f" response={response.text}"
                logger.error(msg)
                raise APIException(msg)
            if "Error Message" in data:
                logger.error(data["Error Message"])
                raise APIException(data["Error Message"])

            logger.info(f"Response data from {response.request.url}: {data}")
            return data
        except Exception as e:
            logger.exception(str(e))
            raise APIException(str(e))


class FetchAlphavantageQuotesStory:
    """Gets exchange rates from Alphavantage and store they in DB"""

    exchange_client_class = AlphavantageClient

    def __init__(self, base_asset: str, quote_asset: str) -> None:
        self.base_asset = base_asset
        self.quote_asset = quote_asset

    def main(self) -> ExchangeRate:
        rate = self.get_rate(base_asset=self.base_asset, quote_asset=self.quote_asset)
        rate_obj = self.save_rate(rate)
        return rate_obj

    @staticmethod
    def _get_aware_datetime(unaware_datetime: str, tz: str) -> datetime:
        """Gets date with timezone"""
        timezone = pytz.timezone(tz)
        date = datetime.strptime(unaware_datetime, "%Y-%m-%d %H:%M:%S")
        return timezone.localize(date)

    def get_rate(self, base_asset: str, quote_asset: str) -> Dict[str, str]:
        """Gets rate from Alphavantage API"""
        response = self.exchange_client_class().make_request(parameters={"function": ALPHAVANTAGE_GET_RATE_FUNCTION,
                                                                         "from_currency": base_asset,
                                                                         "to_currency": quote_asset})
        rate = {
            "rate": response["Realtime Currency Exchange Rate"]["5. Exchange Rate"],
            "base_asset": base_asset,
            "quote_asset": quote_asset,
            "last_updated": self._get_aware_datetime(
                unaware_datetime=response["Realtime Currency Exchange Rate"]["6. Last Refreshed"],
                tz=response["Realtime Currency Exchange Rate"]["7. Time Zone"]
            )
        }
        return rate

    @staticmethod
    def save_rate(rate: Dict[str, str]) -> ExchangeRate:
        """Creates ExchangeRate object in DB"""
        return ExchangeRate.objects.create(**rate)

