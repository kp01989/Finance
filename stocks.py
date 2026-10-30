import streamlit as st
import pandas as pd
import time

# 1. Page Configuration ane Design
st.set_page_config(page_title="Live Market Watch", page_icon="📈", layout="wide")
st.title("📈 Live Broker API Stock Dashboard")
st.markdown("---")

# 2. Broker API Connection Function (Base logic)
def fetch_broker_data():
    # Ahiya aapne pachi thi Fyers ke Dhan nu real API logic nakhi daisu.
    # Atyare design set karva mate random data generate karyo che jethi refresh thatu dekhay.
    import random
    
    return pd.DataFrame({
        "Symbol": ["RELIANCE", "TCS", "SBIN", "JPL"],
        "LTP (₹)": [round(random.uniform(2900, 2950), 2), 
                    round(random.uniform(3900, 3950), 2), 
                    round(random.uniform(750, 760), 2), 
                    round(random.uniform(100, 110), 2)],
        "Change (%)": [round(random.uniform(-2, 2), 2) for _ in range(4)],
        "Volume": [random.randint(10000, 50000) for _ in range(4)]
    })

# 3. UI Layout Set Karvu
col_left, col_right = st.columns([1, 3])

with col_left:
    st.subheader("⚙️ Controls")
    st.success("🟢 Broker API Connected")
    st.info("⏱️ Auto-refresh: 3 Seconds")
    
    # Refresh stop karva mate nu logic
    if st.button("🛑 Stop Live Feed", use_container_width=True):
        st.stop()

with col_right:
    st.subheader("📊 Real-time Data")
    
    # Data fetch karo
    live_df = fetch_broker_data()
    
    # Top par Metric cards batao
    metric_cols = st.columns(len(live_df))
    for index, row in live_df.iterrows():
        with metric_cols[index]:
            st.metric(label=row["Symbol"], 
                      value=f"₹{row['LTP (₹)']}", 
                      delta=f"{row['Change (%)']}%")
            
    # Niche detail table batao
    st.dataframe(live_df, use_container_width=True, hide_index=True)

# 4. 3 Second Auto-Refresh Logic
time.sleep(3)
st.rerun()
