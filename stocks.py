import streamlit as st
import pandas as pd
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Page Configuration (Groww Style Clean Look)
st.set_page_config(page_title="Groww Clone Dashboard", page_icon="📈", layout="wide")

# Custom CSS for clean UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; } /* Light theme by default */
    h1, h2, h3, p { color: #333333; }
    .stRadio > label { display: none; } /* Hide radio label */
    </style>
""", unsafe_allow_html=True)

st.title("📈 Market Watch")
st.markdown("---")

# 2. Mock Data Functions (Ahiya pachi real Broker API aavse)
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
    times = [now - timedelta(minutes=i) for i in range(30, 0, -1)]
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

# 3. UI Layout (Left: Watchlist, Right: Chart)
col_left, col_right = st.columns([1.2, 2.8])
live_df = fetch_broker_data()

with col_left:
    st.subheader("Watchlist")
    
    # Select stock using Radio button
    selected_stock = st.radio("Select Stock:", live_df["Symbol"], label_visibility="collapsed")
    
    # Display Watchlist exactly like Groww
    for index, row in live_df.iterrows():
        color = "#00b852" if row["Change (%)"] >= 0 else "#eb5b3c"
        sign = "+" if row["Change (%)"] >= 0 else ""
        st.markdown(f"""
        <div style="padding: 10px; border-bottom: 1px solid #eee;">
            <strong style="font-size: 16px;">{row['Symbol']}</strong><br>
            <span style="font-size: 14px;">₹{row['LTP (₹)']}</span> 
            <span style="color: {color}; font-size: 14px; float: right; font-weight: bold;">{sign}{row['Change (%)']}%</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("") # Thodi space mate
    if st.button("🛑 Stop Live Feed", use_container_width=True):
        st.stop()

with col_right:
    # Get selected stock data to determine color (Green or Red)
    stock_info = live_df[live_df["Symbol"] == selected_stock].iloc[0]
    is_positive = stock_info["Change (%)"] >= 0
    theme_color = "#00b852" if is_positive else "#eb5b3c"
    sign = "+" if is_positive else ""
    
    st.subheader(f"{selected_stock}")
    st.markdown(f"<h2 style='margin-top:-15px;'>₹{stock_info['LTP (₹)']} <span style='color:{theme_color}; font-size:20px;'>({sign}{stock_info['Change (%)']}%)</span></h2>", unsafe_allow_html=True)
    
    chart_df = get_chart_data(trend="up" if is_positive else "down")
    
    tab1, tab2 = st.tabs(["📈 Line", "🕯️ Candlestick"])
    
    with tab1:
        # Groww style Line Chart (No grid, fill area)
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=chart_df['Time'], y=chart_df['Close'], 
            mode='lines', 
            line=dict(color=theme_color, width=2),
            fill='tozeroy', 
            fillcolor=f"rgba(0,184,82,0.1)" if is_positive else f"rgba(235,91,60,0.1)"
        ))
        fig_line.update_layout(
            margin=dict(l=0, r=0, t=10, b=0), height=400,
            xaxis=dict(showgrid=False, showline=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0', gridwidth=1, side='right'),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
    with tab2:
        # Groww style Candlestick
        fig_candle = go.Figure(data=[go.Candlestick(
            x=chart_df['Time'], open=chart_df['Open'], high=chart_df['High'],
            low=chart_df['Low'], close=chart_df['Close'],
            increasing_line_color='#00b852', decreasing_line_color='#eb5b3c'
        )])
        fig_candle.update_layout(
            margin=dict(l=0, r=0, t=10, b=0), height=400,
            xaxis=dict(showgrid=False, rangeslider=dict(visible=False)),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0', side='right'),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig_candle, use_container_width=True)

# 4. Auto-Refresh Logic (3 Seconds)
time.sleep(3)
st.rerun()
