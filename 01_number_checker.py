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

# Main routine
get_int = number_checker("How many do you need? ", "Please enter an amount more than 0", int)

get_cost = number_checker("How much does it cost? $", "Please enter an amount more than 0", float)

print("You need {}" .format(get_int))
print("It costs ${:.2f}".format(get_cost))
