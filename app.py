import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For color palettes
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI
st.set_page_config(page_title="Revenue Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Revenue Analysis Dashboard")

# Set the month order explicitly
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Overall Revenue Trend Chart (Average Revenue by Type)
st.subheader("Total Revenue Trend by Month")
melted_df = df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)'], 
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
fig_target.add_trace(go.Scatter(x=act_avg.index, y=act_avg, mode='lines+markers', name='Actual Revenue', marker=dict(symbol='circle', color='#00CC96')))
fig_target.add_trace(go.Scatter(x=act_tg.index, y=act_tg, mode='lines+markers', name='Actual Target', marker=dict(symbol='square', color='#636EFA')))

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
fig_exloss.add_trace(go.Scatter(x=exloss_avg.index, y=exloss_avg, mode='lines+markers', name='ExgRate - Gain/Loss (Current)', marker=dict(symbol='circle', color='#EF553B')))
fig_exloss.add_trace(go.Scatter(x=exloss_avg_ly.index, y=exloss_avg_ly, mode='lines+markers', name='ExgRate - Gain/Loss (Last Year)', marker=dict(symbol='square', color='#636EFA')))
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

# Fourth graph: Revenue Contribution by Region
con_act_avg_region = df.groupby('Region')['REVENUE CONT. % - Actual'].mean()
con_ly_avg_region = df.groupby('Region')['REVENUE CONT. %-LYR'].mean()

# Creating the Plotly chart for revenue contribution by Region
fig_contribution_region = go.Figure()
fig_contribution_region.add_trace(go.Scatter(
    x=con_act_avg_region.index, 
    y=con_act_avg_region, 
    mode='lines+markers', 
    name='Contribution - Actual', 
    marker=dict(symbol='circle', color='#00CC96')
))
fig_contribution_region.add_trace(go.Scatter(
    x=con_ly_avg_region.index, 
    y=con_ly_avg_region, 
    mode='lines+markers', 
    name='Contribution - Last Year', 
    marker=dict(symbol='square', color='#636EFA')
))

fig_contribution_region.update_layout(
    title="Revenue Contribution by Region",
    xaxis_title="Region",
    yaxis_title="Contribution (%)",
    legend_title="Legend",
    xaxis=dict(tickangle=45)
)

# Displaying the new graph in the dashboard
st.subheader("Revenue Contribution by Region")
st.plotly_chart(fig_contribution_region, use_container_width=True)

# Adding custom CSS styles for the dashboard and filters
st.markdown("""
    <style>
    /* Apply background color to the entire dashboard */
    .block-container {
        background-color: #f4f8fb;  /* Light blue background */
    }

    /* Apply background color to the filter widgets */
    .stSelectbox, .stMarkdown, .stRadio, .stButton {
        background-color: #e8f0fe;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Customizing filter text and dropdown */
    .stSelectbox select {
        font-size: 16px;
        color: #333;
    }

    .stSelectbox label {
        color: #4f5d73;
        font-weight: bold;
    }

    .stButton {
        background-color: #66b3ff;
        color: white;
    }

    .stButton:hover {
        background-color: #0059b3;
    }

    .stSelectbox select:focus {
        border: 2px solid #66b3ff;
        outline: none;
    }

    .stSelectbox label:hover {
        color: #0059b3;
    }
    </style>
""", unsafe_allow_html=True)

# Filters Section
st.subheader("Filters")
selected_region_filter = st.selectbox("Select Region", options=["All"] + list(sorted(df['Region'].unique())), index=0)

# Filter POS by Region: Based on the region selected, show corresponding POS
if selected_region_filter != "All":
    # Filter the POS options by the selected region
    pos_options = df[df['Region'] == selected_region_filter]['POINT OF SALE'].unique()
else:
    # If "All" is selected, show all POS options
    pos_options = df['POINT OF SALE'].unique()

# POS filter for the selected region
selected_pos = st.selectbox("Select POS", options=["All"] + list(sorted(pos_options)), index=0)

# Matplotlib Plot: Revenue by Month and Region
st.subheader("Revenue by Month and Region")

# Grouping the data by Month and Region
act_avg_region = df.groupby(['Month', 'Region'])['ACT -USD'].mean().reset_index()

# Defining the order of months for consistent plotting
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
act_avg_region['Month'] = pd.Categorical(act_avg_region['Month'], categories=month_order, ordered=True)
act_avg_region = act_avg_region.sort_values('Month')

# Setting the color palette
palette = sns.color_palette("husl", len(act_avg_region['Region'].unique()))

# Creating the plot
plt.figure(figsize=(14, 8))

# Looping through each region to plot its line
for i, region in enumerate(act_avg_region['Region'].unique()):
    region_data = act_avg_region[act_avg_region['Region'] == region]
    plt.plot(region_data['Month'], region_data['ACT -USD'],
             marker='o', linestyle='-', color=palette[i], label=region)

# Adding gridlines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adding labels, title, and legend
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (USD)', fontsize=12)
plt.title('Revenue by Month and Region', fontsize=14)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# Adding tight layout for better spacing
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)
