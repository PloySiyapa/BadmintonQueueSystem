# Author: Ethan Thongmanivong
# date: January 29 2025
# Purpose: Prove of concept waiting time estimation 
import numpy as np
import pandas as pd
import scipy.stats as stats
import heapq  # For managing court availability times

# Load historical data from the Excel file
file_path = "C:/Users/ethan/Downloads/schoolDownloads/BadmintonProject/BadmintonDataSeconds.xlsx"  # Replace with actual path
data = pd.read_excel(file_path)

# Filter for games played to 21 points
filtered_data = data[data['points'] == 21]

# Extract game durations in minutes
historical_durations = filtered_data['Time(s)'] / 60  # Convert seconds to minutes

# Fit a distribution to historical data
mean_duration = np.mean(historical_durations)
std_dev_duration = np.std(historical_durations)

print(f"Mean Game Duration: {mean_duration:.2f} minutes")
print(f"Standard Deviation: {std_dev_duration:.2f} minutes")

# Simulate game durations using a normal distribution
simulated_durations = stats.norm(mean_duration, std_dev_duration).rvs(10000)

# Constants
num_courts = 3
players_per_match = 4
players_per_round = num_courts * players_per_match  # 12 players on court at once

# enter the loop for the program
while True:
    user_input = input("\nEnter your queue position (or 'Quit' to exit): ").strip()
    if user_input.upper() == 'Quit':
        print("Exiting the program. Goodbye!")
        break

    try:
        queue_position = int(user_input)
        if queue_position < 1:
            print("Queue position must be a positive integer.")
            continue

        # Monte Carlo simulation for estimating wait times
        total_wait_times = []
        for _ in range(10000):  # Run 10,000 simulations
            court_heap = [0] * num_courts  # Track when each court becomes available
            wait_time = 0  # Player's total wait time
            
            for i in range(1, queue_position + 1, players_per_match):  # Process each group of 4
                # The next available court is the one that opens the soonest
                soonest_court = heapq.heappop(court_heap)
                
                # Assign a new random duration for this game
                game_duration = np.random.choice(simulated_durations)
                new_court_time = soonest_court + game_duration

                # Update court availability
                heapq.heappush(court_heap, new_court_time)

                # If this is the player’s match, record wait time
                if i <= queue_position < i + players_per_match:
                    wait_time = new_court_time
            
            total_wait_times.append(wait_time)

        # Output estimated wait time
        mean_wait_time = np.mean(total_wait_times)
        wait_time_ci = np.percentile(total_wait_times, [2.5, 97.5])  # 95% confidence interval

        print(f"\nPredicted Wait Time for Queue Position {queue_position}:")
        print(f"Mean: {mean_wait_time:.2f} minutes")
        print(f"95% Confidence Interval: {wait_time_ci[0]:.2f} - {wait_time_ci[1]:.2f} minutes")

    except ValueError:
        print("Invalid input. Please enter a positive integer for queue position or 'E' to exit.")
