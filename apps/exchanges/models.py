from django.db import models
from django_extensions.db.models import TimeStampedModel


class ExchangeRate(TimeStampedModel):
    """Describes ExchangeRate Model"""

    rate = models.DecimalField(max_digits=16, decimal_places=8)
    base_asset = models.CharField(max_length=6)
    quote_asset = models.CharField(max_length=6)
    last_updated = models.DateTimeField()

    class Meta:
        ordering = ("-last_updated",)

    def __str__(self):
        return f"{self.base_asset} / {self.quote_asset} -- {self.rate} -- {self.last_updated}"





