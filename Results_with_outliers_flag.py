import pandas as pd
import os

# Setting the current working path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("current working path:", os.getcwd())

# Read files
df = pd.read_csv("./Results_21Mar2022.csv")

# Keep needed columns
columns_needed = [
    'mc_run_id', 'grouping', 'mean_watscar', 'mean_watuse', 'sd_watscar', 'sd_watuse',
    'n_participants', 'sex', 'diet_group', 'age_group'
]
df = df[columns_needed]
df = df[df['diet_group'].isin(['vegan', 'veggie'])].copy()

# Generate diet_sex_group
df['diet_sex_group'] = df['diet_group'] + '_' + df['sex']

# Defining Correspondence
diet_sex_to_outlier_code = {
    'vegan_female': 1,
    'vegan_male': 2,
    'veggie_female': 3,
    'veggie_male': 4
}
df['outliers'] = 0 # initialize outliers=0 (none are outliers by default)

# Grouping each grouping
for group_name, group_data in df.groupby('grouping'):
    if group_data.empty:
        continue

    # Calculate quartiles
    q1 = group_data['mean_watuse'].quantile(0.25)
    q3 = group_data['mean_watuse'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Find the outliers
    outlier_indices = group_data[
        (group_data['mean_watuse'] < lower_bound) | (group_data['mean_watuse'] > upper_bound)
    ].index

    # Assign corresponding codes to outliers
    for idx in outlier_indices:
        diet_sex = df.at[idx, 'diet_sex_group']
        code = diet_sex_to_outlier_code.get(diet_sex, 0)
        df.at[idx, 'outliers'] = code

# Generate a new table
# Stored in Data_Output
df.to_csv("./Data_Output/Results_with_outliers_flag.csv", index=False)

