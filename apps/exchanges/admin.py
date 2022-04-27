from django.contrib import admin
from apps.exchanges.models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    """
    Admin class for ExchangeRate model
    """

    list_display = (
        "rate",
        "base_asset",
        "quote_asset",
        "last_updated",
    )