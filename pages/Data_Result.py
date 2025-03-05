import pandas as pd
import streamlit as st

st.title("🔢 Data Result")
st.sidebar.header("🔢 Data Result - Page 1")
st.write("""In this page, the data is dynamically updated based on the chosen timeframe.
         \nBase on the data index, the stakeholders are able to select a custom date range to analyze electricity usage, total bill and pricing for a specific period.""")

# Load data
path1 = 'Electricity_20-09-2024.csv'
path2 = 'sahkon-hinta-010121-240924.csv'

df1 = pd.read_csv(path1, sep=';')
df2 = pd.read_csv(path2, sep=',')

df1['Time'] = pd.to_datetime(df1['Time'].str.strip(), dayfirst=True, errors='coerce')
df2['Time'] = pd.to_datetime(df2['Time'], format='%d-%m-%Y %H:%M:%S', errors='coerce')

merged_df = pd.merge(df1, df2, on='Time', how='inner')

# Data processing
merged_df['Energy (kWh)'] = merged_df['Energy (kWh)'].str.replace(',', '.').astype(float)
merged_df['Price (cent/kWh)'] = merged_df['Price (cent/kWh)'].astype(float)
merged_df['Temperature'] = merged_df['Temperature'].str.replace(',', '.').astype(float)

# Hourly Bill
merged_df['Hourly Bill'] = merged_df['Energy (kWh)'] * merged_df['Price (cent/kWh)']

# Streamlit visualisation
merged_df.set_index('Time', inplace=True)

start_date = st.date_input("Start Date", merged_df.index.min().date())
end_date = st.date_input("End Date", merged_df.index.max().date())

filtered_df = merged_df[(merged_df.index >= pd.to_datetime(start_date)) &
                        (merged_df.index <= pd.to_datetime(end_date))]

st.write(f"Selected Date Range: **{start_date}** to **{end_date}**")
st.write(f"Total consumption: **{filtered_df['Energy (kWh)'].sum():,.2f} kWh**")
st.write(f"Total bill: **{filtered_df['Hourly Bill'].sum()/100:,.2f} €**")
st.write(f"Average hourly price: **{filtered_df['Price (cent/kWh)'].mean():.2f} cents**")
