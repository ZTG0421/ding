import socket
import threading
import time
import re
import keyboard
import winsound

address = ('127.0.0.1', 90)


# ding
def playDingSound():
    filename = '0141ding.wav'
    winsound.PlaySound(filename, winsound.SND_FILENAME)


def connect_to_server(server_address):
    print('connecting to {}...'.format(server_address))
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
    print('OK  CONNECTED WITH {}',server_address)
    return client


# 开ding
def receive_ding(sock):
    while True:
        rec = sock.recv(1024)
        #当前毫秒时间戳 整数
        current_time=int(round(time.time(),4)*10000)
        rec=rec.decode('utf-8')
        result = re.findall(r'[a-zA-Z]+', rec)
        rec_time = re.findall(r'\d+', rec)
        #对方毫秒时间戳 整数
        rec_time=int(rec_time[0])
        result = result[0]
        if result == 'ding':
            print('ding/'+str(current_time-rec_time)+'ms')
            threading.Thread(target=playDingSound).start()


def send_ding(sock):
    while True:
        keyboard.wait('w')
        presend='ding'+str(int(round(time.time(),4)*10000))
        sock.send(presend.encode('utf-8'))
        # 0.5s保护
        time.sleep(1)


so = connect_to_server(address)
st = threading.Thread(target=send_ding, args=(so,))
rt = threading.Thread(target=receive_ding, args=(so,))
st.start()
rt.start()
