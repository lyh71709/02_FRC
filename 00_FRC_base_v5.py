# Implement recommended price and round up

import pandas
import math
import os

# yes_no_checker goes here
# ensures that a field must be answered with either yes or no
def yes_no_checker(question):
    to_check = ["yes", "no"]

    valid = False
    while not valid:
        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item
            
        print("Please enter either yes or no \n")

# Number checker function goes here
# Checks that it is not 0
def number_checker(question, error, num_type):
    valid = False
    while not valid:

        try:
            response = num_type(input(question))
        
            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)

# not_blank function here
# Ensures that any input must not be left blank, the field must not be left empty
def not_blank(question, error):
    valid = False

    while not valid:
        response = input(question)

        if response != "":
            return response
        else:
            print(error)
            print()

# currency function goes here
# Puts something into a currency format with two decimal places
def currency(x):
    return "${:.2f}".format(x)

# get_expenses function goes here
# Gets expenses and then returns them as a list which has the data frame and sub total
def get_expenses(var_fixed):
    
    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity and price
    item_name = ""
    while item_name.lower() != "xxx":

        print()
        # get name, quantity and item
        item_name = not_blank("Item name: ", "Name cannot be blank")
        if item_name.lower() == "xxx":
            print("No Costs were given")
            break

        if var_fixed == "variable":
            quantity = number_checker("Quantity: ", "The amount must be a whole number", int)
        else:
            quantity = 1

        price = number_checker("How much for a single item $", "The price must be a number more than 0", float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Find sub total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]

# expense_print function goes here
# Displays the expenses in a legible way
def expense_print(heading, frame, subtotal):
    print()
    print("{} Costs".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))

    return ""

# profit_goal goes here
# Figures out the needed profit (percentage or amount)
def profit_goal(total_costs):

    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # ask for profit goal
        response = input("What is your profit goal (e.g. $500 or 50%)? ")

        # check if first character is $
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (Everything before the %)
            amount = response[:-1]
        else:
            # Set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no_checker("Do you mean ${:.2f}. ie {:.2f} dollars?, y / n? ".format(amount, amount))

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no_checker("Do you mean {}%?, y / n? ".format(amount))

            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal

# round_up function
# rounds a number upwards
def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


# Main Routine

clear = lambda:os.system('cls')
clear()

# Get user data
product_name = not_blank("Product name: ", "Product Name cannot be blank")

how_many = number_checker("How many items will you be producing? ", "The number of items must be a whole and more than zero", int)

print()
print("Please enter your variable costs below...")

# Variable Costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

print()
have_fixed = yes_no_checker("Do you have fixed costs (y/n)? ")

if have_fixed == "yes":

    # Fixed Costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]

else:
    fixed_sub = 0

# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculates total sales needed to reach goal
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = number_checker("Round to nearest...? $", "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print("\nSelling Price (unrounded): ${:.2f}".format(selling_price))

recommended_price = round_up(selling_price, round_to)

# Write data to file
# create file to hold data (add .txt extension)
file_name = "{}.txt".format(product_name)
text_file = open(file_name, "w+")

# Change dataframe to string (so it can be written to a text file)
variable_txt = pandas.DataFrame.to_string(variable_frame)
fixed_txt = pandas.DataFrame.to_string(fixed_frame)

profit_target_txt = ("${}".format(profit_target))
selling_price_txt = ("${}".format(selling_price))
recommended_price_txt = ("${}".format(recommended_price))

# to_write is put in the middle because the variables aren't defined at the beginning
to_write = [product_name, variable_txt, fixed_txt, profit_target_txt, selling_price_txt, recommended_price_txt]

# heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()

# Printing Area
print()
print("Fundraising - {}".format(product_name))
print()

expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

print()
print("Total Costs: ${:.2f}".format(all_costs))
print()

print()
print("Profit and Sales Targets")
print("Profit Target: ${:.2f}".format(profit_target))
print("Total Sales: ${:.2f}".format(all_costs + profit_target))

print()
print("Recommended Selling Price: ${:.2f}".format(selling_price))
