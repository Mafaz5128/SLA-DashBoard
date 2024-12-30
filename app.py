import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For color palettes
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI
st.set_page_config(page_title="Station Revenue Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Revenue Analysis Dashboard")

# Set the month order explicitly
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Filters Section
st.subheader("Filters")

# Region filter
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

# Filter the data based on selected Region and POS
if selected_region_filter != "All":
    filtered_df = df[df['Region'] == selected_region_filter]
else:
    filtered_df = df

if selected_pos != "All":
    filtered_df = filtered_df[filtered_df['POINT OF SALE'] == selected_pos]

# Revenue by Month and Region Section
st.subheader("Revenue by Month and Region")

# Create a 2x2 grid of plots
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# First graph: Total Revenue Trend by Month
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)'], 
                     var_name='Revenue Type', value_name='Revenue (USD)')

avg_revenue_df = melted_df.groupby(['Month', 'Revenue Type'])['Revenue (USD)'].sum().reset_index()
avg_revenue_df['Month'] = pd.Categorical(avg_revenue_df['Month'], categories=month_order, ordered=True)

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
col1.plotly_chart(fig, use_container_width=True)

# Second graph: Revenue Contribution by Region (Pie Chart)
# Step 1: Calculate the sum of 'ACT -USD' by Region
revenue_by_region = filtered_df.groupby('Region')['ACT -USD'].sum()

# Step 2: Calculate the total 'ACT -USD'
total_revenue = revenue_by_region.sum()

# Step 3: Calculate the percentage contribution by region
revenue_percentage = (revenue_by_region / total_revenue) * 100

# Step 4: Create the Pie chart
fig_pie = go.Figure(data=[go.Pie(
    labels=revenue_percentage.index,
    values=revenue_percentage,
    hoverinfo='label+percent',
    textinfo='percent',
    marker=dict(colors=sns.color_palette("Set3", len(revenue_percentage)).as_hex())  # Use a seaborn color palette
)])

# Customize layout (title centered)
fig_pie.update_layout(
    title={
        'text': "Revenue Contribution by Region",
        'x': 0.5,  # Center the title horizontally
        'xanchor': 'center',  # Anchor title to the center
    },
    margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins for better visibility
)

# Display pie chart
col2.plotly_chart(fig_pie, use_container_width=True)

# Third graph: Revenue by Month (Actual vs Target)
act_avg = filtered_df.groupby('Month')['ACT -USD'].mean()
act_tg = filtered_df.groupby('Month')[' TGT-USD'].mean()

# Ensure proper month ordering
act_avg = act_avg.reindex(month_order)
act_tg = act_tg.reindex(month_order)

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

col3.plotly_chart(fig_target, use_container_width=True)

# Fourth graph: Exchange Rate Gain/Loss by Month
exloss_avg = filtered_df.groupby('Month')['Exchange - gain/( loss)'].sum()
exloss_avg_ly = filtered_df.groupby('Month')['Exchange  -gain/(loss)'].sum()

# Ensure proper month ordering
exloss_avg = exloss_avg.reindex(month_order)
exloss_avg_ly = exloss_avg_ly.reindex(month_order)

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

col4.plotly_chart(fig_exloss, use_container_width=True)

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
