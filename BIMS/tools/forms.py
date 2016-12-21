#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" forms"""

__pyname__ = 'forms.py'
__author__ = 'Hedwig'
__date__ = '2016/11/27'

from django import forms

class User(forms.Form):
    username = forms.CharField(max_length=30)                  #用户名
    # password  = forms.CharField(max_length=30)                  #密码
    # tel       = forms.IntegerField(required=False)              #电话
    # email     = forms.EmailField(required=False)                #邮箱
    # sex       = forms.IntegerField(required=False)              #性别 1男 2女 0其他
    # birthday  = forms.DateField(required=False)                 #生日
    # age       = forms.IntegerField(required=False)              #年龄
    # locate    = forms.CharField(required=False)                 #所在地
    # remark    = forms.CharField(max_length=500,required=False)  #个人简介
    # image     = forms.ImageField(required=False)                #头像