''' Certificate in Data Analytics for Aviation
    Assignment Project
    Roisin Hickey '''

import pandas as pd
import numpy as np
import collections
import matplotlib.pyplot as plt
import requests

# Import data as csv file into pandas dataframe
crash_data = pd.read_csv("Airplane_Crashes_and_Fatalities_Since_1908_20190820105639.csv")

# Quick vew of data in file
print("Sample of csv file:")
print(crash_data.head())
print(crash_data.shape)
print("\n")

# Drop duplicate rows
crash_data = crash_data.drop_duplicates()

# Count missing values in each column to see quality of the data file
print("Missing values per column after duplicate rows are dropped:")
missing_values_count = crash_data.isnull().sum()
print(missing_values_count[:])
print("\n")

# Drop columns with a lot of missing data and that are not needed
crash_data = crash_data.drop(columns = ["Time", "Flight #", "Registration", "cn/ln"])
print("Dataframe shape after dropping 4 columns:")
print(crash_data.shape)
print("\n")

# Count missing values in each column after deleting 4 columns
print("Missing values per column after dropping 4 columns:")
missing_values_count = crash_data.isnull().sum()
print(missing_values_count[:])
print("\n")

# Delete rows with missing integer vales
crash_data = crash_data.dropna(subset = ["Aboard", "Aboard Passangers", "Aboard Crew", "Fatalities", "Fatalities Passangers", "Fatalities Crew"])
print("Dataframe shape after dropping rows with missing integer vales:")
print(crash_data.shape)
print("\n")

# Custom function to fill missing values
def fill_values(column, value):
    crash_data[column] = crash_data[column].fillna(value)

# Fill missing values with indexing to access string columns
string_columns = [2, 3, 4, 5, 12]

x = 1
# Loop through columns to fill missing values
for column in crash_data:
    if x in string_columns:
        fill_values(column, "Unknown")
    else: fill_values(column, "No Summary Report")
    x = x + 1

# Check if there are still missing values
print("Are there any missing values?")
print(crash_data.isnull().values.any())
print("\n")

# Group by operator and sort in descending order
crash_by_operator = crash_data.groupby(["Operator"]).sum()
crash_by_operator = crash_by_operator.sort_values(by=["Fatalities"], ascending=False)
crash_by_operator.iloc[0:10, 4].plot.barh()
plt.title("Number of Fatalities Per Operator")
plt.xlabel("Number of Fatalities")
plt.ylabel("Operator")
plt.yticks(fontsize=8, rotation=45)
plt.show()

# Scatter plot to show total number of fatalities v number of fatalities per crash
operator_occurrences = collections.Counter(crash_data["Operator"])
total_fatalities_per_operator = crash_by_operator.iloc[0:10, 4]
total_crashes_per_operator = list(operator_occurrences.values())
total_crashes_per_operator.sort(reverse=True)
total_crashes_per_operator = total_crashes_per_operator[0:10]
fatalities_per_crash = []
for operator in total_fatalities_per_operator.keys():
    fatalities_per_crash.append(total_fatalities_per_operator.get(operator)/operator_occurrences.get(operator))
sorted_fatalities_per_crash = fatalities_per_crash[0:10]
plt.scatter(total_fatalities_per_operator, fatalities_per_crash)
for i, label in enumerate(list(crash_by_operator.index)[0:10]):
    plt.annotate(label, (total_fatalities_per_operator[i], fatalities_per_crash[i]))
plt.grid(True)
plt.title("Total Number of Fatalities Vs Number of Fatalities per Crash")
plt.xlabel("Total Number of Fatalities")
plt.ylabel("Number of Fatalities per Crash")
plt.show()

# Create list of the year of each crash
crash_by_year = pd.DatetimeIndex(crash_data["Date"]).year.tolist()
year_occurrences = collections.Counter(crash_by_year)
keys = year_occurrences.keys()
values = year_occurrences.values()
plt.bar(keys, values)
plt.title("Number of Crashes Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Crashes")
plt.show()

# Using slicing to show proportion of people aboard that were fatalities for operators with the most amount of crashes
sample = slice(0, 10)
crash_by_operator[sample].plot(kind="bar")
plt.title("People Aboard Analysis")
plt.xlabel("Operator")
plt.ylabel("People")
plt.xticks(rotation=45)
plt.show()

# Merging dataframes
df1 = crash_by_operator.iloc[:3, ]
df2 = crash_by_operator.iloc[2171:, ]
merged_df = df1.append(df2)
print(merged_df)
merged_df.plot()
plt.title("Top and Bottom Operators People Aboard Analysis")
plt.xlabel("Operator")
plt.ylabel("People")
plt.show()

# Could also get data from an API using requests
request=requests.get("http://api.open-notify.org/astros.json")
print(request.status_code)
print(request.text)

# NumPy example
numbers1 = np.array([[2,5,8], [8,9,10], [22,20,18]])
numbers2 = np.array([[18,20,22], [10,9,8], [8,5,2]])
result = np.add(numbers1, numbers2)
print(result)