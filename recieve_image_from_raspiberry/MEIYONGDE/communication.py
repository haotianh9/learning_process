import socket
import threading
import time
import numpy as np
import cv2
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('10.2.9.124',8080)
ser.bind(address)

ser.listen(True)          

print('Server is running...')       # 打印运行提示

def tcplink(connect, addr):
    print('Accept new connection from %s:%s...' % addr)
    connect.send(b'Welcome!\r\n'+b'Please tell me your name:')
    data = connect.recv(1024)
    connect.send(('Hello, %s' % data.decode('utf-8')).encode('utf-8'))
    while True:
        data = connect.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        print("Device: %s, Data: %s, Size: %s" % (addr[0], data.decode('utf-8'), len(data)))
        connect.send(b'Data Receive')
        if data.decode('utf-8') == "send image":
            recieveimage(connect)
    connect.close()
    print('Connection from %s:%s closed' % addr)


def recieveimage(connect):
    data = connect.recv(209000)
    print(type(data))
    print(len(data))
    data1 = np.fromstring(data, dtype='uint8')
    image=cv2.imdecode(data1,1)
    # display the image on screen and wait for a keypress
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    connect.send(b'Data Receive')
    return
while True:
    sock, addr = ser.accept()
    pthread = threading.Thread(target=tcplink, args=(sock, addr))   #多线程处理socket连接
    pthread.start()
