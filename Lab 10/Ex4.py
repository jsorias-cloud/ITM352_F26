# Read a json file of taxi trip and create a dataframe and simple stats 
import pandas as pd 

# Read the JSOW files into a dataframe 
results_df = pd.read_json('Taxi_Trips.json')

# Display the first five rows of the dataframe 
print(results_df.head(6))

# Display basic statistics about the DataFrame 
print(results_df.describe())

median = results_df["fare"].median()
print("The median fare value is:", median)

