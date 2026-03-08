import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Daten einlesen 
df = pd.read_csv('TestDataRotor.csv')

# 1. Label all data points where velocity >= 120 kmh
df['high_speed'] = df['velocity'] > 120

# 2. Plot an example of a consecutive time series
high_speed_trips = df[df['high_speed']]['tripId'].unique() # take first entry with over 120 kmh
example_trip = high_speed_trips[0]
example_data = df[df['tripId'] == example_trip].sort_values('timeUnix') # sort according to time

# --Plot erstellen--
fig, ax1 = plt.subplots(figsize=(12,6))

# x-Achse
time_series = pd.to_datetime(example_data['timeUnix'], unit='ms')

ax1.plot(time_series, example_data['velocity'], 'b-', label='Velocity (km/h)')
ax1.set_xlabel('Time')
ax1.set_ylabel('Velocity (km/h)')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(time_series, example_data['temperatureRotorBack'], 'r-', label='Temp Rotor Back (°C)')
ax2.set_ylabel('Temperature Rotor Back (°C)', color='r')
ax2.tick_params('y', colors='r')

plt.title(f'Time Series for Trip: {example_trip}')
plt.show()


# 3. Calculate the average temperatureRotorBack
avg_temp_high_speed = df[df['velocity'] >= 120]['temperatureRotorBack'].mean()
avg_temp_low_speed = df[df['velocity'] < 120]['temperatureRotorBack'].mean()

print(f"Average Temperature Rotor Back High Speed in °C: {avg_temp_high_speed:.2f}")
print(f"Avergae Temperature Rotor Back Low Speed in °C: {avg_temp_low_speed:.2f}")

# 4. Calculate correlations
correlation_back = df['velocity'].corr(df['temperatureRotorBack'])
correlation_front = df['velocity'].corr(df['temperatureRotorFront'])

print(f"Correlation Velocity & Temperature Rotor Back: {correlation_back:.2f}")
print(f"Correlation Velocity & Temperature Rotor Front: {correlation_front:.2f}")

# 5. Plot Histograms of TemperatureRotorBack
plt.figure(figsize=(10, 6))

min_val = df['temperatureRotorBack'].min()
max_val = df['temperatureRotorBack'].max()

bins = np.arange(int(min_val), int(max_val) + 5, 5) # Bin Size 5, daher max +5 und Schrittweite 5

plt.hist(df[df['velocity'] >= 120]['temperatureRotorBack'].dropna(), bins=bins, alpha=0.5, label='>= 120 kmh', color='red')
plt.hist(df[df['velocity'] < 120]['temperatureRotorBack'].dropna(), bins=bins, alpha=0.5, label='>= 120 kmh', color='blue')

plt.xlabel('Temperature Rotor Back in °C')
plt.ylabel('Frequency')
plt.title('Histogram of Temperature Rotor Back')
plt.legend()
plt.show()

# 6. Trip Statistics
# Trip mit längster Dauer
trip_duration = df.groupby('tripId')['timeUnix'].agg(['min', 'max'])
trip_duration['duration_ms'] = trip_duration['max'] - trip_duration['min']
longest_trip = trip_duration['duration_ms'].idxmax()
longest_duration = trip_duration['duration_ms'].max()

# Trip mit höchster Durchschnittsgeschwindigkeit
highest_avg_vel_trip = df.groupby('tripId')['velocity'].mean().idxmax()
highest_avg_velocity = df.groupby('tripId')['velocity'].mean().max()

print(f"Longest Trip: {longest_trip} with duration: {longest_duration} ms ({longest_duration/1000/60:.2f} min)")
print(f"Highest Average Velocity Trip: {highest_avg_vel_trip} with {highest_avg_velocity:.2f}: kmh")