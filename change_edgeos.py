import paramiko
import getpass
import time

#Get Router List
with open("routers.txt", "r") as f:
    routers = list(line for line in (l.strip() for l in f) if line)

#Get Command List
with open("command-list.txt", "r") as f:
    commands = list(line for line in (l.strip() for l in f) if line)

#Send Command Function
def send_command(channel, command):
    channel.send(command+"\n")
    time.sleep(1)
    while not channel.recv_ready():
        pass
    stdout = channel.recv(2048).decode()

    print("Command: " + command)
    print("Output: " + stdout)
    with open("log.txt", "a") as f:
        f.write("Command: " + command + "\n")
        f.write("Output: " + stdout + "\n")

#Do Connection Work Funciton
def do_connection_commands(username, password, router, commands, f):
    # Log the router we are trying to connect to
    f.write(f"\n\n -------Connecting to {router}-------\n\n")
    print("\n\n -------Connecting to "+router+"-------\n\n")
  
    client.connect(router, username=username, password=password, look_for_keys=False, allow_agent=False, timeout=5)

    time.sleep(1)
    channel = client.invoke_shell()
    stdout = channel.recv(2048).decode()
    f.write("Command: Connect" + "\n")
    f.write("Output: " + stdout + "\n")

    print(stdout + "-\n-----Running Commands------\n")
    f.write("------Running Commands------\n")
    for command in commands:
        send_command(channel, command)


#Define Error Conditions and Attempts to Trye
auth_error = "Authentication"
max_attempts = 3


# Get SSH credentials
username = input("Username: ")
password = getpass.getpass()
TempUser = username
TempPass = password

# Create an SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with open("log.txt", "w") as f:
    for router in routers:
        for attempt in range(max_attempts):
            try:
                do_connection_commands(username, password, router, commands, f)
                username = TempUser
                password = TempPass

            except Exception as e:
                if attempt < max_attempts - 1 and auth_error in str(e):
                    f.write(f"Error connecting to {router}: {e} Try Again \n")
                    print(f"Error connecting to {router}: {e} \n Try Again")  

                    #try credentials again
                    username = input("Username For "+router+": ")
                    password = getpass.getpass()
                    continue
                else:
                    f.write(f"Error connecting to {router}: {e}\n")
                    print(f"Error connecting to {router}: {e}")
                    pass
            break




