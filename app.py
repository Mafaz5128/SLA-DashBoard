import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Load data
df = pd.read_excel("Stationary_Perf.xlsx")

# Grouping data
act_avg = df.groupby('Month')['ACT -USD'].mean()
lyr_avg = df.groupby('Month')['LYR-USD (2023/24)'].mean()
act_tg = df.groupby('Month')[' TGT-USD'].mean()
exrate_avg = df.groupby('Month')['Act. Using-Bgt. ex. Rates'].mean()
exloss_avg = df.groupby('Month')['Exchange - gain/( loss)'].mean()
exloss_avg_ly = df.groupby('Month')['Exchange  -gain/(loss)'].mean()

month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
act_avg = act_avg.reindex(month_order)
lyr_avg = lyr_avg.reindex(month_order)
act_tg = act_tg.reindex(month_order)
exrate_avg = exrate_avg.reindex(month_order)
exloss_avg = exloss_avg.reindex(month_order)
exloss_avg_ly = exloss_avg_ly.reindex(month_order)

# Streamlit Layout
st.title("Station Revenue Analytics")

# Adding a dropdown to choose between ACTUAL, LAST YEAR, and TARGET data
chart_type = st.selectbox(
    "Choose the Chart Type",
    ["Revenue Trend (ACTUAL vs LAST YEAR)", "Revenue Trend (ACTUAL vs TARGET)", "Exchange Rate Trend", "Exchange Rate Gain/Loss"]
)

# Revenue Trend by Month (ACTUAL vs LAST YEAR)
if chart_type == "Revenue Trend (ACTUAL vs LAST YEAR)":
    st.subheader("Revenue Trend by Month (ACTUAL vs LAST YEAR)")
    fig1 = go.Figure()

    # Adding Actual and Last Year data
    fig1.add_trace(go.Scatter(x=month_order, y=act_avg, mode='lines+markers', name='ACTUAL', line=dict(color='blue')))
    fig1.add_trace(go.Scatter(x=month_order, y=lyr_avg, mode='lines+markers', name='LAST YEAR (2023/24)', line=dict(color='green')))

    fig1.update_layout(
        title='ACTUAL vs LAST YEAR Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue (USD)',
        xaxis=dict(tickmode='array', tickvals=month_order),
        template='plotly_dark'
    )
    st.plotly_chart(fig1)

# Revenue Trend by Month (ACTUAL vs TARGET)
elif chart_type == "Revenue Trend (ACTUAL vs TARGET)":
    st.subheader("Revenue Trend by Month (ACTUAL vs TARGET)")
    fig2 = go.Figure()

    # Adding Actual and Target data
    fig2.add_trace(go.Scatter(x=month_order, y=act_avg, mode='lines+markers', name='ACTUAL', line=dict(color='blue')))
    fig2.add_trace(go.Scatter(x=month_order, y=act_tg, mode='lines+markers', name='TARGET', line=dict(color='red')))

    fig2.update_layout(
        title='ACTUAL vs TARGET Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue (USD)',
        xaxis=dict(tickmode='array', tickvals=month_order),
        template='plotly_dark'
    )
    st.plotly_chart(fig2)

# Average Exchange Rate by Month
elif chart_type == "Exchange Rate Trend":
    st.subheader("Average Exchange Rate by Month")
    fig3 = go.Figure()

    # Adding Average Exchange Rate data
    fig3.add_trace(go.Scatter(x=month_order, y=exrate_avg, mode='lines+markers', name='Average Exchange Rate', line=dict(color='purple')))

    fig3.update_layout(
        title='Average Exchange Rate Trend',
        xaxis_title='Month',
        yaxis_title='Exchange Rate',
        xaxis=dict(tickmode='array', tickvals=month_order),
        template='plotly_dark'
    )
    st.plotly_chart(fig3)

# Exchange Rate Gain/Loss by Month (Current Year vs Last Year)
elif chart_type == "Exchange Rate Gain/Loss":
    st.subheader("Exchange Rate Gain/Loss by Month (Current Year vs Last Year)")
    fig4 = go.Figure()

    # Adding Gain/Loss data
    fig4.add_trace(go.Scatter(x=month_order, y=exloss_avg, mode='lines+markers', name='ExgRate - gain/Loss', line=dict(color='orange')))
    fig4.add_trace(go.Scatter(x=month_order, y=exloss_avg_ly, mode='lines+markers', name='ExgRate - gain/loss (LY)', line=dict(color='cyan')))

    fig4.update_layout(
        title='ExgRate Gain/Loss by Month',
        xaxis_title='Month',
        yaxis_title='Gain/Loss (USD)',
        xaxis=dict(tickmode='array', tickvals=month_order),
        template='plotly_dark'
    )
    st.plotly_chart(fig4)
