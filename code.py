import pandas as pd
import numpy as np
from scipy.integrate import simps

# Load the file (can change this file path when needed)
file = "LBG + XG.xlsx"

# Read the Excel file and get all sheet names
sheet_names = pd.ExcelFile(file).sheet_names  # Get all sheet names

# Function to calculate area under curve
def calculate(x, y, start, end, abs_value=False):
    # Select range
    mask = (x >= start) & (x <= end)
    x_selected = x[mask]
    y_selected = y[mask]

    # Option to take absolute values of the force if required
    if abs_value:
        y_selected = np.abs(y_selected)

    # Compute area
    area = simps(y_selected, x=x_selected)
    return area

# Create a list to store results
results = []

# Loop through each sheet
for sheet in sheet_names[:]:
    # Load the current sheet
    df = pd.read_excel(file, sheet_name=sheet)

    # Selecting columns
    force = df['Force']
    time = df['Time']
    distance = df['Distance']

    # Remove the first row if distance == 0 on the first line
    df_filtered = df.iloc[1:]  # Exclude the first row
    force = df_filtered['Force']
    time = df_filtered['Time']
    distance = df_filtered['Distance']

    # Automatically find t1_start, t1_end, t2_start, and t2_end
    t1_start = 0

    # t1_end = time when distance reaches 0 the first time
    t1_end = time[distance == 0].iloc[0]

    # t2_start = last time distance reaches 0
    t2_start = time[distance == 0].iloc[-1]

    # Find the index of t2_start
    t2_start_index = time[time == t2_start].index[0]

    # Select the range after t2_start (skip negative or zero forces)
    time_after_t2_start = time.iloc[t2_start_index + 1:]  # Start after t2_start
    force_after_t2_start = force.iloc[t2_start_index + 1:]

    # Skip negative or zero forces after t2_start until we find a positive force
    for i in range(len(force_after_t2_start)):
        if force_after_t2_start.iloc[i] > 0:  # Find first positive force after t2_start
            force_after_t2_start = force_after_t2_start.iloc[i:]
            time_after_t2_start = time_after_t2_start.iloc[i:]
            break

    # Now, find t2_end: the time when the force reaches zero again or near zero
    t2_end_index = force_after_t2_start[force_after_t2_start <= 0].idxmax()
    t2_end = time[t2_end_index]

    # Calculate cohesiveness
    area_1 = calculate(time, force, t1_start, t1_end)
    area_2 = calculate(time, force, t2_start, t2_end)
    cohesiveness = area_2 / area_1 if area_1 != 0 else 0

    # Springiness calculation
    t1_max_force_index = force[time >= t1_start].idxmax()
    t1_end_spring = time[t1_max_force_index]

    t2_max_force_index = force[time >= t2_start].idxmax()
    t2_end_spring = time[t2_max_force_index]

    t1_time_diff = t1_end_spring - t1_start
    t2_time_diff = t2_end_spring - t2_start
    springiness = (t2_time_diff / t1_time_diff) if t1_time_diff != 0 else 0

    # Collect the results for the current sheet
    results.append({
        'Sheet': sheet,
        'Area_1': area_1,
        'Area_2': area_2,
        'Hardness': max(force[time >= t1_start]),
        'Cohesiveness': cohesiveness,
        'Springiness': springiness
    })

# Create a DataFrame to store all results
results_df = pd.DataFrame(results)

# Display the results
print(results_df)
