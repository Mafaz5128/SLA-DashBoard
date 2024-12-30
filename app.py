import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI
st.set_page_config(page_title="Revenue Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Revenue Analysis Dashboard")

# Sidebar for filters (Only POS)
st.sidebar.header("Filters")
selected_pos = st.sidebar.selectbox(
    "Select POS", 
    options=["All"] + list(sorted(df['POINT OF SALE'].unique())), 
    index=0
)

# Additional filters for separate graphs (POS, Month, and Region)
st.sidebar.header("Additional Filters")
selected_month_filter = st.sidebar.selectbox(
    "Select Month for Separate Graph", 
    options=['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'], 
    index=0
)
selected_region_filter = st.sidebar.selectbox(
    "Select Region for Separate Graph", 
    options=["All"] + list(sorted(df['Region'].unique())), 
    index=0
)

# Function to filter dataframe based on selected filters
def filter_df(df, pos=None):
    filtered_df = df.copy()
    if pos and pos != "All":
        filtered_df = filtered_df[filtered_df['POINT OF SALE'] == pos]
    return filtered_df

# Filtered Data based on selected POS filter
filtered_df = filter_df(df, selected_pos)

# Set the month order explicitly
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
filtered_df['Month'] = pd.Categorical(filtered_df['Month'], categories=month_order, ordered=True)

# Overall Revenue Trend Chart (Average Revenue by Type)
st.subheader("Total Revenue Trend by Month")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)'],  # Removed 'TGT-USD'
                             var_name='Revenue Type', value_name='Revenue (USD)')

# Group by Month and Revenue Type to calculate total revenue
avg_revenue_df = melted_df.groupby(['Month', 'Revenue Type'])['Revenue (USD)'].sum().reset_index()

# Ensure month ordering is reflected in the plot
avg_revenue_df['Month'] = pd.Categorical(avg_revenue_df['Month'], categories=month_order, ordered=True)

# Plot the chart with total revenue
fig = px.line(
    avg_revenue_df,
    x='Month',
    y='Revenue (USD)',
    color='Revenue Type',
    title="Overall Revenue Trend by Month",
    markers=True
)

# Customizing the legend labels
fig.for_each_trace(
    lambda t: t.update(
        name="Actual Revenue" if t.name == "ACT -USD" else "Last Year Revenue" if t.name == "LYR-USD (2023/24)" else t.name
    )
)

fig.update_layout(xaxis_title="Month", yaxis_title="Total Revenue (USD)")

# Side-by-side graphs
col1, col2 = st.columns(2)

# First graph: Overall Revenue Trend
col1.plotly_chart(fig, use_container_width=True)

# Second graph: Revenue by Month (Actual vs Target)
act_avg = df.groupby('Month')['ACT -USD'].mean()
act_tg = df.groupby('Month')[' TGT-USD'].mean()

# Ensure proper month ordering
act_avg = act_avg.reindex(month_order)
act_tg = act_tg.reindex(month_order)

# Creating the second graph with Plotly
fig_target = go.Figure()
fig_target.add_trace(go.Scatter(x=act_avg.index, y=act_avg, mode='lines+markers', name='Actual Revenue', marker=dict(symbol='circle')))
fig_target.add_trace(go.Scatter(x=act_tg.index, y=act_tg, mode='lines+markers', name='Actual Target', marker=dict(symbol='square')))

fig_target.update_layout(
    title="Average Revenue by Month (Actual vs Target)",
    xaxis_title="Month",
    yaxis_title="Average Revenue (USD)",
    legend_title="Legend",
    xaxis=dict(tickangle=45)
)

# Display the second graph in the second column
col2.plotly_chart(fig_target, use_container_width=True)

# Third graph: Exchange Rate Gain/Loss by Month
st.subheader("Exchange Rate Gain/Loss by Month")
exloss_avg = df.groupby('Month')['Exchange - gain/( loss)'].sum()
exloss_avg_ly = df.groupby('Month')['Exchange  -gain/(loss)'].sum()

# Ensure proper month ordering
exloss_avg = exloss_avg.reindex(month_order)
exloss_avg_ly = exloss_avg_ly.reindex(month_order)

# Creating the third graph with Plotly
fig_exloss = go.Figure()
fig_exloss.add_trace(go.Scatter(x=exloss_avg.index, y=exloss_avg, mode='lines+markers', name='ExgRate - Gain/Loss (Current)', marker=dict(symbol='circle')))
fig_exloss.add_trace(go.Scatter(x=exloss_avg_ly.index, y=exloss_avg_ly, mode='lines+markers', name='ExgRate - Gain/Loss (Last Year)', marker=dict(symbol='square')))

# Adding a line at 0 for reference
fig_exloss.add_trace(go.Scatter(x=exloss_avg.index, y=[0]*len(exloss_avg), mode='lines', line=dict(color='gray', dash='dash'), name='Zero Line'))

fig_exloss.update_layout(
    title="Exchange Rate Gain/Loss by Month",
    xaxis_title="Month",
    yaxis_title="Gain/Loss (USD)",
    legend_title="Legend",
    xaxis=dict(tickangle=45)
)

# Display the third graph
st.plotly_chart(fig_exloss, use_container_width=True)

# Additional Graphs with Separate Filters
# Filtered Data based on additional filters
filtered_df_separate = filtered_df.copy()
if selected_month_filter != "All":
    filtered_df_separate = filtered_df_separate[filtered_df_separate['Month'] == selected_month_filter]
if selected_region_filter != "All":
    filtered_df_separate = filtered_df_separate[filtered_df_separate['Region'] == selected_region_filter]

# Revenue Trend for Separate Filters
st.subheader("Separate Revenue Trend by Filters")
melted_df_separate = filtered_df_separate.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)'],
                                               var_name='Revenue Type', value_name='Revenue (USD)')

fig_separate = px.line(
    melted_df_separate,
    x='Month',
    y='Revenue (USD)',
    color='Revenue Type',
    title="Revenue Trend by Filters",
    markers=True
)

# Customizing the legend labels
fig_separate.for_each_trace(
    lambda t: t.update(
        name="Actual Revenue" if t.name == "ACT -USD" else "Last Year Revenue" if t.name == "LYR-USD (2023/24)" else t.name
    )
)

fig_separate.update_layout(xaxis_title="Month", yaxis_title="Revenue (USD)")
st.plotly_chart(fig_separate)
