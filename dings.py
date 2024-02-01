import socket
import threading
import time

import keyboard
import winsound

address = ('0.0.0.0', 90)


# ding
def playDingSound():
    filename = '0141ding.wav'
    winsound.PlaySound(filename, winsound.SND_FILENAME)


def listen(listen_address):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 90))
    server.listen()
    print('等待连接')
    client, addr = server.accept()
    print('connect:', addr)
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


so = listen(address)
st = threading.Thread(target=send_ding, args=(so,))
rt = threading.Thread(target=receive_ding, args=(so,))
st.start()
rt.start()
