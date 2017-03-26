""" 爬取图书图片 """

import urllib.request as urllib

import pymysql
import requests
import time
from bs4 import BeautifulSoup

__pyname__ = 'spider_cover'
__author__ = 'Hedwig'
__date__ = '2017/03/15'


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
    cursor.execute("select `book_id` , `book_url` from all_book")
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def insert_table(update_id, cover_url):
    """
    将数据插入表中
    :param update_id:入表的数据
    :param cover_url:入表的数据
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'UPDATE `all_book` set `cover_url` ="%s" where `book_id` = %s' % (cover_url, update_id)
    cursor.execute(sql)
    conn.commit()
    conn.close()

print('go!')
index = int(input('输入起始编号:'))
book_infos = select_table()
path = 'E:\\GitHub\\Book_Info_Manager_System\\BIMS\static\\image\\book\\cover\\'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': 'bid=P0tNWfw2GP0; gr_user_id=007d83db-caf6-479b-b32f-aa73804ae093; __utmt_douban=1; __utmt=1; viewed="1770782_1009257"; _vwo_uuid_v2=BDC1CA5796473A9D248DD18DEEFA7FA2|d2cb955d6deafc4a832877da194bb5dd; __utma=30149280.1144085401.1489570681.1489570681.1489570681.1; __utmb=30149280.2.10.1489570681; __utmc=30149280; __utmz=30149280.1489570681.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=81379588.768202022.1489570681.1489570681.1489570681.1; __utmb=81379588.2.10.1489570681; __utmc=81379588; __utmz=81379588.1489570681.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=afbd2b92-6b6b-4423-b5b6-7d60e9689036; gr_cs1_afbd2b92-6b6b-4423-b5b6-7d60e9689036=user_id%3A0; _pk_id.100001.3ac3=271075fc596bf8f4.1488852758.2.1489570811.1488852786.; _pk_ses.100001.3ac3=*; ps=y; ue="1432659378@qq.com"; dbcl2="83764412:krVzuDu4/v4"'
    }
for i, book_info in enumerate(book_infos):
    if i >= index-1:
        book_id = book_info['book_id']
        book_url = book_info['book_url'].rstrip()
        web_data = requests.get(book_url, headers=headers)
        print(web_data.status_code)
        print('爬取' + str(i+1) + ' ' + book_url + '成功')
        soup = BeautifulSoup(web_data.text, 'lxml')
        img_url = soup.find_all(class_='nbg')
        for url in img_url:
            cover = url.get('href')
            insert_table(book_id, cover)
            urllib.urlretrieve(cover, path + str(book_id+10000)+'.jpg')
            print(cover+'入库成功')
            time.sleep(1)
print('end')
# 2329
