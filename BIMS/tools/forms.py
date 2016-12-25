#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" forms"""

__pyname__ = 'forms.py'
__author__ = 'Hedwig'
__date__ = '2016/11/27'

from django import forms

class User(forms.Form):
    username = forms.CharField(max_length=30)                   #用户名
    password  = forms.CharField(max_length=30)                  #密码
    tel       = forms.IntegerField(required=False)              #电话
    email     = forms.EmailField(required=False)                #邮箱
    sex       = forms.IntegerField(required=False)              #性别 1男 2女 0其他
    birthday  = forms.DateField(required=False)                 #生日
    age       = forms.IntegerField(required=False)              #年龄
    locate    = forms.CharField(required=False)                 #所在地
    remark    = forms.CharField(max_length=500,required=False)  #个人简介
    image     = forms.ImageField(required=False)                #头像


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'username', 'placeholder': '输入用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' ,'id':'password', 'placeholder': '输入密码'}))
    tel = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'tel', 'placeholder': '输入手机号'}),required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control' ,'id':'email', 'placeholder': '输入邮箱'}),required=False)
    CHOICES = (('1', '男',), ('2', '女',),('3','其他'))
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    birthday = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'birthday', 'placeholder': '输入生日','value':'','readonly':'readonly'}),required=False)
    province = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','id':'province'}))
    city = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','id':'city'}))
    introduce = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'introduce', 'placeholder': '一句话介绍自己'}),required=False)
    required_css_class = 'sr-only'
