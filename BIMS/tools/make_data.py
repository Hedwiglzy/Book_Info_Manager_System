#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 造数据 """

import pymysql
import random
from datetime import datetime

__pyname__ = 'make_data'
__author__ = 'Hedwig'
__date__ = '2017/3/22'


def connect_db():
    """
    连接数据库
    """
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='qwer1234',
        db='BIMS',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def make_book_collection(count):
    """
    制造图书收藏数据
    :param count: 次数
    :return:
    """
    for i in range(count):
        user_id = random.randint(100000, 100009)
        book_id = random.randint(10001, 16129)
        day = datetime.today().date().day + random.randint(-11, 0)
        create_date = str(datetime.today().date())[:7] + '-' + str(day)
        conn = connect_db()
        cursor = conn.cursor()
        sql = "INSERT INTO `bims_collectionbook` (`user_id`, `book_id`, `create_date`) VALUES (%d, %d,\'%s\');" % \
              (user_id, book_id, create_date)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()

if __name__ == '__main__':
    make_book_collection(5000)
