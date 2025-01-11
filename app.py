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


# Region filter - Change to checkboxes
selected_regions = []
for region in sorted(df['Region'].unique()):
    if st.sidebar.checkbox(region, value=True):  # Set default to True for all regions
        selected_regions.append(region)

# Filter POS by Region: Based on the selected regions, show corresponding POS
if selected_regions:
    pos_options = df[df['Region'].isin(selected_regions)]['POINT OF SALE'].unique()
else:
    pos_options = df['POINT OF SALE'].unique()

# POS filter for the selected regions - Change to dropdown (selectbox)
selected_pos = st.sidebar.selectbox(
    "Select POS", 
    options=["All"] + list(sorted(pos_options)),
    index=0  # Default to "All"
)

# Filter the data based on selected Regions and POS
filtered_df = df[df['Region'].isin(selected_regions)] if selected_regions else df

if selected_pos != "All":
    filtered_df = filtered_df[filtered_df['POINT OF SALE'] == selected_pos]

# Revenue by Month and Region Section
st.subheader("Revenue by Month and Region")

# First graph: Total Revenue Trend by Month
melted_df = filtered_df.melt(
    id_vars=["Month"],
    value_vars=['ACT -USD', 'LYR-USD (2023/24)', ' TGT-USD'], 
    var_name='Revenue Type',
    value_name='Revenue (USD)'
)

# Group and calculate total revenue
avg_revenue_df = melted_df.groupby(['Month', 'Revenue Type'])['Revenue (USD)'].sum().reset_index()
avg_revenue_df['Month'] = pd.Categorical(avg_revenue_df['Month'], categories=month_order, ordered=True)
pivoted_df = avg_revenue_df.pivot_table(
    index='Month',
    columns='Revenue Type',
    values='Revenue (USD)',
    aggfunc='sum'
).reset_index()


# Tabs: Chart and Table
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

# Tab 1: Chart
with tab1:
    # Create the line plot
    fig = px.line(
        avg_revenue_df,
        x='Month',
        y='Revenue (USD)',
        color='Revenue Type',
        title="Overall Revenue (USD) Trend by Month",
        markers=True
    )

    # Customizing the legend labels
    legend_labels = {
        "ACT -USD": "Actual Revenue",
        "LYR-USD (2023/24)": "Last Year Revenue",
        "TGT-USD": "Target Revenue"
    }

    fig.for_each_trace(
        lambda t: t.update(name=legend_labels.get(t.name, t.name))
    )

    # Update layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Revenue (USD)"
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Data Table
with tab2:
    # Display the table
    st.dataframe(pivoted_df)


# Create a 2x2 grid of plots

st.subheader("Revenue Contribution by Month and Region")
col1, col2, col3 = st.columns([2, 4, 4])
col4, col5 = st.columns(2)
# Pie chart
# Step 1: Sidebar radio button for month selection (only call once)
selected_month = col1.radio(
    "Select a Month:", 
    sorted(df['Month'].unique()),
    horizontal=False # Provide sorted list of months
)

# Step 2: Filter DataFrame for the selected month
filtered_df_month = df[df['Month'] == selected_month]

# Step 3: Calculate the revenue contribution by region
# Since percentages are already provided, we sum them directly

revenue_cont_month = filtered_df_month.groupby('Region')['REVENUE CONT. % - Actual'].sum()

# Step 4: Create the Pie chart for actual
fig_pie = go.Figure(data=[go.Pie(
    labels=revenue_cont_month.index,  # Use region names as labels
    values=revenue_cont_month,        # Use the summed percentages as values
    hoverinfo='label+percent',        # Show label and percentage on hover
    textinfo='percent',               # Display percentage inside the pie
    marker=dict(colors=sns.color_palette("Set3", len(revenue_cont_month)).as_hex())
)])

# Customize layout for Actual Revenue Contribution
fig_pie.update_layout(
    title={
        'text': f"Actual Revenue Contribution by Region - {selected_month}",
        'x': 0.5,  # Center the title horizontally
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 11},  # Reduce title size
    },
    margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins for better visibility
    height=450,  # Increase the height of the pie chart to make it larger
)

# Display pie chart for Actual Revenue Contribution
col2.plotly_chart(fig_pie, use_container_width=True)

#Create the Pie chart for actual
revenue_cont_month_ly = filtered_df_month.groupby('Region')['REVENUE CONT. %-LYR'].sum()
fig_pie2 = go.Figure(data=[go.Pie(
    labels=revenue_cont_month_ly.index,  # Use region names as labels
    values=revenue_cont_month_ly,        # Use the summed percentages as values
    hoverinfo='label+percent',        # Show label and percentage on hover
    textinfo='percent',               # Display percentage inside the pie
    marker=dict(colors=sns.color_palette("Set3", len(revenue_cont_month_ly)).as_hex())  # Seaborn palette
)])

# Customize layout for Last Year Revenue Contribution
fig_pie2.update_layout(
    title={
        'text': f"Last Revenue Contribution by Region - {selected_month}",
        'x': 0.5,  # Center the title horizontally
        'xanchor': 'center',  # Anchor title to the center
        'font': {'size': 11},  # Reduce title size
    },
    margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins for better visibility
    height=450,  # Increase the height of the pie chart to make it larger
)

# Display pie chart for Last Year Revenue Contribution
col3.plotly_chart(fig_pie2, use_container_width=True)

st.plotly_chart(fig_target, use_container_width=True)

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

col5.plotly_chart(fig_exloss, use_container_width=True)


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
