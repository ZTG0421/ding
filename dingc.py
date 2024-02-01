import socket
import threading
import time

import keyboard
import winsound

address = ('127.0.0.1', 90)


# ding
def playDingSound():
    filename = '0141ding.wav'
    winsound.PlaySound(filename, winsound.SND_FILENAME)


def connect_to_server(server_address):
    print('trying to connect to {}'.format(server_address))
    # 循环try
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(server_address)
        except ConnectionRefusedError:
            print('failed')
            time.sleep(1)
            continue
        else:
            break
    print('OK')
    return client


# 开ding
def receive_ding(sock):
    while True:
        rec = sock.recv(1024)
        print('recv:' + rec.decode('utf-8'))
        if rec.decode('utf-8') == 'ding':
            threading.Thread(target=playDingSound).start()


def send_ding(sock):
    while True:
        keyboard.wait('w')
        sock.send('ding'.encode('utf-8'))
        # 0.5s保护
        time.sleep(1)


so = connect_to_server(address)
st = threading.Thread(target=send_ding, args=(so,))
rt = threading.Thread(target=receive_ding, args=(so,))
st.start()
rt.start()
