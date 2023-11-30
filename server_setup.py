import os

dirs = [
    "/home/botnet/client/clients",
    "/home/botnet/server/client_control",
    "/home/botnet/server/client_output",
    "/home/botnet/server/custom_cmd/output",
    "/home/botnet/server/online",
    "/home/botnet/server/sendfile/output",
    "/home/botnet/server/vir/output"
]

files = [
    "/home/botnet/client/clients_num.txt",
    "/home/botnet/server/custom_cmd/cmd_info.txt",
    "/home/botnet/server/vir/vir_info.txt"
]

for x in dirs:
    os.makedirs(x)

for x in files:
    with open(x, "w") as f:
        pass

print("1. Install interface.py, server_main.py, and server.py from the github at https://github.com/40x50/NETP.\n\t(make sure to install it in the \"/home/botnet/server/\" directory)")
print("2. Once installed, run the server with \"python3 server_main.py\".")
print("3. Find the \"Initialize Server\" section on the github and follow the steps accordingly.")
print("4. You're server is all set!")