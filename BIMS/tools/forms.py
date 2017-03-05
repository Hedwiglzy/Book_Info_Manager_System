#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" forms"""
import datetime

from django import forms

__pyname__ = 'forms.py'
__author__ = 'Hedwig'
__date__ = '2016/11/27'


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': '输入用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': '输入密码'}))
    tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'tel', 'placeholder': '输入手机号'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': '输入邮箱'}), required=False)
    CHOICES = (('1', '男',), ('2', '女',), ('3', '其他'))
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    birthday = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'birthday', 'placeholder': '输入生日', 'value': datetime.date.today(), 'readonly': 'readonly'}), required=False)
    province = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'province'}))
    city = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'city'}))
    remark = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'remark', 'placeholder': '一句话介绍自己'}), required=False)
    required_css_class = 'sr-only'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': '输入用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': '输入密码'}))
    required_css_class = 'sr-only'


class SreachForm(forms.Form):
    sreach = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'sreach', 'placeholder': '输入你感兴趣的东西'}))
    required_css_class = 'sr-only'


class EvaluateForm(forms.Form):
    book_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'book_id', 'type': 'hidden'}))
    evaluate = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'evaluate', 'placeholder': '输入你的评论'}))
    required_css_class = 'sr-only'


class NoteForm(forms.Form):
    book_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'book_id', 'type': 'hidden'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'note_title', 'placeholder': '输入标题'}), required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'remark', 'rows': 25, 'placeholder': '输入内容'}), required=False)
    required_css_class = 'sr-only'
