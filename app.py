# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tTF67sfIci-V6lAB0rUxaXlBLqWefsFe
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel("C:/Users/mafaz/OneDrive/Desktop/SriLankan Airlines/Station data/Stationary_Perf.xlsx")

# Get default values for dropdowns
default_pos = df['POINT OF SALE'].unique()[0] if len(df['POINT OF SALE'].unique()) > 0 else None
default_region = df['Region'].unique()[0] if len(df['Region'].unique()) > 0 else None
default_month = 'April'  # Default month is set to 'April'

# Streamlit UI
st.title("Revenue Analysis Dashboard")

# Filters
st.sidebar.header("Filters")
selected_pos = st.sidebar.selectbox("Select POS", options=[None] + list(sorted(df['POINT OF SALE'].unique())), index=0)
selected_region = st.sidebar.selectbox("Select Region", options=[None] + list(sorted(df['Region'].unique())), index=0)
selected_month = st.sidebar.selectbox("Select Month", options=['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'], index=0)

# Function to filter dataframe based on selected filters
def filter_df(df, pos=None, region=None, month=None):
    filtered_df = df.copy()
    if pos:
        filtered_df = filtered_df[filtered_df['POINT OF SALE'] == pos]
    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if month:
        filtered_df = filtered_df[filtered_df['Month'] == month]
    return filtered_df

# Filtered Data
filtered_df = filter_df(df, selected_pos, selected_region, selected_month)

# Overall Revenue Trend Chart
st.subheader("Overall Revenue Trend")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', 'TGT-USD'],
                             var_name='Revenue Type', value_name='Revenue (USD)')
fig = px.line(
    melted_df,
    x='Month',
    y='Revenue (USD)',
    color='Revenue Type',
    title="Overall Revenue Trend by Month",
    markers=True
)
fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (USD)")
st.plotly_chart(fig)

# Overall Exchange Rate Gain/Loss Chart
st.subheader("Overall Exchange Rate Gain/Loss")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['Exchange - gain/( loss)', 'Exchange  -gain/(loss)'],
                             var_name='Exchange Rate Type', value_name='Gain/Loss (USD)')
fig = px.bar(
    melted_df,
    x='Month',
    y='Gain/Loss (USD)',
    color='Exchange Rate Type',
    title="Overall Exchange Rate Gain/Loss by Month"
)
fig.update_layout(xaxis_title="Month", yaxis_title="Gain/Loss (USD)")
st.plotly_chart(fig)

# Specific Revenue Trend Chart
st.subheader("Specific Revenue Trend")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', 'TGT-USD'],
                             var_name='Revenue Type', value_name='Revenue (USD)')
fig = px.line(
    melted_df,
    x='Month',
    y='Revenue (USD)',
    color='Revenue Type',
    title="Specific Revenue Trend by Month",
    markers=True
)
fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (USD)")
st.plotly_chart(fig)

# Specific Exchange Rate Gain/Loss Chart
st.subheader("Specific Exchange Rate Gain/Loss")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['Exchange - gain/( loss)', 'Exchange  -gain/(loss)'],
                             var_name='Exchange Rate Type', value_name='Gain/Loss (USD)')
fig = px.bar(
    melted_df,
    x='Month',
    y='Gain/Loss (USD)',
    color='Exchange Rate Type',
    title="Specific Exchange Rate Gain/Loss by Month"
)
fig.update_layout(xaxis_title="Month", yaxis_title="Gain/Loss (USD)")
st.plotly_chart(fig)

