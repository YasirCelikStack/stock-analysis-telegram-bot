def _yesno(cond: bool) -> str:
    return "✅" if cond else "❌"


LABELS = {
    "tr": {
        "TECH": "TEKNIK",
        "OVERVIEW": "OVERVIEW",
        "FUND": "TEMEL",
        "RATIOS": "TTM Oranlar",
        "VALUATION": "Degerleme",
        "CLOSE": "Close",
        "PRICE": "Price",
        "NO_DATA": "Veri yok",
        "NET_Q": "Net Kar (Ceyreklik)",
        "NET_Y": "Net Kar (Yillik)",
        "PEER": "Peer Kiyas",
        "PEER_NONE": "Peer kiyas verisi su an hesaplanamadi.",
        "PEER_SET": "Peer set",
    },
    "en": {
        "TECH": "TECHNICAL",
        "OVERVIEW": "OVERVIEW",
        "FUND": "FUNDAMENTALS",
        "RATIOS": "TTM Ratios",
        "VALUATION": "Valuation",
        "CLOSE": "Close",
        "PRICE": "Price",
        "NO_DATA": "No data",
        "NET_Q": "Quarterly Net Income",
        "NET_Y": "Annual Net Income",
        "PEER": "Peer Comparison",
        "PEER_NONE": "Peer comparison is not available right now.",
        "PEER_SET": "Peer set",
    }
}


def L(lang: str, key: str) -> str:
    lang = "en" if lang not in LABELS else lang
    return LABELS[lang].get(key, LABELS["en"].get(key, key))


def format_ta(symbol: str, ind: dict, lang: str = "tr") -> str:
    close = ind["close"]
    ma30, ma100, ma200 = ind["ma30"], ind["ma100"], ind["ma200"]

    return (
        f"📈 <b>{symbol.upper()} — {L(lang,'TECH')}</b>\n"
        f"{L(lang,'CLOSE')}: <b>{close:.2f}</b>\n\n"
        f"MA30:  {ma30:.2f}  {_yesno(close > ma30)}\n"
        f"MA100: {ma100:.2f} {_yesno(close > ma100)}\n"
        f"MA200: {ma200:.2f} {_yesno(close > ma200)}\n\n"
        f"RSI(14): <b>{ind['rsi14']:.1f}</b>\n"
        f"MACD: {ind['macd']:.3f}\n"
        f"Signal: {ind['macd_signal']:.3f}\n"
        f"Hist: {ind['macd_hist']:.3f}\n"
    )


def format_overview(symbol: str, ov: dict | None, lang: str = "tr") -> str:
    if not ov:
        return f"🪪 <b>{symbol.upper()} — {L(lang,'OVERVIEW')}</b>\n{L(lang,'NO_DATA')}"

    sector = ov.get("Sector")
    industry = ov.get("Industry")
    beta = ov.get("Beta")
    high_52 = ov.get("52WeekHigh")
    low_52 = ov.get("52WeekLow")
    div_yield = ov.get("DividendYield")

    lines = [f"🪪 <b>{symbol.upper()} — {L(lang,'OVERVIEW')}</b>"]

    if sector or industry:
        s = sector or "?"
        i = industry or "?"
        lines.append(f"Sector/Industry: <b>{s}</b> • <b>{i}</b>")

    if beta not in [None, "", "None"]:
        try:
            lines.append(f"Beta: <b>{float(beta):.2f}</b>")
        except Exception:
            pass

    if high_52 not in [None, "", "None"] and low_52 not in [None, "", "None"]:
        try:
            lines.append(f"52W Range: <b>{float(low_52):.2f}</b> – <b>{float(high_52):.2f}</b>")
        except Exception:
            pass

    if div_yield not in [None, "", "None"]:
        try:
            dy = float(div_yield) * 100
            lines.append(f"Dividend Yield: <b>{dy:.2f}%</b>")
        except Exception:
            pass

    return "\n".join(lines)


