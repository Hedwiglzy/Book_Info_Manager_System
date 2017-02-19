#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用
"""
from datetime import datetime
import time
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

from threading import Thread


def haha(n):
    for i in range(n):
        print(datetime.now(), '第' + str(i) + '次循环')
        time.sleep(1)

threads = []
t1 = Thread(target=haha, args=(2,))
t2 = Thread(target=haha, args=(5,))
threads.append(t1)
threads.append(t2)

for t in threads:
    t.start()


