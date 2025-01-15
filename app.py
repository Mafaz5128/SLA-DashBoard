import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import altair as alt

# Enable a dark theme for Altair
alt.themes.enable("dark")

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI Configuration
st.set_page_config(
    page_title="Station Revenue Analysis Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Load CSS styles
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title Section
st.markdown(
    """
    <h1 style="text-align: center; color: black;">
        Station Revenue Analysis
    </h1>
    """,
    unsafe_allow_html=True
)
st.subheader("Revenue by Month and Region")

# Set the month order explicitly
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Sidebar filters for Region and Point of Sale (POS)
col11, col12, col13 = st.columns([1, 4, 1])

regions = sorted(df['Region'].unique())
selected_regions = []

# Region filter
col11.write("Select Regions:")
if col11.checkbox("All", value=True):
    selected_regions = regions
else:
    for region in regions:
        if col11.checkbox(region):
            selected_regions.append(region)

# POS filter
pos_options = df[df['Region'].isin(selected_regions)]['POINT OF SALE'].unique() if selected_regions else df['POINT OF SALE'].unique()
selected_pos = col13.selectbox("Select POS", options=["All"] + list(sorted(pos_options)), index=0)

# Filter data based on selections
filtered_df = df[df['Region'].isin(selected_regions)] if selected_regions else df
if selected_pos != "All":
    filtered_df = filtered_df[filtered_df['POINT OF SALE'] == selected_pos]

# Revenue Analysis Section
melted_df = filtered_df.melt(
    id_vars=["Month"],
    value_vars=['ACT -USD', 'LYR-USD (2023/24)', ' TGT-USD'], 
    var_name='Revenue Type',
    value_name='Revenue (USD)'
)
avg_revenue_df = melted_df.groupby(['Month', 'Revenue Type'])['Revenue (USD)'].sum().reset_index()
avg_revenue_df['Month'] = pd.Categorical(avg_revenue_df['Month'], categories=month_order, ordered=True)

# Tabs for Revenue Chart and Data Table
tab1, tab2 = col12.tabs(["📈 Chart", "🗃 Data"])

# Revenue Trend Chart
with tab1:
    fig = px.line(
        avg_revenue_df,
        x='Month',
        y='Revenue (USD)',
        color='Revenue Type',
        title=f"Revenue (USD) Trend by Month - {', '.join(selected_regions) or 'All Regions'}",
        markers=True
    )

    # Customize legend labels and layout
    legend_labels = {
        "ACT -USD": "Actual Revenue",
        "LYR-USD (2023/24)": "Last Year Revenue",
        "TGT-USD": "Target Revenue"
    }
    fig.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))
    fig.update_layout(xaxis_title="Month", yaxis_title="Total Revenue (USD)")
    tab1.plotly_chart(fig, use_container_width=True)

# Revenue Data Table
with tab2:
    pivoted_df = avg_revenue_df.pivot_table(
        index='Month',
        columns='Revenue Type',
        values='Revenue (USD)',
        aggfunc='sum'
    ).reset_index()
    tab2.dataframe(pivoted_df)
a1,a2,a3 = st.columns([4,2,2])
# Exchange Rate Gain/Loss Chart
a1.subheader("Exchange Rate Gain/Loss by Month")
exloss_avg = filtered_df.groupby('Month')['Exchange - gain/( loss)'].sum().reindex(month_order)
exloss_avg_ly = filtered_df.groupby('Month')['Exchange  -gain/(loss)'].sum().reindex(month_order)

fig_exloss = go.Figure()
fig_exloss.add_trace(go.Scatter(x=exloss_avg.index, y=exloss_avg, mode='lines+markers', name='Current', marker=dict(symbol='circle', color='#EF553B')))
fig_exloss.add_trace(go.Scatter(x=exloss_avg_ly.index, y=exloss_avg_ly, mode='lines+markers', name='Last Year', marker=dict(symbol='square', color='#636EFA')))
fig_exloss.add_trace(go.Scatter(x=exloss_avg.index, y=[0]*len(exloss_avg), mode='lines', line=dict(color='gray', dash='dash'), name='Zero Line'))

fig_exloss.update_layout(
    title="Exchange Rate Gain/Loss by Month",
    xaxis_title="Month",
    yaxis_title="Gain/Loss (USD)",
    xaxis=dict(tickangle=45)
)
a1.plotly_chart(fig_exloss, use_container_width=True)
# Extract Key Perfomencers
a2.subheader("Key Players -2024 ")







# Revenue Contribution Pie Charts
st.subheader("Revenue Contribution by Month and Region")
selected_month = st.selectbox("Select a Month:", sorted(df['Month'].unique()))

filtered_df_month = df[df['Month'] == selected_month]
revenue_cont_month = filtered_df_month.groupby('Region')['REVENUE CONT. % - Actual'].sum()
revenue_cont_month_ly = filtered_df_month.groupby('Region')['REVENUE CONT. %-LYR'].sum()

col1, col2 = st.columns(2)

# Actual Revenue Contribution Pie
fig_pie = go.Figure(data=[go.Pie(labels=revenue_cont_month.index, values=revenue_cont_month, marker=dict(colors=sns.color_palette("Set3").as_hex()))])
fig_pie.update_layout(title=f"Actual Revenue Contribution - {selected_month}")
col1.plotly_chart(fig_pie, use_container_width=True)

# Last Year Revenue Contribution Pie
fig_pie2 = go.Figure(data=[go.Pie(labels=revenue_cont_month_ly.index, values=revenue_cont_month_ly, marker=dict(colors=sns.color_palette("Set3").as_hex()))])
fig_pie2.update_layout(title=f"Last Year Revenue Contribution - {selected_month}")
col2.plotly_chart(fig_pie2, use_container_width=True)
