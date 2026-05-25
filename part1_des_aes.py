# Part 1 - Symmetric Encryption: DES & AES
# Requires: pip install pycryptodome
#
# NOTE: ECB mode is used here for teaching simplicity only.
# In production, use CBC or GCM (GCM also provides authentication).
# DES is deprecated (retired by NIST) and included for demonstration.

from Crypto.Cipher import DES, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


class encryptDecrypt:
    # ---- Keys ----
    def getADesKey(self):
        return get_random_bytes(8)   # DES uses an 8-byte key

    def getAesKey(self):
        return get_random_bytes(16)  # AES-128 uses a 16-byte key

    # ---- DES ----
    def encryptDes(self, plainText, key):
        paddedText = pad(plainText, DES.block_size)
        desCipher = DES.new(key, DES.MODE_ECB)
        return desCipher.encrypt(paddedText)

    def decryptDes(self, cipheredText, key):
        desCipher = DES.new(key, DES.MODE_ECB)
        return unpad(desCipher.decrypt(cipheredText), DES.block_size)

    # ---- AES ----
    def encryptAes(self, plainText, key):
        paddedText = pad(plainText, AES.block_size)
        aesCipher = AES.new(key, AES.MODE_ECB)
        return aesCipher.encrypt(paddedText)

    def decryptAes(self, cipheredText, key):
        aesCipher = AES.new(key, AES.MODE_ECB)
        return unpad(aesCipher.decrypt(cipheredText), AES.block_size)


if __name__ == "__main__":
    obj = encryptDecrypt()
    plainText = b'Python is a very powerful language'

    # --- DES round trip ---
    desKey = obj.getADesKey()
    encDes = obj.encryptDes(plainText, desKey)
    encDes_b64 = b64encode(encDes).decode('utf-8')
    decDes = obj.decryptDes(b64decode(encDes_b64), desKey)
    print("DES Decrypted Text:")
    print(decDes)

    # --- AES round trip ---
    aesKey = obj.getAesKey()
    encAes = obj.encryptAes(plainText, aesKey)
    encAes_b64 = b64encode(encAes).decode('utf-8')
    decAes = obj.decryptAes(b64decode(encAes_b64), aesKey)
    print("\nAES Decrypted Text:")
    print(decAes)
