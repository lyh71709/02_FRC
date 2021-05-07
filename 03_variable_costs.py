import pandas

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

# yes/no checker goes here
# ensures that the input is either yes or no

# not_blank function here
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
def currency(x):
    return "${:.2f}".format(x)


# Main Routine

# Set up dictionaries and lists

item_list = []
quantity_list = []
price_list = []
a_list = [1]
pz_list = [5]

variable_dict = {
    "Item": item_list,
    "Quantity": quantity_list,
    "A": a_list,
    "Price": price_list,
    "Z": pz_list,
}

# Get user data
product_name = not_blank("Product name: ")

# loop to get component, quantity and price
item_name = ""
while item_name.lower() != "xxx":

    print()
    # get name, quantity and item
    item_name = not_blank("Item name: ")
    if item_name.lower() == "xxx":
        break

    quantity = number_checker("Quantity: ", "The amount must be a whole number more than zero", int)

    price = number_checker("How much for a single item? $", "The price must be a number (more than 0)", float)

    # add item, quantity and price to lists
    print()
    item_list.append(item_name)
    quantity_list.append(quantity)
    price_list.append(price)

    variable_frame = pandas.DataFrame(variable_dict)
    variable_frame = variable_frame.set_index('Item')

    # Calculate cost of each component
    variable_frame['Cost'] = variable_frame['Quantity'] * variable_frame['Price']

    # Find sub total
    variable_sub = variable_frame['Cost'].sum()

    # Currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        variable_frame[item] = variable_frame[item].apply(currency)

    # Printing Area
    print(variable_frame)
    print()
    print("Variable Costs: {:.2f}".format(variable_sub))
