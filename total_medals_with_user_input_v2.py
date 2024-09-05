import helper_v2

data = helper_v2.read_data()

print("Welcome to the Group 5 Olympics Spreadsheet Analysis Project!")

# while loop keeps the menu running until the user explicitly chooses to exit.
while True:
    print("Please pick an option from the following menus:")
    print("\n'Total' for total medals won across all competing countries")
    print("'Country' to enable user input to view medals won by a specific country")
    print("'Top' to view the top ten scoring countries in descending order")
    print("'Percentage' to view what percentage of total medals each country won")
    print("'Exit' to close the program.")

    menu_choice = input("\nPlease enter which menu you would like: ")

    if menu_choice.lower() == "total":
        helper_v2.total_medals()
    elif menu_choice.lower() == "country":
        helper_v2.country_details()
    elif menu_choice.lower() == "top":
        medal_totals = helper_v2.add_medals(data)
        helper_v2.top_ten(medal_totals)
    elif menu_choice.lower() == "percentage":
        medal_totals = helper_v2.add_medals(data)
        helper_v2.medal_percentages(medal_totals)
    elif menu_choice.lower() == "exit":
        print("Exiting the program. Thank you!")
        break
    else:
        print("Input not recognised, please try again.")
