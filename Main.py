import subprocess










# This function extracts commands and directory addresses from user input
def input_separator(user_input):
    user_input = user_input.rstrip("}")
    user_input = user_input.lstrip("{")
    commands = user_input.split(">, ")
    output_commands = []
    i = 0
    while i < len(commands) - 1:
        command = commands[i]
        command = command.lstrip("<")
        single_command_list = command.split(", ")
        for j in single_command_list:
            output_commands.append(j)
        i += 1

    output_file_location = commands[len(commands) - 1]
    output_file_location = output_file_location.lstrip("<")
    output_file_location = output_file_location.rstrip(">")
    output_commands.append(output_file_location)
    return output_commands


# This function terminates three generated dockers
def dockers_terminator():
    subprocess.run("docker stop cloud_computing_container1")
    subprocess.run("docker rm cloud_computing_container1")
    subprocess.run("docker stop cloud_computing_container2")
    subprocess.run("docker rm cloud_computing_container2")
    subprocess.run("docker stop cloud_computing_container3")
    subprocess.run("docker rm cloud_computing_container3")
    print("All dockers terminated")






# Main part of the code starts here
while True:
    user_input = input("Input: ")
    if user_input == "exit":
        dockers_terminator()

    else:
        commands_list = input_seperator(user_input)
















