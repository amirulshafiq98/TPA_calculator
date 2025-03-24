import pandas as pd
import numpy as np
from scipy.integrate import simps

# Load the file
file = "LBG + XG.xlsx"
sheet_names = pd.ExcelFile(file).sheet_names  # Get all sheet names

# Function to calculate area under curve
def calculate_area(x, y, start, end, abs_value=False):
    mask = (x >= start) & (x <= end)
    x_selected = x[mask]
    y_selected = y[mask]
    if abs_value:
        y_selected = np.abs(y_selected)
    return simps(y_selected, x=x_selected) if not x_selected.empty else 0

# Step 1: Data Preprocessing
def preprocess_data(sheet_name):
    df = pd.read_excel(file, sheet_name=sheet_name)
    df_filtered = df.iloc[1:].dropna()  # Remove first row and NaN values
    return df_filtered

# Step 2: Identify Key Timestamps
def identify_timestamps(time, distance):
    t1_start = 0
    t1_end = time[distance == 0].iloc[0]
    t2_start = time[distance == 0].iloc[-1]
    t2_start_index = time[time == t2_start].index[0]
    return t1_start, t1_end, t2_start, t2_start_index

# Step 3: Remove Negative Data after First Compression
def filter_positive_force(time, force, t2_start_index):
    time_after_t2 = time.iloc[t2_start_index + 1:].dropna()
    force_after_t2 = force.iloc[t2_start_index + 1:].dropna()
    for i in range(len(force_after_t2)):
        if force_after_t2.iloc[i] > 0:
            return time_after_t2.iloc[i:], force_after_t2.iloc[i:]
    return time_after_t2, force_after_t2

# Step 4: Identify t2_end
def get_t2_end(time_after_t2, force_after_t2):
    t2_end_index = force_after_t2[force_after_t2 <= 0].first_valid_index()
    return time_after_t2[t2_end_index] if t2_end_index is not None else time_after_t2.iloc[-1]

# Step 5: TPA Calculations
def calculate_tpa(time, force, t1_start, t1_end, t2_start, t2_end):
    area_1 = calculate_area(time, force, t1_start, t1_end)
    area_2 = calculate_area(time, force, t2_start, t2_end)
    cohesiveness = area_2 / area_1 if area_1 != 0 else 0
    
    t1_max_force_index = force[time >= t1_start].idxmax()
    t1_end_spring = time[t1_max_force_index] if t1_max_force_index is not None else t1_start
    
    t2_max_force_index = force[time >= t2_start].idxmax()
    t2_end_spring = time[t2_max_force_index] if t2_max_force_index is not None else t2_start
    
    t1_time_diff = t1_end_spring - t1_start
    t2_time_diff = t2_end_spring - t2_start
    springiness = (t2_time_diff / t1_time_diff) if t1_time_diff != 0 else 0
    
    return area_1, area_2, cohesiveness, springiness

# Step 6: Process Each Sheet and Store Results
results = []
for sheet in sheet_names:
    df = preprocess_data(sheet)
    time, force, distance = df['Time'], df['Force'], df['Distance']
    t1_start, t1_end, t2_start, t2_start_index = identify_timestamps(time, distance)
    time_after_t2, force_after_t2 = filter_positive_force(time, force, t2_start_index)
    t2_end = get_t2_end(time_after_t2, force_after_t2)
    area_1, area_2, cohesiveness, springiness = calculate_tpa(time, force, t1_start, t1_end, t2_start, t2_end)
    
    results.append({
        'Sheet': sheet,
        'Area_1': area_1,
        'Area_2': area_2,
        'Hardness': max(force[time >= t1_start], default=0),
        'Cohesiveness': cohesiveness,
        'Springiness': springiness
    })

# Step 7: Store Results in DataFrame
results_df = pd.DataFrame(results)
print(results_df)
