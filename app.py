import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI
st.set_page_config(page_title="Station Revenue Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Station Revenue Analysis")

# Set the month order explicitly
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)


# Region filter - Change to multiselect
selected_region_filter = st.sidebar.multiselect(
    "Select Region", 
    options=list(sorted(df['Region'].unique())), 
    default=[df['Region'].unique()[0]]  # Default to the first region
)

# Filter POS by Region: Based on the selected regions, show corresponding POS
if selected_region_filter:
    # Filter the POS options by the selected regions
    pos_options = df[df['Region'].isin(selected_region_filter)]['POINT OF SALE'].unique()
else:
    # If no region is selected, show all POS options
    pos_options = df['POINT OF SALE'].unique()

# POS filter for the selected region - Change to multiselect
selected_pos = st.sidebar.multiselect(
    "Select POS", 
    options=["All"] + list(sorted(pos_options)),
    default=["All"]  # Default to "All"
)

# Filter the data based on selected Region and POS
filtered_df = df[df['Region'].isin(selected_region_filter)] if selected_region_filter else df

if "All" not in selected_pos:
    filtered_df = filtered_df[filtered_df['POINT OF SALE'].isin(selected_pos)]


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

# Fifth graph: Revenue Contribution Percentage by Region (Actual and LY)
con_act_avg_region = filtered_df.groupby('Region')['REVENUE CONT. % - Actual'].mean()
con_ly_avg_region = filtered_df.groupby('Region')['REVENUE CONT. %-LYR'].mean()

# Create the line plot for Revenue Contribution Percentage by Region
fig_contribution_region = go.Figure()

# Actual Revenue Contribution by Region
fig_contribution_region.add_trace(go.Scatter(
    x=con_act_avg_region.index, 
    y=con_act_avg_region, 
    mode='lines+markers', 
    name='Contribution - Actual', 
    marker=dict(symbol='circle', color='#00CC96')
))

# Last Year Revenue Contribution by Region
fig_contribution_region.add_trace(go.Scatter(
    x=con_ly_avg_region.index, 
    y=con_ly_avg_region, 
    mode='lines+markers', 
    name='Contribution - Last Year', 
    marker=dict(symbol='square', color='#636EFA')
))

fig_contribution_region.update_layout(
    title="Revenue Contribution by Region (Actual vs Last Year)",
    xaxis_title="Region",
    yaxis_title="Contribution (%)",
    legend_title="Legend",
    xaxis=dict(tickangle=45)
)

# Display the contribution percentage graph
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
