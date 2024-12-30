import streamlit as st
import pandas as pd
import plotly.express as px
import inspect
import textwrap
from demo_echarts import ST_DEMOS
from demo_pyecharts import ST_PY_DEMOS

# Load the data
df = pd.read_excel("C:/Users/mafaz/OneDrive/Desktop/SriLankan Airlines/Station data/Stationary_Perf.xlsx")

# Streamlit UI
st.set_page_config(page_title="Revenue Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Revenue Analysis Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")
selected_pos = st.sidebar.selectbox("Select POS", options=[None] + list(sorted(df['POINT OF SALE'].unique())), index=0)
selected_region = st.sidebar.selectbox("Select Region", options=[None] + list(sorted(df['Region'].unique())), index=0)
selected_month = st.sidebar.selectbox("Select Month", options=['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'], index=0)

# Additional filters for separate graphs
st.sidebar.header("Additional Filters")
selected_month_filter = st.sidebar.selectbox("Select Month for Separate Graph", options=['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'], index=0)
selected_region_filter = st.sidebar.selectbox("Select Region for Separate Graph", options=[None] + list(sorted(df['Region'].unique())), index=0)

# Function to filter dataframe based on selected filters
def filter_df(df, pos=None, region=None, month=None):
    filtered_df = df.copy()
    if pos:
        filtered_df = filtered_df[filtered_df['POINT OF SALE'] == pos]
    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if month:
        filtered_df = filtered_df[filtered_df['Month'] == month]
    return filtered_df

# Filtered Data based on main filters
filtered_df = filter_df(df, selected_pos, selected_region, selected_month)

# Overall Revenue Trend Chart
st.subheader("Overall Revenue Trend")
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', 'TGT-USD'],
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
melted_df = filtered_df.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', 'TGT-USD'],
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

# Filtered Data based on additional filters (Month and Region for separate graphs)
filtered_df_separate = filter_df(df, selected_pos, selected_region_filter, selected_month_filter)

# Separate graphs for filtered data by month
st.subheader("Separate Revenue Trend by Month")
melted_df_separate = filtered_df_separate.melt(id_vars=["Month"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', 'TGT-USD'],
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
melted_df_region = filtered_df_separate.melt(id_vars=["Region"], value_vars=['ACT -USD', 'LYR-USD (2023/24)', 'TGT-USD'],
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

# Add Streamlit ECharts for enhanced visualizations
def main():
    st.title("Streamlit ECharts Demo")

    with st.sidebar:
        st.header("Configuration")
        api_options = ("echarts", "pyecharts")
        selected_api = st.selectbox(
            label="Choose your preferred API:",
            options=api_options,
        )

        page_options = (
            list(ST_PY_DEMOS.keys())
            if selected_api == "pyecharts"
            else list(ST_DEMOS.keys())
        )
        selected_page = st.selectbox(
            label="Choose an example",
            options=page_options,
        )
        demo, url = (
            ST_DEMOS[selected_page]
            if selected_api == "echarts"
            else ST_PY_DEMOS[selected_page]
        )

        if selected_api == "echarts":
            st.caption(
                """ECharts demos are extracted from https://echarts.apache.org/examples/en/index.html, 
            by copying/formattting the 'option' json object into st_echarts.
            Definitely check the echarts example page, convert the JSON specs to Python Dicts and you should get a nice viz."""
            )
        if selected_api == "pyecharts":
            st.caption(
                """Pyecharts demos are extracted from https://github.com/pyecharts/pyecharts-gallery,
            by copying the pyecharts object into st_pyecharts. 
            Pyecharts is still using ECharts 4 underneath, which is why the theming between st_echarts and st_pyecharts is different."""
            )

    demo()

    sourcelines, _ = inspect.getsourcelines(demo)
    with st.expander("Source Code"):
        st.code(textwrap.dedent("".join(sourcelines[1:])))
    st.markdown(f"Credit: {url}")

if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit ECharts Demo", page_icon=":chart_with_upwards_trend:")
    main()

    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/andfanilo">@andfanilo</a></h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="margin-top: 0.75em;"><a href="https://www.buymeacoffee.com/andfanilo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()