def format_fa(symbol: str, quote: dict | None, profile: dict | None, ratios: dict | None, lang: str = "tr") -> str:
    name = (profile or {}).get("companyName") or symbol.upper()
    price = (quote or {}).get("price")

    lines = [f"🏦 <b>{name} — {L(lang,'FUND')}</b>"]
    if price is not None:
        lines.append(f"{L(lang,'PRICE')}: <b>{float(price):.2f}</b>")

    if ratios:
        def pick(*keys):
            for k in keys:
                v = ratios.get(k)
                if v is not None:
                    return v
            return None

        current_ratio = pick("currentRatioTTM")
        net_margin = pick("netProfitMarginTTM")

        pe = pick("priceToEarningsRatioTTM", "peRatioTTM")
        pb = pick("priceToBookRatioTTM", "pbRatioTTM")

        lines.append("")
        lines.append(f"📌 <b>{L(lang,'RATIOS')}</b>")
        if current_ratio is not None:
            lines.append(f"Current Ratio: <b>{float(current_ratio):.2f}</b>")
        if net_margin is not None:
            lines.append(f"Net Margin: <b>{float(net_margin)*100:.1f}%</b>")

        lines.append("")
        lines.append(f"💸 <b>{L(lang,'VALUATION')}</b>")
        if pe is not None:
            lines.append(f"P/E: <b>{float(pe):.2f}</b>" if lang == "en" else f"F/K (P/E): <b>{float(pe):.2f}</b>")
        if pb is not None:
            lines.append(f"P/B: <b>{float(pb):.2f}</b>" if lang == "en" else f"PD/DD (P/B): <b>{float(pb):.2f}</b>")
    else:
        lines.append(f"\n({L(lang,'NO_DATA')})")

    return "\n".join(lines)


def _extract_date(row: dict) -> str:
    return row.get("date") or row.get("fiscalDateEnding") or row.get("calendarYear") or "?"


def _extract_year(row: dict) -> str:
    y = row.get("calendarYear")
    if y:
        return str(y)
    d = row.get("date") or row.get("fiscalDateEnding") or ""
    return d[:4] if len(d) >= 4 else "?"


def _extract_net_income(row: dict):
    ni = row.get("netIncome")
    if ni is None:
        return None
    try:
        return float(ni)
    except Exception:
        return None


def format_net_income_quarterly(rows: list[dict], max_rows: int = 8, lang: str = "tr") -> str:
    if not rows:
        return f"📊 <b>{L(lang,'NET_Q')}</b>\n{L(lang,'NO_DATA')}"

    lines = [f"📊 <b>{L(lang,'NET_Q')}</b>"]
    for r in rows[:max_rows]:
        date = _extract_date(r)
        ni = _extract_net_income(r)
        if ni is None:
            continue
        ni_b = ni / 1_000_000_000
        sign = "🟢" if ni >= 0 else "🔴"
        lines.append(f"{date}: {sign} <b>{ni_b:.2f}B</b>")
    return "\n".join(lines)


def format_net_income_annual(rows: list[dict], max_rows: int = 5, lang: str = "tr") -> str:
    if not rows:
        return f"📈 <b>{L(lang,'NET_Y')}</b>\n{L(lang,'NO_DATA')}"

    lines = [f"📈 <b>{L(lang,'NET_Y')}</b>"]
    for r in rows[:max_rows]:
        year = _extract_year(r)
        ni = _extract_net_income(r)
        if ni is None:
            continue
        ni_b = ni / 1_000_000_000
        sign = "🟢" if ni >= 0 else "🔴"
        lines.append(f"{year}: {sign} <b>{ni_b:.2f}B</b>")
    return "\n".join(lines)


def format_peer_compare(
    my_pe: float | None,
    my_pb: float | None,
    peer_pe_avg: float | None,
    peer_pb_avg: float | None,
    peers_used: int,
    lang: str = "tr"
) -> str:
    lines = [f"🧩 <b>{L(lang,'PEER')}</b>"]

    if my_pe is not None and peer_pe_avg is not None:
        if lang == "en":
            lines.append(f"P/E: <b>{my_pe:.2f}</b> | Peer avg: <b>{peer_pe_avg:.2f}</b>")
        else:
            lines.append(f"F/K: <b>{my_pe:.2f}</b> | Peer ort: <b>{peer_pe_avg:.2f}</b>")

    if my_pb is not None and peer_pb_avg is not None:
        if lang == "en":
            lines.append(f"P/B: <b>{my_pb:.2f}</b> | Peer avg: <b>{peer_pb_avg:.2f}</b>")
        else:
            lines.append(f"PD/DD: <b>{my_pb:.2f}</b> | Peer ort: <b>{peer_pb_avg:.2f}</b>")

    if len(lines) == 1:
        lines.append(L(lang, "PEER_NONE"))

    lines.append(f"({L(lang,'PEER_SET')}: {peers_used})")
    return "\n".join(lines)


def format_full(*blocks: str) -> str:
    blocks = [b for b in blocks if b and b.strip()]
    return "\n\n".join(blocks)
