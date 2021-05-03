import sqlite3

class DB(object):
    """sqlite3 database class that holds testers jobs"""
    address = r'../mydatabase.db'

    def __init__(self):
        self.connection = sqlite3.connect(address)
        self.cur = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def close(self):
        self.connection.close()

    def create_table():
        self.cursor.execute('create table if not exists user (username, password)') 
   
    def create_files_table(self):
        self.cursor.execute('create table if not exists files (user_id, file_id, text, sentiment)')

    def create_news_table(self):
        self.cursor.execute('create table if not exists news (user_id, id INTEGER PRIMARY KEY, keyword, title, url, content, sentiment)')

    def execute(self, new_data):
        self.cur.execute(new_data)

    def get_files(self):
        files_records = self.cursor.execute('select file_id from files where user_id=?', (username,)).fetchall()
        return files_records
    
    def get_news(self):
        news_records = self.cursor.execute('select id, title from news where user_id=?', (username,)).fetchall()
        return news_records

    def commit(self):
        self.connection.commit()