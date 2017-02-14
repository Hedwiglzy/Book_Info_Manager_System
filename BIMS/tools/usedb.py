#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 操作Mysql数据库"""

import pymysql

__pyname__ = 'usedb'
__author__ = 'Hedwig'
__date__ = '2017/2/14'


def connect_db(db_name, username, password):
    """
    连接数据库
    :param db_name:数据库名称
    :param username:连接数据库用户名称
    :param password:连接数据库用户密码
    :return:数据库连接
    """
    connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user=username,
            password=password,
            db=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
    )
    return connection


# def insert_table(table_name, **kwargs):
#     """
#     将数据插入表中
#     :param table_name:表名
#     :param kwargs
#     """
#     conn = connect_db()
#     cursor = conn.cursor()
#     columns = '`' + '`,`'.join(kwargs['columns']) + '`'
#     datas = "\'" + "\',\'".join(kwargs['datas']) + "\'"
#     sql = 'INSERT INTO `%s` (%s)VALUES (%s)' % (table_name, columns, datas)
#     try:
#         cursor.execute(sql)
#         conn.commit()
#         conn.close()
#     except pymysql:
#         pass

def insert_table(table_name, **kwargs):
    db_name = kwargs['db_name']
    # username = kwargs['username']
    # password = kwargs['password']
    print(db_name)
    print(table_name)

insert_table('book',db_name='haha')