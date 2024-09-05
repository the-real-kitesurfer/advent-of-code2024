import csv
# Reads a CSV file and returns a list of dictionaries
from pprint import pprint
from collections import defaultdict
def read_data():
    data = []
    with open("Olympics_2024.csv", "r", encoding="utf-8-sig") as csvfile:
        spreadsheet = csv.DictReader(csvfile)
        for row in spreadsheet:
            data.append(row)
    return data
data = read_data()

# Calculates total medals per country
def calculate_total_medals():
    total_medals_per_country = {}  # Defines variables for dictionaries
    for row in data:
        country = row["NOC"]
        total_medals = int(row["Total"])   # Convert the total value to integer
        if country not in total_medals_per_country:
            total_medals_per_country[country] = 0
        total_medals_per_country[country] += total_medals  # Sum the medals
    return total_medals_per_country

# Displays total number of medals per country from csv
def total_medals():
    results = calculate_total_medals()
    print("Total Medals Per Country:\n")
    for country, total_medals in results.items():
        print(f'{country}: {total_medals}')

# Displays the total medals won for each competition per country specified in user input
def country_details():
    user_input = ""
    while user_input != "exit":
        user_input = input("Enter the country to view olympic details (or 'exit' to quit):\n")
        if user_input == "exit":
            break
        filtered_data = filter_data(user_input)

        if filtered_data:
            pprint(filtered_data)
        else:
            print("Invalid input or country not in csv, try again (or 'exit' to quit):\n")


# Filters the data based on the country name entered by user

def filter_data(user_input):
    filter_data_per_country = []
    for row in data:
        country = row['NOC'].strip().lower()
        if country == user_input.lower():
            filter_data_per_country.append(row)
    return filter_data_per_country

def add_medals(data): # We need this to add all the "total medals" together or we get duplicates
    medal_totals = defaultdict(int)
    for row in data:
        country = row['NOC'].strip().lower()
        total_medals = int(row["Total"])
        medal_totals[country] += total_medals
    return medal_totals

def top_ten(medal_totals):  # Determine the top ten medal-scoring countries in descending order
    sorted_data = sorted(medal_totals.items(), key=lambda x: x[1], reverse=True)

    top_ten = sorted_data[:10]

    print("Top Ten Countries by Total Medals:\n")
    for country, total in top_ten:
        pprint(f"{country}: {total}")

def medal_percentages(medal_totals):
    total_medals = sum(medal_totals.values())

    print("Percentage of Total Medals Won by Each Country:\n")

    for country, total in medal_totals.items():
        percentage = (total / total_medals) * 100
        print(f"{country}: {percentage:.2f}%")
