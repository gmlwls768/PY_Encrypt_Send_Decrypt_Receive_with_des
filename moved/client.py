# receiver

from socket import *
import os
import sys
from DES import *
clientSock = socket(AF_INET, SOCK_STREAM)

local_ulsan = '192.168.0.7'
localhost = '127.0.0.1'
vpn = '10.8.0.1'
clientSock.connect((localhost, 2498))


def dec():
    imgp = open(r"./receiver/encodedimg.jpg", 'rb')
    img = imgp.read()
    des = myDES('itiskey1')
    des.decrypt_ECB(img)
    os.remove(
        './receiver/encodedimg.jpg')
    # imgp.close()


print('연결에 성공했습니다.')

filename = 'river_image.jpg'
clientSock.sendall(filename.encode('utf-8'))

data = clientSock.recv(1024)
data_transferred = 0

if not data:
    print('파일 %s 가 서버에 존재하지 않음' % filename)
    sys.exit()
nowdir = os.getcwd()
nowdir += '/receiver'
# nowdir = '/Users/ocean/SynologyDrive/code/school_python/secure/receiver'
with open(nowdir+'/encodedimg.jpg', 'wb') as f:  # 현재dir에 filename으로 파일을 받는다
    try:
        while data:  # 데이터가 있을 때까지
            f.write(data)  # 1024바이트 쓴다
            data_transferred += len(data)
            data = clientSock.recv(1024)  # 1024바이트를 받아 온다
    except Exception as ex:
        print(ex)
dec()


print('파일 %s 받기 완료. 전송량 %d' % (filename, data_transferred))
