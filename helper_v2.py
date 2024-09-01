import csv
# Reads a CSV file and returns a list of dictionaries
from pprint import pprint
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

def top_ten():
    sorted_data = sorted(data, key=lambda x: int(x["Total"]), reverse=True)

    top_ten = sorted_data[:10]

    print("Top Ten Countries by Total Medals:\n")
    for row in top_ten:
        pprint(f"{row['NOC']}: {row['Total']}")
