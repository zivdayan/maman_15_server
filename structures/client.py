class Client:
    SQL_COLUMNS_DESCRIPTION = """
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        public_key TEXT,
        last_seen DATE,
        aes_key TEXT
        """

    def __init__(self, id, name, public_key, last_seen, aes_key):
        self.id = id
        self.name = name
        self.public_key = public_key
        self.last_seen = last_seen
        self.aes_key = aes_key
