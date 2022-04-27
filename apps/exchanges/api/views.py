from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.exchanges.constants import BTC, USD
from apps.exchanges.exchange_clients import FetchAlphavantageQuotesStory
from apps.exchanges.models import ExchangeRate
from apps.exchanges.api.serializers import ExchangeRateCreateRetrieveSerializer


class ExchangeRateCreateRetrieveView(GenericAPIView):
    """View for getting exchange rate"""

    serializer_class = ExchangeRateCreateRetrieveSerializer
    queryset = ExchangeRate.objects.filter(base_asset=BTC, quote_asset=USD)
    service_class = FetchAlphavantageQuotesStory

    def get(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_queryset().first()
        if not instance:
            raise NotFound()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            instance = self.service_class(base_asset=BTC, quote_asset=USD).main()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"details": str(e)}, status.HTTP_422_UNPROCESSABLE_ENTITY)