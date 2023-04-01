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

HOST = localhost  # 접속 주소 설정
PORT = 2498

client_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)  # 소켓 객체를 생성 IPv4 이용한 TCP연결
client_socket.connect((HOST, PORT))  # ip주소와 포트주소를 이용하여 연결
my_socket_name = client_socket.getsockname()  # 접속한 클라이언트 객체의 ip주소 포트번호를 리턴받음

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리


def recvall(sock, size):
    message = bytearray()  # 바이트어레이 객체 생성
    # Loop until all expected data is received.
    while len(message) < size:  # message의 크기가 size와 같아질 때까지
        # 버퍼를 통해 size에서 message의 값을 뺀만큼 받아옴
        buffer = sock.recv(size - len(message))
        if not buffer:  # 받을 파일이 없을 경우
            # End of stream was found when unexpected.
            # raise EOFError('Could not receive all expected data!')
            return bytes(message)  # 리턴

        message.extend(buffer)  # message배열에 받은 버퍼 추가
    return bytes(message)  # message를 바이트단위로 리턴


def createFolder(directory):
    try:
        if not os.path.exists(directory):  # 디렉토리가 존재안할경우
            os.makedirs(directory)  # 생성
    except OSError:
        print('Error: Creating directory. ' + directory)


def enc():
    imgp = open(r"./river_image.jpg", 'rb')  # 송신 할 파일 읽기
    img = imgp.read()
    des = myDES('itiskey1')  # des객체 생성 및 키값 넣기
    des.encrypt_ECB(img)  # des 함수 암호화
    with open('encodedimg.jpg', 'rb') as f:
        try:
            data = f.read()  # 암호화된 파일을 읽는다
            # struct를 이용해 data의 크기를 알아내서 리턴
            size = struct.pack('!I', len(data))
            client_socket.sendall(size + data)  # data와 size 값을 전송

        except Exception as ex:
            print(ex)
    os.remove("encodedimg.jpg")  # 파일 저장하고 암호화된 파일을 삭제


def dec(pathnum):
    # 현재 위치 알아내고 매개변수를 이용하여 현위치 + 접속한 클라이언트 주소 string 생성
    nowdir = str(os.getcwd()) + '/' + str(my_socket_name)
    imgp = open(rf'{nowdir}/receivedEncodedimg.jpg', 'rb')  # 송신측에서 파일 읽기
    img = imgp.read()
    os.remove(f"{nowdir}/receivedEncodedimg.jpg")  # 서버에서 받은 암호화 파일 삭제하기 !!
    des = myDES('itiskey1')  # des객체 생성 및 키값 넣기
    des.decrypt_ECB(img, pathnum)  # des 함수 복호화 , 암호화값과 클라이언트 주소를 인수값으로


def clear():
    os.system('clear')  # 터미널 clear
    print('Client: ', str(my_socket_name))  # 접속한 클라이언트 주소 print


def recv_data(client_socket):
    while True:

        # recvall 함수를 이용하여서 데이터 크기 패킹 값 받음
        packed = recvall(client_socket, struct.calcsize('!I'))
        # Decode the size and get the image data.
        try:
            size = struct.unpack('!I', packed)[0]  # 패킹했던 데이터 크기 값 받기
            print('Receiving data from:')
            data = recvall(client_socket, size)  # 데이터크기를 이용하여 데이터 받음
        except:
            pass

        nowdir = str(os.getcwd()) + '/' + \
            str(my_socket_name)  # 현위치 + 클라이언트 주소 스트링값으로
        createFolder(nowdir)  # 폴더 생성

        with open(f'{nowdir}/receivedEncodedimg.jpg', 'wb') as f:  # 현재dir에 filename으로 파일을 받는다
            f.write(data)  # 파일 작성
            dec(my_socket_name)  # 파일 받은 것을 통해 복호화 진행

            clear()

            print('received data in folder :: \r\n', nowdir)  # 저장했던 위치 프린트
            print('Enter to confirm')
            global loop
            loop = False


clear()


start_new_thread(recv_data, (client_socket,))  # recv_data 함수를 새로운 thread에서 실행
print('>> Connect Server')
loop = True
while loop:  # 반복문을 이용하여 인풋값 입력

    message = input('Do: ')
    if message == 'quit':
        break

    elif message == 'send':  # send 입력시에 암호화 함수인 enc로 이동
        encod = enc()


client_socket.close()
