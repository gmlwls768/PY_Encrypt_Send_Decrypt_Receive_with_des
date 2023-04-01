# use pycryptodome
from Crypto.Cipher import DES
from Crypto.Hash import SHA256 as SHA
from Crypto.Util.Padding import pad, unpad
import base64
import os

BLOCK_SIZE = 8


class myDES():

    # DES 초기화
    def __init__(self, keytext):
        hash = SHA.new()
        hash.update(keytext.encode('utf-8'))
        key = hash.digest()  # 입력된 keytext를 SHA-256 해시값으로 변환
        # keytext를 해시화했을 때 첫 8byte를 key로 함
        self.key = key[:8]

    # ECB 모드로 암호화
    def encrypt_ECB(self, plaintext):
        # padding값을 추가해 8byte로 만들어줌
        des = DES.new(self.key, DES.MODE_ECB)  # des 객체 만듬
        plaintext = base64.encodebytes(plaintext)  # image파일이기에 base64로 인코딩

        # 평문과 블록사이즈를 패딩(8바이트로 맞춰줌)하여 des객체로 암호화 암호화한 메시지를 변수에 저장
        encryptMsg = des.encrypt(pad(plaintext, BLOCK_SIZE))
        imr = open(
            'encodedimg.jpg', 'wb')
        imr.write(encryptMsg)  # encodeimg라는 파일 작성
        imr.close()

    # ECB 모드로 암호화된 암호문을 복호화

    def decrypt_ECB(self, ciphertext, user_pathnum):
        des = DES.new(self.key, DES.MODE_ECB)  # des 객체 만듬
        descryptMsg = des.decrypt(ciphertext)  # des객체로 복호화 암호화한 메시지를 변수에 저장
        unpadMsg = unpad(descryptMsg, BLOCK_SIZE)  # 언패딩하여 변수에 저장
        unpadMsg = base64.decodebytes(unpadMsg)  # base64로 디코딩하여 변수에 저장
        # os함수 이용하여 매개변수로 받은 path를 string값으로 만든다
        nowdir = str(os.getcwd()) + '/' + str(user_pathnum)
        self.createFolder(nowdir)  # 함수를 이용해 path기반하여 그 경로에 폴더 만듬
        imr = open(f'{nowdir}/river_image.jpg', 'wb')  # 복호화한 파일 작성
        imr.write(unpadMsg)
        imr.close()

    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):  # 경로에 폴더 없을시
                os.makedirs(directory)  # 만듬
        except OSError:
            print('Error: Creating directory. ' + directory)
