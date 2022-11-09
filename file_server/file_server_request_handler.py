from structures.file import File
from structures.client import Client

from structures.request import FileServerRequest, InvalidRequest, UserAlreadyRegistered
from structures.response import FileServerResponse
from structures.consts import *

from typing import Callable, Dict
from sqlite_dal import SQLiteDatabase
from datetime import datetime
from sqlite3 import IntegrityError
import binascii
import secrets

from crypto.utils import *
from base64 import b64encode
import struct

clients = list()


class FileServerRequestHandler:
    BASE_TABLES = {f"{c.__name__}": c.SQL_COLUMNS_DESCRIPTION for c in [File, Client]}
    DUMMY_INVALID_CRC = 0

    def __init__(self, raw_request):
        self.raw_request = raw_request
        self.request: FileServerRequest = None
        self.init_db()

    def handle(self) -> FileServerResponse:
        request: FileServerRequest = FileServerRequest.parse_binary_request(self.raw_request)
        self.request = request
        if self.request.code is not REQUEST_REGISTER_CODE:
            self.update_last_seen()
        requested_function = self.request_to_function_mapping.get(request.code)

        response: FileServerResponse = requested_function()

        return response

    def update_last_seen(self):
        with SQLiteDatabase() as db:
            db.update(
                "UPDATE Client SET last_seen = ? WHERE id=?", datetime.now(), binascii.hexlify(self.request.client_id)
            )

    @property
    def request_to_function_mapping(self) -> Dict[int, Callable]:
        return {1100: self.register_user, 1101: self.save_public_key, 1103: self.send_file, 1104: self.valid_crc,
                1105: self.invalid_crc, 1106: self.invalid_crc_terminating}

    @staticmethod
    def init_db():
        with SQLiteDatabase() as db:
            db.init_db(FileServerRequestHandler.BASE_TABLES)

    def register_user(self):
        global clients

        client_id = self.request.client_id = binascii.unhexlify(secrets.token_hex(16))
        client_user_name = self.request.payload[:-1].decode()  # Normalizing the input - removing the trailing NULL-BYTE

        with SQLiteDatabase() as db:
            try:
                db.write(
                    f"INSERT INTO Client(id,name,public_key,last_seen,aes_key) VALUES(?,?,NULL,NULL,NULL)",
                    binascii.hexlify(client_id), client_user_name)
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    return FileServerResponse(version=self.request.version, code=RESPONSE_REGISTERATION_FAILED,
                                              payload_size=0,
                                              payload=str())
                    raise UserAlreadyRegistered('User already registered - username is taken')
            except Exception as e:
                return FileServerResponse(version=self.request.version, code=RESPONSE_REGISTERATION_FAILED,
                                          payload_size=0,
                                          payload=None)

        clients.append(Client(client_id, client_user_name, None, datetime.now(), None))

        return FileServerResponse(version=self.request.version, code=RESPONSE_REGISTERED_SUCCESSFULLY, payload_size=16,
                                  payload=client_id)

    def save_public_key(self):
        global clients

        client_user_name: bytearray = self.request.payload[:255]
        client_user_name: str = client_user_name[0:client_user_name.find(b'\0')].decode()
        public_key = self.request.payload[255:]

        base64_encoded_public_key = b64encode(public_key).decode()

        generated_aes_key = generate_aes_key()
        client = [client for client in clients if client.id == self.request.client_id][0]
        client.aes_key = generated_aes_key

        base64_encoded_aes_key = b64encode(generated_aes_key).decode()

        with SQLiteDatabase() as db:
            db.update(
                "UPDATE Client SET public_key = ? WHERE name=?", base64_encoded_public_key, client_user_name
            )
            db.update(
                "UPDATE Client SET aes_key = ? WHERE name=?", base64_encoded_aes_key, client_user_name
            )

        print(f"generated aes key {generated_aes_key}")
        encrypted_aes_key = rsa_encryption(data=generated_aes_key, public_key=public_key)

        raw_payload = struct.pack(f"16s{len(encrypted_aes_key)}s", self.request.client_id, encrypted_aes_key)
        return FileServerResponse(version=self.request.version, code=RESPONSE_PK_RECIEVED_SENDING_AES_KEY,
                                  payload_size=len(raw_payload),
                                  payload=raw_payload)

    def send_file(self):
        global clients
        try:
            total_payload_headers_size = 275
            headers = struct.unpack('<16sI255s', self.request.payload[:total_payload_headers_size])
            client_id, content_size, file_name = headers

            message_content = self.request.payload[total_payload_headers_size:]
            client = [client for client in clients if client.id == self.request.client_id][0]
            decrypted_file = aes_decryption(aes_key=client.aes_key, data=message_content)

            payload = struct.pack('<16sI255sI', client_id, content_size, file_name, get_crc_sum(decrypted_file))

        except Exception as e:
            print(e)
            dummy_payload = struct.pack('<16sI255sI', client_id, content_size, file_name, self.DUMMY_INVALID_CRC)
            payload = dummy_payload

        return FileServerResponse(version=self.request.version, code=RESPONSE_VALID_FILE_RECV_CRC,
                                  payload_size=len(payload), payload=payload)

    def valid_crc(self):
        return FileServerResponse(version=self.request.version, code=RESPONSE_RECIEVED_ACK,
                                  payload_size=0, payload=None)

    def invalid_crc(self):
        return FileServerResponse(version=self.request.version, code=RESPONSE_RECIEVED_ACK,
                                  payload_size=0, payload=None)

    def invalid_crc_terminating(self):
        return FileServerResponse(version=self.request.version, code=RESPONSE_RECIEVED_ACK,
                                  payload_size=0, payload=None)
