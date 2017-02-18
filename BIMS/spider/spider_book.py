#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 爬取图书信息"""

import re
from datetime import datetime
from threading import Thread

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


def insert_table(table_name, column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12):
    """
    将数据插入表中
    :param table_name:表名
    :param column1:入表的字段
    :param data1:入表的数据
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'INSERT INTO `%s` (`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`)VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (table_name, column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12)
    print(sql)
    log.write(str(datetime.now()) + '--' + data1 + '正在入表!' + '\n')
    try:
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except pymysql:
        pass


def select_table(table_name, column1, column2, low, high):
    """
    将数据插入表中
    :param table_name:表名
    :param column1:查询的字段1
    :param column2:查询的字段2
    :param low:查询的字段3
    :param high:查询的字段3
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT `%s`,`%s`from `%s` where book_id >=%d AND  book_id<=%d' % (column1, column2, table_name, int(low), int(high))
    print(str(datetime.now()) + '--' + sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
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
        book_name = soup.find_all(property='v:itemreviewed')[0].get_text()
        log.write(str(datetime.now()) + '--' + '正在爬取--' + book_name + '\n')
        print(str(datetime.now()) + '--' + '正在爬取--' + book_name + '\n')
        raw_book_info = soup.find_all(id='info')[0]
        hrefs = raw_book_info.find_all('a')
        info_text = raw_book_info.get_text()
        try:
            press_house = re.findall(r'出版社:([^\n$]+)', info_text)[0].strip()
        except IndexError:
            press_house = '不详'
        try:
            publication_date = re.findall(r'出版年:([^\n$]+)', info_text)[0].strip()
        except IndexError:
            publication_date = '不详'
        try:
            pages = re.findall(r'页数:([^\n$]+)', info_text)[0].strip()
        except IndexError:
            pages = 300
        try:
            price = re.findall(r'定价:([^\n$]+)', info_text)[0].strip()
        except IndexError:
            price = '39.90元'
        try:
            package = re.findall(r'装帧:([^\n$]+)', info_text)[0].strip()
        except IndexError:
            package = '平装'
        try:
            isbn = re.findall(r'ISBN:([^\n$]+)', info_text)[0].strip()
        except IndexError:
            isbn = 9999999999999
        try:
            content_summary = soup.find_all(class_='intro')[0].get_text().strip()
        except IndexError:
            content_summary = '暂无简介'
        book_info = {
            'book_name': book_name,
            'author_name': hrefs[0].get_text(),
            'press_house': press_house,
            'publication_date': publication_date,
            'pages': pages,
            'price': price,
            'package': package,
            'isbn': int(isbn),
            'score': soup.find_all(property='v:average')[0].get_text().strip(),
            'evaluate_num': soup.find_all(href='collections')[0].get_text().strip(),
            'content_summary': content_summary,
        }
        return book_info
    else:
        print('未获取到信息--' + book_url)


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


def start_spider(low, high):
    """
    开始爬取
    :param low:book_id最小(包含)
    :param high:book_id最大(包含)
    """
    book_classes_and_urls = select_table('all_book', 'book_class', 'book_url', low, high)
    for book_class_and_url in book_classes_and_urls:
            book_info = get_book_info(book_class_and_url['book_url'])
            if book_info['evaluate_num'] == '评价人数不足':
                evaluate_num = 10
            else:
                evaluate_num = int(book_info['evaluate_num'][:-3])
            insert_table('bims_book', 'book_name', 'author_name', 'press_house', 'publication_date', 'pages', 'price', 'package', 'isbn', 'score', 'evaluate_num', 'content_summary', 'title', book_info['book_name'], book_info['author_name'], book_info['press_house'], book_info['publication_date'], book_info['pages'], book_info['price'], book_info['package'], book_info['isbn'], book_info['score'], evaluate_num, book_info['content_summary'], book_class_and_url['book_class'])
            log.write(str(datetime.now()) + '--' + book_info['book_name'] + '入表成功!' + '\n')
            print(book_info['book_name'] + '入库成功!')


# 获取图书名及链接 ########################################################################################
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


# # 多线程获取图书信息,并入库##################################################################################
# if __name__ == '__main__':
#     print('go!')
#     THREADS = []
#     with open('./log2.txt', 'a', encoding='utf-8') as log:
#         log.write(str(datetime.now()) + '-- 程序开始' + '\n')
#         t1 = Thread(target=start_spider, args=(0, 1000))
#         THREADS.append(t1)
#         t2 = Thread(target=start_spider, args=(1001, 2000))
#         THREADS.append(t2)
#         t3 = Thread(target=start_spider, args=(2100, 3000))
#         THREADS.append(t3)
#         t4 = Thread(target=start_spider, args=(3001, 4000))
#         THREADS.append(t4)
#         t5 = Thread(target=start_spider, args=(4001, 500))
#         THREADS.append(t5)
#         t6 = Thread(target=start_spider, args=(5001, 6000))
#         THREADS.append(t6)
#         t7 = Thread(target=start_spider, args=(6001, 7000))
#         THREADS.append(t7)
#         t8 = Thread(target=start_spider, args=(7001, 8000))
#         THREADS.append(t8)
#         t9 = Thread(target=start_spider, args=(8001, 9000))
#         THREADS.append(t9)
#         t10 = Thread(target=start_spider, args=(9001, 10000))
#         THREADS.append(t10)
#         t11 = Thread(target=start_spider, args=(10001, 11000))
#         THREADS.append(t11)
#         t12 = Thread(target=start_spider, args=(11001, 12000))
#         THREADS.append(t12)
#         t13 = Thread(target=start_spider, args=(12001, 13000))
#         THREADS.append(t13)
#         t14 = Thread(target=start_spider, args=(13001, 14000))
#         THREADS.append(t14)
#         t15 = Thread(target=start_spider, args=(14001, 15000))
#         THREADS.append(t15)
#         t16 = Thread(target=start_spider, args=(15001, 16000))
#         THREADS.append(t16)
#         t17 = Thread(target=start_spider, args=(16001, 17000))
#         THREADS.append(t17)
#         t18 = Thread(target=start_spider, args=(17001, 18000))
#         THREADS.append(t18)
#         t19 = Thread(target=start_spider, args=(18001, 19000))
#         THREADS.append(t19)
#         t20 = Thread(target=start_spider, args=(19001, 20235))
#         THREADS.append(t20)
#         for THR in THREADS:
#             THR.setDaemon(True)
#             THR.start()
#         t20.join()
#     print('程序运行完成!')


# # 获取图书信息测试#########################################################################################
# if __name__ == '__main__':
#     with open('./log2.txt', 'a', encoding='utf-8') as log:
#         BOOK_INFO = get_book_info('https://book.douban.com/subject/26148066/')
#         print(BOOK_INFO)

# 将文件入表
if __name__ == '__main__':
    with open('./all_book.csv', 'r', encoding='utf-8') as data_source:
        for line in data_source:
            data = line.split(',')
            conn = connect_db()
            cursor = conn.cursor()
            sql = 'INSERT INTO `%s`VALUES (%d,\'%s\',\'%s\',\'%s\')' % ('all_book', int(data[0]), data[1], data[2], data[3])
            print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.close()

