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
def status_list_changer(containers_list, container_index, number_of_commands, user_id):
    time.sleep(number_of_commands * 1.5)
    containers_list[container_index] = "idle"
    print("User" + str(user_id) + " tasks finished")


# This function assigns a task to the input task
def task_assigner(container_name, task, containers_list):
    user_id = task[1]
    # making the output directory in the container
    subprocess.run("docker exec " + str(container_name) + " mkdir -p /home/cloud_computing/Output/user" + str(user_id) + "_output")
    subprocess.run("docker exec " + str(container_name) + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/min.txt")
    subprocess.run("docker exec " + str(container_name) + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/max.txt")
    subprocess.run("docker exec " + str(container_name) + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/average.txt")
    subprocess.run("docker exec " + str(container_name) + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/sort.txt")
    subprocess.run("docker exec " + str(container_name) + " touch /home/cloud_computing/Output/user" + str(user_id) + "_output" + "/wordcount.txt")
    if container_name == "container1":
        threading.Thread(target=status_list_changer, args=(containers_list, 0, task[2], user_id)).start()
    elif container_name == "container2":
        threading.Thread(target=status_list_changer, args=(containers_list, 1, task[2], user_id)).start()
    elif container_name == "container3":
        threading.Thread(target=status_list_changer, args=(containers_list, 2, task[2], user_id)).start()
    subprocess.run(task[0].replace("container1", container_name))


# This function selects an idle container and it is the dispatcher
def container_selector(containers_list, tasks_list):
    while not stop_flag:
        if containers_list[0] == "idle" and len(tasks_list) != 0:
            containers_list[0] = "busy"
            threading.Thread(target=task_assigner, args=("container1", tasks_list[0], containers_list)).start()
            tasks_list.pop(0)
        if containers_list[1] == "idle" and len(tasks_list) != 0:
            containers_list[1] = "busy"
            threading.Thread(target=task_assigner, args=("container2", tasks_list[0], containers_list)).start()
            tasks_list.pop(0)
        if containers_list[2] == "idle" and len(tasks_list) != 0:
            containers_list[2] = "busy"
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

    else:
        commands_list, number_of_commands = input_separator(user_input)
        commands_string = "docker exec container1 python /home/cloud_computing/Script.py "
        for i in commands_list:
            commands_string += i + " "
        commands_string = commands_string.rstrip(" ")
        commands_string += "/user" + str(user_id) + "_output"
        tasks.append([commands_string, user_id, number_of_commands])
        # start_time = time.time()
        # print("The command is: " + commands_string)
        print("User" + str(user_id) + " tasks are processing")
        user_id += 1
        # subprocess.run(commands_string)
        # stop_time = time.time()
        # print("Time: " + str(round(stop_time - start_time, 2)) + " s")














