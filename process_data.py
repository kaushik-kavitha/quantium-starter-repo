import pandas as pd
import os

# Define the data directory
data_dir = './data'
output_file = 'formatted_pink_morsel_data.csv'

# List to store processed dataframes
processed_dataframes = []

# Loop through the files in the data folder
for file_name in os.listdir(data_dir):
    if file_name.endswith('.csv'):
        # 1. Load the data
        file_path = os.path.join(data_dir, file_name)
        df = pd.read_csv(file_path)

        # 2. Filter for Pink Morsels only
        # We use .str.lower() to ensure we catch "pink morsel" regardless of capitalization
        df = df[df['product'].str.lower() == 'pink morsel']

        # 3. Clean the price field (remove '$' if present) and convert to float
        df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
        
        # 4. Create the 'sales' field (price * quantity)
        df['sales'] = df['price'] * df['quantity']

        # 5. Keep only the required columns: sales, date, region
        df = df[['sales', 'date', 'region']]

        # Add to our list
        processed_dataframes.append(df)

# Combine all dataframes into one
final_df = pd.concat(processed_dataframes, ignore_index=True)

# Save the final output
final_df.to_csv(output_file, index=False)

print(f"Data processing complete! Created {output_file}")
