import math

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

# round_up function
# rounds a number upwards
def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to

# Main Routine starts here
how_many = number_checker("How many items? ", "Can't be 0", int)
total = number_checker("Total Costs? ", "More than 0", float)
profit_goal = number_checker
