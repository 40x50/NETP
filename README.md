# NETP
Botnet written in Python using Paramiko
------------------------------------------------------------

# Setup Server
------------------------------------------------------------
1. install setup.py on your linux server
2. run it with "python3 setup.py"
3. follow the steps provided to setup the rest of the server

# Setup Client (only works on windows machines)
------------------------------------------------------------
1. install all of the files in the "client_side" folder
2. open the "client_virus.py" file and add your executable name, linux server ip address, linux server username, and linux server password (NOTE: THESE ARE IN PLAIN TEXT IN THE FILE)
3. install requirements (see requirements section)
4. compile the "client_virus.py" file into an exe, make sure to change the name to the executable name that you set in the code (it won't work otherwise) and i recommend adding an icon to the executable aswell.
5. Your client file is all set!

# Requirements
------------------------------------------------------------
win32crypt, pycrypt, paramiko, playsound, keyboard, pillow, requests, psutil, pyautogui, bs4, fernet
