import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import time

st.set_page_config(page_title="Fraud Analytics SOC", layout="wide")
st.markdown("<h1 style='text-align: center;'>Live Fraud Detection Analytics</h1>", unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ Big Data Engine")
st.sidebar.info("**Processing:** Apache Spark (PySpark)\n\n**Streaming:** Spark Structured Streaming\n\n**Storage:** SQLite\n\n**Frontend:** Streamlit")
st.sidebar.markdown("---")

city_coords = {
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5072, "lon": -0.1276},
    "Dubai": {"lat": 25.2048, "lon": 55.2708}
}

if os.path.exists("fraud_data.db"):
    conn = sqlite3.connect("fraud_data.db")
    df = pd.read_sql_query("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 500", conn)
    conn.close()

    if not df.empty:
        st.sidebar.header("SOC Controls")
        
        # Prominent Play/Pause Toggle
        auto_refresh = st.sidebar.toggle("Live Auto-Refresh", value=True)
        if auto_refresh:
            st.sidebar.success("🟢 System Live: Auto-refreshing")
        else:
            st.sidebar.warning("⏸️ System Paused: Safe for full screen")
        
        risk_filter = st.sidebar.multiselect("Filter by Risk Level", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])
        filtered_df = df[df['risk_level'].isin(risk_filter)]
        
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])

        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📥 Export Threat Data (CSV)",
            data=csv,
            file_name='soc_threat_logs.csv',
            mime='text/csv',
        )

        latest_high_risk = df[df['risk_level'] == 'High'].head(1)
        if not latest_high_risk.empty:
            st.error(f"🚨 **LATEST HIGH RISK ALERT:** ${latest_high_risk.iloc[0]['amount']:,.2f} at {latest_high_risk.iloc[0]['merchant']} in {latest_high_risk.iloc[0]['location']} (User: {latest_high_risk.iloc[0]['user_id']})")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Monitored Events (Spark Stream)", len(df))
        col2.metric("High Risk Flags", len(df[df['risk_level'] == 'High']))
        col3.metric("Processing Volume", f"${df['amount'].sum():,.2f}")
        col4.metric("Avg Transaction", f"${df['amount'].mean():,.2f}")

        st.markdown("---")
        if not auto_refresh:
            st.info("💡 **Analyst Tip:** The system is paused. You can now safely expand charts to full screen or analyze the ledger.")
            
        chart_col1, chart_col2, chart_col3 = st.columns(3)
        
        with chart_col1:
            st.subheader("Risk Distribution")
            fig_pie = px.pie(filtered_df, names='risk_level', hole=0.4, 
                             color='risk_level', color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
            fig_pie.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with chart_col2:
            st.subheader("Fraud by Merchant")
            high_risk_df = filtered_df[filtered_df['risk_level'] != 'Low']
            if not high_risk_df.empty:
                fig_bar = px.histogram(high_risk_df, x='merchant', color='risk_level', barmode='group',
                                       color_discrete_map={'High': 'red', 'Medium': 'orange'})
                fig_bar.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, xaxis_title="", yaxis_title="Incident Count")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.write("No alerts in current window.")
                
        with chart_col3:
            st.subheader("Geographic Hotspots")
            map_df = filtered_df.copy()
            map_df['lat'] = map_df['location'].map(lambda x: city_coords.get(x, {}).get('lat', 0))
            map_df['lon'] = map_df['location'].map(lambda x: city_coords.get(x, {}).get('lon', 0))
            
            fig_map = px.scatter_geo(map_df, lat='lat', lon='lon', color='risk_level', 
                                     size='amount', hover_name='location', projection="natural earth",
                                     color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
            fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("---")
        
        st.subheader("Live Transaction Velocity (Events per Second)")
        velocity_df = filtered_df.set_index('timestamp').resample('1s').size().reset_index(name='Transactions')
        fig_velocity = px.line(velocity_df, x='timestamp', y='Transactions', markers=True, 
                               color_discrete_sequence=['#00d4ff'])
        fig_velocity.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, xaxis_title="Time", yaxis_title="Volume")
        st.plotly_chart(fig_velocity, use_container_width=True)

        st.subheader("PySpark Processed Ledger")
        def color_risk(val):
            if val == 'High': return 'background-color: #5c1616; color: white'
            elif val == 'Medium': return 'background-color: #5c3a16; color: white'
            return ''
            
        styled_df = filtered_df.head(50).style.map(color_risk, subset=['risk_level'])
        st.dataframe(styled_df, use_container_width=True)

        if auto_refresh:
            time.sleep(2)
            st.rerun()

    else:
        st.warning("Database exists but is empty. Start the generator and processor.")
else:
    st.error("Awaiting data stream. Please run generator.py and processor.py.")