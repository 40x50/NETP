import re
import uuid
import socket
import requests
import getpass
import platform
import json

class GatherInfo:
    def __init__(self):
        self.location = self.location()
        self.mac = self.mac()
        self.private_ip = self.private_ip()
        self.public_ip = self.public_ip()
        self.machine_name = self.machine_name()
        self.username = self.username()

        self.contents = f"""
Public IP: {self.public_ip}
Private IP: {self.private_ip}
Username: {self.username}
Machine Name: {self.machine_name}
MAC Address: {self.mac}
Country: {self.location["country_name"]}
City: {self.location["city"]}
Postal Code: {self.location["postal"]}
State: {self.location["state"]}
        """.strip() + "\n"

    def public_ip(self):
        try:
            return self.public_ip_addr()
        except:
            return self.public_ip_addr()

    def location(self):
        try:
            return self.geolocation()
        except:
            return self.geolocation()

    def geolocation(self):
        r = requests.get("https://geolocation-db.com/jsonp/" + self.public_ip()).content.decode()
        r = r.split("(")[1].strip(")")
        return json.loads(r)

    def mac(self):
        return ";".join(re.findall("..", "%012x" % uuid.getnode()))
    
    def private_ip(self):
        return socket.gethostbyname(socket.gethostname())
    
    def public_ip_addr(self):
        return requests.get('https://api.ipify.org').content.decode('utf8')
    
    def machine_name(self):
        return platform.node()
    
    def username(self):
        return getpass.getuser()