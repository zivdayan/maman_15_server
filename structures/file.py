class File:
    def __init__(self, id, file_name, path_name, verified):
        self.id = id
        self.file_name = file_name
        self.path_name = path_name
        self.verified = verified

    @staticmethod
    def sql_columns_description():
        return """
        id TEXT PRIMARY KEY,
        file_name TEXT NOT NULL,
        path_name TEXT NOT NULL,
        verified INTEGER NOT NULL UNIQUE,
        """
