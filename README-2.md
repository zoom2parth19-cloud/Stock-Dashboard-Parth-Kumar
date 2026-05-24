# ⚡ StockMaster 3000 💹

> Real-time stock analysis web app built with Python + Streamlit. Its actually really good.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Working%20(mostly)-green)

---

## 🚀 What It Does

StockMaster 3000 is a stock market analysis dashboard I built for my CS class (and also because I wanted to). You type in any ticker symbol and it pulls **real live data** from Yahoo Finance and gives you:

- 📈 **Live price charts** — line, candlestick, and area charts
- ⚡ **Hyper-Trend™ Momentum Predictor** — my custom algorithm I invented (its a moving average but smarter)
- 🧠 **AI Analysis Engine** — analyzes signals and tells you if a stock looks bullish or bearish
- 📊 **Fundamental Data** — P/E ratio, market cap, revenue, all that stuff
- 🎨 **Dark mode terminal UI** — looks like a real Bloomberg terminal I think

---

## 🛠️ How To Run It

Make sure you have Python installed. Then:

```bash
# install the libraries
pip install streamlit yfinance plotly pandas

# run the app
streamlit run app.py
```

It will open in your browser automatically at `http://localhost:8501`. Thats it!!

---

## 📦 Requirements

```
streamlit
yfinance
plotly
pandas
```

Or just run `pip install streamlit yfinance plotly pandas` and youre good.

---

## 🖼️ Features

| Feature | Description |
|--------|-------------|
| 🚀 Dashboard | Overview with key metrics and price chart |
| 📈 Chart Lab | Candlestick and advanced charting |
| 🧠 AI Analyzer | Hyper-Trend™ signal + buy/sell analysis |
| 📊 Fundamentals | Company financials and valuation data |

---

## ⚠️ Disclaimer

This is NOT financial advice. I am a high school student who codes for fun. Please do not put your life savings into stocks because an app I made told you to. Do your own research!!

---

## 📝 Notes

- Data comes from Yahoo Finance via `yfinance` (free, no API key needed!!)
- The Hyper-Trend™ algorithm updates in real time
- Works with stocks, ETFs, crypto tickers, basically anything on Yahoo Finance
- Sometimes yfinance is slow, thats not my fault

---

i built it thanks
