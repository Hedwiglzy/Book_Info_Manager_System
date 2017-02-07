#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型层
"""
from django.db import models


# Create your models here.


class User(models.Model):
    """
    用户信息模型
    """
    user_id = models.AutoField(primary_key=True)  # 用户ID
    user_name = models.CharField(max_length=30)  # 用户名
    password = models.CharField(max_length=30)  # 密码
    tel = models.BigIntegerField(null=True)  # 电话
    email = models.EmailField(null=True)  # 邮箱
    sex = models.IntegerField(null=True)  # 性别 1男 2女 0其他
    birthday = models.DateField(null=True)  # 生日
    age = models.IntegerField(null=True)  # 年龄
    locate = models.CharField(max_length=50, null=True)  # 所在地
    remark = models.CharField(max_length=500, null=True)  # 个人简介
    image = models.ImageField(null=True)  # 头像
    create_date = models.DateField(null=True)  # 创建日期

    def __str__(self):
        return self.user_name


class Book(models.Model):
    """
    图书信息模型
    """
    book_id = models.AutoField(primary_key=True)  # 图书ID
    book_name = models.CharField(max_length=100)  # 图书名
    author_name = models.CharField(max_length=100)  # 作者名
    press = models.CharField(max_length=100, null=True)  # 出版社
    translator = models.CharField(max_length=100, null=True)  # 翻译者
    publication_date = models.CharField(max_length=100, null=True)  # 出版日期
    pages = models.IntegerField(null=True)  # 页数
    price = models.IntegerField(null=True)  # 价格
    package = models.CharField(max_length=10, null=True)  # 装帧
    isbn = models.BigIntegerField(null=True)  # ISBN
    score = models.IntegerField(null=True)  # 评分
    evaluate_num = models.IntegerField(null=True)  # 评价人数
    collect_num = models.IntegerField(null=True)  # 收藏人数
    content_summary = models.TextField(null=True)  # 内容简介

    def __str__(self):
        return self.book_name


class Author(models.Model):
    """
    作者信息模型
    """
    author_id = models.AutoField(primary_key=True)  # 作者ID
    author_name = models.CharField(max_length=100)  # 作者名
    nationality = models.CharField(max_length=100, null=True)  # 国籍
    author_summary = models.TextField(null=True)  # 作者简介

    def __str__(self):
        return self.author_name
