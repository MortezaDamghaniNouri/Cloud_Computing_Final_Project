import sys


def min_function(input_file_location, output_folder):
    output_file = open(output_folder + "/min.txt", "wt")
    input_file = open(input_file_location, "rt")
    input_numbers = []
    for line in input_file:
        input_numbers.append(int(line))
    output_file.write("The list is: " + str(input_numbers) + "\n")
    minimum_number = input_numbers[0]
    i = 1
    while i < len(input_numbers):
        if input_numbers[i] < minimum_number:
            minimum_number = input_numbers[i]
        i += 1
    output_file.write("The minimum number is: " + str(minimum_number) + "\n")





# Main part of the code starts here
args_list = sys.argv
args_list.pop(0)

output_folder = args_list[len(args_list) - 1]
i = 0
while i < len(args_list) - 3:
    command = args_list[i]
    input_file_location = args_list[i + 1]
    if command == "min":
        min_function(input_file_location, output_folder)

    if command == "max":
        max_function(input_file_location, output_folder)

    if command == "average":
        average_function(input_file_location, output_folder)

    if command == "sort":
        sort_function(input_file_location, output_folder)

    if command == "wordcount":
        wordcount_function(input_file_location, output_folder)















    i += 1



















