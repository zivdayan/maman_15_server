from structures.file import File
from structures.client import Client

from structures.request import FileServerRequest, InvalidRequest, UserAlreadyRegistered
from typing import Callable, Dict
from sqlite_dal import SQLiteDatabase

from sqlite3 import IntegrityError

import secrets

from crypto.utils import *


class FileServerRequestHandler:
    BASE_TABLES = {f"{c.__name__}": c.SQL_COLUMNS_DESCRIPTION for c in [File, Client]}

    def __init__(self, raw_request):
        self.raw_request = raw_request
        self.request: FileServerRequest = None

    def handle(self):
        request: FileServerRequest = FileServerRequest.parse_binary_request(self.raw_request)
        self.request = request

        requested_function = self.request_to_function_mapping.get(request.code)

        requested_function()

    @property
    def request_to_function_mapping(self) -> Dict[int, Callable]:
        return {1100: self.register_user, 1101: self.send_public_key, 1103: self.send_file, 1104: self.valid_crc,
                1105: self.invalid_crc, 1106: self.invalid_crc_terminating}

    @staticmethod
    def init_db():
        with SQLiteDatabase() as db:
            db.init_db(FileServerRequestHandler.BASE_TABLES)

    def register_user(self):
        client_id = self.request.client_id = secrets.token_hex(16)
        client_user_name = self.request.payload

        with SQLiteDatabase() as db:
            try:
                db.write(
                    f"INSERT INTO Client(id,name,public_key,last_seen,aes_key) VALUES('{client_id}','{client_user_name}',NULL,NULL,NULL)")
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    raise UserAlreadyRegistered('User already registered - username is taken')

    def save_public_key(self):
        client_user_name = self.request.payload[:255]
        public_key = self.request.payload[255:]

        with SQLiteDatabase() as db:
            db.update(
                f"UPDATE Clients SET aes_key = '{public_key}' WHERE name={client_user_name}"
            )

        return rsa_encryption(data=generate_aes_key(), public_key=public_key)

    def send_file(self):
        pass

    def valid_crc(self):
        pass

    def invalid_crc(self):
        pass

    def invalid_crc_terminating(self):
        pass
