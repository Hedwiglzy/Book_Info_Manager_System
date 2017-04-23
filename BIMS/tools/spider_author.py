#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 爬取作者信息 """


import pymysql
import requests
import time
from bs4 import BeautifulSoup


__pyname__ = 'spider_author'
__author__ = 'Hedwig'
__date__ = '2017/4/23'


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
    cursor.execute("select `book_url` from all_book")
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def spider_author(book_url, headers):
    web_data = requests.get(book_url, headers=headers)
    print(web_data.status_code)
    soup = BeautifulSoup(web_data.text, 'lxml')
    raw_book_info = soup.find_all(id='info')[0]
    hrefs = raw_book_info.find_all('a')
    try:
        author_name = hrefs[0].get_text().strip()
        author_name = ''.join(author_name.split())
    except IndexError:
        author_name = '佚名'
    try:
        author_summary = soup.find_all(class_='intro')[1].get_text().strip()
    except BaseException:
        author_summary = '暂无简介'
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'INSERT INTO `all_author`(author_name,author_summary)VALUES (\'%s\',\'%s\')' % (author_name, author_summary.replace("'", "\\'"))
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()


print('go!')
index = int(input('输入起始编号:'))
book_infos = select_table()
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Cookie': 'bid=E4Idlx5piXA'
    }
for i, book_info in enumerate(book_infos):
    if i >= index-1:
        book_url = book_info['book_url'].rstrip()
        spider_author(book_url, headers)
        time.sleep(0.5)
print('end')
