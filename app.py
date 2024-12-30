import streamlit as st
import pandas as pd
import plotly.express as px

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
    options=['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], 
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
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
filtered_df['Month'] = pd.Categorical(filtered_df['Month'], categories=month_order, ordered=True)

# Overall Revenue Trend Chart (Average Revenue by Type)
st.subheader("Total Revenue Trend by Month")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)'],  # Removed 'TGT-USD'
                             var_name='Revenue Type', value_name='Revenue (USD)')

# Group by Month and Revenue Type to calculate average revenue
avg_revenue_df = melted_df.groupby(['Month', 'Revenue Type'])['Revenue (USD)'].sum().reset_index()

# Ensure month ordering is reflected in the plot
avg_revenue_df['Month'] = pd.Categorical(avg_revenue_df['Month'], categories=month_order, ordered=True)

# Plot the chart with average revenue
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

fig.update_layout(xaxis_title="Month", yaxis_title="Average Revenue (USD)")
st.plotly_chart(fig)

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
