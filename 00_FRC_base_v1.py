# import libraries

# Functions go here

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

# Main routine
    