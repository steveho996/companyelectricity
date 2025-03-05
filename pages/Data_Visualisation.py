import pandas as pd
import streamlit as st

st.title("📈 Data Visualization")
st.sidebar.header("📈 Data Visualization - Page 2")
st.write("""In this page, data can be grouped by daily, weekly, or monthly intervals for trend analysis.
        \nThe data is visualized using line charts, which help stakeholders track the fluctuations and trends of each data component, 
         such as electricity consumption, electricity price, electricity bill, and temperature. 
         This enables stakeholders to plan the use of electricity effectively, which leads to reduced operational costs.""")

# Load data 
path1 = '/Users/HoLuongDuc/Mac Air Data/Master Degree/Data and Math/Python/Electricity_20-09-2024.csv'
path2 = 'sahkon-hinta-010121-240924.csv'

df1 = pd.read_csv(path1, sep=';')
df2 = pd.read_csv(path2, sep=',')

df1['Time'] = pd.to_datetime(df1['Time'].str.strip(), dayfirst=True, errors='coerce')
df2['Time'] = pd.to_datetime(df2['Time'], format='%d-%m-%Y %H:%M:%S', errors='coerce')

merged_df = pd.merge(df1, df2, on='Time', how='inner')

merged_df['Energy (kWh)'] = merged_df['Energy (kWh)'].str.replace(',', '.').astype(float)
merged_df['Price (cent/kWh)'] = merged_df['Price (cent/kWh)'].astype(float)
merged_df['Temperature'] = merged_df['Temperature'].str.replace(',', '.').astype(float)
merged_df['Hourly Bill'] = merged_df['Energy (kWh)'] * merged_df['Price (cent/kWh)']
merged_df.set_index('Time', inplace=True)

# Filter Data
start_date = st.date_input("Start Date", merged_df.index.min().date())
end_date = st.date_input("End Date", merged_df.index.max().date())

filtered_df = merged_df[(merged_df.index >= pd.to_datetime(start_date)) &
                        (merged_df.index <= pd.to_datetime(end_date))]

# Data Grouping
grouping_interval = st.selectbox("Group By:", ["Daily", "Weekly", "Monthly"])
grouped_df = filtered_df.resample(
    {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'M'}[grouping_interval]
).agg({
    'Energy (kWh)': 'sum',
    'Price (cent/kWh)': 'mean',
    'Temperature': 'mean',
    'Hourly Bill': 'sum'
})

# Streamlit Charts
st.subheader("Electricity consumption (kWh)")
st.write("""Represents the volume of electrical energy used over a specified period, measured in kilowatt-hours. 
         This metric is foundational for understanding usage trends, peak demand periods, or seasonal variations.""" )
st.line_chart(grouped_df['Energy (kWh)'])

st.subheader("Electricity price (cents/kWh)")
st.write("""Indicates the cost per unit of electricity, likely reflecting tariffs, regional pricing, or time-of-use rates. 
         This variable helps correlate consumption behavior with financial implications.""")
st.line_chart(grouped_df['Price (cent/kWh)'])

st.subheader("Electricity bill (€)")
st.write("""Represents the total cost of electricity consumed, calculated as Consumption (kWh) × Price (cost/kWh). 
         This metric ties usage and pricing to financial outcomes, highlighting cost-saving opportunities or budget impacts.""")
st.line_chart(grouped_df['Hourly Bill'])

st.subheader("Temperature")
st.write("""Acts as a contextual variable, 
         likely showing correlations between weather conditions.""")
st.line_chart(grouped_df['Temperature'])
