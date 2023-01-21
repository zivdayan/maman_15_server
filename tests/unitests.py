import unittest
from Crypto.Cipher import AES
from crypto.utils import generate_aes_key
from structures.request import FileServerRequest, InvalidRequest as InvalidFileServerRequest
from structures.response import FileServerResponse, InvalidRequest as InvalidFileServerResponse
from file_server.file_server_request_handler import FileServerRequestHandler
from unittest.mock import patch

from sqlite3.dbapi2 import IntegrityError
import logging

logger = logging.getLogger(__name__)


class UnitTests(unittest.TestCase):
    DATA = 'RANDOM'.encode()

    def test_aes(self, data=DATA):
        key = generate_aes_key()
        raw_data = data

        # Encryption
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        # Decryption
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)

        self.assertEqual(raw_data, plaintext)

    def test_malformed_request(self):
        with self.assertRaises(InvalidFileServerRequest):
            reqeust = FileServerRequest('id', 0.1, 1, 2, 'random')
            reqeust.parse_binary_request('random'.encode())

    def test_unknown_code(self):
        RANDOM_CODE = '112'
        handler = FileServerRequestHandler('test', 'test', None)
        self.assertEqual(handler.request_to_function_mapping.get(RANDOM_CODE), None)

    def test_user_already_registered(self):
        logger = logging.getLogger(__name__)
        with patch('sqlite_dal.SQLiteDatabase.write', side_effect=IntegrityError('UNIQUE constraint failed')):
            with self.assertLogs(logger=logger, level='WARNING') as cm:
                request = FileServerRequest('id', 0.1, 1, 2, b'random')
                handler = FileServerRequestHandler('test', 'test', logger)
                handler.request = request
                handler.register_user()

        # FOR DEMO:
        # fail test using - self.assertEqual(len(cm), 0)
        self.assertRegex(cm.output[0], 'already registered')


if __name__ == '__main__':
    unittest.main()
