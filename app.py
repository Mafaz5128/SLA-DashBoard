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
exrate_avg = df.groupby('Month')['Act. Using-Bgt. ex. Rates'].mean()  # Mean for Exchange Rates
exloss_avg = df.groupby('Month')['Exchange - gain/( loss)'].mean()  # Exchange Rate Gain/Loss
exloss_avg_ly = df.groupby('Month')['Exchange  -gain/(loss)'].mean()  # Exchange Rate Gain/Loss (Last Year)

# Sorting the index (month names) to ensure proper order
month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
act_avg = act_avg.reindex(month_order)
lyr_avg = lyr_avg.reindex(month_order)
act_tg = act_tg.reindex(month_order)
exrate_avg = exrate_avg.reindex(month_order)
exloss_avg = exloss_avg.reindex(month_order)
exloss_avg_ly = exloss_avg_ly.reindex(month_order)

# Creating 2x2 grid for subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Plot 1: ACTUAL vs LAST YEAR Revenue Trend
axes[0, 0].plot(act_avg, marker='o', label='ACTUAL', color='blue')
axes[0, 0].plot(lyr_avg, marker='s', label='LAST YEAR(2023/24)', color='green')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Revenue (USD)')
axes[0, 0].set_title('Revenue Trend by Month (ACTUAL vs LAST YEAR)')
axes[0, 0].set_xticklabels(month_order, rotation=45)
axes[0, 0].legend()

# Plot 2: ACTUAL vs TARGET Revenue Trend
axes[0, 1].plot(act_avg, marker='o', label='ACTUAL', color='blue')
axes[0, 1].plot(act_tg, marker='s', label='TARGET', color='red')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Revenue (USD)')
axes[0, 1].set_title('Revenue Trend by Month (ACTUAL vs TARGET)')
axes[0, 1].set_xticklabels(month_order, rotation=45)
axes[0, 1].legend()

# Plot 3: Average Exchange Rate
axes[1, 0].plot(exrate_avg, marker='o', label='Average Exchange Rate', color='purple')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Exchange Rate')
axes[1, 0].set_title('Average Exchange Rate by Month')
axes[1, 0].set_xticklabels(month_order, rotation=45)
axes[1, 0].legend()

# Plot 4: Exchange Rate Gain/Loss (Current Year vs Last Year)
axes[1, 1].plot(exloss_avg, marker='o', label='ExgRate - gain/Loss', color='orange')
axes[1, 1].plot(exloss_avg_ly, marker='s', label='ExgRate - gain/loss (LY)', color='cyan')
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Gain/Loss(USD)')
axes[1, 1].set_title('ExgRate Gain/Loss by Month')
axes[1, 1].set_xticklabels(month_order, rotation=45)
axes[1, 1].legend()

# Adding tight layout for better spacing
plt.tight_layout()

# Display the 2x2 grid of plots in Streamlit
st.subheader("ACTUAL vs LAST YEAR Revenue Trend")
st.pyplot(fig)

# Optional: Showing individual plots as well if needed
# st.pyplot(fig1)  # For individual plot if required, for example
