#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 爬取图书信息"""

__pyname__ = 'spider_book.py'
__author__ = 'Hedwig'
__date__ = '2017/2/9'

import re
import requests
from bs4 import BeautifulSoup

def get_douban_info():
    """
    爬取豆瓣图书信息
    """
    douban_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    web_data = requests.get(douban_url)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    tags = soup.find_all(href = re.compile(r'tag'))
    for tag in tags:
        url = 'https://book.douban.com'+tag.get('href')
        title = tag.get_text()
        TIELES.append(title)
        URL_AND_TITLE[title]=url

if __name__ == '__main__':
    URL_AND_TITLE = {}
    TIELES=[]
    print('go!')
    get_douban_info()
    for TIELE in TIELES:
        print(URL_AND_TITLE[TIELE])
    