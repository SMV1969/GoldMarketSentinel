import os
import sys

# 1. ALWAYS set up your paths before importing local modules
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import streamlit as st
from src.fred_client import FredClient
from src.market_client import MarketClient
from src.correlation_engine import CorrelationEngine
from src.rule_engine import RuleEngine
from src.alert_store import alert_already_sent, save_alert

st.set_page_config(page_title="Market Sentinel Dashboard", layout="wide")

st.title("📊 Market Sentinel Live Dashboard")

# ----------------------------
# INIT COMPONENTS
# ----------------------------
fred = FredClient()
market = MarketClient()
engine = CorrelationEngine()
rule_engine = RuleEngine()

# ----------------------------
# DATA FETCH
# ----------------------------
# ----------------------------
# DATA FETCH (Safeguarded for Cloud)
# ----------------------------
@st.cache_data(ttl=300)  # Cache data for 5 minutes so it stays incredibly fast
def load_market_data():
    try:
        y_data = fred.get_real_yield()
    except Exception as e:
        y_data = {"value": "N/A (API Error)"}
        
    try:
        u_inr = market.get_usdinr()
    except Exception as e:
        u_inr = {"value": "N/A (API Error)"}
        
    try:
        g_price = market.get_gold_price()
    except Exception as e:
        g_price = {"value": "N/A (API Error)"}
        
    try:
        corr = engine.compute()
    except Exception as e:
        corr = {"score": 0}
        
    return y_data, u_inr, g_price, corr

# Execute the cloud-safe data fetch
yield_data, usdinr, gold, correlation = load_market_data()

# Check for active alerts evaluated by the rule engine
try:
    alerts = rule_engine.evaluate()
except Exception as e:
    alerts = []
    st.sidebar.error(f"Rule Engine Error: {e}")
    
# yield_data = fred.get_real_yield()
# usdinr = market.get_usdinr()
# gold = market.get_gold_price()
# correlation = engine.compute()

# Check for active alerts evaluated by the rule engine
alerts = rule_engine.evaluate()

# ----------------------------
# LAYOUT
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
# CORRELATION SCORE
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
        
        # If it hasn't been sent before, save it now!
        if not was_sent_before:
            save_alert(alert_key)
else:
    st.write("No new signals")

st.divider()

# ----------------------------
# ALERT STATE LOGS
# ----------------------------
st.subheader("📌 Evaluated Alerts JSON History Status")

if alert_sent_status:
    for alert_name, info in alert_sent_status.items():
        # Create a visually clean container for each alert status
        with st.container(border=True):
            st.markdown(f"### **🟢 {alert_name}**")
            
            # Show a formatted badge based on whether it was already logged
            if info["already_logged_in_json"]:
                st.info("ℹ️ **Status:** Already saved in system logs (`alerts.json`)")
            else:
                st.success("🆕 **Status:** New alert successfully saved to logs!")
                
            st.markdown(f"**Log Message:** \n*{info['message']}*")
else:
    st.info("No active rule engine alerts to track right now.")
    
    
# ----------------------------
# MANUAL REFRESH
# ----------------------------
st.button("🔄 Refresh Dashboard")