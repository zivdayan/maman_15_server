class Client:
    def __init__(self, id, name, public_key, last_seen, aes_key):
        self.id = id
        self.name = name
        self.public_key = public_key
        self.last_seen = last_seen
        self.aes_key = aes_key

    @staticmethod
    def sql_columns_description():
        return """
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        public_key TEXT NOT NULL,
        last_seen DATE NOT NULL UNIQUE,
        aes_key TEXT NOT NULL UNIQUE
        """
