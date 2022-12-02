QUERY_UPDATE_PK_BY_NAME = 'UPDATE Client SET public_key = ? WHERE name=?'
QUERY_UPDATE_AES_KEY_BY_NAME='UPDATE Client SET aes_key = ? WHERE name=?'
ID_NOT_UNIQUE_ERROR = 'UNIQUE constraint failed'
QUERY_UPDATE_LAST_SEEN = 'UPDATE Client SET last_seen = ? WHERE id=?'
INSERT_NEW_USER = "INSERT INTO Client(id,name,public_key,last_seen,aes_key) VALUES(?,?,NULL,NULL,NULL)"