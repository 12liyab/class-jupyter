import pandas as pd
import matplotlib.pyplot as plt

# Thi is to Load the Dataset 
df = pd.read_csv('ncr_ride_bookings (2).csv')

# Data Cleaning and Preparation
df['Booking Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df_cleaned = df.dropna(subset=['Booking ID'])

# Setting up the figure for the subplots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 18))
plt.style.use('seaborn-v0_8-whitegrid')
plt.subplots_adjust(hspace=0.5)

# 1. Plotting Booking Patterns (Daily Bookings)
daily_bookings = df_cleaned.groupby(df_cleaned['Booking Datetime'].dt.date).size()
axes[0].plot(daily_bookings.index, daily_bookings.values, color='dodgerblue')
axes[0].set_title('Daily Booking Trends', fontsize=16)
axes[0].set_xlabel('Date', fontsize=12)
axes[0].set_ylabel('Number of Bookings', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(True)
axes[0].set_ylim(bottom=0)

# 2. Plotting Revenue Streams (Total Revenue by Vehicle Type)
revenue_by_vehicle = df_cleaned.groupby('Vehicle Type')['Booking Value'].sum().sort_values(ascending=False)
axes[1].bar(revenue_by_vehicle.index, revenue_by_vehicle.values, color='mediumseagreen')
axes[1].set_title('Total Revenue by Vehicle Type', fontsize=16)
axes[1].set_xlabel('Vehicle Type', fontsize=12)
axes[1].set_ylabel('Total Revenue ($)', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(axis='y', linestyle='--')
axes[1].set_ylim(bottom=0)

# 3. Plotting Cancellation Behaviors (Booking Status Counts)
booking_status_counts = df_cleaned['Booking Status'].value_counts()
axes[2].bar(booking_status_counts.index, booking_status_counts.values, color='firebrick')
axes[2].set_title('Booking Status Counts', fontsize=16)
axes[2].set_xlabel('Booking Status', fontsize=12)
axes[2].set_ylabel('Number of Bookings', fontsize=12)
axes[2].tick_params(axis='x', rotation=45)
axes[2].grid(axis='y', linestyle='--')
axes[2].set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('uber_analytics_dashboard.png')
