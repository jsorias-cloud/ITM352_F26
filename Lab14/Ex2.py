# Grab 1 month interest rate data from the US Treasury website

from io import StringIO

import pandas as pd
import requests

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"
print("Retrieving", url)

response = requests.get(url, timeout=30)
response.raise_for_status()

tables = pd.read_html(StringIO(response.text))
df = tables[0]
print("Columns:", df.columns.tolist())
print(df.to_string(index=False))

int_rate_table = df[0]

# Print the table of 1 month interest rates 
print("1 Month Interest Rates:")

for index, row in int_rate_table.iterrows():
    print(f"")