import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.params = {
            'host': "",
            'port': "",
            'database': "",
            'user': "",
            'password': "",
        }
        self.connection = psycopg2.connect(**self.params)

    def execute(self, query):
        response = None
        if query:
            try:
                cur = self.connection.cursor()
                cur.execute(query)
                response = cur.fetchall()
            except(Exception, psycopg2.Error) as error:
                pass
        return response

DB = Database()