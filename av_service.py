import os
import httpx

BASE = "https://www.alphavantage.co/query"


def get_av_key() -> str:
    key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not key:
        raise ValueError("ALPHAVANTAGE_API_KEY yok. .env dosyasına ekle.")
    return key


async def av_get(params: dict):
    params = dict(params)
    params["apikey"] = get_av_key()

    async with httpx.AsyncClient(timeout=25) as client:
        r = await client.get(BASE, params=params)
        r.raise_for_status()
        return r.json()


def _is_av_blocked(data: dict) -> bool:
    # Rate limit / hata mesajlarını yakala
    return any(k in data for k in ["Note", "Information", "Error Message"])


async def get_income_statement(symbol: str):
    """
    Alpha Vantage INCOME_STATEMENT:
    returns dict with 'annualReports' and 'quarterlyReports'
    each report contains 'fiscalDateEnding' and 'netIncome' (string)
    """
    data = await av_get({"function": "INCOME_STATEMENT", "symbol": symbol.upper()})

    if not isinstance(data, dict) or _is_av_blocked(data):
        return {"annual": [], "quarter": []}

    annual = data.get("annualReports") or []
    quarter = data.get("quarterlyReports") or []
    return {"annual": annual, "quarter": quarter}


async def get_overview(symbol: str) -> dict | None:
    """
    Alpha Vantage OVERVIEW:
    returns company overview fields like Sector, Industry, Beta, 52WeekHigh/Low, DividendYield, etc.
    """
    data = await av_get({"function": "OVERVIEW", "symbol": symbol.upper()})

    if not isinstance(data, dict) or _is_av_blocked(data):
        return None

    # AV bazen boş dict döndürebiliyor (yanlış sembol vs.)
    if not data:
        return None

    return data
