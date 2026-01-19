INFO_TEXT = """
📚 <b>BOT METRİK AÇIKLAMALARI</b>

Bu bot sana iki şey yapar:
1) Veriyi verir (teknik + temel + finansal)
2) Verinin anlamını öğretir (bu sayfa)

────────────────────────
<b>📈 TEKNİK ANALİZ</b>

<b>Close</b>:
• Günlük kapanış fiyatı. (Gün içi değil, gün sonu “son söz” gibi.)

<b>MA30 / MA100 / MA200 (Hareketli Ortalamalar)</b>:
• Son 30/100/200 gün kapanış fiyatlarının ortalaması.
• Fiyat MA'nın <b>üstündeyse</b> genelde trend güçlü ✅
• Fiyat MA'nın <b>altındaysa</b> genelde zayıflık ❌
• <b>MA200</b> uzun vade trend filtresi gibi düşünülür.

<b>RSI(14)</b>:
• 0–100 arası momentum göstergesi.
• <b>RSI &gt; 70</b> → aşırı alım (çok hızlı yükselmiş olabilir)
• <b>RSI &lt; 30</b> → aşırı satım (çok hızlı düşmüş olabilir)
• 40–60 arası genelde nötr.

<b>MACD</b>:
• Trend + momentum ölçer.
• <b>MACD &gt; Signal</b> → momentum pozitif (bullish)
• <b>MACD &lt; Signal</b> → momentum negatif (bearish)
• <b>Hist</b> (Histogram) = MACD − Signal
  Hist artıyorsa momentum güçleniyor, düşüyorsa zayıflıyor.

────────────────────────
<b>🪪 OVERVIEW (ŞİRKET KİMLİĞİ)</b>

<b>Sector / Industry</b>:
• Şirketin hangi sektörde olduğunu gösterir (örn: Technology / Semiconductors).
• Kıyas yaparken “aynı sektör mü?” sorusunu cevaplar.

<b>Beta</b>:
• Hissenin piyasaya (genelde S&amp;P 500 gibi) göre oynaklığını ölçer.
• Beta ≈ 1 → piyasa kadar oynak
• Beta &gt; 1 → piyasadan daha oynak (daha agresif)
• Beta &lt; 1 → daha sakin

<b>52W Range</b>:
• Son 52 haftadaki (1 yıl) en düşük ve en yüksek fiyat aralığı.
• Fiyat aralığın üst bandına yakınsa: “yıl içi zirve bölgesi”
• Alt bandına yakınsa: “yıl içi dip bölgesi”

<b>Dividend Yield</b>:
• Temettü verimi. Yıllık temettünün fiyata oranı (yaklaşık %).
• %0.02 gibi çok düşükse: şirket temettüden çok büyüme/buyback odaklı olabilir.

────────────────────────
<b>🏦 TEMEL ANALİZ</b>

<b>Price</b>:
• Anlık/son fiyat. (Kaynağa göre kapanıştan küçük fark olabilir.)

<b>Current Ratio (Cari Oran)</b>:
• Kısa vadeli borç ödeme gücü.
• Formül: Dönen Varlıklar / Kısa Vadeli Borçlar
• <b>1’in altı</b> → kısa vadede daha riskli olabilir
• <b>1–2</b> → genelde sağlıklı
• Çok yüksek (3+) → “para kasada fazla duruyor” yorumu da yapılabilir.

<b>Net Margin (Net Kâr Marjı)</b>:
• Satışların yüzde kaçı net kâr kaldı?
• Örn: %25 → 100$ satıştan 25$ net kâr.
• Yüksek olması güçlü fiyatlama + verimli operasyon göstergesi olabilir.

<b>F/K (P/E)</b>:
• Kârına göre pahalı mı ucuz mu?
• Formül: Hisse fiyatı / Hisse başı kâr (EPS)
• Yüksek F/K → büyüme beklentisi yüksek olabilir
• Aşırı yüksek → pahalı olabilir (risk artar)

<b>PD/DD (P/B)</b>:
• Defter değerine göre pahalı mı?
• Formül: Piyasa değeri / Defter değeri
• Banka/sigorta gibi sektörlerde daha kritik,
  teknoloji hisselerinde yüksek çıkması daha normal.

────────────────────────
<b>📊 NET KÂR TABLOLARI</b>

<b>Net Kâr (Çeyreklik)</b>:
• Her çeyrek (3 ay) sonunda şirketin toplam net kârı/zararı.
• Trend yükseliyorsa: kârlılık büyüyor; düşüyorsa baskı olabilir.
• “Tek çeyrek” yanıltabilir — birkaç çeyrek birlikte okunur.

<b>Net Kâr (Yıllık)</b>:
• Yılın toplam net kârı/zararı.
• Şirketin uzun vadeli kârlılık hikayesini görürsün.

────────────────────────
<b>🧩 PEER KIYAS</b>

<b>Peer</b> = benzer şirketler (aynı sektör + benzer büyüklük gibi).
• Amaç: “Bu hisse pahalı mı?” sorusunu tek başına değil,
  benzerleriyle karşılaştırarak cevaplamak.

Botta şunu görürsün:
• “F/K: senin değer | peer ort”
• “PD/DD: senin değer | peer ort”

Eğer peer set 0 gelirse:
• veri kaynağı o sembol için peer listesi döndürmemiş olabilir
• ya da rate limit/endpoint kısıtı vardır

✅ İpucu: Verileri gör: <code>/stock NVDA</code>
✅ Metrik açıklaması: <code>/info</code>
"""

INFO_MAP = {
    "close": "📌 <b>Close</b>: Günlük kapanış fiyatı.",
    "ma": "📌 <b>MA</b>: Fiyat MA'nın üstündeyse trend güçlü; altındaysa zayıflık.",
    "rsi": "📌 <b>RSI</b>: RSI &gt; 70 aşırı alım, RSI &lt; 30 aşırı satım. 40–60 nötr.",
    "macd": "📌 <b>MACD</b>: MACD &gt; Signal pozitif momentum; MACD &lt; Signal negatif momentum.",
    "sector": "📌 <b>Sector/Industry</b>: Şirketin sektör kimliği; kıyas için temel.",
    "beta": "📌 <b>Beta</b>: Piyasaya göre oynaklık. 1=market, &gt;1 daha agresif, &lt;1 daha sakin.",
    "52w": "📌 <b>52W Range</b>: Son 1 yılın dip-zirve fiyat aralığı.",
    "dividend": "📌 <b>Dividend Yield</b>: Temettü verimi (%).",
    "currentratio": "📌 <b>Current Ratio</b>: Dönen varlıklar / kısa vadeli borçlar. 1–2 genelde sağlıklı.",
    "netmargin": "📌 <b>Net Margin</b>: Net kâr / ciro. %25 = 100$ satıştan 25$ net kâr.",
    "pe": "📌 <b>F/K (P/E)</b>: Fiyat / EPS. Çok yüksekse pahalı olabilir.",
    "pb": "📌 <b>PD/DD (P/B)</b>: Piyasa değeri / defter değeri.",
    "netincome": "📌 <b>Net Kâr</b>: Şirketin dönem sonunda elde ettiği net kâr/zarar.",
    "peer": "📌 <b>Peer kıyas</b>: Benzer şirket ortalamalarına göre pahalı/ucuz kıyası."
}
