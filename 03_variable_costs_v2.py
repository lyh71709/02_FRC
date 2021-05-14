import pandas

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
def not_blank(question):
    valid = False
    error = "Sorry - this can't be blank, please enter your name"

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

    expense_frame = 0
    sub_total = 0
    
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
        item_name = not_blank("Item name: ")
        if item_name.lower() == "xxx":
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
        expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame["Price"]

        # Find sub total
        sub_total = expense_frame['Cost'].sum()

        # Currency Formatting (uses currency function)
        add_dollars = ['Price', 'Cost']
        for item in add_dollars:
            expense_frame[item] = expense_frame[item].apply(currency)

    return[expense_frame, sub_total]

def expense_print(heading, frame, subtotal):
    print()
    print("{} Costs".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))

    return ""


# Main Routine


# Get user data
product_name = not_blank("Product name: ")

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

# Printing Area
print()
print("Fundraising - {}".format(product_name))
print()
if variable_frame == 0:
    print("No Variable Costs Given")
else:
    expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes" and fixed_frame != 0:
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)
else:
    print("No Fixed Costs Given")

print()
print("Total Costs: ${:.2f}".format(variable_sub + fixed_sub))
