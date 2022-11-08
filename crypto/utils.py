from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from Crypto.Util.Padding import unpad
import zlib

def get_crc_sum(data : bytes):
    return zlib.crc32(data) & 0xffffffff


def rsa_encryption(public_key, data):
    cipher = PKCS1_OAEP.new(RSA.importKey(public_key))
    return cipher.encrypt(data)


def generate_aes_key():
    return get_random_bytes(16)


def aes_decryption(aes_key, data):
    iv = bytearray([0] * AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data), AES.block_size)

def calculate_crc(data):
    return get_crc_sum(data.encode())
