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
    sql = 'INSERT INTO `%s` (`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`)VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (
        table_name, column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12)
    print(sql)
    log.write(str(datetime.now()) + '--' + data1 + '正在入表!' + '\n')
    try:
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except BaseException:
        pass


def select_table(table_name, column1, column2, low, high):
    """
    从表里面选择数据
    :param table_name:表名
    :param column1:查询的字段1
    :param column2:查询的字段2
    :param low:查询的字段3
    :param high:查询的字段3
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT `%s`,`%s`from `%s` where book_id >=%d AND  book_id<=%d' % (
        column1, column2, table_name, int(low), int(high))
    print(str(datetime.now()) + '--' + sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    except BaseException:
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
        'Cookie': 'bid=JDkJwopchqY; gr_user_id=2a50a37c-f1e0-4d56-b15c-3b49dd29e51f; ll="118123"; viewed="2158192_1059419"; _ga=GA1.2.1895736562.1482849878; ue="1432659378@qq.com"; dbcl2="83764412:dFc8oOuogsw"_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1486902016%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSjdO3k-NOKHE_oRvb8kkXA27TjX3Q7itKW4FMK9pF_ZUgu35vi253z--E7jf7vJs%26wd%3D%26eqid%3Da832a71b00411b090000000358a052fa%22%5D; _pk_id.100001.8cb4=00429bbc98989df1.1482849877.19.1486902016.1486730024.; ct=y; ck=-y1h; _vwo_uuid_v2=2444B6545FEA6C4CBA6360C8DCC21CAF|4d0717074c01a40d50a1ea48f9482e2d; ap=1; __utmt_douban=1; push_doumail_num=0; __utma=30149280.1895736562.1482849878.1486985237.1486987766.47; __utmb=30149280.2.10.1486987766; __utmc=30149280; __utmz=30149280.1486730025.41.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.8376; push_noty_num=0'
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
        'Cookie': 'guid=74056395b89f9cd12f461b7d6a60c85a; plt_PLT_oauth_7_last_key=KUU9cgM84o0FxSnbT1%2BDfgZl8po%2F4i9W7XfwepjWohaMAdKGNcZONJZVLIUK9EDO9u%2F9bzwq6MT%2FXP%2BchHolPE7Auow%2Fn5yGBU350nfBbMozSa1PlTYfk%2FuOQOBXy%2Fi72t0H%2F6DUn0UlznfuZ%2BzF0PhpNib7KIHtXfabkwG%2FeObbaDzoNmH2XTe6KlWzTadjOs0Qnfz%2BWDdVuruFe3%2F5MZOsR%2BxgiOL0J0BjK74BBuRtdV2pTbpCJoZO2v6jBWcbroU5xi2jNePTNs2I7bKPWhS5DFL0y20tZ62C9PuY8fI%3D; addFavor=1; Hm_lvt_7705e8554135f4d7b42e62562322b3ad=1479544357,1479545127; __utma=188916852.669699889.1461046276.1469275819.1479544357.6; __utmz=188916852.1479544357.6.3.utmcsr=item.jd.com|utmccn=(referral)|utmcmd=referral|utmcct=/173134.html; from_device=chrome; plt_subsite_id=3'
    }
    web_data = requests.get(book_url, headers=headers)
    status = {
        100: '继续',
        101: '转换协议',
        102: '继续处理',
        200: '请求成功',
        201: '请求完成',
        202: '请求被接受',
        204: '服务器端已经实现了请求',
        300: '该状态码不被HTTP/1.0的应用程序直接使用',
        301: '请求到的资源都会分配一个永久的URL',
        302: '请求到的资源在一个不同的URL处临时保存',
        304: '请求的资源未更新',
        400: '非法请求',
        401: '未授权',
        403: '禁止',
        404: '没有找到页面',
        500: '服务器内部错误',
        501: '服务器无法识别',
        502: '错误网关',
        503: '服务出错',
    }
    print(str(web_data.status_code) + '--' + status[web_data.status_code])
    if web_data.status_code == 200:
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'lxml')
        book_name = soup.find_all(property='v:itemreviewed')[0].get_text()
        print(str(datetime.now()) + '--' + '正在爬取--' + book_name + '\n')
        log.write(str(datetime.now()) + '--' + '正在爬取--' + book_name + '\n')
        raw_book_info = soup.find_all(id='info')[0]
        hrefs = raw_book_info.find_all('a')
        info_text = raw_book_info.get_text()
        try:
            author_name = hrefs[0].get_text()
        except IndexError:
            author_name = '佚名'
        try:
            press_house = re.findall(r'出版社:([^\n$]+)', info_text)[0].strip()
        except IndexError:
            press_house = '不详'
        try:
            publication_date = re.findall(
                r'出版年:([^\n$]+)', info_text)[0].strip()
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
            content_summary = soup.find_all(class_='intro')[
                0].get_text().strip()
        except IndexError:
            content_summary = '暂无简介'
        book_info = {
            'book_name': book_name,
            'author_name': author_name,
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
        get_info_fail = {'book_name': 'get_info_fail'}
        print('未获取到信息--' + book_url)
        return get_info_fail


def get_book_urls(title_url):
    """
    获取某分类所有图书的名称和链接
    :param title_url:分类的链接
    :return:图书名称和链接(list)
    """
    book_urls = []
    full_title_urls = [
        title_url + '?start={}&type=T'.format(str(title_page * 20)) for title_page in range(50)]
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
    book_classes_and_urls = select_table(
        'all_book', 'book_class', 'book_url', low, high)
    for book_class_and_url in book_classes_and_urls:
        book_info = get_book_info(book_class_and_url['book_url'])
        if book_info['book_name'] == 'get_info_fail':
            continue
        else:
            if book_info['evaluate_num'] == '评价人数不足':
                evaluate_num = 10
            else:
                evaluate_num = int(book_info['evaluate_num'][:-3])
            if len(book_info['score']) == 0:
                score = 0
            else:
                score = book_info['score']
            content_summary = re.sub("'", '"', book_info['content_summary'])
            insert_table('bims_book', 'book_name', 'author_name', 'press_house', 'publication_date', 'pages', 'price', 'package', 'isbn', 'score', 'evaluate_num', 'content_summary', 'title', book_info['book_name'], book_info['author_name'], book_info['press_house'], book_info['publication_date'], book_info['pages'], book_info['price'], book_info['package'], book_info['isbn'], score, evaluate_num, content_summary, book_class_and_url['book_class'])
            log.write(str(datetime.now()) + '--' +
                      book_info['book_name'] + '入库成功!' + '\n')
            print(book_info['book_name'] + '入库成功!')


def main_csv_to_table():
    """
    文件入表main函数 直接运行
    """
    with open('./all_book.csv', 'r', encoding='utf-8') as data_source:
        for line in data_source:
            data = line.split(',')
            conn = connect_db()
            cursor = conn.cursor()
            sql = 'INSERT INTO `%s`VALUES (%d,\'%s\',\'%s\',\'%s\')' % (
                'all_book', int(data[0]), data[1], data[2], data[3])
            print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.close()


def main_get_bookname_and_url():
    """
    获取图书名及链接 main函数 直接运行
    """
    title_urls = get_title_urls()
    for title_url in title_urls:
        log_info = '正在爬取' + title_url['title'] + '类的图书链接' + '\n'
        log.write(str(datetime.now()) + '--' + log_info)
        print(log_info)
        book_urls = get_book_urls(title_url['url'])
        for book_url in book_urls:
            if re.search("'", book_url['name']):
                continue
            else:
                insert_table('all_book_temp', 'book_class', 'book_name', 'book_url', title_url['title'], book_url['name'], book_url['url'])
    print('运行完成!')


def main_get_book_info_test(book_url):
    """
    获取图书信息测试 main函数 直接运行
    :param book_url:图书链接
    """
    book_info = get_book_info(book_url)
    print(book_info)
    print('运行完成!')


def main_multithreading_spider():
    """
    多线程获取图书信息,并入库 main函数 直接运行
    """
    threads = []
    thread1 = Thread(target=start_spider, args=(0, 1000))
    threads.append(thread1)
    thread2 = Thread(target=start_spider, args=(1001, 2000))
    threads.append(thread2)
    thread3 = Thread(target=start_spider, args=(2100, 3000))
    threads.append(thread3)
    thread4 = Thread(target=start_spider, args=(3001, 4000))
    threads.append(thread4)
    thread5 = Thread(target=start_spider, args=(4001, 500))
    threads.append(thread5)
    thread6 = Thread(target=start_spider, args=(5001, 6000))
    threads.append(thread6)
    thread7 = Thread(target=start_spider, args=(6001, 7000))
    threads.append(thread7)
    thread8 = Thread(target=start_spider, args=(7001, 8000))
    threads.append(thread8)
    thread9 = Thread(target=start_spider, args=(8001, 9000))
    threads.append(thread9)
    thread10 = Thread(target=start_spider, args=(9001, 10000))
    threads.append(thread10)
    thread11 = Thread(target=start_spider, args=(10001, 11000))
    threads.append(thread11)
    thread12 = Thread(target=start_spider, args=(11001, 12000))
    threads.append(thread12)
    thread13 = Thread(target=start_spider, args=(12001, 13000))
    threads.append(thread13)
    thread14 = Thread(target=start_spider, args=(13001, 14000))
    threads.append(thread14)
    thread15 = Thread(target=start_spider, args=(14001, 15000))
    threads.append(thread15)
    thread16 = Thread(target=start_spider, args=(15001, 16000))
    threads.append(thread16)
    thread17 = Thread(target=start_spider, args=(16001, 17000))
    threads.append(thread17)
    thread18 = Thread(target=start_spider, args=(17001, 18000))
    threads.append(thread18)
    thread19 = Thread(target=start_spider, args=(18001, 19000))
    threads.append(thread19)
    thread20 = Thread(target=start_spider, args=(19001, 20235))
    threads.append(thread20)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('运行完成!')

# 运行程序
if __name__ == '__main__':
    print('go!')
    with open('../log/spider_bookinfo.txt', 'a', encoding='utf-8') as log:
        log.write(str(datetime.now()) + '-- 程序开始' + '\n')
        main_multithreading_spider()
