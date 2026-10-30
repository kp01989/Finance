import streamlit as st
import pandas as pd
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Page Configuration (Exact Groww Clone Layout)
st.set_page_config(page_title="Explore - Groww", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# 2. Aggressive CSS to Override Streamlit UI and match Groww exactly
st.markdown("""
    <style>
    /* Reset and Base Colors */
    .stApp { background-color: #ffffff; color: #44475b; font-family: 'Roboto', sans-serif; }
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding-top: 1rem; max-width: 1200px; }
    
    /* -----------------------------------------
       WATCHLIST STYLING (Vertical Radio Hack) 
       ----------------------------------------- */
    /* Hide the radio circles */
    div[aria-orientation="vertical"] > label > div:first-child { display: none !important; }
    
    /* Style the list to look like Groww rows */
    div[aria-orientation="vertical"] { gap: 0px !important; }
    div[aria-orientation="vertical"] > label {
        padding: 16px 10px !important;
        border-bottom: 1px solid #f1f2f4 !important;
        margin: 0 !important;
        border-radius: 0 !important;
        background-color: white;
        transition: 0.2s;
        cursor: pointer;
    }
    div[aria-orientation="vertical"] > label:hover { background-color: #f8f9fa !important; }
    
    /* Text inside Watchlist */
    div[aria-orientation="vertical"] p {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #44475b !important;
    }

    /* -----------------------------------------
       CHART TOGGLE STYLING (Horizontal Radio) 
       ----------------------------------------- */
    /* Hide the radio circles */
    div[aria-orientation="horizontal"] > label > div:first-child { display: none !important; }
    
    /* Style as a pill container */
    div[aria-orientation="horizontal"] {
        background-color: #f1f2f4 !important;
        border-radius: 20px !important;
        padding: 4px !important;
        gap: 0 !important;
        width: fit-content;
    }
    /* Style individual pills */
    div[aria-orientation="horizontal"] > label {
        padding: 6px 16px !important;
        border-radius: 20px !important;
        margin: 0 !important;
    }
    /* Active pill style */
    div[aria-orientation="horizontal"] > label[data-checked="true"] {
        background-color: white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    div[aria-orientation="horizontal"] p { font-size: 13px !important; font-weight: 500 !important; }

    /* -----------------------------------------
       BUY / SELL BUTTONS 
       ----------------------------------------- */
    div[data-testid="stButton"] button {
        width: 100%;
        padding: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        transition: 0.2s;
    }
    .buy-btn button { background-color: #00d09c !important; color: white !important; }
    .buy-btn button:hover { background-color: #00b386 !important; color: white !important; }
    
    .sell-btn button { background-color: #eb5b3c !important; color: white !important; }
    .sell-btn button:hover { background-color: #d14a2f !important; color: white !important; }
    
    /* Hide running indicator */
    .stSpinner { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Fake Top Navbar (Just for the Groww look)
st.markdown("""
    <div style="display: flex; align-items: center; padding-bottom: 15px; border-bottom: 1px solid #f1f2f4; margin-bottom: 30px;">
        <div style="font-size: 26px; font-weight: 900; color: #101828; letter-spacing: -0.5px; margin-right: 40px;">Groww</div>
        <div style="background-color: #f1f2f4; padding: 10px 20px; border-radius: 8px; width: 400px; color: #7c7e8c; font-size: 14px;">
            🔍 What are you looking for today?
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Mock Data Generation (To be replaced with Broker API later)
def fetch_broker_data():
    return pd.DataFrame({
        "Symbol": ["RELIANCE", "TCS", "SBIN", "JPL"],
        "LTP (₹)": [round(random.uniform(2900, 2950), 2), 
                    round(random.uniform(3900, 3950), 2), 
                    round(random.uniform(750, 760), 2), 
                    round(random.uniform(100, 110), 2)],
        "Change (%)": [round(random.uniform(-2, 2), 2) for _ in range(4)]
    })

def get_chart_data(trend="up"):
    now = datetime.now()
    times = [now - timedelta(minutes=i) for i in range(40, 0, -1)]
    base = 2900
    data = []
    for t in times:
        o = base + random.uniform(-5, 5)
        c = o + random.uniform(-2, 10) if trend == "up" else o - random.uniform(-2, 10)
        h = max(o, c) + random.uniform(0, 5)
        l = min(o, c) - random.uniform(0, 5)
        data.append([t, round(o,2), round(h,2), round(l,2), round(c,2)])
        base = c
    return pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close'])

# Constants for Groww Colors
GROWW_GREEN = "#00d09c"
GROWW_RED = "#eb5b3c"

# Fetch Live Data
live_df = fetch_broker_data()

# 5. UI Layout Structure
col_left, col_right = st.columns([1.2, 2.8], gap="large")

with col_left:
    st.markdown("<h3 style='font-size: 18px; color: #44475b; margin-bottom: 10px;'>Watchlist</h3>", unsafe_allow_html=True)
    
    # Custom format for Watchlist Radio (Symbol + Price + Change)
    def format_watchlist(sym):
        row = live_df[live_df["Symbol"] == sym].iloc[0]
        change = row["Change (%)"]
        price = row["LTP (₹)"]
        sign = "+" if change >= 0 else ""
        # Adding some space to make it look clean
        return f"{sym}  |  ₹{price}  |  {sign}{change}%"

    # Single, clean clickable watchlist using Streamlit Radio
    selected_stock = st.radio("Watchlist", live_df["Symbol"], format_func=format_watchlist, label_visibility="collapsed")

with col_right:
    # Get selected stock data
    stock_info = live_df[live_df["Symbol"] == selected_stock].iloc[0]
    is_positive = stock_info["Change (%)"] >= 0
    theme_color = GROWW_GREEN if is_positive else GROWW_RED
    sign = "+" if is_positive else ""
    
    # Groww Style Huge Header
    st.markdown(f"<h1 style='font-size: 28px; margin-bottom: 5px; color: #101828;'>{selected_stock}</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='display: flex; align-items: baseline; gap: 12px; margin-bottom: 20px;'>
            <h2 style='font-size: 34px; font-weight: 500; margin: 0; color: #101828;'>₹{stock_info['LTP (₹)']}</h2>
            <span style='font-size: 16px; font-weight: 500; color: {theme_color};'>{sign}{stock_info['Change (%)']}% (1D)</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Chart Toggle (Line / Candlestick)
    chart_type = st.radio("Chart Type", ["Line", "Candlestick"], horizontal=True, label_visibility="collapsed")
    
    # Generate Chart Data
    chart_df = get_chart_data(trend="up" if is_positive else "down")
    
    # Render Exact Groww Style Minimal Chart
    if chart_type == "Line":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_df['Time'], y=chart_df['Close'], 
            mode='lines', 
            line=dict(color=theme_color, width=2.5),
            fill='tozeroy', 
            fillcolor=f"rgba(0, 208, 156, 0.05)" if is_positive else f"rgba(235, 91, 60, 0.05)",
            hoverinfo='y'
        ))
    else:
        fig = go.Figure(data=[go.Candlestick(
            x=chart_df['Time'], open=chart_df['Open'], high=chart_df['High'],
            low=chart_df['Low'], close=chart_df['Close'],
            increasing_line_color=GROWW_GREEN, increasing_fillcolor=GROWW_GREEN,
            decreasing_line_color=GROWW_RED, decreasing_fillcolor=GROWW_RED
        )])
        
    # Remove all background grids and axes (Groww look)
    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0), height=380,
        xaxis=dict(showgrid=False, visible=False, rangeslider=dict(visible=False)),
        yaxis=dict(showgrid=False, visible=False, side='right'),
        plot_bgcolor='white', paper_bgcolor='white',
        hovermode='x unified', showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Groww Style Buy/Sell Buttons
    st.markdown("<br>", unsafe_allow_html=True)
    c_buy, c_sell = st.columns(2, gap="medium")
    with c_buy:
        st.markdown('<div class="buy-btn">', unsafe_allow_html=True)
        st.button("BUY", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c_sell:
        st.markdown('<div class="sell-btn">', unsafe_allow_html=True)
        st.button("SELL", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 6. Auto-Refresh Logic (Hidden from UI)
time.sleep(2)
st.rerun()
