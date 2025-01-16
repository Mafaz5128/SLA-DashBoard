import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import altair as alt

# Enable a dark theme for Altair
alt.themes.enable("dark")

# Streamlit UI Configuration
st.set_page_config(
    page_title="Station Revenue Analysis Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Load CSS styles
#with open('style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title Section
st.markdown(
    """
    <h1 style="text-align: center; color: white;">
        Station Revenue Analysis
    </h1>
    """,
    unsafe_allow_html=True
)
st.link_button(
    label="Data set Maker",
    url="https://datasetmaker-3uy2exn2eq89ubuazxwwwu.streamlit.app/"
)
# File uploader widget
uploaded_file = st.file_uploader("Upload your Excel file", type=["csv"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Load the uploaded Excel file
    df = pd.read_csv(uploaded_file)

    # Show a preview of the uploaded data
    st.write("Data preview:", df.head())

    # Continue with the rest of your code here

    st.subheader("Revenue by Month and Region")




    # Define the standard month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Extract the unique months present in the data
    unique_months = df['Month'].unique()

# Sort the unique months based on the standard month order
    sorted_month_order = [month for month in month_order if month in unique_months]

# Ensure the 'Month' column is ordered by the sorted month order
    df['Month'] = pd.Categorical(df['Month'], categories=sorted_month_order, ordered=True)

    # Rest of your code continues as usual...


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

    # Exchange Rate Gain/Loss Chart
    a1, a2, a3 = st.columns([1, 1, 1])

    a1.subheader("Exchange Rate Gain/Loss by Month")
    exloss_avg = filtered_df.groupby('Month')['Exchange - gain/( loss)'].sum().reindex(sorted_month_order)
    exloss_avg_ly = filtered_df.groupby('Month')['Exchange  -gain/(loss)'].sum().reindex(sorted_month_order)

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

    # Extract the top 5 performers by POS based on ACT-USD
    select_region = df[df['Region'].isin(selected_regions)] if selected_regions else df
    top_performers = (
        select_region.groupby('POINT OF SALE')['ACT -USD']
        .sum()
        .nlargest(5)
        .reset_index()
    )

    # Optional: Visualize the top 5 performers with a bar chart
    fig_top_performers = px.bar(
        top_performers,
        x='POINT OF SALE',
        y='ACT -USD',
        title=f"Top 5 Performers of {', '.join(selected_regions) or 'All Regions'}-2024",
        text_auto='.2s',
        color='ACT -USD',
        labels={'ACT -USD': 'Actual Revenue (USD)', 'POINT OF SALE': 'Point of Sale'},
        color_continuous_scale=px.colors.sequential.Viridis
    )

    # Update chart layout
    fig_top_performers.update_layout(
        xaxis_title="Point of Sale",
        yaxis_title="Actual Revenue (USD)",
        title_x=0.1, # Center the chart title
        title_font = dict(size=12)
    )

    # Display the bar chart
    a2.plotly_chart(fig_top_performers, use_container_width=True)

    # Extract Key Performers for Last Year
    # Extract the top 5 performers by POS based on LYR-USD (2023/24)
    top_performers_last_year = (
        select_region.groupby('POINT OF SALE')['LYR-USD (2023/24)']
        .sum()
        .nlargest(5)
        .reset_index()
    )

    # Optional: Visualize the top 5 performers for last year with a bar chart
    fig_top_performers_last_year = px.bar(
        top_performers_last_year,
        x='POINT OF SALE',
        y='LYR-USD (2023/24)',
        title=f"Top 5 Performers of {', '.join(selected_regions) or 'All Regions'}-2023",
        color = 'LYR-USD (2023/24)',
        text_auto='.2s',
        labels={'LYR-USD (2023/24)': 'Last Year Revenue (USD)', 'POINT OF SALE': 'Point of Sale'},
        color_continuous_scale=px.colors.sequential.Plasma
    )

    # Update chart layout
    fig_top_performers_last_year.update_layout(
        xaxis_title="Point of Sale",
        yaxis_title="Last Year Revenue (USD)",
        title_x=0.1,  # Center the chart title
        title_font = dict(size=12)
    )

    # Display the bar chart for last year
    a3.plotly_chart(fig_top_performers_last_year, use_container_width=True)

    # Revenue Contribution Pie Charts
    st.subheader("Revenue Contribution by Month and Region")
    selected_month = st.selectbox("Select a Month:", sorted(df['Month'].unique()))

    filtered_df_month = df[df['Month'] == selected_month]
    revenue_cont_month = filtered_df_month.groupby('Region')['REVENUE CONT. % - Actual'].sum()
    revenue_cont_month_ly = filtered_df_month.groupby('Region')['REVENUE CONT. %-LYR'].sum()

    col1, col2 = st.columns(2)

    # Actual Revenue Contribution Pie
    fig_pie = go.Figure(data=[go.Pie(labels=revenue_cont_month.index, values=revenue_cont_month, hole=0.4, marker=dict(colors=sns.color_palette("Paired").as_hex()))])
    fig_pie.update_layout(title=f"Actual Revenue Contribution - {selected_month}")
    col1.plotly_chart(fig_pie, use_container_width=True)

    # Last Year Revenue Contribution Pie
    fig_pie2 = go.Figure(data=[go.Pie(labels=revenue_cont_month_ly.index, values=revenue_cont_month_ly,hole=0.4, marker=dict(colors=sns.color_palette("Paired").as_hex()))])
    fig_pie2.update_layout(title=f"Last Year Revenue Contribution - {selected_month}")
    col2.plotly_chart(fig_pie2, use_container_width=True)

else:
    st.write("Please upload a file to get started.")
