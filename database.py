import psycopg2
import os
from psycopg2.extras import RealDictCursor


class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            DATABASE_URL = os.environ['DATABASE_URL']
            cls.__instance.conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        return cls.__instance

    def get_cred(self, chat_id):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM auth WHERE chat_id = %s", (str(chat_id),))
        return cursor.fetchall()[0]

    def is_auth(self, chat_id):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT chat_id FROM auth WHERE chat_id = %s", (str(chat_id),))
        if cursor.fetchone() is not None:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    def delete_cred(self, chat_id):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("DELETE FROM auth WHERE chat_id = %s", (str(chat_id),))
        self.conn.commit()
        cursor.close()
