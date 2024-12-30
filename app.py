import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For color palettes

# Load the data
df = pd.read_excel("Stationary_Perf.xlsx")

# Streamlit UI
st.title("Station Revenue Analytics")

# Grouping by month and calculating the average for both columns
act_avg = df.groupby('Month')['ACT -USD'].mean()  # Mean for ACTUAL
lyr_avg = df.groupby('Month')['LYR-USD (2023/24)'].mean()  # Mean for LAST YEAR
act_tg = df.groupby('Month')[' TGT-USD'].mean()  # Mean for TARGET

# Sorting the index (month names) to ensure proper order
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
act_avg = act_avg.reindex(month_order)
lyr_avg = lyr_avg.reindex(month_order)
act_tg = act_tg.reindex(month_order)

# Plotting the first graph for ACTUAL and LAST YEAR
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(act_avg, marker='o', label='ACTUAL')
ax.plot(lyr_avg, marker='s', label='LAST YEAR(2023/24)')

# Adding labels, title, and legend for the first graph
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (USD)')
ax.set_title('Revenue Trend by Month (ACTUAL vs LAST YEAR)')
ax.set_xticklabels(month_order, rotation=45)
ax.legend()

# Displaying the first plot in Streamlit
st.subheader("ACTUAL vs LAST YEAR Revenue Trend")
st.pyplot(fig)

# Plotting the second graph for ACTUAL and TARGET
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(act_avg, marker='o', label='ACTUAL')
ax.plot(act_tg, marker='s', label='TARGET')

# Adding labels, title, and legend for the second graph
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (USD)')
ax.set_title('Revenue Trend by Month (ACTUAL vs TARGET)')
ax.set_xticklabels(month_order, rotation=45)
ax.legend()

# Displaying the second plot in Streamlit
st.subheader("ACTUAL vs TARGET Revenue Trend")
st.pyplot(fig)

# Grouping the data by Month and Region for the third graph
act_avg_region = df.groupby(['Month', 'Region'])['ACT -USD'].mean().reset_index()

# Defining the order of months for consistent plotting
act_avg_region['Month'] = pd.Categorical(act_avg_region['Month'], categories=month_order, ordered=True)
act_avg_region = act_avg_region.sort_values('Month')

# Setting the color palette
palette = sns.color_palette("husl", len(act_avg_region['Region'].unique()))

# Creating the third plot for Revenue by Month and Region
fig, ax = plt.subplots(figsize=(14, 8))

# Looping through each region to plot its line
for i, region in enumerate(act_avg_region['Region'].unique()):
    region_data = act_avg_region[act_avg_region['Region'] == region]
    ax.plot(region_data['Month'], region_data['ACT -USD'],
             marker='o', linestyle='-', color=palette[i], label=region)

# Adding gridlines
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Adding labels, title, and legend for the third graph
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue (USD)', fontsize=12)
ax.set_title('Revenue by Month and Region', fontsize=14)
ax.set_xticklabels(month_order, rotation=45, fontsize=10)
ax.set_yticklabels(fontsize=10)
ax.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# Adding tight layout for better spacing
plt.tight_layout()

# Displaying the third plot in Streamlit
st.subheader("Revenue by Month and Region")
st.pyplot(fig)
