![Logo](https://www.rheologylab.com/wp-content/uploads/2022/10/Texture-Analyzer-1.png)

# Project Background
Texture Profile Analysis (TPA) is widely used in food science to quantify textural properties such as hardness, cohesiveness, and springiness. This project automates the calculation of TPA parameters from force-time-distance data using Python (pandas, numpy, scipy).

# Data Structure
The dataset consists of force-time-distance measurements across multiple Excel sheets, each representing different formulations or tests. Below is how the columns are arranged in the excel file:

- Force (N): Applied force on the sample
- Time (s): Time progression of the compression test
- Distance (mm): Compression distance
  
![Data](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

# Executive Summary
## Overview:
This code helps to extract key TPA attributes (Hardness, Cohesiveness, Springiness) from force-time-distance curves that are generated by the texture analyser. The script automates the process for multiple datasets (Excel sheets) to ensure efficiency. This provides accurate and reproducible textural measurements for analysis on a large scale instead of painstakingly copy and paste each TPA measurement from the software directly Below is an example of what the output of the code looks like.

![Final Table](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

## Data preprocessing:
- Read all Excel sheets containing force-time-distance data

- Remove unnecessary negative data after the first compression

- Identify key timestamps for calculations (t1_start, t1_end, t2_start, t2_end)

![TPA_1](https://github.com/user-attachments/assets/df8db66f-9772-48e3-ba4d-3be2acaf2bb0)
![TPA_2](https://github.com/user-attachments/assets/6f3f7f37-d051-401e-8a60-0217082bd6ce)
![TPA_3](https://github.com/user-attachments/assets/8072072c-11a8-4692-ac16-ff3ebd2c2557)

## TPA calculation:
Here is the code for calculating the different TPA metrics:<br/>
![Calculation](https://github.com/user-attachments/assets/4cd39015-f05f-4e86-b657-b13a21a29a80)

#### Hardness
- Maximum force (peak) exerted during first compression 

#### Cohesiveness
- Ratio of energy (area under the curve) between the second and first compression cycles:

$$ Cohesiveness = {Area~1 \over Area~2} $$ 

Where:
- Area_1 = Area under the force-time curve for the first compression.
- Area_2 = Area under the force-time curve for the second compression.

#### Springiness
- Time ratio between the two peak forces to indicate sample recovery:

$$ Springiness = {T2~max - T2~start \over T1~max - T1~start} $$ 

Where:
- T1_max = Time of peak force in first compression.
- T2_max = Time of peak force in second compression

# Recommendations
- Formulations with low cohesiveness may require hydrocolloid adjustments to improve gel strength
- Hardness values should align with consumer preferences, ensuring chewability and bite characteristics match the intended product profile
- Variations in springiness could indicate formulation inconsistencies. Therefore, adjustments should be made to maintain uniformity
