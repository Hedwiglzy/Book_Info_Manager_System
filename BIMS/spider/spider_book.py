#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 爬取图书信息"""

import re
from datetime import datetime

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


def insert_table(table_name, column1, column2, column3, data1, data2, data3):
    """
    将数据插入表中
    :param table_name:表名
    :param column1:入表的字段1
    :param column2:入表的字段2
    :param column3:入表的字段3
    :param data1:入表的数据1
    :param data2:入表的数据2
    :param data3:入表的数据3
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'INSERT INTO `%s` (`%s`,`%s`,`%s`)VALUES (\'%s\',\'%s\',\'%s\')' % (table_name, column1, column2, column3, data1, data2, data3)
    print(sql)
    #  log.write(str(datetime.now()) + '--' + column2 + '正在入表!' + '\n')
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': 'bid=JDkJwopchqY; gr_user_id=2a50a37c-f1e0-4d56-b15c-3b49dd29e51f; ll="118123"; viewed="2158192_1059419"; _ga=GA1.2.1895736562.1482849878; ue="1432659378@qq.com"; dbcl2="83764412:dFc8oOuogsw"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1486902016%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSjdO3k-NOKHE_oRvb8kkXA27TjX3Q7itKW4FMK9pF_ZUgu35vi253z--E7jf7vJs%26wd%3D%26eqid%3Da832a71b00411b090000000358a052fa%22%5D; _pk_id.100001.8cb4=00429bbc98989df1.1482849877.19.1486902016.1486730024.; ct=y; ck=-y1h; _vwo_uuid_v2=2444B6545FEA6C4CBA6360C8DCC21CAF|4d0717074c01a40d50a1ea48f9482e2d; ap=1; __utmt_douban=1; push_doumail_num=0; __utma=30149280.1895736562.1482849878.1486985237.1486987766.47; __utmb=30149280.2.10.1486987766; __utmc=30149280; __utmz=30149280.1486730025.41.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.8376; push_noty_num=0'
    }
    web_data = requests.get(douban_url, headers=headers)
    if web_data.status_code == 200:
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')
        tags = soup.find_all(href=re.compile(r'tag'))
        tags.pop(0)
        tags.pop(0)
        for tag in tags:
            title_and_url = {
                'title': tag.get_text(),
                'url': 'https://book.douban.com' + tag.get('href')
            }
            title_urls.append(title_and_url)
        return title_urls
    else:
        print('请求失败!')


def get_book_info(book_url):
    """
    获取图书信息
    :param book_url:图书链接
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': 'bid=JDkJwopchqY; gr_user_id=2a50a37c-f1e0-4d56-b15c-3b49dd29e51f; ll="118123"; viewed="2158192_1059419"; _ga=GA1.2.1895736562.1482849878; ue="1432659378@qq.com"; dbcl2="83764412:dFc8oOuogsw"; ct=y; ap=1; ck=-y1h; __utmt_douban=1; __utma=30149280.1895736562.1482849878.1486998452.1487161093.49; __utmb=30149280.7.10.1487161093; __utmc=30149280; __utmz=30149280.1486730025.41.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.8376; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=2444B6545FEA6C4CBA6360C8DCC21CAF|4d0717074c01a40d50a1ea48f9482e2d; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=45072aed-d767-45f5-b7bb-5ce14081ee8a; gr_cs1_45072aed-d767-45f5-b7bb-5ce14081ee8a=user_id%3A1'
    }
    web_data = requests.get(book_url, headers=headers)
    if web_data.status_code == 200:
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')
        raw_book_info = soup.find_all(id='info')[0]
        hrefs = raw_book_info.find_all('a')
        info_text = raw_book_info.get_text()
        book_info = {
            'book_name': soup.find_all(property='v:itemreviewed')[0].get_text(),
            'author_name': hrefs[0].get_text(),
            'press_house': re.findall(r'出版社:([^\n$]+)', info_text)[0].strip(),
            'publication_date': re.findall(r'出版年:([^\n$]+)', info_text)[0].strip(),
            'pages': re.findall(r'页数:([^\n$]+)', info_text)[0].strip(),
            'price': re.findall(r'定价:([^\n$]+)', info_text)[0].strip(),
            'package': re.findall(r'装帧:([^\n$]+)', info_text)[0].strip(),
            'isbn': re.findall(r'ISBN:([^\n$]+)', info_text)[0].strip(),
        }
        print(book_info)


def get_book_urls(title_url):
    """
    获取某分类所有图书的名称和链接
    :param title_url:分类的链接
    :return:图书名称和链接(list)
    """
    book_urls = []
    full_title_urls = [title_url + '?start={}&type=T'.format(str(title_page * 20)) for title_page in range(50)]
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

# if __name__ == '__main__':
#     print('go!')
#     with open('./log.txt', 'a', encoding='utf-8') as log:
#         log.write(str(datetime.now()) + '-- 程序开始' + '\n')
#         TITLE_URLS = get_title_urls()
#         for TITLE_URL in TITLE_URLS:
#             LOG = '正在爬取' + TITLE_URL['title'] + '类的图书链接' + '\n'
#             log.write(str(datetime.now()) + '--' + LOG)
#             print(LOG)
#             BOOK_URLS = get_book_urls(TITLE_URL['url'])
#             for BOOK_URL in BOOK_URLS:
#                 if re.search("'", BOOK_URL['name']):
#                     continue
#                 else:
#                     insert_table('all_book_temp', 'book_class', 'book_name', 'book_url', TITLE_URL['title'], BOOK_URL['name'], BOOK_URL['url'])
#     print('运行完成!')

if __name__ == '__main__':
    get_book_info('https://book.douban.com/subject/1770782/')
