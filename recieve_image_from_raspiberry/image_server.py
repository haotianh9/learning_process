import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl
import camera_yolo_v3_object_detection
import cv2
import numpy as np
import json
import time
server_socket = socket.socket()
server_socket.bind(('10.2.9.124', 8000))  # ADD IP HERE
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
conn, addr =server_socket.accept()
connection = conn.makefile('rb')

try:
    img = None
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        frame = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)  

        indexs,boxes,confidences,classIDs,lbs=camera_yolo_v3_object_detection.yolo_v3_object_detection(frame)
 
        conn.sendall(str(len(indexs)).encode('utf-8'))
        print(lbs,confidences,boxes)
        # print(len(indexs))
        if len(indexs) > 0:
            for i in range(len(indexs)):
                # print(i)
                dic={"label": lbs[i], "confidences": confidences[i],"box": boxes[i]}

                s=json.dumps(dic)
                # b = ' '.join(format(ord(letter), 'b') for letter in s)
                # print(type(b))
                conn.sendall(s.encode('utf-8'))
                time.sleep(0.1)
                # conn.sendall(str(confidences[i]).encode('utf-8'))
                # conn.sendall(np.array(boxes[i]).tobytes())
                
        if img is None:
            img = pl.imshow(image)
        else:
            img.set_data(image)

        pl.pause(0.01)
        pl.draw()

        print('Image is %dx%d' % image.size)
        image.verify()
        print('Image is verified')
finally:
    connection.close()

    server_socket.close()