from requests import get
from fastapi import HTTPException
from datetime import datetime, timezone

from app.core.config import settings
from app.api.models.currency import Convert

_URL = "https://api.apilayer.com/currency_data"
_ROUTES = {
    "convert": "/convert",
    "list": "/list",
}
_HEADERS = {"apikey": settings.external_api_token}


async def convert(query: Convert) -> Convert:
    query_str = (
        f"?to={query.currency_to}&from={query.currency_from}&amount={query.amount}"
        + ("" if not query.date else f"&date={query.date.strftime('%Y-%m-%d')}")
    )

    response = get(_URL + _ROUTES["convert"] + query_str, headers=_HEADERS)
    if response.status_code != 200:
        raise HTTPException(response.status_code, detail=response.reason)

    result = response.json()
    query.result = float(result["result"])
    query.date = datetime.fromtimestamp(
        result["info"]["timestamp"], timezone.utc
    ).date()
    return query
