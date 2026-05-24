import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================================
# STOCKMASTER 3000 - by me
# started this project on a friday night lol
# its actually really good i think
# ============================================================

# This sets up the page!! Very important do not delete
st.set_page_config(
    page_title="StockMaster 3000 💹",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THE CSS STYLES (i learned this from youtube)
# makes everything look super professional
# ============================================================
st.markdown("""
<style>
    /* import a cool font from google */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    /* dark background like a real trading terminal */
    .stApp {
        background-color: #050510;
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(0, 255, 180, 0.04) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 20%, rgba(0, 200, 255, 0.06) 0%, transparent 50%);
    }

    /* the main title style */
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.2em;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ffb4, #00c8ff, #00ffb4);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s linear infinite;
        letter-spacing: 4px;
        padding: 10px 0;
        text-shadow: none;
    }

    @keyframes shimmer {
        to { background-position: 200% center; }
    }

    /* subtitle */
    .subtitle {
        font-family: 'Share Tech Mono', monospace;
        text-align: center;
        color: #00ffb4;
        font-size: 0.9em;
        letter-spacing: 3px;
        opacity: 0.7;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* the metric cards - i made these myself */
    .metric-card {
        background: linear-gradient(135deg, #0a0a2e 0%, #0d1f1a 100%);
        border: 1px solid #00ffb4;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 180, 0.15), inset 0 0 30px rgba(0, 255, 180, 0.03);
        margin-bottom: 10px;
        font-family: 'Share Tech Mono', monospace;
    }

    .metric-label {
        color: #00ffb4;
        font-size: 0.75em;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    .metric-value {
        color: #ffffff;
        font-size: 2em;
        font-weight: bold;
        font-family: 'Orbitron', monospace;
        margin: 5px 0;
    }

    .metric-delta-up {
        color: #00ffb4;
        font-size: 0.85em;
    }

    .metric-delta-down {
        color: #ff4466;
        font-size: 0.85em;
    }

    /* the analysis box - this is my fav part */
    .analysis-box {
        background: linear-gradient(135deg, #0a1628 0%, #0a2010 100%);
        border: 2px solid #00c8ff;
        border-radius: 10px;
        padding: 25px;
        font-family: 'Share Tech Mono', monospace;
        color: #e0e0e0;
        line-height: 1.8;
        box-shadow: 0 0 30px rgba(0, 200, 255, 0.1);
        margin: 15px 0;
    }

    .analysis-box h3 {
        color: #00c8ff;
        font-family: 'Orbitron', monospace;
        letter-spacing: 2px;
    }

    /* sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #08081e;
        border-right: 1px solid rgba(0, 255, 180, 0.3);
    }

    /* make the sidebar text look cool */
    [data-testid="stSidebar"] .stMarkdown {
        font-family: 'Share Tech Mono', monospace;
        color: #00ffb4;
    }

    /* input boxes */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background-color: #0a0a2e !important;
        color: #00ffb4 !important;
        border: 1px solid #00ffb4 !important;
        font-family: 'Share Tech Mono', monospace !important;
        border-radius: 4px !important;
    }

    /* the buttons */
    .stButton button {
        background: linear-gradient(90deg, #00ffb4, #00c8ff) !important;
        color: #050510 !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        border: none !important;
        padding: 10px 30px !important;
        border-radius: 4px !important;
        transition: all 0.3s !important;
    }

    .stButton button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 180, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    /* section headers */
    h2, h3 {
        font-family: 'Orbitron', monospace !important;
        color: #00ffb4 !important;
        letter-spacing: 2px;
    }

    /* the glowing divider line thing */
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00ffb4, #00c8ff, #00ffb4, transparent);
        margin: 25px 0;
        opacity: 0.6;
    }

    /* momentum indicator box */
    .momentum-box {
        background: linear-gradient(135deg, #0f0a28 0%, #0a1a10 100%);
        border: 1px solid rgba(0, 255, 180, 0.4);
        border-radius: 8px;
        padding: 20px;
        font-family: 'Share Tech Mono', monospace;
        margin: 10px 0;
    }

    /* footer */
    .footer {
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        color: rgba(0, 255, 180, 0.4);
        font-size: 0.75em;
        padding: 20px;
        letter-spacing: 2px;
        border-top: 1px solid rgba(0, 255, 180, 0.1);
        margin-top: 40px;
    }

    /* hide streamlit default stuff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* make tabs look cool */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #08081e;
        border-bottom: 1px solid #00ffb4;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', monospace;
        color: #00ffb4;
        letter-spacing: 1px;
    }

    /* scrollbar (small detail but looks sick) */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #050510; }
    ::-webkit-scrollbar-thumb { background: #00ffb4; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# THE SIDEBAR - navigation and settings
# i copied the idea from a youtube video but coded it myself
# ============================================================
with st.sidebar:
    st.markdown("## 💹 StockMaster 3000")
    st.markdown("---")

    # This is where the user picks what page they want!!
    st.markdown("### 🗺️ Navigation")
    page = st.radio(
        "Go to:",
        ["🚀 Dashboard", "📈 Chart Lab", "🧠 AI Analyzer", "📊 Fundamentals", "⚙️ About"]
    )

    st.markdown("---")

    # The stock ticker input!! This is really important
    st.markdown("### 🔍 Stock Lookup")
    ticker_input = st.text_input(
        "Enter Ticker Symbol:",
        value="TSLA",
        help="Try TSLA, AAPL, NVDA, SPY, etc"
    ).upper()

    # Time period selector
    st.markdown("### 📅 Time Period")
    time_period = st.selectbox(
        "Select Period:",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3,
        format_func=lambda x: {
            "1mo": "1 Month",
            "3mo": "3 Months",
            "6mo": "6 Months",
            "1y": "1 Year",
            "2y": "2 Years",
            "5y": "5 Years"
        }[x]
    )

    st.markdown("---")
    st.markdown("### ⚡ Options")
    show_volume = st.checkbox("Show Volume", value=True)
    show_momentum = st.checkbox("Show Hyper-Trend™", value=True)
    show_ma50 = st.checkbox("Show 50-Day MA", value=True)

    st.markdown("---")
    # my credit lol
    st.markdown("""
    <div style='font-family: Share Tech Mono; color: rgba(0,255,180,0.5); font-size:0.75em; text-align:center;'>
    i built it thanks
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FETCHING THE DATA FROM THE INTERNET!!!
# yfinance is so cool it gets real stock prices
# this took me like 2 hours to figure out
# ============================================================
@st.cache_data(ttl=300)  # this saves the data so it doesnt reload every second (learned this from stackoverflow)
def get_stock_data(ticker, period):
    """Gets all the stock info we need. Returns None if ticker is bad"""
    try:
        # Create the stock object
        stock = yf.Ticker(ticker)

        # Get the history data (this is the prices over time)
        history = stock.history(period=period)

        # Get general info about the company
        info = stock.info

        return history, info
    except Exception as e:
        # If something goes wrong we return None
        return None, None


# ============================================================
# THE HYPER-TREND MOMENTUM PREDICTOR™
# this is my custom algorithm i invented
# it uses advanced mathematical calculations
# (its a moving average but i made it sound cooler)
# ============================================================
def calculate_hyper_trend_momentum(price_data, window=10):
    """
    THE HYPER-TREND MOMENTUM PREDICTOR™
    Proprietary algorithm for detecting market momentum shifts.
    Uses multi-dimensional price vector analysis.
    (ok its actually just a 10-day moving average but it works really well)
    """
    # Calculate the "Hyper-Trend" value (moving average)
    hyper_trend = price_data['Close'].rolling(window=window).mean()

    # Calculate momentum score (price divided by the trend line)
    # if this is above 1.0 then price is above the trend = good signal
    momentum_score = price_data['Close'] / hyper_trend

    # Signal strength - how far above/below the trend we are (as percentage)
    signal_strength = (momentum_score - 1.0) * 100

    return hyper_trend, momentum_score, signal_strength


# ============================================================
# THE ANALYSIS ENGINE!!!
# this uses ADVANCED AI LOGIC to analyze stocks
# (its actually just if/else statements but they work great)
# ============================================================
def run_ai_analysis(current_price, ma_50, ma_200, volume, avg_volume, signal_strength, ticker):
    """
    Runs the proprietary StockMaster 3000 AI analysis algorithm.
    Uses multiple technical indicators to generate a signal.
    (i got the logic from investopedia lol)
    """

    # Start building the analysis report
    signals = []
    bullish_count = 0
    bearish_count = 0

    # CHECK 1: Is price above the 50 day moving average??
    if current_price > ma_50:
        signals.append("✅ Price is ABOVE the 50-day moving average — BULLISH signal detected!")
        bullish_count += 1
    else:
        signals.append("⚠️ Price is BELOW the 50-day moving average — bearish pressure present")
        bearish_count += 1

    # CHECK 2: Golden cross or death cross check (learned about this on reddit)
    if ma_50 > ma_200:
        signals.append("✅ GOLDEN CROSS confirmed — 50MA above 200MA — historically very bullish!")
        bullish_count += 1
    else:
        signals.append("⚠️ Death cross pattern — 50MA below 200MA — proceed with caution")
        bearish_count += 1

    # CHECK 3: Volume check - is more people trading than usual?
    if volume > avg_volume * 1.5:
        signals.append("✅ HIGH VOLUME detected — 50%+ above average — strong conviction in move!")
        bullish_count += 1 if current_price > ma_50 else 0
        bearish_count += 1 if current_price < ma_50 else 0
    elif volume < avg_volume * 0.7:
        signals.append("ℹ️ Low volume — market conviction is weak right now")
    else:
        signals.append("ℹ️ Volume is normal — no unusual activity detected")

    # CHECK 4: The Hyper-Trend™ momentum signal!!!
    if signal_strength > 3:
        signals.append(f"✅ HYPER-TREND™ Signal: +{signal_strength:.1f}% above trend — MAXIMUM MOMENTUM!")
        bullish_count += 2  # extra points because this is the best indicator
    elif signal_strength > 0:
        signals.append(f"✅ HYPER-TREND™ Signal: +{signal_strength:.1f}% above trend — positive momentum")
        bullish_count += 1
    elif signal_strength < -3:
        signals.append(f"⚠️ HYPER-TREND™ Signal: {signal_strength:.1f}% below trend — DANGER ZONE!")
        bearish_count += 2
    else:
        signals.append(f"⚠️ HYPER-TREND™ Signal: {signal_strength:.1f}% below trend — weak momentum")
        bearish_count += 1

    # NOW GENERATE THE FINAL VERDICT based on the signals
    # this is the most important part!!
    total_signals = bullish_count + bearish_count
    bull_ratio = bullish_count / total_signals if total_signals > 0 else 0.5

    if bull_ratio >= 0.75:
        verdict = f"🚀🚀🚀 STRONG BUY — {ticker} IS GOING TO THE MOON!! ALL SYSTEMS GREEN!!"
        verdict_color = "#00ffb4"
        rating = "STRONG BUY"
    elif bull_ratio >= 0.55:
        verdict = f"🚀 BUY THE DIP — {ticker} looking good!! Hyper-Trend™ agrees. WAGMI!!"
        verdict_color = "#00ff88"
        rating = "BUY"
    elif bull_ratio == 0.5:
        verdict = f"😐 HOLD — {ticker} mixed signals. Diamond hands time. HODL until clarity."
        verdict_color = "#ffcc00"
        rating = "HOLD"
    elif bull_ratio >= 0.25:
        verdict = f"⚠️ CAUTION — {ticker} showing weakness. Maybe wait for a better entry..."
        verdict_color = "#ff8844"
        rating = "CAUTION"
    else:
        verdict = f"🔴 BEARISH WARNING — {ticker} not looking great rn. Dip buy opportunity maybe?"
        verdict_color = "#ff4466"
        rating = "BEARISH"

    return signals, verdict, verdict_color, rating


# ============================================================
# MAIN APP STARTS HERE!!!
# everything above was just setup
# ============================================================

# The big title at the top
st.markdown('<div class="main-title">⚡ STOCKMASTER 3000 ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">[ REAL-TIME MARKET INTELLIGENCE SYSTEM v3.0.0 ]</div>', unsafe_allow_html=True)
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# Load the data!!! This is the most important function call
with st.spinner(f"📡 Downloading {ticker_input} data from the internet..."):
    history_data, stock_info = get_stock_data(ticker_input, time_period)

# Check if we got real data or if the ticker was wrong
if history_data is None or history_data.empty:
    st.error(f"❌ ERROR: Could not find ticker '{ticker_input}'. Please check the symbol and try again!")
    st.info("💡 Try: TSLA, AAPL, NVDA, MSFT, AMZN, SPY, QQQ")
    st.stop()  # stop the app from running if theres no data

# Calculate all the stuff we need
# DO NOT TOUCH THIS SECTION IT BREAKS EVERYTHING
current_price = history_data['Close'].iloc[-1]
prev_price = history_data['Close'].iloc[-2]
price_change = current_price - prev_price
price_change_pct = (price_change / prev_price) * 100

# calculate moving averages
# these are CRITICAL for the analysis
ma_50 = history_data['Close'].rolling(window=50).mean().iloc[-1] if len(history_data) >= 50 else history_data['Close'].mean()
ma_200 = history_data['Close'].rolling(window=200).mean().iloc[-1] if len(history_data) >= 200 else history_data['Close'].mean()

# volume stuff
current_volume = history_data['Volume'].iloc[-1]
avg_volume = history_data['Volume'].mean()

# Run the Hyper-Trend algorithm!!!
hyper_trend, momentum_score, signal_strength = calculate_hyper_trend_momentum(history_data)
current_signal_strength = signal_strength.iloc[-1] if not pd.isna(signal_strength.iloc[-1]) else 0

# Get company name if we have it
company_name = stock_info.get('longName', ticker_input) if stock_info else ticker_input
company_name_display = company_name[:35] + "..." if len(company_name) > 35 else company_name


# ============================================================
# DASHBOARD PAGE
# ============================================================
if page == "🚀 Dashboard":
    st.markdown(f"## 🏢 {company_name_display} ({ticker_input})")

    # The metric cards row - shows the most important numbers
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta_color = "metric-delta-up" if price_change >= 0 else "metric-delta-down"
        delta_arrow = "▲" if price_change >= 0 else "▼"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Current Price</div>
            <div class="metric-value">${current_price:.2f}</div>
            <div class="{delta_color}">{delta_arrow} {abs(price_change):.2f} ({abs(price_change_pct):.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # 52 week high and low
        high_52 = history_data['High'].max()
        low_52 = history_data['Low'].min()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 Period High/Low</div>
            <div class="metric-value" style="font-size:1.3em;">${high_52:.2f}</div>
            <div class="metric-delta-down">LOW: ${low_52:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        vol_status = "📈 HIGH" if volume_ratio > 1.5 else ("📉 LOW" if volume_ratio < 0.7 else "➡️ NORMAL")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📦 Volume</div>
            <div class="metric-value" style="font-size:1.2em;">{current_volume/1e6:.1f}M</div>
            <div class="metric-delta-up">{vol_status} ({volume_ratio:.1f}x avg)</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        ht_color = "metric-delta-up" if current_signal_strength >= 0 else "metric-delta-down"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚡ Hyper-Trend™</div>
            <div class="metric-value" style="font-size:1.4em;">{momentum_score.iloc[-1]:.3f}</div>
            <div class="{ht_color}">SIGNAL: {current_signal_strength:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # Quick summary chart on dashboard
    st.markdown("## 📈 Price Overview")

    # Build the chart with plotly (way better than the default streamlit chart)
    fig_main = go.Figure()

    # The main price line - color based on if stock went up or down
    line_color = "#00ffb4" if price_change >= 0 else "#ff4466"
    fig_main.add_trace(go.Scatter(
        x=history_data.index,
        y=history_data['Close'],
        name="Close Price",
        line=dict(color=line_color, width=2),
        fill='tozeroy',
        fillcolor=f"rgba(0, 255, 180, 0.05)" if price_change >= 0 else "rgba(255, 68, 102, 0.05)"
    ))

    # 50 day moving average line
    if show_ma50 and len(history_data) >= 50:
        ma50_line = history_data['Close'].rolling(window=50).mean()
        fig_main.add_trace(go.Scatter(
            x=history_data.index,
            y=ma50_line,
            name="50-Day MA",
            line=dict(color="#ffcc00", width=1.5, dash="dash"),
        ))

    # Hyper-Trend line!!!
    if show_momentum:
        fig_main.add_trace(go.Scatter(
            x=history_data.index,
            y=hyper_trend,
            name="Hyper-Trend™ (10D)",
            line=dict(color="#00c8ff", width=1.5, dash="dot"),
        ))

    # Make the chart look like a real trading terminal
    fig_main.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(5, 5, 16, 0.8)',
        font=dict(family='Share Tech Mono', color='#00ffb4'),
        xaxis=dict(
            gridcolor='rgba(0, 255, 180, 0.1)',
            color='#00ffb4',
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='rgba(0, 255, 180, 0.1)',
            color='#00ffb4',
            showgrid=True,
            tickprefix='$'
        ),
        legend=dict(
            bgcolor='rgba(5, 5, 16, 0.8)',
            bordercolor='rgba(0, 255, 180, 0.3)',
            borderwidth=1
        ),
        hovermode='x unified',
        height=400,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_main, use_container_width=True)

    # Volume chart below the price chart
    if show_volume:
        st.markdown("## 📦 Volume")
        vol_colors = ['#00ffb4' if c >= o else '#ff4466'
                      for c, o in zip(history_data['Close'], history_data['Open'])]

        fig_vol = go.Figure(go.Bar(
            x=history_data.index,
            y=history_data['Volume'],
            marker_color=vol_colors,
            opacity=0.7,
            name="Volume"
        ))
        fig_vol.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(5, 5, 16, 0.8)',
            font=dict(family='Share Tech Mono', color='#00ffb4'),
            xaxis=dict(gridcolor='rgba(0, 255, 180, 0.1)', color='#00ffb4'),
            yaxis=dict(gridcolor='rgba(0, 255, 180, 0.1)', color='#00ffb4'),
            height=200,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_vol, use_container_width=True)


# ============================================================
# CHART LAB PAGE
# this is where you can see the candlestick chart
# i learned about candlesticks from tiktok actually
# ============================================================
elif page == "📈 Chart Lab":
    st.markdown(f"## 📈 Chart Lab — {ticker_input}")
    st.markdown("*Advanced charting tools for serious traders (like me)*")

    # Chart type selector
    chart_type = st.radio(
        "Chart Type:",
        ["🕯️ Candlestick", "📈 Line Chart", "⛰️ Area Chart"],
        horizontal=True
    )

    fig_lab = go.Figure()

    if chart_type == "🕯️ Candlestick":
        # Candlestick chart!! These look so professional
        fig_lab.add_trace(go.Candlestick(
            x=history_data.index,
            open=history_data['Open'],
            high=history_data['High'],
            low=history_data['Low'],
            close=history_data['Close'],
            name=ticker_input,
            increasing_line_color='#00ffb4',
            decreasing_line_color='#ff4466',
            increasing_fillcolor='rgba(0, 255, 180, 0.3)',
            decreasing_fillcolor='rgba(255, 68, 102, 0.3)'
        ))

    elif chart_type == "📈 Line Chart":
        fig_lab.add_trace(go.Scatter(
            x=history_data.index,
            y=history_data['Close'],
            line=dict(color='#00ffb4', width=2),
            name="Close"
        ))

    else:  # Area chart
        fig_lab.add_trace(go.Scatter(
            x=history_data.index,
            y=history_data['Close'],
            fill='tozeroy',
            line=dict(color='#00c8ff', width=2),
            fillcolor='rgba(0, 200, 255, 0.1)',
            name="Close"
        ))

    # Always add the moving averages on top
    if show_ma50 and len(history_data) >= 50:
        fig_lab.add_trace(go.Scatter(
            x=history_data.index,
            y=history_data['Close'].rolling(50).mean(),
            name="50 MA",
            line=dict(color='#ffcc00', width=1.5, dash='dash')
        ))

    if len(history_data) >= 200:
        fig_lab.add_trace(go.Scatter(
            x=history_data.index,
            y=history_data['Close'].rolling(200).mean(),
            name="200 MA",
            line=dict(color='#ff8844', width=1.5, dash='dot')
        ))

    # Hyper-Trend on the lab chart too
    if show_momentum:
        fig_lab.add_trace(go.Scatter(
            x=history_data.index,
            y=hyper_trend,
            name="⚡Hyper-Trend™",
            line=dict(color='#cc44ff', width=2)
        ))

    fig_lab.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(5, 5, 16, 0.9)',
        font=dict(family='Share Tech Mono', color='#00ffb4'),
        xaxis=dict(gridcolor='rgba(0, 255, 180, 0.1)', color='#00ffb4', rangeslider=dict(visible=False)),
        yaxis=dict(gridcolor='rgba(0, 255, 180, 0.1)', color='#00ffb4', tickprefix='$'),
        legend=dict(bgcolor='rgba(5,5,16,0.8)', bordercolor='rgba(0,255,180,0.3)', borderwidth=1),
        hovermode='x unified',
        height=550,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_lab, use_container_width=True)

    # Price stats table
    st.markdown("### 📊 Price Statistics")
    col1, col2 = st.columns(2)
    with col1:
        stats_data = {
            "Metric": ["Open (Latest)", "High (Latest)", "Low (Latest)", "Close (Latest)", "Volume (Latest)"],
            "Value": [
                f"${history_data['Open'].iloc[-1]:.2f}",
                f"${history_data['High'].iloc[-1]:.2f}",
                f"${history_data['Low'].iloc[-1]:.2f}",
                f"${history_data['Close'].iloc[-1]:.2f}",
                f"{history_data['Volume'].iloc[-1]:,.0f}"
            ]
        }
        st.dataframe(pd.DataFrame(stats_data), hide_index=True, use_container_width=True)

    with col2:
        stats_data2 = {
            "Metric": ["Period High", "Period Low", "Avg Volume", "50-Day MA", "Price Change"],
            "Value": [
                f"${history_data['High'].max():.2f}",
                f"${history_data['Low'].min():.2f}",
                f"{history_data['Volume'].mean():,.0f}",
                f"${ma_50:.2f}",
                f"{price_change_pct:+.2f}%"
            ]
        }
        st.dataframe(pd.DataFrame(stats_data2), hide_index=True, use_container_width=True)


# ============================================================
# THE AI ANALYZER PAGE!!!
# this is definitely the coolest feature
# uses advanced AI logic (if/else statements)
# ============================================================
elif page == "🧠 AI Analyzer":
    st.markdown(f"## 🧠 AI Analysis Engine — {ticker_input}")
    st.markdown("*Powered by the StockMaster Hyper-Trend™ Algorithm*")

    # Run the analysis!!!
    signals, verdict, verdict_color, rating = run_ai_analysis(
        current_price, ma_50, ma_200, current_volume, avg_volume, current_signal_strength, ticker_input
    )

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # Show the Hyper-Trend chart
    st.markdown("### ⚡ Hyper-Trend™ Momentum Visualizer")

    fig_ht = go.Figure()

    # The signal strength line (above zero = bullish, below = bearish)
    signal_colors = ['#00ffb4' if v >= 0 else '#ff4466' for v in signal_strength.dropna()]
    fig_ht.add_trace(go.Bar(
        x=signal_strength.dropna().index,
        y=signal_strength.dropna().values,
        marker_color=signal_colors,
        name="Hyper-Trend Signal™",
        opacity=0.8
    ))

    # Zero line reference
    fig_ht.add_hline(y=0, line_color="rgba(255,255,255,0.3)", line_width=1)
    fig_ht.add_hline(y=3, line_color="#00ffb4", line_width=1, line_dash="dot",
                     annotation_text="Strong Bull Zone", annotation_font_color="#00ffb4")
    fig_ht.add_hline(y=-3, line_color="#ff4466", line_width=1, line_dash="dot",
                     annotation_text="Danger Zone", annotation_font_color="#ff4466")

    fig_ht.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(5, 5, 16, 0.9)',
        font=dict(family='Share Tech Mono', color='#00ffb4'),
        xaxis=dict(gridcolor='rgba(0, 255, 180, 0.1)', color='#00ffb4'),
        yaxis=dict(gridcolor='rgba(0, 255, 180, 0.1)', color='#00ffb4', ticksuffix='%'),
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_ht, use_container_width=True)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # Signal breakdown
    st.markdown("### 🔍 Signal Breakdown")
    for signal in signals:
        st.markdown(f"""
        <div class="momentum-box" style="margin:8px 0; padding:12px 18px;">
            {signal}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # THE FINAL VERDICT!!!
    # this is what everyone actually wants to see
    st.markdown("### 🎯 FINAL VERDICT")
    st.markdown(f"""
    <div class="analysis-box" style="border-color: {verdict_color}; text-align: center;">
        <div style="font-family: Orbitron; font-size: 1.4em; color: {verdict_color}; letter-spacing: 2px; margin-bottom: 15px;">
            STOCKMASTER 3000 SAYS:
        </div>
        <div style="font-size: 1.3em; color: white; font-weight: bold; line-height: 1.6;">
            {verdict}
        </div>
        <div style="margin-top: 15px; color: rgba(255,255,255,0.5); font-size: 0.8em;">
            ⚠️ NOT REAL FINANCIAL ADVICE. DO YOUR OWN RESEARCH. I AM A HIGH SCHOOLER.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FUNDAMENTALS PAGE
# shows the boring but important numbers about the company
# ============================================================
elif page == "📊 Fundamentals":
    st.markdown(f"## 📊 Fundamental Data — {ticker_input}")
    st.markdown("*The boring numbers that actually matter apparently*")

    if stock_info:
        # Helper function to safely get info (some stocks dont have all data)
        def safe_get(key, default="N/A", is_number=False, prefix="", suffix="", divisor=1):
            val = stock_info.get(key, default)
            if val is None or val == "N/A":
                return "N/A"
            try:
                if is_number:
                    return f"{prefix}{float(val)/divisor:,.2f}{suffix}"
                return str(val)
            except:
                return str(val)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🏢 Company Info")
            info_data = {
                "Field": ["Sector", "Industry", "Country", "Employees", "Website"],
                "Value": [
                    safe_get('sector'),
                    safe_get('industry'),
                    safe_get('country'),
                    safe_get('fullTimeEmployees', is_number=True),
                    safe_get('website')
                ]
            }
            st.dataframe(pd.DataFrame(info_data), hide_index=True, use_container_width=True)

            st.markdown("#### 💰 Valuation")
            val_data = {
                "Field": ["Market Cap", "P/E Ratio", "P/B Ratio", "EV/EBITDA", "Beta"],
                "Value": [
                    safe_get('marketCap', is_number=True, prefix="$", divisor=1e9, suffix="B"),
                    safe_get('forwardPE', is_number=True, suffix="x"),
                    safe_get('priceToBook', is_number=True, suffix="x"),
                    safe_get('enterpriseToEbitda', is_number=True, suffix="x"),
                    safe_get('beta', is_number=True)
                ]
            }
            st.dataframe(pd.DataFrame(val_data), hide_index=True, use_container_width=True)

        with col2:
            st.markdown("#### 📈 Financials")
            fin_data = {
                "Field": ["Revenue (TTM)", "Gross Profit", "Net Income", "EPS (TTM)", "Dividend Yield"],
                "Value": [
                    safe_get('totalRevenue', is_number=True, prefix="$", divisor=1e9, suffix="B"),
                    safe_get('grossProfits', is_number=True, prefix="$", divisor=1e9, suffix="B"),
                    safe_get('netIncomeToCommon', is_number=True, prefix="$", divisor=1e9, suffix="B"),
                    safe_get('trailingEps', is_number=True, prefix="$"),
                    safe_get('dividendYield', is_number=True, suffix="%",
                             divisor=0.01) if stock_info.get('dividendYield') else "N/A (No dividend)"
                ]
            }
            st.dataframe(pd.DataFrame(fin_data), hide_index=True, use_container_width=True)

            st.markdown("#### 📊 Price Targets")
            target_data = {
                "Field": ["Analyst Target", "52W High", "52W Low", "Current Price", "From 52W High"],
                "Value": [
                    safe_get('targetMeanPrice', is_number=True, prefix="$"),
                    safe_get('fiftyTwoWeekHigh', is_number=True, prefix="$"),
                    safe_get('fiftyTwoWeekLow', is_number=True, prefix="$"),
                    f"${current_price:.2f}",
                    f"{((current_price / stock_info.get('fiftyTwoWeekHigh', current_price)) - 1) * 100:.1f}%"
                    if stock_info.get('fiftyTwoWeekHigh') else "N/A"
                ]
            }
            st.dataframe(pd.DataFrame(target_data), hide_index=True, use_container_width=True)

        # Company description (if we have it)
        description = stock_info.get('longBusinessSummary', '')
        if description:
            st.markdown("#### 📝 About the Company")
            # Only show first 400 characters so it doesnt take over the page
            short_desc = description[:400] + "..." if len(description) > 400 else description
            st.markdown(f"""
            <div class="analysis-box" style="font-size: 0.9em; opacity: 0.85;">
                {short_desc}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Could not load fundamental data for this ticker. Try a different stock!")


# ============================================================
# ABOUT PAGE
# i wrote this myself
# ============================================================
elif page == "⚙️ About":
    st.markdown("## ⚙️ About StockMaster 3000")
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="analysis-box">
        <h3>🚀 What is StockMaster 3000?</h3>
        <p>StockMaster 3000 is a real-time stock analysis web application I built
        using Python and Streamlit. It pulls live data from Yahoo Finance using the
        yfinance library and shows you everything you need to know about a stock.</p>

        <h3>⚡ The Hyper-Trend™ Algorithm</h3>
        <p>The Hyper-Trend™ Momentum Predictor is my custom technical indicator.
        It calculates a 10-period momentum factor by comparing the current price
        to its rolling average, then expresses this as a percentage deviation signal.
        When the signal is positive, price is above its short-term trend (bullish).
        When negative, it's below (bearish). Works really well in my testing.</p>

        <h3>🛠️ Tech Stack</h3>
        <p>
        • Python 3.x<br>
        • Streamlit (the web framework)<br>
        • yfinance (gets the stock data for free!!)<br>
        • Plotly (makes the charts look professional)<br>
        • Pandas (data processing)
        </p>

        <h3>⚠️ Disclaimer</h3>
        <p>THIS IS NOT REAL FINANCIAL ADVICE. I am a high school student who
        likes coding and thought stocks were interesting. Please do not make
        real investment decisions based on this app. Do your own research!!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)


# ============================================================
# FOOTER - at the bottom of every page
# ============================================================
st.markdown("""
<div class="footer">
    ⚡ STOCKMASTER 3000 &nbsp;|&nbsp; REAL-TIME DATA VIA YFINANCE &nbsp;|&nbsp; i built it thanks
</div>
""", unsafe_allow_html=True)

# thats it!! the whole app. pretty good right
