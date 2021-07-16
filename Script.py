import sys


# This function finds the minimum number in the input file
def min_function(input_file_location, output_folder):
    output_file = open(output_folder + "\\min.txt", "wt")
    input_file = open(input_file_location, "rt")
    input_numbers = []
    for line in input_file:
        line = line.rstrip("\n")
        if line != "":
            input_numbers.append(int(line))
    # output_file.write("The list is: " + str(input_numbers) + "\n")
    minimum_number = input_numbers[0]
    i = 1
    while i < len(input_numbers):
        if input_numbers[i] < minimum_number:
            minimum_number = input_numbers[i]
        i += 1
    output_file.write("The minimum number is: " + str(minimum_number) + "\n")
    input_file.close()
    output_file.close()


# This function finds the maximum number in the input file
def max_function(input_file_location, output_folder):
    output_file = open(output_folder + "\\max.txt", "wt")
    input_file = open(input_file_location, "rt")
    input_numbers = []
    for line in input_file:
        line = line.rstrip("\n")
        if line != "":
            input_numbers.append(int(line))
    # output_file.write("The list is: " + str(input_numbers) + "\n")
    maximum_number = input_numbers[0]
    i = 1
    while i < len(input_numbers):
        if input_numbers[i] > maximum_number:
            maximum_number = input_numbers[i]
        i += 1
    output_file.write("The maximum number is: " + str(maximum_number) + "\n")
    input_file.close()
    output_file.close()


# This function finds the average of the numbers in the input file
def average_function(input_file_location, output_folder):
    output_file = open(output_folder + "\\average.txt", "wt")
    input_file = open(input_file_location, "rt")
    input_numbers = []
    for line in input_file:
        line = line.rstrip("\n")
        if line != "":
            input_numbers.append(int(line))
    # output_file.write("The list is: " + str(input_numbers) + "\n")
    sum = input_numbers[0]
    i = 1
    while i < len(input_numbers):
        sum += input_numbers[i]
        i += 1
    output_file.write("The average is: " + str(round(sum / len(input_numbers), 2)) + "\n")
    input_file.close()
    output_file.close()


# This function sorts the input list
def sort_function(input_file_location, output_folder):
    output_file = open(output_folder + "\\sort.txt", "wt")
    input_file = open(input_file_location, "rt")
    input_numbers = []
    for line in input_file:
        line = line.rstrip("\n")
        if line != "":
            input_numbers.append(int(line))
    # output_file.write("The list is: " + str(input_numbers) + "\n")
    j = len(input_numbers) - 1
    while j != 0:
        i = 0
        while i < j:
            if input_numbers[i + 1] > input_numbers[i]:
                temp = input_numbers[i]
                input_numbers[i] = input_numbers[i + 1]
                input_numbers[i + 1] = temp
            i += 1
        j = j - 1
    output_file.write("The sorted list:" + "\n" + str(input_numbers) + "\n")
    input_file.close()
    output_file.close()


# This function counts the words in the input file
def wordcount_function(input_file_location, output_folder):
    output_file = open(output_folder + "\\wordcount.txt", "wt")
    input_file = open(input_file_location, "rt")
    lines = []
    word_count = {}
    for line in input_file:
        lines.append(line)
    for line in lines:
        line_words = line.split()
        for word in line_words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    # Sorting the word_count dictionary
    sorted_list = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    for i in sorted_list:
        output_file.write(i[0] + (20 - len(i[0])) * " " + str(i[1]) + "\n")
    input_file.close()
    output_file.close()


# Main part of the code starts here

# args_list = sys.argv
args_list = ["temp", "min", "E:\Input\\numbers.txt", "max", "E:\Input\\numbers.txt", "average", "E:\Input\\numbers.txt", "sort", "E:\Input\\numbers.txt", "wordcount", "E:\Input\\words.txt", "E:\Output"]
print("The args are: ")
for i in args_list:
    print(i)






args_list.pop(0)

output_folder = args_list[len(args_list) - 1]
i = 0
while i <= len(args_list) - 3:
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


    i += 2



















