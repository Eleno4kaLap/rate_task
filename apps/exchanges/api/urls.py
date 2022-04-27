from django.urls import path

from apps.exchanges.api.views import ExchangeRateCreateRetrieveView

app_name = "exchanges"

urlpatterns = [
    path("", ExchangeRateCreateRetrieveView.as_view(), name="rate_create_retrieve"),
]