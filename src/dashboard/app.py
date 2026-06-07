import os
import sys
from datetime import datetime

# 1. ALWAYS set up your paths before importing local modules
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Import your custom modules safely
from src.fred_client import FredClient
from src.market_client import MarketClient
from src.correlation_engine import CorrelationEngine
from src.rule_engine import RuleEngine
from src.alert_store import alert_already_sent, save_alert

# ----------------------------
# STREAMLIT PAGE CONFIG & AUTO-REFRESH
# ----------------------------
st.set_page_config(page_title="Market Sentinel Dashboard", layout="wide")

st.title("📊 Market Sentinel Live Dashboard")

# Automatically refresh the visual layout on the web server every 5 minutes (300,000 milliseconds)
st_autorefresh(interval=300000, key="datarefresh")

# ----------------------------
# INIT COMPONENTS
# ----------------------------
fred = FredClient()
market = MarketClient()
engine = CorrelationEngine()
rule_engine = RuleEngine()

# ----------------------------
# SAFE CACHED DATA FETCH FUNCTION
# ----------------------------
# @st.cache_data(ttl=3600)  # Cache data for 5 minutes to stay incredibly fast
@st.cache_data(ttl=86400)  # 24 hours = 86400 seconds. This is the fix.
def load_market_data():
    print("🚀 DEBUG: Initializing Cloud-Safe Data Fetch...")
    
    try:
        print("🚀 DEBUG: Fetching FRED data...")
        y_data = fred.get_real_yield()
    except Exception as e:
        print(f"❌ DEBUG ERROR (FRED): {e}")
        y_data = {"value": "N/A (API Error)"}
        
    try:
        print("🚀 DEBUG: Fetching Market USDINR data...")
        u_inr = market.get_usdinr()
    except Exception as e:
        print(f"❌ DEBUG ERROR (USDINR): {e}")
        u_inr = {"value": "N/A (API Error)"}
        
    try:
        print("🚀 DEBUG: Fetching Gold data...")
        g_price = market.get_gold_price()
    except Exception as e:
        print(f"❌ DEBUG ERROR (Gold): {e}")
        g_price = {"value": "N/A (API Error)"}
        
    try:
        print("🚀 DEBUG: Computing Correlation Engine Score...")
        corr = engine.compute()
    except Exception as e:
        print(f"❌ DEBUG ERROR (Correlation): {e}")
        corr = {"score": 0}
        
    print("🚀 DEBUG: All data processes executed successfully.")
    return y_data, u_inr, g_price, corr

# ----------------------------
# EXECUTE DATA & RULE ENGINES
# ----------------------------

# 1. Execute the cloud-safe data fetch cleanly
yield_data, usdinr, gold, correlation = load_market_data()

# 2. Capture the exact timestamp when this web execution completed
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. Evaluate rules safely inside a protective block
try:
    print("🚀 DEBUG: Evaluating Rule Engine Alerts...")
    alerts = rule_engine.evaluate()
except Exception as e:
    print(f"❌ DEBUG ERROR (Rule Engine): {e}")
    alerts = []
    st.sidebar.error(f"Rule Engine Error: {e}")

# ----------------------------
# DASHBOARD VISUAL LAYOUT
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("US Real Yield (%)", yield_data["value"])

with col2:
    st.metric("USDINR", usdinr["value"])

with col3:
    st.metric("Gold (USD)", gold["value"])

st.divider()

# ----------------------------
# CORRELATION SCORE VISUAL
# ----------------------------
st.subheader("📈 Correlation Engine Score")

score = correlation["score"]

if score > 0:
    st.success(f"Bullish Bias Score: {score}")
elif score < 0:
    st.error(f"Bearish Bias Score: {score}")
else:
    st.info("Neutral Market Condition")

st.divider()

# ----------------------------
# SIGNAL STATUS & ALERT CHECKING
# ----------------------------
st.subheader("🧠 Latest Signal")

# Track if an alert was triggered in this run session
alert_sent_status = {}

if alerts:
    for alert in alerts:
        st.warning(f"{alert['subject']} → {alert['message']}")
        
        # Check if this specific alert has already been logged in alerts.json
        alert_key = alert['subject']
        was_sent_before = alert_already_sent(alert_key)
        
        # Keep track of its status to display at the bottom of the dashboard
        alert_sent_status[alert_key] = {
            "already_logged_in_json": was_sent_before,
            "message": alert['message']
        }
        
        # If it hasn't been sent before, try to save it
        if not was_sent_before:
            save_alert(alert_key)
else:
    st.write("No new signals")

st.divider()

# ----------------------------
# ALERT STATE LOGS HISTORY VISUAL
# ----------------------------
st.subheader("📌 Evaluated Alerts JSON History Status")

if alert_sent_status:
    for alert_name, info in alert_sent_status.items():
        with st.container(border=True):
            st.markdown(f"### **🟢 {alert_name}**")
            
            if info["already_logged_in_json"]:
                st.info("ℹ️ **Status:** Already saved in system logs (`alerts.json`)")
            else:
                st.success("🆕 **Status:** New alert successfully saved to logs!")
                
            st.markdown(f"**Log Message:** \n*{info['message']}*")
else:
    st.info("No active rule engine alerts to track right now.")

st.divider()

# ----------------------------
# TELEMETRY AND REFRESH CONTROLS
# ----------------------------
# Visually maps out exactly when the last background network request occurred
st.markdown(f"⏱️ **Webserver Cache Last Refreshed at:** `{current_time} UTC` (Auto-refreshes every 5 mins)")

if st.button("🔄 Force Manual Refresh Now"):
    st.cache_data.clear()
    st.rerun()