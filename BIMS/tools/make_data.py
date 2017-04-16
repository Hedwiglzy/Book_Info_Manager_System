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


def make_book_score(count):
    """
    制造图书收藏数据
    :param count: 次数
    :return:
    """
    for i in range(count):
        user_id = random.randint(100000, 100009)
        book_id = random.randint(10001, 16129)
        score = random.randint(1, 5)
        day = datetime.today().date().day + random.randint(-11, 0)
        create_date = str(datetime.today().date())[:7] + '-' + str(day)
        conn = connect_db()
        cursor = conn.cursor()
        sql = "INSERT INTO BIMS_bookscore (book_id, user_id, score, create_date) VALUES (%d, %d, %d,\'%s\');" % \
              (book_id, user_id, score, create_date)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()


def distinct_score():
    """
    图书打分表数据去重
    """
    conn = connect_db()
    cursor = conn.cursor()
    for user_id in range(100000, 100010):
        sql = "SELECT book_id,count(book_id) FROM BIMS_bookscore WHERE user_id = %d GROUP BY book_id HAVING count(book_id) > 1" % user_id
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        for result in results:
            book_id = result['book_id']
            sql = "SELECT op_id FROM BIMS_bookscore WHERE book_id = %d AND user_id = %d" % (book_id, user_id)
            cursor.execute(sql)
            result_op = cursor.fetchall()
            op_id = result_op[0]['op_id']
            sql = "DELETE from BIMS_bookscore where op_id = %d" % op_id
            cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    distinct_score()
