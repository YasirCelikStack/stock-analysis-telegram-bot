import os
import httpx

BASE = "https://financialmodelingprep.com"


def get_fmp_key() -> str:
    key = os.getenv("FMP_API_KEY")
    if not key:
        raise ValueError("FMP_API_KEY yok. .env dosyasına ekle.")
    return key


async def fmp_get(path: str, params: dict | None = None):
    params = params or {}
    params["apikey"] = get_fmp_key()

    url = f"{BASE}{path}"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)

        # 402 = endpoint ücretli -> bot patlamasın
        if r.status_code == 402:
            return {"__paid__": True}

        r.raise_for_status()
        return r.json()


async def get_prices(symbol: str, limit: int = 260) -> list[dict]:
    data = await fmp_get("/stable/historical-price-eod/full", {"symbol": symbol.upper()})

    if isinstance(data, dict) and data.get("__paid__"):
        raise ValueError("Fiyat endpoint'i bile ücretli görünüyor (çok garip).")

    if not isinstance(data, list) or not data:
        raise ValueError("Fiyat verisi bulunamadı (stable endpoint boş döndü).")

    return data[:limit]


async def get_quote(symbol: str) -> dict | None:
    data = await fmp_get("/stable/quote-short", {"symbol": symbol.upper()})
    if isinstance(data, dict) and data.get("__paid__"):
        return None
    if not data:
        return None
    return data[0]


async def get_profile(symbol: str) -> dict | None:
    data = await fmp_get("/stable/profile", {"symbol": symbol.upper()})
    if isinstance(data, dict) and data.get("__paid__"):
        return None
    if not data:
        return None
    return data[0]


async def get_ratios_ttm(symbol: str) -> dict | None:
    try:
        data = await fmp_get("/stable/ratios-ttm", {"symbol": symbol.upper()})
        if isinstance(data, dict) and data.get("__paid__"):
            return None
        if not data:
            return None
        return data[0]
    except Exception:
        return None


async def get_income_statement(symbol: str, period: str = "annual", limit: int = 12) -> list[dict]:
    """
    FMP income statement (premium olabilir). Premium ise [] döner.
    """
    data = await fmp_get(
        "/stable/income-statement",
        {"symbol": symbol.upper(), "period": period, "limit": limit},
    )

    if isinstance(data, dict) and data.get("__paid__"):
        return []

    if not isinstance(data, list):
        return []
    return data


async def get_stock_peers(symbol: str) -> list[str]:
    data = await fmp_get("/stable/stock-peers", {"symbol": symbol.upper()})

    if isinstance(data, dict) and data.get("__paid__"):
        return []

    if isinstance(data, dict):
        peers = data.get("peersList") or data.get("peers") or []
        return [p for p in peers if isinstance(p, str)]

    if isinstance(data, list):
        return [p for p in data if isinstance(p, str)]

    return []
