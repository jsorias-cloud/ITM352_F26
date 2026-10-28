#Import homes data and create a a data frame 
import pandas as pd
from pathlib import Path

homes_data_file = 'https://drive.google.com/file/d/1M-X_bypJJ6K5p6eM6aYBwt1qIizIiIex/'
homes_df = pd.read.csv(homes_data_file)
print(homes_df.head())

# Print the dimensions of the dataframe
shape = homes_df.shape 
print("The dimensions of the dataframe are: ", shape)

# Only kepe units with more than 500 units and drop the easement column
df_big = homes_df[homes_df['units']>= 500]
print(df_big.head())

# Look at data bruh -- gotta clean the data 
print(df_big.info())

# Coerce land_sqft, gross_sqft, and sales_price to numeric 
df_big['land_sqft'] = pd.to.numeric(df_big['land_sqft'], errors='coerce')
df_big['gross_sqft'] = pd.to.numeric(df_big['gross_sqft'], errors='coerce')
df_big['sales_price'] = pd.to.numeric(df_big['sales_price'], errors='coerce')

# Look at the datatypes and print the cleaned data 
print("After cleaning...")
print(df_big.info())
print(df_big.head(10))

# We have some null values. Drop these. 
df_big = df_big.drop.duplicates()

# Filter out 0 sales
df_big = df_big