import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI
st.set_page_config(page_title="Revenue Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Revenue Analysis Dashboard")

# Sidebar for filters (Only POS and Region)
st.sidebar.header("Filters")

# Add "Select All" option for POS
selected_pos = st.sidebar.selectbox(
    "Select POS", 
    options=["All"] + list(sorted(df['POINT OF SALE'].unique())), index=0
)

# Additional filters for separate graphs (Including Month and Region for separate graphs)
st.sidebar.header("Additional Filters")
selected_month_filter = st.sidebar.selectbox(
    "Select Month for Separate Graph", 
    options=['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], 
    index=0
)
selected_region_filter = st.sidebar.selectbox(
    "Select Region for Separate Graph", 
    options=["All"] + list(sorted(df['Region'].unique())), index=0
)

# Function to filter dataframe based on selected filters
def filter_df(df, pos=None, month=None):
    filtered_df = df.copy()
    if pos and pos != "All":
        filtered_df = filtered_df[filtered_df['POINT OF SALE'] == pos]
    return filtered_df

# Filtered Data based on selected POS filter
filtered_df = filter_df(df, selected_pos)

# Set the month order explicitly
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Overall Revenue Trend Chart (Average Revenue by Type)
st.subheader("Overall Revenue Trend")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)'],  # Removed 'TGT-USD'
                             var_name='Revenue Type', value_name='Revenue (USD)')

# Group by Month and Revenue Type to calculate average revenue
avg_revenue_df = melted_df.groupby(['Month', 'Revenue Type'])['Revenue (USD)'].mean().reset_index()

# Plot the chart with average revenue
fig = px.line(
    avg_revenue_df,
    x='Month',
    y='Revenue (USD)',
    color='Revenue Type',
    title="Overall Average Revenue Trend by Month",
    markers=True
)

# Customizing the legend labels
fig.update_traces(
    name="ACT -USD - Actual Revenue", selector=dict(name="ACT -USD")
)
fig.update_traces(
    name="LYR-USD (2023/24) - Last Year Revenue", selector=dict(name="LYR-USD (2023/24)")
)

fig.update_layout(xaxis_title="Month", yaxis_title="Average Revenue (USD)")
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

# Filtered Data based on additional filters (POS, Month, Region for separate graphs)
filtered_df_separate = filter_df(df, selected_pos)

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
