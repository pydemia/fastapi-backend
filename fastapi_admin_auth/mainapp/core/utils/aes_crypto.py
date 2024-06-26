from Cryptodome import Random
from Cryptodome.Cipher import AES
import base64
from hashlib import md5

class AESCrypto:
    """
    AES 암호화 / 복호화
    """
    
    def __init__(self):
        self.block_size = 16
        self.passphrase = "fastapi_admin_auth".encode()
        
    def pad(self, data):
        length = self.block_size - (len(data) % self.block_size)
        return data + (chr(length)*length).encode()

    def unpad(self, data):
        return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

    def bytes_to_key(self, data, salt, output=48):
        assert len(salt) == 8, len(salt)
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]

    def encrypt(self, message):
        salt = Random.new().read(8)
        key_iv = self.bytes_to_key(self.passphrase, salt, 32+16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(b"Salted__" + salt + aes.encrypt(self.pad(message)))

    def decrypt(self, encrypted):
        encrypted = base64.b64decode(encrypted)
        assert encrypted[0:8] == b"Salted__"
        salt = encrypted[8:16]
        key_iv = self.bytes_to_key(self.passphrase, salt, 32+16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return self.unpad(aes.decrypt(encrypted[16:]))