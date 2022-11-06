from file_server.file_tcp_server import FileTCPServer
from structures.request import FileServerRequest
from file_server.file_server_request_handler import FileServerRequestHandler
import logging
import traceback

from Crypto.Cipher import PKCS1_OAEP


logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


users_data = dict() # Global variable, containing all of the client's data

def init_server():
    pass


def main():
    with FileTCPServer(logger=logger) as server:
        server.start()



    # import Crypto
    # from Crypto.PublicKey import RSA
    # from Crypto import Random
    # import ast
    #
    # random_generator = Random.new().read
    # key = RSA.generate(1024, random_generator)  # generate pub and priv key
    #
    # publickey = key.publickey()  # pub key export for exchange

    #
    # try:
    #     # a = FileServerRequestHandler('blbla')
    #     # a.init_db()
    #     #
    #     # a.request = FileServerRequest(123123, 1, 123, 123123, ('A'*255).encode() + publickey.export_key('DER'))
    #     # encrypted = a.save_public_key()
    #     # import ast
    #     #
    #     # decryptor = PKCS1_OAEP.new(key)
    #     # decrypted = decryptor.decrypt(ast.literal_eval(str(encrypted)))
    #     # print(decrypted)
    #
    # except Exception as e:
    #     logger.error(str(e) + '\n' + traceback.format_exc())



if __name__ == '__main__':
    main()
