import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI
st.set_page_config(page_title="Revenue Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Revenue Analysis Dashboard")

# Sidebar for filters (Only Month and Region)
st.sidebar.header("Filters")

# Add "Select All" option for Month and Region
selected_month = st.sidebar.selectbox(
    "Select Month", 
    options=["All"] + ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'], index=0
)
selected_region = st.sidebar.selectbox(
    "Select Region", 
    options=["All"] + list(sorted(df['Region'].unique())), index=0
)

# Additional filters for separate graphs (Including POS)
st.sidebar.header("Additional Filters")
selected_pos = st.sidebar.selectbox(
    "Select POS", 
    options=["All"] + list(sorted(df['POINT OF SALE'].unique())), index=0
)
selected_month_filter = st.sidebar.selectbox(
    "Select Month for Separate Graph", 
    options=["All"] + ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'], 
    index=0
)
selected_region_filter = st.sidebar.selectbox(
    "Select Region for Separate Graph", 
    options=["All"] + list(sorted(df['Region'].unique())), index=0
)

# Function to filter dataframe based on selected filters
def filter_df(df, pos=None, region=None, month=None):
    filtered_df = df.copy()
    if pos and pos != "All":
        filtered_df = filtered_df[filtered_df['POINT OF SALE'] == pos]
    if region and region != "All":
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if month and month != "All":
        filtered_df = filtered_df[filtered_df['Month'] == month]
    return filtered_df

# Filtered Data based on main filters (Month and Region)
filtered_df = filter_df(df, None, selected_region, selected_month)

# Overall Revenue Trend Chart
st.subheader("Overall Revenue Trend")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', ' TGT-USD'],
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
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', ' TGT-USD'],
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

# Filtered Data based on additional filters (Month and Region for separate graphs, POS for individual POS graphs)
filtered_df_separate = filter_df(df, selected_pos, selected_region_filter, selected_month_filter)

# Separate graphs for filtered data by month
st.subheader("Separate Revenue Trend by Month")
melted_df_separate = filtered_df_separate.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', ' TGT-USD'],
                                               var_name='Revenue Type', value_name='Revenue (USD)')
fig_separate = px.line(
    melted_df_separate,
    x='Month',
    y='Revenue (USD)',
    color='Revenue Type',
    title="Separate Revenue Trend by Month",
    markers=True
)
fig_separate.update_layout(xaxis_title="Month", yaxis_title="Revenue (USD)")
st.plotly_chart(fig_separate)

# Separate graphs for filtered data by region
st.subheader("Separate Revenue Trend by Region")
melted_df_region = filtered_df_separate.melt(id_vars=["Region"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', ' TGT-USD'],
                                             var_name='Revenue Type', value_name='Revenue (USD)')
fig_region = px.line(
    melted_df_region,
    x='Region',
    y='Revenue (USD)',
    color='Revenue Type',
    title="Separate Revenue Trend by Region",
    markers=True
)
fig_region.update_layout(xaxis_title="Region", yaxis_title="Revenue (USD)")
st.plotly_chart(fig_region)
