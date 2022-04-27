from rest_framework import serializers

from apps.exchanges.models import ExchangeRate


class ExchangeRateCreateRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for ExchangeRateRetrieve View"""

    class Meta:
        model = ExchangeRate
        fields = (
            "base_asset",
            "quote_asset",
            "rate",
            "last_updated",
        )
        read_only_fields = (
            "base_asset",
            "quote_asset",
            "rate",
            "last_updated",
        )

