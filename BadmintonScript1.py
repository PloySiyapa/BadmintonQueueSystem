import numpy as np
import scipy.stats as stats

# Step 1: Inputs
num_courts = 3  # Total number of courts
queue_position = int(input("Enter position in queue: "))  # Player's position in the queue
current_game_durations = [7.5, 8.2, 6.8]  # Ongoing game durations (in minutes)

# Historical game durations (in minutes)
historical_durations = [10, 3.7, 4.4, 8.6, 9.2, 6.1, 11, 8.2, 9.5, 7.3, 6.5, 7.2]

# Step 2: Fit a distribution to historical data
mean_duration = np.mean(historical_durations)
std_dev_duration = np.std(historical_durations)

print(f"Mean Game Duration: {mean_duration:.2f} minutes")
print(f"Standard Deviation of Game Duration: {std_dev_duration:.2f} minutes")

# Step 3: Simulate future game durations using the fitted normal distribution
simulated_durations = stats.norm(mean_duration, std_dev_duration).rvs(10000)

# Step 4: Estimate remaining time for current games
remaining_durations = np.maximum(0, simulated_durations[:len(current_game_durations)] - current_game_durations)

# Step 5: Simulate wait time for queued players
# Simulate games for queued players and track when the player reaches a court
total_wait_times = []
for _ in range(10000):  # Monte Carlo simulation
    simulated_queue = np.random.choice(simulated_durations, size=queue_position - 1)
    simulated_queue_time = np.sum(simulated_queue[:num_courts])  # Sum of first N games
    total_wait_times.append(simulated_queue_time)

# Step 6: Output Predicted Wait Time
mean_wait_time = np.mean(total_wait_times)
wait_time_ci = np.percentile(total_wait_times, [2.5, 97.5])  # 95% confidence interval

print("\nPredicted Wait Time:")
print(f"Mean: {mean_wait_time:.2f} minutes")
print(f"95% Confidence Interval: {wait_time_ci[0]:.2f} - {wait_time_ci[1]:.2f} minutes")
