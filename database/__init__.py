# -*- coding: utf-8 -*-
from playhouse.db_url import connect

# 连接
def create_dsn():
    conn = connect("mysql://%s:%s@%s:%s/%s" % ('user','password','host','port','db_name'))
    return conn

if __name__ == '__main__':
    print(create_dsn())