import pandas as pd


def compute_indicators(hist: list[dict]) -> dict:
    # hist: [{'date': '2026-01-19', 'close': 123.4}, ...]
    df = pd.DataFrame(hist)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")  # old->new

    close = df["close"]

    last = float(close.iloc[-1])
    ma30 = float(close.rolling(30).mean().iloc[-1])
    ma100 = float(close.rolling(100).mean().iloc[-1])
    ma200 = float(close.rolling(200).mean().iloc[-1])

    # RSI(14)
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    rsi14 = float((100 - (100 / (1 + rs))).iloc[-1])

    # MACD(12,26,9)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histo = macd - signal

    return {
        "close": last,
        "ma30": ma30,
        "ma100": ma100,
        "ma200": ma200,
        "rsi14": rsi14,
        "macd": float(macd.iloc[-1]),
        "macd_signal": float(signal.iloc[-1]),
        "macd_hist": float(histo.iloc[-1]),
    }
