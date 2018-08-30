"""
MIT License

Copyright (c) 2018 Aaron Michael Scott

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import sqlite3
from sqlite3 import Error


class SQLConnection(object):

    def __init__(self, db_location):
        self.db_location = db_location
        self.conn = sqlite3.connect(self.db_location)
        self.conn.row_factory = sqlite3.Row
        return
    

    def connection(func):
        def inner(self, *args):
            try:
                return func(self, *args)
            except Error as e:
                raise(e)
        return inner
    
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    @connection
    def iterate_records(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        for row in cursor:
            if len(row) > 0:
                record_dict = {column: value for column, value in zip(row.keys(), row)}
                yield SQLRecord(record_dict)

    
    @connection
    def return_all_records(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        results_list = []
        for row in results:
            record_dict = {column: value for column, value in zip(row.keys(), row)}
            results_list.append(SQLRecord(record_dict))
        return results_list
        
    @connection
    def perform_raw_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    @connection
    def perform_raw_sql(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)

    @connection
    def load_records(self, table, records=[]):
        cursor = self.conn.cursor()
        columns = ', '.join('?' * len(records[0]))
        command = 'insert into {table} values ({columns})'.format(table=table,
                                                                  columns=columns)
        cursor.executemany(command, records)
        self.conn.commit()




class SQLRecord(object):
    def __init__(self, fields):
        self.__dict__ = fields






def connect(db_location):
    conn = SQLConnection(db_location)
    return conn
