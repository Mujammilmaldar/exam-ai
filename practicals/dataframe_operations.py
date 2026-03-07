import pandas as pd

# Read CSV file into DataFrame
df = pd.read_csv("cars.csv")

print("Original Data")
print(df)

# 1 Display records where Sell Price > 4000
print("\nCars with Sell Price greater than 4000:")
result = df[df['Sell_Price'] > 4000]
print(result)

# 2 Sort the car data in ascending order
print("\nSorted Data (Ascending Order by Sell Price):")
sorted_data = df.sort_values(by='Buy_Price', ascending=False)
print(sorted_data)

# 3 Group the data according to Make of car
print("\nGrouped Data by Make:")
grouped = df.groupby('Make')

for name, group in grouped:
    print("\nMake:", name)
    print(group)
