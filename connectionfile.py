from pymysql import *

class connection:
    def connection(self):
        conn = Connect('localhost', 'root', '', 'onlineshopping_db')
        return conn