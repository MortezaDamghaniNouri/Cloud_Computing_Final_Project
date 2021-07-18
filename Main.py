import subprocess
import threading
import time

# This flag will set to True to stop the container selector thread
stop_flag = False


# This function separates the different parts of the input string
def input_separator(user_input):
    user_input = user_input.rstrip("}")
    user_input = user_input.lstrip("{")
    commands = user_input.split(">, ")
    number_of_commands = len(commands) - 1
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
    return output_commands, number_of_commands


# This function terminates three generated dockers
def dockers_terminator():
    print("Terminating dockers...")
    subprocess.run("docker stop container1")
    subprocess.run("docker rm container1")
    subprocess.run("docker stop container2")
    subprocess.run("docker rm container2")
    subprocess.run("docker stop container3")
    subprocess.run("docker rm container3")
    print("All dockers terminated")


# This function changes the status of containers in the containers list
def status_list_changer(containers_list, container_index, number_of_commands, user_id, output_folder):
    # print("The sleep time is: " + str(number_of_commands * 1.5))
    time.sleep(number_of_commands * 1.5)
    if container_index == 0:
        subprocess.run("docker cp container1:/home/cloud_computing/Output/user" + str(user_id) + "_output " + output_folder)
    if container_index == 1:
        subprocess.run("docker cp container2:/home/cloud_computing/Output/user" + str(user_id) + "_output " + output_folder)
    if container_index == 2:
        subprocess.run("docker cp container3:/home/cloud_computing/Output/user" + str(user_id) + "_output " + output_folder)
    containers_list[container_index] = "idle"
    print("User" + str(user_id) + " tasks finished")


# This function checks if the input task exists among user input commands
def does_task_exist(input_task_name, commands_list):
    i = 0
    while i < len(commands_list) - 1:
        if commands_list[i] == input_task_name:
            return True
        i += 2
    return False


# This function assigns a task to the input task
def task_assigner(container_name, task, containers_list):
    user_id = task[1]
    commands_list = task[0]
    # Program command input counter
    counter = 1
    # Making input directory in the container
    subprocess.run("docker exec " + container_name + " mkdir -p /home/cloud_computing/Input/user" + str(user_id) + "_input")
    # Making the output directory in the container
    subprocess.run("docker exec " + container_name + " mkdir -p /home/cloud_computing/Output/user" + str(user_id) + "_output")
    if does_task_exist("min", commands_list):
        subprocess.run("docker exec " + container_name + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/min.txt")
    if does_task_exist("max", commands_list):
        subprocess.run("docker exec " + container_name + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/max.txt")
    if does_task_exist("average", commands_list):
        subprocess.run("docker exec " + container_name + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/average.txt")
    if does_task_exist("sort", commands_list):
        subprocess.run("docker exec " + container_name + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/sort.txt")
    if does_task_exist("wordcount", commands_list):
        subprocess.run("docker exec " + container_name + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/wordcount.txt")

    commands_string = "docker exec container1 python /home/cloud_computing/Script.py "
    i = 0
    while i < len(commands_list):
        if i % 2 == 1:
            if commands_list[i - 1] != "program":
                subprocess.run("docker cp " + commands_list[i] + " " + container_name + ":/home/cloud_computing/Input/user" + str(user_id) + "_input/input" + str((i + 1) / 2) + ".txt")
                commands_string += "/home/cloud_computing/Input/user" + str(user_id) + "_input/input" + str((i + 1) / 2) + ".txt" + " "
        else:
            if i == len(commands_list) - 1:
                commands_string += "/home/cloud_computing/Output/user" + str(user_id) + "_output"
            else:
                if commands_list[i] != "program":
                    commands_string += commands_list[i] + " "
                else:
                    input_file_folder = commands_list[i + 1]
                    subprocess.run("docker exec " + container_name + " touch " + "/home/cloud_computing/Input/user" + str(user_id) + "_input/input_program.py")
                    subprocess.run("docker cp " + input_file_folder + " " + container_name + ":/home/cloud_computing/Input/user" + str(user_id) + "_input/input_program.py")
                    # Executing the program execution tasks in container
                    output = subprocess.run("docker exec " + container_name + " python /home/cloud_computing/Input/user" + str(user_id) + "_input/input_program.py", capture_output=True)
                    program_output_file = open(commands_list[len(commands_list) - 1] + "\python_program_output_" + "user" + str(user_id) + " program" + str(counter) + ".txt", "wt")
                    counter += 1
                    program_output_file.write(output.stdout.decode())
                    program_output_file.write(output.stderr.decode())
                    program_output_file.close()
        i += 1

    if container_name == "container1":
        threading.Thread(target=status_list_changer, args=(containers_list, 0, task[2], user_id, commands_list[len(commands_list) - 1])).start()
    elif container_name == "container2":
        threading.Thread(target=status_list_changer, args=(containers_list, 1, task[2], user_id, commands_list[len(commands_list) - 1])).start()
    elif container_name == "container3":
        threading.Thread(target=status_list_changer, args=(containers_list, 2, task[2], user_id, commands_list[len(commands_list) - 1])).start()
    subprocess.run(commands_string.replace("container1", container_name))


# This function selects an idle container and it is the dispatcher
def container_selector(containers_list, tasks_list):
    while not stop_flag:
        if containers_list[0] == "idle" and len(tasks_list) != 0:
            containers_list[0] = "busy"
            print("User" + str(tasks_list[0][1]) + " tasks are assigned to container1")
            threading.Thread(target=task_assigner, args=("container1", tasks_list[0], containers_list)).start()
            tasks_list.pop(0)
        if containers_list[1] == "idle" and len(tasks_list) != 0:
            containers_list[1] = "busy"
            print("User" + str(tasks_list[0][1]) + " tasks are assigned to container2")
            threading.Thread(target=task_assigner, args=("container2", tasks_list[0], containers_list)).start()
            tasks_list.pop(0)
        if containers_list[2] == "idle" and len(tasks_list) != 0:
            containers_list[2] = "busy"
            print("User" + str(tasks_list[0][1]) + " tasks are assigned to container3")
            threading.Thread(target=task_assigner, args=("container3", tasks_list[0], containers_list)).start()
            tasks_list.pop(0)






# Main part of the code starts here
print("Creating container1, container2 and container3...")
containers_status = ["idle", "idle", "idle"]
tasks = []
subprocess.run("docker run -t -d --name container1 cloud_computing_image")
subprocess.run("docker run -t -d --name container2 cloud_computing_image")
subprocess.run("docker run -t -d --name container3 cloud_computing_image")
threading.Thread(target=container_selector, args=(containers_status, tasks)).start()




user_id = 1

while True:
    user_input = input("Input: ")
    if user_input == "exit":
        dockers_terminator()
        stop_flag = True
        break

    if user_input == "status":
        print("container1: " + containers_status[0])
        print("container2: " + containers_status[1])
        print("container3: " + containers_status[2])

    if user_input != "exit" and user_input != "status":
        commands_list, number_of_commands = input_separator(user_input)
        tasks.append([commands_list, user_id, number_of_commands])
        # start_time = time.time()
        # print("The command is: " + commands_string)
        user_id += 1
        # subprocess.run(commands_string)
        # stop_time = time.time()
        # print("Time: " + str(round(stop_time - start_time, 2)) + " s")














