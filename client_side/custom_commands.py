import os
import ctypes
import keyboard
import threading
import webbrowser
from PIL import ImageGrab
from playsound import playsound

class CustomCommands:
    def __init__(self, cmd, cmd_split):
        self.cmd = cmd
        self.cmd_split = cmd_split
    
    def check_cmds(self):
        output = 0
        
        if self.cmd_split[0] == "openfile":
            self.openfile()
        elif self.cmd_split[0] == "closefile":
            self.closefile()
        elif self.cmd_split[0] == "openweb":
            self.openweb()
        elif self.cmd_split[0] == "playsound":
            self.playsound()
        elif self.cmd_split[0] == "ss":
            self.screenshot()
        elif self.cmd_split[0] == "sendkeys":
            self.sendkeys()
        elif self.cmd_split[0] == "spkeys":
            self.specialkeys()
        elif self.cmd_split[0] == "bg":
            self.bg()
        elif self.cmd_split[0] == "del":
            self.del_()
        elif self.cmd_split[0] == "popup":
            threading.Thread(target=self.popup).start()
        else:
            output = 1
        
        return output, self.cmd_split[0]
    
    def sendkeys(self):
        keys = "1234567890!@#$%^&*()-=_+[]{};':\",./<>?QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm\|`~ "
        for x in " ".join(self.cmd_split[1:]):
            for i in keys:
                if x == i:
                    keyboard.press_and_release(x)
    
    def specialkeys(self):
        keys = [
            "caps_lock", "space", "tab", "right_shift", "shift", "alt", "right_alt",
            "ctrl", "right_ctrl", "esc", "up", "down", "left", "right", "enter", "backspace",
            "num_lock", "delete", "end", "print_screen", "page_down", "page_up", "insert",
            "home", "left_windows", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10",
            "f11", "f12"
        ]

        for x in keys:
            if self.cmd_split[1] == x:
                keyboard.press_and_release(x)
    
    def popup(self):
        ctypes.windll.user32.MessageBoxW(0, self.cmd_split[2].replace("_", " "), 
                                        self.cmd_split[1].replace("_", " "), 0x0 | 0x10) 

    def bg(self):
        os.startfile(self.cmd_split[1])
        keyboard.press_and_release("ctrl+b")
        os.system("taskkill /F /IM PhotosApp.exe")
    
    def openfile(self):
        os.startfile(self.cmd_split[1])
    
    def closefile(self):
        os.system("taskkill /F /IM " + self.cmd_split[1])

    def openweb(self):
        webbrowser.open(self.cmd_split[1])
    
    def playsound(self):
        playsound(self.cmd_split[1])

    def screenshot(self):
        ImageGrab.grab().save(self.cmd_split[1])
    
    def del_(self):
        os.remove(self.cmd_split[1])