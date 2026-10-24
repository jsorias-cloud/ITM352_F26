# Calculate fare totals and maximum trip distance for fares over $10.
import csv

filename = "taxi_1000.csv"

with open(filename, "r", newline="") as file:
    csv_reader = csv.reader(file)

    header = next(csv_reader)
    fare_index = header.index("Fare")
    distance_index = header.index("Trip Miles")

    total_fare = 0.0
    max_distance = 0.0
    qualifying_rows = 0

    for row in csv_reader:
        fare = float(row[fare_index])
        if fare > 10:
            distance = float(row[distance_index])
            total_fare += fare
            max_distance = max(max_distance, distance)
            qualifying_rows += 1

average_fare = total_fare / qualifying_rows if qualifying_rows else 0.0

print(f"Total Fare (fares over $10): ${total_fare:.2f}")
print(f"Average Fare (fares over $10): ${average_fare:.2f}")
print(f"Max Trip Distance (fares over $10): {max_distance:.2f} miles")