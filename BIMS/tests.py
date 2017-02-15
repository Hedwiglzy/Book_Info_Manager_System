#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用
"""
from datetime import datetime

# from django import forms
# from django.db import connection
# from django.test import TestCase
# from BIMS.models import User
# alist = User.objects.all()
# print(alist)

# Create your tests here.
# Book_Info_Manager_System
# os.environ['DJANGO_SETTINGS_MODULE'] = 'Book_Info_Manager_System.settings'
# cursor = connection.cursor()
# test git
# birthday = '1995-10-02'
import re

info_text = """出版社: 上海人民出版社
原作名: The Kite Runner

 译者:


        李继宏

出版年: 2006-5
页数: 362
定价: 29.00元
装帧: 平装
丛书: 卡勒德·胡赛尼作品
ISBN: 9787208061644
"""
test = info_text.split(':')
print(test)
