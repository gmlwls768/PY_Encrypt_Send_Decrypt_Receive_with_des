# use pycryptodome
from Crypto.Cipher import DES
from Crypto.Hash import SHA256 as SHA
from Crypto.Util.Padding import pad, unpad
import base64

BLOCK_SIZE = 8


class myDES():

    # DES 초기화
    def __init__(self, keytext):
        hash = SHA.new()
        hash.update(keytext.encode('utf-8'))
        # keytext를 해시화했을 때 첫 8byte를 key로 함
        key = hash.digest()
        self.key = key[:8]

    # ECB 모드로 암호화
    def encrypt_ECB(self, plaintext):
        # padding값을 추가해 8byte로 만들어줌
        # plaintext = pad(plaintext, BLOCK_SIZE)

        des = DES.new(self.key, DES.MODE_ECB)

        plaintext = base64.encodebytes(plaintext)
        encryptMsg = des.encrypt(pad(plaintext, BLOCK_SIZE))
        imr = open(
            'encodedimg.jpg', 'wb')
        imr.write(encryptMsg)
        imr.close()
    # ECB 모드로 암호화된 암호문을 복호화

    def decrypt_ECB(self, ciphertext):
        des = DES.new(self.key, DES.MODE_ECB)
        descryptMsg = des.decrypt(ciphertext)
        unpadMsg = unpad(descryptMsg, BLOCK_SIZE)
        unpadMsg = base64.decodebytes(unpadMsg)
        imr = open('./receiver/river_image.jpg', 'wb')
        imr.write(unpadMsg)
        imr.close()


# user_input = int(input('1: encrypt 2: decrypt: '))
# if user_input == 1:
#     imgp = open(
#         r"/Users/ocean/SynologyDrive/code/school_python/secure/river_image.jpg", 'rb')
#     img = imgp.read()
#     # base64 is used to conver binary to ASCII values
#     img64 = base64.encodebytes(img)
#     des = myDES('itiskey1')
#     des.encrypt_ECB(img)
# elif user_input == 2:
#     imgp = open(
#         r"/Users/ocean/SynologyDrive/code/school_python/secure/encodedimg.jpg", 'rb')
#     img = imgp.read()
#     des = myDES('itiskey1')
#     des.decrypt_ECB(img)
