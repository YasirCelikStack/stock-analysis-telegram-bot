import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from i18n import t, set_lang, get_lang

from info_text import INFO_TEXT as INFO_TEXT_TR, INFO_MAP as INFO_MAP_TR
from info_text_en import INFO_TEXT as INFO_TEXT_EN, INFO_MAP as INFO_MAP_EN

from fmp_service import (
    get_prices,
    get_quote,
    get_profile,
    get_ratios_ttm,
    get_income_statement as fmp_income_statement,
    get_stock_peers,
)

from av_service import (
    get_income_statement as av_income_statement,
    get_overview,
)

from indicators import compute_indicators

from formatters import (
    format_ta,
    format_overview,
    format_fa,
    format_net_income_quarterly,
    format_net_income_annual,
    format_peer_compare,
    format_full,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()


def parse_symbol(text: str) -> str | None:
    parts = text.strip().split()
    if len(parts) < 2:
        return None
    return parts[1].upper()


def _avg(nums: list[float]) -> float | None:
    nums = [x for x in nums if x is not None]
    return sum(nums) / len(nums) if nums else None


def _pick_ratio(ratios: dict | None, *keys: str) -> float | None:
    if not ratios:
        return None
    for k in keys:
        v = ratios.get(k)
        if v is not None:
            try:
                return float(v)
            except Exception:
                pass
    return None


async def peer_valuation(sym: str, max_peers: int = 10) -> dict:
    peers = await get_stock_peers(sym)
    peers = [p for p in peers if isinstance(p, str)][:max_peers]

    pe_list: list[float] = []
    pb_list: list[float] = []

    for p in peers:
        r = await get_ratios_ttm(p)
        pe = _pick_ratio(r, "priceToEarningsRatioTTM", "peRatioTTM")
        pb = _pick_ratio(r, "priceToBookRatioTTM", "pbRatioTTM")
        if pe is not None:
            pe_list.append(pe)
        if pb is not None:
            pb_list.append(pb)

    return {
        "peers_used": len(peers),
        "pe_avg": _avg(pe_list),
        "pb_avg": _avg(pb_list),
    }


async def get_net_income_tables(sym: str):
    # 1) FMP dene (premium olabilir)
    q = await fmp_income_statement(sym, period="quarter", limit=12)
    y = await fmp_income_statement(sym, period="annual", limit=8)
    if q and y:
        return q, y

    # 2) Alpha Vantage fallback
    av = await av_income_statement(sym)
    av_q = av.get("quarter", [])
    av_y = av.get("annual", [])
    return (av_q[:12], av_y[:8])


@dp.message(Command("start"))
async def start(m: Message):
    user_id = m.from_user.id
    tg_code = getattr(m.from_user, "language_code", None)
    await m.answer(t(user_id, "START", tg_code), parse_mode="HTML")


@dp.message(Command("lang"))
async def lang_cmd(m: Message):
    user_id = m.from_user.id
    tg_code = getattr(m.from_user, "language_code", None)

    parts = (m.text or "").split()
    if len(parts) < 2:
        cur = get_lang(user_id, tg_code)
        return await m.answer(
            f"Usage: <code>/lang tr</code> or <code>/lang en</code>\nCurrent: <b>{cur}</b>",
            parse_mode="HTML",
        )

    lang = parts[1].lower().strip()
    set_lang(user_id, lang)
    await m.answer(t(user_id, "LANG_SET", tg_code, lang=lang), parse_mode="HTML")


@dp.message(Command("info"))
async def info_cmd(m: Message):
    user_id = m.from_user.id
    tg_code = getattr(m.from_user, "language_code", None)
    lang = get_lang(user_id, tg_code)

    if lang == "tr":
        INFO_TEXT = INFO_TEXT_TR
        INFO_MAP = INFO_MAP_TR
    else:
        INFO_TEXT = INFO_TEXT_EN
        INFO_MAP = INFO_MAP_EN

    parts = (m.text or "").strip().split(maxsplit=1)

    # /info rsi gibi parametreli ise tek mesaj
    if len(parts) > 1:
        key = parts[1].strip().lower().replace("/", "").replace(" ", "")
        txt = INFO_MAP.get(key)

        if not txt:
            return await m.answer(
                "Unknown metric 😄\n\n"
                "Examples:\n"
                "<code>/info</code>\n"
                "<code>/info rsi</code>\n"
                "<code>/info macd</code>\n"
                "<code>/info ma</code>\n"
                "<code>/info pe</code>\n"
                "<code>/info pb</code>\n",
                parse_mode="HTML",
            )

        return await m.answer(txt, parse_mode="HTML")

    # /info full (uzun) ise iki parçaya böl
    text = INFO_TEXT.strip()

    split_marker = "────────────────────────"
    chunks = text.split(split_marker)

    if len(chunks) >= 2:
        part1 = (chunks[0] + split_marker + chunks[1]).strip()
        part2 = (split_marker.join(chunks[2:])).strip()
        if not part2:
            mid = len(text) // 2
            part1, part2 = text[:mid], text[mid:]
    else:
        mid = len(text) // 2
        part1, part2 = text[:mid], text[mid:]

    await m.answer(part1.strip(), parse_mode="HTML")
    await m.answer(part2.strip(), parse_mode="HTML")


@dp.message(Command("ta"))
async def ta_cmd(m: Message):
    sym = parse_symbol(m.text or "")
    if not sym:
        return await m.answer("Usage: <code>/ta AAPL</code>", parse_mode="HTML")

    user_id = m.from_user.id
    tg_code = getattr(m.from_user, "language_code", None)
    lang = get_lang(user_id, tg_code)

    try:
        hist = await get_prices(sym)
        ind = compute_indicators(hist)
        await m.answer(format_ta(sym, ind, lang=lang), parse_mode="HTML")
    except Exception as e:
        await m.answer(f"Hata: {e}")


@dp.message(Command("fa"))
async def fa_cmd(m: Message):
    sym = parse_symbol(m.text or "")
    if not sym:
        return await m.answer("Usage: <code>/fa AAPL</code>", parse_mode="HTML")

    user_id = m.from_user.id
    tg_code = getattr(m.from_user, "language_code", None)
    lang = get_lang(user_id, tg_code)

    try:
        quote = await get_quote(sym)
        profile = await get_profile(sym)
        ratios = await get_ratios_ttm(sym)
        await m.answer(format_fa(sym, quote, profile, ratios, lang=lang), parse_mode="HTML")
    except Exception as e:
        await m.answer(f"Hata: {e}")


@dp.message(Command("stock"))
async def stock_cmd(m: Message):
    sym = parse_symbol(m.text or "")
    if not sym:
        return await m.answer("Usage: <code>/stock AAPL</code>", parse_mode="HTML")

    user_id = m.from_user.id
    tg_code = getattr(m.from_user, "language_code", None)
    lang = get_lang(user_id, tg_code)

    try:
        # 1) Teknik
        hist = await get_prices(sym)
        ind = compute_indicators(hist)
        ta_txt = format_ta(sym, ind, lang=lang)

        # 2) Overview
        ov = await get_overview(sym)
        ov_txt = format_overview(sym, ov, lang=lang)

        # 3) Temel + Degerleme
        quote = await get_quote(sym)
        profile = await get_profile(sym)
        ratios = await get_ratios_ttm(sym)
        fa_txt = format_fa(sym, quote, profile, ratios, lang=lang)

        # 4) Net kar tabloları
        ni_q, ni_y = await get_net_income_tables(sym)
        niq_txt = format_net_income_quarterly(ni_q, max_rows=8, lang=lang)
        niy_txt = format_net_income_annual(ni_y, max_rows=5, lang=lang)

        # 5) Peer
        my_pe = _pick_ratio(ratios, "priceToEarningsRatioTTM", "peRatioTTM")
        my_pb = _pick_ratio(ratios, "priceToBookRatioTTM", "pbRatioTTM")

        peer = await peer_valuation(sym, max_peers=10)
        peer_txt = format_peer_compare(
            my_pe=my_pe,
            my_pb=my_pb,
            peer_pe_avg=peer["pe_avg"],
            peer_pb_avg=peer["pb_avg"],
            peers_used=peer["peers_used"],
            lang=lang,
        )

        full = format_full(ta_txt, ov_txt, fa_txt, niq_txt, niy_txt, peer_txt)

        # Telegram limit koruması
        if len(full) > 3800:
            await m.answer(format_full(ta_txt, ov_txt, fa_txt), parse_mode="HTML")
            await m.answer(format_full(niq_txt, niy_txt, peer_txt), parse_mode="HTML")
        else:
            await m.answer(full, parse_mode="HTML")

    except Exception as e:
        await m.answer(f"Hata: {e}")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN yok. .env dosyasina ekle.")
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
