import pandas as pd
import numpy as np
import os

# Setting the current working path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("current working path:", os.getcwd())

# Read files
file_path = './jp_lca_dat.csv'
df_food = pd.read_csv(file_path, encoding='latin1')

# Rename columns
df_food = df_food.rename(columns={
    'Product id': 'Product_id',
    'Data S2 Name': 'food_name',
    'Country': 'country_origin',
    'Water Use (L)': 'water_use_l',
    'Scarcity Weighted Water Use (L eq)': 'scarcity_weighted_l',
    'Weight': 'supply_chain_weight'
})

# Keep needed columns
df_food = df_food[['food_name', 'id', 'Product_details', 'country_origin', 'water_use_l', 'scarcity_weighted_l', 'supply_chain_weight']]

# Process the weight field by removing the percent sign and converting to decimals
df_food['supply_chain_weight'] = df_food['supply_chain_weight'].str.replace('%', '')
df_food['supply_chain_weight'] = pd.to_numeric(df_food['supply_chain_weight'], errors='coerce') / 100

# Fill in missing values
df_food = df_food.fillna(0)

# Filter Vegan/Veggie related foods
vegan_veggie_keywords = [
    'Apple', 'Bananas', 'Barley (Beer)', 'Beet Sugar', 'Berries & Grapes', 'Brassicas', 
    'Cane Sugar', 'Cassava', 'Cheese', 'Citrus Fruit', 'Coffee', 'Dark Chocolate', 'Groundnuts', 
    'Maize (Meal)', 'Milk', 'Nuts', 'Oatmeal', 'Olive Oil', 'Onions & Leeks', 'Other Fruit', 
    'Other Pulses', 'Other Vegetables', 'Palm Oil', 'Peas', 'Potatoes', 'Rapeseed Oil', 
    'Rice', 'Root Vegetables', 'Soybean Oil', 'Soymilk', 'Sunflower Oil', 'Tofu', 'Tomatoes', 
    'Wheat & Rye (Bread)', 'Wine'
]
df_filtered = df_food[df_food['food_name'].str.contains('|'.join(vegan_veggie_keywords), case=False, na=False)]

# Screening the data, selecting only the 20 products with the highest water use and selecting the 5 Class II products with the highest environmental impact according to weight values
food_group_burden = df_filtered.groupby('food_name')['water_use_l'].sum().reset_index()

top20_foods = food_group_burden.sort_values(by='water_use_l', ascending=False).head(20)['food_name'] # Top 20 water use 
df_top20_filtered = df_filtered[df_filtered['food_name'].isin(top20_foods)].copy()
df_top20_filtered['rank_within_food'] = df_top20_filtered.groupby('food_name')['supply_chain_weight'].rank(method='first', ascending=False) # Top 5 Weight value
df_top20_final = df_top20_filtered[df_top20_filtered['rank_within_food'] <= 5]

# Remove data with an environmental burden of 0
df_top20_final = df_top20_final[df_top20_final['water_use_l'] > 0.01]

# Final needed columns
df_result = df_top20_final[['food_name', 'id', 'Product_details', 'country_origin', 'water_use_l', 'scarcity_weighted_l', 'supply_chain_weight']]
df_result['supply_chain_weight'] = df_result['supply_chain_weight'].round(3)

# Generate CSV data source files for the final treemap.
# Files are stored in the Data_Output folder
df_result.to_csv('./Data_Output/vegan_veggie_treemap_ready.csv', index=False)


