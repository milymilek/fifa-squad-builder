import config
from src.SingletonMeta import SingletonMeta

import mysql.connector

class DBHandler(metaclass=SingletonMeta):
    def __init__(self):
        self.db = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT,
            database=config.DB_DATABASE
        )

    def query_return(self, q):
        cursor = self.db.cursor()
        cursor.execute(q)
        return cursor.fetchall()
