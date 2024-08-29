from pprint import pprint
import helper

data = helper.read_data()

# Displays total number of medals per country from csv
results = helper.calculate_total_medals()
print("Total Medals Per Country:\n")
for country, total_medals in results.items():
    print(f'{country}: {total_medals}')


user_input = ""
while user_input != "exit":
    user_input = input("Enter the country to view olympic details (or 'exit' to quit):\n")
    if user_input == "exit":
        break
    filtered_data = helper.filter_data(user_input)

    pprint(filtered_data)
