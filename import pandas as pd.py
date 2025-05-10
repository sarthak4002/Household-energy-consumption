import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv(r"C:\Users\sarth\Downloads\individual+household+electric+power+consumption\household_power_consumption.txt", 
                   sep=';', 
                   parse_dates={'timestamp': ['Date', 'Time']}, 
                   infer_datetime_format=True, 
                   low_memory=False, 
                   na_values=['nan', '?'])

# Drop rows with missing values
data.dropna(inplace=True)

# Convert relevant columns to numeric
data['Global_active_power'] = pd.to_numeric(data['Global_active_power'])
data['Global_reactive_power'] = pd.to_numeric(data['Global_reactive_power'])
data['Voltage'] = pd.to_numeric(data['Voltage'])
data['Global_intensity'] = pd.to_numeric(data['Global_intensity'])
data['Sub_metering_1'] = pd.to_numeric(data['Sub_metering_1'])
data['Sub_metering_2'] = pd.to_numeric(data['Sub_metering_2'])
data['Sub_metering_3'] = pd.to_numeric(data['Sub_metering_3'])

# Resample data to hourly consumption
data.set_index('timestamp', inplace=True)
hourly_data = data.resample('H').mean()  # Aggregating to hourly data

# Add columns for 'hour' and 'weekday'
hourly_data['hour'] = hourly_data.index.hour
hourly_data['weekday'] = hourly_data.index.weekday

# Define peak hours (6 AM - 9 AM, 5 PM - 9 PM)
def get_peak_hours(df):
    return df[(df['hour'] >= 6) & (df['hour'] <= 9) | (df['hour'] >= 17) & (df['hour'] <= 21)]

# Filter for peak hours
peak_data = get_peak_hours(hourly_data)

# Calculate overall average to define a threshold for inefficient usage
overall_avg = peak_data['Global_active_power'].mean()

# Set a higher threshold (e.g., 1.5 times the overall average)
threshold = overall_avg * 2

# Identify inefficient users (rows where consumption exceeds the threshold)
inefficient_users = peak_data[peak_data['Global_active_power'] > threshold]

# Create a set to keep track of inefficient days
inefficient_days = set(inefficient_users.index.date)

# Provide energy-saving recommendations for users with high consumption
if inefficient_users.empty:
    print("No inefficient users detected during peak hours.")
else:
    for index, row in inefficient_users.iterrows():
        print(f"At {index}, your energy consumption is above the threshold.")
        print(f"Recommendation: Consider turning off unused appliances or using energy-efficient devices during peak hours.\n")

# Display all inefficient days at once
print("Inefficient days (where high consumption was detected):")
for day in sorted(inefficient_days):
    print(day)

# Plotting the distribution of Global Active Power
plt.figure(figsize=(12, 6))
plt.hist(peak_data['Global_active_power'], bins=50, color='blue', alpha=0.7)
plt.axvline(overall_avg, color='red', linestyle='dashed', linewidth=2, label='Overall Average')
plt.axvline(threshold, color='orange', linestyle='dashed', linewidth=2, label='Threshold')
plt.title('Distribution of Global Active Power During Peak Hours')
plt.xlabel('Global Active Power (kilowatts)')
plt.ylabel('Frequency')
plt.legend()
plt.grid()
plt.show()

# Additional analysis: Average consumption by weekday
weekday_avg = hourly_data.groupby('weekday')['Global_active_power'].mean()
print("\nAverage energy consumption by weekday:")
print(weekday_avg)
