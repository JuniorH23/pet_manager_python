import os

import mysql.connector


class DbData:
    def __init__(self):
        self.host = os.getenv("PETMANAGER_DB_HOST", "127.0.0.1")
        self.port = int(os.getenv("PETMANAGER_DB_PORT", "3306"))
        self.user = os.getenv("PETMANAGER_DB_USER", "root")
        self.password = os.getenv("PETMANAGER_DB_PASSWORD", "")
        self.database = os.getenv("PETMANAGER_DB_NAME", "administracionmascotasbd")

    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            connection_timeout=5,
        )
