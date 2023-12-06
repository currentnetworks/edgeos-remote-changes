import paramiko
import time
import logging
import os
import getpass
 
# Set up logging to file and console
logging.basicConfig(level=logging.INFO, filename='log.txt', filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('paramiko.transport').setLevel(logging.ERROR)  # Only log errors and above for paramiko.transport
logging.getLogger('').addHandler(console)

def file_exists(filename):
    return os.path.isfile(filename)

def load_file_contents(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

def send_command(channel, command):
    channel.send(command + "\n")
    time.sleep(1)
    while not channel.recv_ready():
        time.sleep(1)
    output = channel.recv(2048).decode()
    logging.info(f"Command: {command}\nOutput: {output}")
    return output

def execute_commands(client, commands, router):
    with client.invoke_shell() as channel:
        for command in commands:
            send_command(channel, command)

def create_ssh_client(hostname, username, password, timeout=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password, look_for_keys=False, allow_agent=False, timeout=timeout, banner_timeout=30)
        return client
    except paramiko.SSHException as e:
        logging.error(f"Connection to {hostname} failed: {e}")
        return None

def do_connection_commands(username, password, router, commands):
    logging.info(f"\n\n -------Connecting to {router}-------\n\n")
    client = create_ssh_client(router, username, password)
    if client:
        execute_commands(client, commands, router)
        client.close()
    return client

def main():
    if not file_exists("routers.txt") or not file_exists("command-list.txt"):
        logging.error("Necessary files (routers.txt or command-list.txt) are missing.")
        return

    routers = load_file_contents("routers.txt")
    commands = load_file_contents("command-list.txt")

    auth_error = "Authentication"
    max_attempts = 3

    username = input("Initial Username: ")
    password = getpass.getpass("Initial Password: ")

    TempUser = username
    TempPass = password

    additional_commands_exist = file_exists("additional-commands.txt")
    additional_commands = load_file_contents("additional-commands.txt") if additional_commands_exist else []

    use_new_credentials = False
    new_username = ""
    new_password = ""

    if additional_commands_exist:
        print("File additional-commands.txt exists.")
        use_new_credentials = input("Do you need to use different credentials for these additional commands? (yes/no): ").lower() == 'yes'
        if use_new_credentials:
            new_username = input("New Username for additional commands: ")
            new_password = getpass.getpass("New Password for additional commands: ")

    for router in routers:
        for attempt in range(max_attempts):
            try:
                client = do_connection_commands(username, password, router, commands)
                if client and additional_commands_exist:
                    if use_new_credentials:
                        # Use new credentials for additional commands
                        do_connection_commands(new_username, new_password, router, additional_commands)
                    else:
                        # Use the same credentials for additional commands
                        do_connection_commands(username, password, router, additional_commands)
                break
            except Exception as e:
                logging.error(f"Error connecting to {router}: {e}")
                if attempt < max_attempts - 1 and auth_error in str(e):
                    logging.error(f"Error connecting to {router}: {e}. Trying again.")
                    username = input(f"Username For {router}: ")
                    password = getpass.getpass(f"Password For {router}: ")
                else:
                    break
            finally:
                # Reset the credentials for the next router
                username = TempUser
                password = TempPass


if __name__ == "__main__":
    main()
