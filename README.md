# stock-analysis-telegram-bot
# 📊 Stock & ETF Analysis Telegram Bot (TR/EN)

A Telegram bot that provides **full analysis for US stocks & ETFs** using a single command.

It supports:
- ✅ Technical Analysis (MA30/100/200, RSI, MACD)
- ✅ Fundamental Metrics (Current Ratio, Net Margin, P/E, P/B)
- ✅ Company Overview (Sector/Industry, Beta, 52W Range, Dividend Yield)
- ✅ Net Income tables (Quarterly & Annual)
- ✅ Peer Comparison (P/E & P/B vs similar companies)
- ✅ TR/EN language support

Data sources:
- **Alpha Vantage** (Overview + Net Income / Fundamentals)
- **Financial Modeling Prep (FMP)** (price history, ratios, peers)

---

## ✨ Features

### 📌 Commands
| Command | Description |
|--------|-------------|
| `/start` | Start the bot |
| `/lang tr` | Switch to Turkish |
| `/lang en` | Switch to English |
| `/stock AAPL` | Full report (TA + Overview + FA + Net Income + Peer compare) |
| `/ta AAPL` | Technical analysis only |
| `/fa AAPL` | Fundamentals only |
| `/info` | Explanation of all metrics |
| `/info rsi` | Explanation for a specific metric |

---

## 🧠 Example Output

The `/stock NVDA` command returns:
- Technical indicators
- Company overview
- Fundamental ratios
- Quarterly & annual net income tables
- Peer valuation comparison

---

## 🛠️ Tech Stack
- Python 3.12+
- aiogram (Telegram Bot framework)
- httpx (API requests)
- dotenv (.env config)

---

## 📂 Project Structure

├── bot.py
├── formatters.py
├── indicators.py
├── av_service.py
├── fmp_service.py
├── i18n.py
├── info_text.py
├── info_text_en.py
├── requirements.txt
└── .env

---

## ✅ Installation

### 1) Clone the repository
git clone https://github.com/<your-username>/telegram-stock-analysis-bot.git
cd telegram-stock-analysis-bot
2) Install dependencies
python -m pip install -r requirements.txt
3) Create .env file
Create a .env file in the project root:

BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ALPHAVANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_KEY
FMP_API_KEY=YOUR_FMP_KEY
🔑 Getting API Keys
Telegram Bot Token
Open Telegram and message @BotFather

Use /newbot

Copy the bot token into .env

Alpha Vantage API Key (Free)
Create an account at Alpha Vantage

Copy your API Key into .env

Financial Modeling Prep (FMP) API Key
Create an account at Financial Modeling Prep

Copy your API Key into .env

▶️ Run the Bot
python bot.py
⚠️ Notes
Alpha Vantage free tier may have rate limits

Some FMP endpoints may be paid; the bot uses fallbacks where possible

Outputs are automatically split if Telegram message limit is exceeded

📌 Roadmap / Next Improvements
Add Free Cash Flow (FCF) analysis

News sentiment integration

Smart caching to reduce API calls

Alerts system (price or indicator-based)

📜 License
MIT License — feel free to use, modify and improve.

🤝 Credits
Built by Mr. Virtual 🚀
If you like it, feel free to ⭐ the repo and share feedback!
