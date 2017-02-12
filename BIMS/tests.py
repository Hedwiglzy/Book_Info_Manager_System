#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用
"""
import datetime

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

import pymysql
import re
DATA = "haha"
if re.search("'", DATA):
    print(DATA)
