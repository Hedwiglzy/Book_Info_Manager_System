#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 爬取图书信息"""

import re

import pymysql
import requests
from bs4 import BeautifulSoup

__pyname__ = 'spider_book.py'
__author__ = 'Hedwig'
__date__ = '2017/2/9'


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


def insert_table(table_name, data1, data2, data3):
    """
    将数据插入表中
    :param table_name:表名
    :param data1:入表的数据1
    :param data2:入表的数据2
    :param data3:入表的数据3
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'INSERT INTO `%s`VALUES (\'%s\',\'%s\',\'%s\')' % (table_name, data1, data2, data3)
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except pymysql:
        pass


def truncate_table(table_name):
    """
    清空表
    :param table_name: 表名
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'TRUNCATE TABLE `%s`' % table_name
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_title_urls():
    """
    获取分类名称、链接
    :return:分类名称、链接(list)
    """
    title_urls = []
    douban_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    web_data = requests.get(douban_url)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    tags = soup.find_all(href=re.compile(r'tag'))
    tags.pop(0)
    tags.pop(0)
    counts = soup.find_all('b')
    for tag, count in zip(tags, counts):
        title_and_url = {
            'title': tag.get_text(),
            'url': 'https://book.douban.com' + tag.get('href')
        }
        title_urls.append(title_and_url)
    return title_urls


def get_book_urls(title_url):
    """
    获取某分类所有图书的名称和链接
    :param title_url:分类的链接
    :return:图书名称和链接(list)
    """
    book_urls = []
    full_title_urls = [title_url+'?start={}&type=T'.format(str(title_page*20)) for title_page in range(50)]
    for full_title_url in full_title_urls:
        request_code = requests.get(full_title_url).status_code
        if request_code == 200:
            web_data = requests.get(full_title_url)
            web_data.encoding = 'utf-8'
            soup = BeautifulSoup(web_data.text, 'lxml')
            tags = soup.find_all(class_='info')
            for tag in tags:
                name_and_url = {
                    'name': tag.a.get('title'),
                    'url': tag.a.get('href')
                }
                book_urls.append(name_and_url)
        else:
            continue
    return book_urls

if __name__ == '__main__':
    print('go!')
    # TITLE_URLS = [{'title': 'UCD', 'url': 'https://book.douban.com/tag/UCD'}]
    TITLE_URLS = get_title_urls()
    for TITLE_URL in TITLE_URLS:
        BOOK_URLS = get_book_urls(TITLE_URL['url'])
        for BOOK_URL in BOOK_URLS:
            if re.search("'", BOOK_URL['name']):
                continue
            else:
                insert_table('all_book', TITLE_URL['title'], BOOK_URL['name'], BOOK_URL['url'])
    print('运行完成!')
