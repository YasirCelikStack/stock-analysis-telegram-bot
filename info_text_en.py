# info_text_en.py
INFO_TEXT = """
📚 <b>METRIC EXPLANATIONS</b>

This bot does two things:
1) Shows data (technical + fundamentals + financials)
2) Explains how to interpret them (this page)

────────────────────────
<b>📈 TECHNICAL</b>

<b>Close</b>:
• Daily closing price (end-of-day).

<b>MA30 / MA100 / MA200 (Moving Averages)</b>:
• Average of the last 30/100/200 daily closes.
• Price <b>above</b> MA → trend tends to be stronger ✅
• Price <b>below</b> MA → trend tends to be weaker ❌
• <b>MA200</b> is often used as a long-term trend filter.

<b>RSI(14)</b>:
• Momentum oscillator between 0–100.
• <b>RSI &gt; 70</b> → overbought
• <b>RSI &lt; 30</b> → oversold
• 40–60 is often neutral.

<b>MACD</b>:
• Measures trend + momentum.
• <b>MACD &gt; Signal</b> → positive momentum (bullish)
• <b>MACD &lt; Signal</b> → negative momentum (bearish)
• <b>Hist</b> = MACD − Signal (momentum strength)

────────────────────────
<b>🪪 OVERVIEW</b>

<b>Sector / Industry</b>:
• Company classification; helps compare with similar businesses.

<b>Beta</b>:
• Volatility vs the market.
• Beta ≈ 1 → similar to market
• Beta &gt; 1 → more volatile
• Beta &lt; 1 → less volatile

<b>52W Range</b>:
• Lowest and highest price over the last 52 weeks.

<b>Dividend Yield</b>:
• Approx. annual dividends / price (%).

────────────────────────
<b>🏦 FUNDAMENTALS</b>

<b>Current Ratio</b>:
• Short-term liquidity.
• Current Assets / Current Liabilities
• &lt; 1 can be risky; 1–2 is often healthy.

<b>Net Margin</b>:
• Net income / revenue (profitability).

<b>P/E</b>:
• Price / EPS (valuation).
• Higher can mean higher growth expectations (or more expensive).

<b>P/B</b>:
• Market value relative to book value.

────────────────────────
<b>📊 NET INCOME TABLES</b>

<b>Quarterly Net Income</b>:
• Company’s net profit/loss per quarter.

<b>Annual Net Income</b>:
• Net profit/loss per year.

────────────────────────
<b>🧩 PEER COMPARISON</b>

Peers = similar companies (sector + size).
• Compare your P/E and P/B vs peer averages.

✅ Tip: Run <code>/stock NVDA</code>
✅ Explanations: <code>/info</code>
"""

INFO_MAP = {
    "rsi": "📌 <b>RSI</b>: RSI &gt; 70 overbought, RSI &lt; 30 oversold.",
    "macd": "📌 <b>MACD</b>: MACD &gt; Signal bullish momentum; MACD &lt; Signal bearish.",
    "ma": "📌 <b>MA</b>: Price above MA often indicates stronger trend.",
    "pe": "📌 <b>P/E</b>: Price / EPS (valuation).",
    "pb": "📌 <b>P/B</b>: Market value / book value.",
    "currentratio": "📌 <b>Current Ratio</b>: Short-term liquidity (assets / liabilities).",
    "netmargin": "📌 <b>Net Margin</b>: Net income / revenue.",
    "peer": "📌 <b>Peers</b>: Compare valuation vs similar companies."
}
