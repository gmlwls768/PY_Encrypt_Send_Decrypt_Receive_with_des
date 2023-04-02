import socket
from _thread import *
import struct
client_sockets = []  # 서버에 접속한 클라이언트 목록

# 서버 IP 및 열어줄 포트
HOST = ''
PORT = 2498

# 서버 소켓 생성
print('>> Server Start')
server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)  # 소켓 객체를 생성 IPv4 이용한 TCP연결
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))  # 소켓에 주소와 포트번호를 할당
server_socket.listen()  # 소켓을 수신 대기 상태로


# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
def recvall(sock, size):
    message = bytearray()  # 바이트어레이 객체 생성
    # Loop until all expected data is received.
    while len(message) < size:  # message의 크기가 size와 같아질 때까지
        # 버퍼를 통해 size에서 message의 값을 뺀만큼 받아옴
        buffer = sock.recv(size - len(message))
        if not buffer:  # 받을 파일이 없을 경우
            # End of stream was found when unexpected.
            # raise EOFError('Could not receive all expected data!')
            # return bytes(message)  # 리턴
            break

        message.extend(buffer)  # message배열에 받은 버퍼 추가
    return bytes(message)  # message를 바이트단위로 리턴


def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:

        try:
            # recvall 함수를 이용하여서 데이터 크기 패킹 값 받음
            packed = recvall(client_socket, struct.calcsize('!I'))
            # Decode the size and get the image data.
            size = struct.unpack('!I', packed)[0]  # 패킹했던 데이터 크기 값 받기
            print('Receiving data from:')
            data = recvall(client_socket, size)  # 데이터크기를 이용하여 데이터 받음
            for client in client_sockets:
                if client != client_socket:  # 보낸 클라이언트가 아닌 클라이언트 일때

                    # Shutdown the socket and create the image file.
                    # struct를 이용해 data의 크기를 알아내서 리턴
                    size = struct.pack('!I', len(data))
                    client.sendall(size + data)  # data와 size 값을 전송
                    client.shutdown(socket.SHUT_RDWR)  # 소켓의 송수신 중단
                    client.close()  # 소켓 종료
                    # with open('serverreceivedEncodedimg.jpg', 'wb') as file:
                    #     file.write(data)
                    # checking receive file
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            print('>> Received from ' + addr[0],
                  ':', addr[1], 'data receive from ')

        except:
            continue

    if client_socket in client_sockets:  # 클라이언트 종료될 경우 리스트에서 제거하고 출력함
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()


try:
    while True:
        print('>> Wait')
        client_socket,  addr = server_socket.accept()  # 들어오는 클라이언트 연결을 기다림
        client_sockets.append(client_socket)  # 클라이언트 저장배열에 추가
        start_new_thread(threaded, (client_socket, addr)
                         )  # threaded 함수를 새로운 스레드에서 실행
        print("참가자 수 : ", len(client_sockets))

except Exception as e:
    print('에러는? : ', e)

finally:
    server_socket.close()
