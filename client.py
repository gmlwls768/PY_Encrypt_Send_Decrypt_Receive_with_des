from DES import *
import socket
from _thread import *
import os
import struct
local_ulsan = '192.168.0.7'
localhost = '127.0.0.1'
vpn = '10.8.0.1'
tmp = '192.168.189.138'
saewoo = '192.168.189.134'

HOST = localhost
PORT = 2498

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
my_socket_name = client_socket.getsockname()

data_transferred = 0
# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리


def recvall(sock, size):
    message = bytearray()
    # Loop until all expected data is received.
    while len(message) < size:
        buffer = sock.recv(size - len(message))
        if not buffer:
            # End of stream was found when unexpected.
            # raise EOFError('Could not receive all expected data!')
            return bytes(message)

        message.extend(buffer)
    return bytes(message)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def enc():
    imgp = open(r"./river_image.jpg", 'rb')  # 송신측에서 파일 읽기
    img = imgp.read()
    des = myDES('itiskey1')
    des.encrypt_ECB(img)  # des 함수 암호화
    # client_socket.sendall(my_enc)
    with open('encodedimg.jpg', 'rb') as f:
        try:
            data = f.read()  # 1024바이트 읽는다
            size = struct.pack('!I', len(data))
            client_socket.sendall(size + data)

        except Exception as ex:
            print(ex)
    os.remove("encodedimg.jpg")


def dec(pathnum):
    nowdir = str(os.getcwd()) + '/' + str(my_socket_name)
    imgp = open(rf'{nowdir}/receivedEncodedimg.jpg', 'rb')  # 송신측에서 파일 읽기
    img = imgp.read()
    os.remove(f"{nowdir}/receivedEncodedimg.jpg")  # 서버에서 받은 암호화 파일 삭제하기 !!
    des = myDES('itiskey1')
    des.decrypt_ECB(img, pathnum)  # des 함수 복호화 , 암호화값과 클라이언트 주소를 인수값으로


def clear():
    os.system('clear')
    print('Client: ', str(my_socket_name))


def recv_data(client_socket):
    while True:

        packed = recvall(client_socket, struct.calcsize('!I'))
        # Decode the size and get the image data.
        try:
            size = struct.unpack('!I', packed)[0]
            print('Receiving data from:')
            data = recvall(client_socket, size)
        except:
            pass

        nowdir = str(os.getcwd()) + '/' + str(my_socket_name)
        createFolder(nowdir)

        with open(f'{nowdir}/receivedEncodedimg.jpg', 'wb') as f:  # 현재dir에 filename으로 파일을 받는다
            f.write(data)  # 1024바이트 쓴다
            dec(my_socket_name)

            clear()

            print('received data in folder :: \r\n', nowdir)
            print('Enter to confirm')
            global loop
            loop = False


clear()


start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')
loop = True
while loop:

    message = input('Do: ')
    if message == 'quit':
        break

    elif message == 'send':
        encod = enc()


client_socket.close()
