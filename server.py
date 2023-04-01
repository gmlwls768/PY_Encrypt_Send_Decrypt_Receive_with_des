import socket
from _thread import *
import struct
client_sockets = []  # 서버에 접속한 클라이언트 목록

# 서버 IP 및 열어줄 포트
HOST = ''
PORT = 2498

# 서버 소켓 생성
print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

IMAGE_FILE = 'encodedimg.jpg'


# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
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


def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:

        try:
            packed = recvall(client_socket, struct.calcsize('!I'))
            # Decode the size and get the image data.
            size = struct.unpack('!I', packed)[0]
            print('Receiving data from:')
            data = recvall(client_socket, size)
            for client in client_sockets:
                if client != client_socket:

                    # Shutdown the socket and create the image file.
                    size = struct.pack('!I', len(data))
                    client.sendall(size + data)
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    # with open('serverreceivedEncodedimg.jpg', 'wb') as file:
                    #     file.write(data)
                    # checking receive file
            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            print('>> Received from ' + addr[0],
                  ':', addr[1], 'data receive from ')

        except:
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()


try:
    while True:
        print('>> Wait')
        client_socket,  addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("참가자 수 : ", len(client_sockets))

except Exception as e:
    print('에러는? : ', e)

finally:
    server_socket.close()
