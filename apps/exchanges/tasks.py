from celery.utils.log import get_task_logger

from apps.exchanges.exchange_clients import FetchAlphavantageQuotesStory
from config.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True)
def get_exchange_rates(self, base_asset: str, quote_asset: str) -> None:
    """
    Periodic task for getting exchange rates from Alphavantage
    """
    logger.info(
        "{} received args={}, kwargs={}".format(
            self.name, self.request.args, self.request.kwargs
        )
    )
    FetchAlphavantageQuotesStory(base_asset=base_asset, quote_asset=quote_asset).main()
