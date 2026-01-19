# i18n.py
from __future__ import annotations
from typing import Dict

# kullanıcı dilini RAM'de tutalım (MVP)
USER_LANG: Dict[int, str] = {}

STRINGS = {
    "tr": {
        "START": "Hoş geldiniz. \n\nKomutlar:\n/stock AAPL → FULL rapor\n/info → metrik açıklamaları\n/lang tr|en → dil seç",
        "INFO_TITLE": "📚 <b>BOT METRİK AÇIKLAMALARI</b>",
        "UNKNOWN_INFO": "Bu metrik için bilgi bulamadım.",
        "USAGE_INFO": "Kullanım: <code>/info</code> veya <code>/info rsi</code>",
        "LANG_SET": "Dil ayarlandı: <b>{lang}</b>",
    },
    "en": {
        "START": "Welcome. \n\nCommands:\n/stock AAPL → FULL report\n/info → metric explanations\n/lang tr|en → set language",
        "INFO_TITLE": "📚 <b>METRIC EXPLANATIONS</b>",
        "UNKNOWN_INFO": "I couldn't find info for that metric.",
        "USAGE_INFO": "Usage: <code>/info</code> or <code>/info rsi</code>",
        "LANG_SET": "Language set: <b>{lang}</b>",
    }
}

def get_lang(user_id: int, tg_code: str | None = None) -> str:
    # kullanıcı seçtiyse onu kullan
    if user_id in USER_LANG:
        return USER_LANG[user_id]
    # telegram dili
    if tg_code:
        tg = tg_code.lower()
        if tg.startswith("tr"):
            return "tr"
        if tg.startswith("en"):
            return "en"
    # default
    return "en"

def set_lang(user_id: int, lang: str):
    lang = lang.lower()
    if lang not in STRINGS:
        lang = "en"
    USER_LANG[user_id] = lang

def t(user_id: int, key: str, tg_code: str | None = None, **kwargs) -> str:
    lang = get_lang(user_id, tg_code)
    s = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
    if kwargs:
        return s.format(**kwargs)
    return s
