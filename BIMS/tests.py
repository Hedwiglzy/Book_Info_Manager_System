#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试
"""
import pandas
import pymysql
import plotly
from plotly.graph_objs import Scatter, Layout


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


def select_table():
    """
    从表里面选择数据
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('select * from `bims_user`')
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


RESULTS = select_table()
INFO = pandas.DataFrame([result for result in RESULTS])
print(INFO)
plotly.offline.plot({
    "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": Layout(title="hello world")
})
