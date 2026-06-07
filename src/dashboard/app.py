import os
import sys
from datetime import datetime

# 1. Path Setup
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Import your custom modules
from src.fred_client import FredClient
from src.market_client import MarketClient
from src.correlation_engine import CorrelationEngine
from src.rule_engine import RuleEngine
from src.alert_store import alert_already_sent, save_alert

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Market Sentinel", layout="wide")
st.title("📊 Market Sentinel Live Dashboard")
st_autorefresh(interval=300000, key="datarefresh") # 5 min refresh

# Init Components
fred = FredClient()
market = MarketClient()
engine = CorrelationEngine()
rule_engine = RuleEngine()

# ----------------------------
# DATA FETCHING
# ----------------------------
@st.cache_data(ttl=60)
def load_market_data():
    data = {
        "yield": fred.get_real_yield(),
        "usdinr": market.get_usdinr(),
        "gold": market.get_gold_price(),
        "corr": engine.compute()
    }
    return data

# Execute
data = load_market_data()
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ----------------------------
# DASHBOARD UI
# ----------------------------
col1, col2, col3 = st.columns(3)

# US Yield
#with col1:
#    st.metric("US Real Yield (%)", data["yield"].get("value", "N/A"))
# Define the note
    yield_note = (
    "US Real Yield = Nominal Treasury Yield - Expected Inflation. "
    "It represents the 'true' cost of borrowing. When this rises, "
    "it acts as a headwind for Gold and Stocks, as bonds become "
    "more attractive on an inflation-adjusted basis."
)

with col1:
    st.metric(
        label="US Real Yield (%)", 
        value=data["yield"].get("value", "N/A"),
        help=yield_note  # This adds the "!" tooltip icon
    )    

# USDINR
with col2:
    st.metric("USDINR", data["usdinr"].get("value", "N/A"))

# Gold with Spot Proxy Logic
with col3:
    raw_gold = data["gold"].get("value")
    if raw_gold != "N/A":
        spot_proxy = float(raw_gold) * 10
        tooltip = (
            "This is a 'Spot Proxy' price. GLD is an ETF share representing ~1/10th "
            "of an ounce of gold. Multiplying the share price by 10 provides a "
            "close estimate of the current Spot Gold price per ounce."
        )
        st.metric("Gold (USD) [Spot Proxy]", f"${spot_proxy:,.2f}", help=tooltip)
    else:
        st.metric("Gold (USD)", "N/A")
# --- UPDATE THIS SECTION IN app.py ---



st.divider()

# Correlation Score
st.subheader("📈 Correlation Engine Score")
score = data["corr"].get("score", 0)
if score > 0: st.success(f"Bullish Bias: {score}")
elif score < 0: st.error(f"Bearish Bias: {score}")
else: st.info("Neutral Market Condition")

st.divider()

# ----------------------------
# ALERTS & HISTORY
# ----------------------------
st.subheader("🧠 Latest Signal")
try:
    alerts = rule_engine.evaluate()
    if alerts:
        for alert in alerts:
            st.warning(f"**{alert['subject']}**: {alert['message']}")
            if not alert_already_sent(alert['subject']):
                save_alert(alert['subject'])
    else:
        st.write("No active signals.")
except Exception as e:
    st.error(f"Rule Engine Error: {e}")

st.divider()

# Telemetry
st.markdown(f"⏱️ **Last Refreshed:** `{current_time} UTC`")
if st.button("🔄 Force Manual Refresh"):
    st.cache_data.clear()
    st.rerun()
