from structures.file import File
from structures.client import Client

from structures.request import FileServerRequest, InvalidRequest, UserAlreadyRegistered
from structures.response import FileServerResponse
from structures.consts import *

from typing import Callable, Dict
from sqlite_dal import SQLiteDatabase

from sqlite3 import IntegrityError

import secrets

from crypto.utils import *
from base64 import b64encode
import struct


class FileServerRequestHandler:
    BASE_TABLES = {f"{c.__name__}": c.SQL_COLUMNS_DESCRIPTION for c in [File, Client]}

    def __init__(self, raw_request):
        self.raw_request = raw_request
        self.request: FileServerRequest = None
        self.init_db()

    def handle(self) -> FileServerResponse:
        request: FileServerRequest = FileServerRequest.parse_binary_request(self.raw_request)
        self.request = request

        requested_function = self.request_to_function_mapping.get(request.code)

        response: FileServerResponse = requested_function()

        return response

    @property
    def request_to_function_mapping(self) -> Dict[int, Callable]:
        return {1100: self.register_user, 1101: self.save_public_key, 1103: self.send_file, 1104: self.valid_crc,
                1105: self.invalid_crc, 1106: self.invalid_crc_terminating}

    @staticmethod
    def init_db():
        with SQLiteDatabase() as db:
            db.init_db(FileServerRequestHandler.BASE_TABLES)

    def register_user(self):
        client_id = self.request.client_id = secrets.token_hex(16)
        client_user_name = self.request.payload[:-1].decode()  # Normalizing the input - removing the trailing NULL-BYTE

        with SQLiteDatabase() as db:
            try:
                db.write(
                    f"INSERT INTO Client(id,name,public_key,last_seen,aes_key) VALUES('{client_id}','{client_user_name}',NULL,NULL,NULL)")
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return FileServerResponse(version=self.request.version, code=RESPONSE_REGISTERATION_FAILED,
                                              payload_size=0,
                                              payload=str())
                    raise UserAlreadyRegistered('User already registered - username is taken')
            except Exception as e:
                print(str(e))

        return FileServerResponse(version=self.request.version, code=RESPONSE_REGISTERED_SUCCESSFULLY, payload_size=16,
                                  payload=client_id)

    def save_public_key(self):
        client_user_name: bytearray = self.request.payload[:255]
        client_user_name: str = client_user_name[0:client_user_name.find(b'\0')].decode()
        public_key = self.request.payload[255:]

        base64_encoded_public_key = b64encode(public_key).decode()
        with SQLiteDatabase() as db:
            db.update(
                f"UPDATE Client SET aes_key = '{base64_encoded_public_key}' WHERE name='{client_user_name}'"
            )
        generated_aes_key = generate_aes_key()

        print(f"generated aes key {generated_aes_key}")
        encrypted_aes_key = rsa_encryption(data=generated_aes_key, public_key=public_key)

        raw_payload = struct.pack(f"16s{len(encrypted_aes_key)}s", self.request.client_id, encrypted_aes_key)
        return FileServerResponse(version=self.request.version, code=RESPONSE_PK_RECIEVED_SENDING_AES_KEY,
                                  payload_size=len(raw_payload),
                                  payload=raw_payload)

    def send_file(self, aes_key):
        headers = struct.unpack('<16sI255s', self.request[:255])
        client_id, content_size, file_name = headers
        message_content = self.request[256:]
        message_content = message_content[:content_size]

        decrypted_file = aes_decryption(aes_key=aes_key, data=message_content)
        return get_crc_sum(decrypted_file)

    def valid_crc(self):
        pass

    def invalid_crc(self):
        pass

    def invalid_crc_terminating(self):
        pass
