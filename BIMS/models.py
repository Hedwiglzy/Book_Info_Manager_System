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
    province = models.CharField(max_length=50, null=True)  # 省
    city = models.CharField(max_length=50, null=True)  # 省
    remark = models.CharField(max_length=500, null=True)  # 个人简介
    image = models.IntegerField(null=True)  # 头像
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
    press_house = models.CharField(max_length=100, null=True)  # 出版社
    translator = models.CharField(max_length=100, null=True)  # 翻译者
    publication_date = models.CharField(max_length=100, null=True)  # 出版日期
    pages = models.CharField(max_length=100, null=True)  # 页数
    price = models.CharField(max_length=100, null=True)  # 价格
    package = models.CharField(max_length=10, null=True)  # 装帧
    isbn = models.BigIntegerField(null=True)  # ISBN
    score = models.DecimalField(max_digits=10, decimal_places=1, null=True)  # 评分
    evaluate_num = models.IntegerField(null=True)  # 评价人数
    collect_num = models.IntegerField(null=True)  # 收藏人数
    content_summary = models.TextField(null=True)  # 内容简介
    title = models.CharField(max_length=100, null=True)  # 分类
    create_date = models.DateField(null=True)  # 创建日期
    author_id = models.IntegerField(null=True)  # 作者ID

    def __str__(self):
        return self.book_name


class Author(models.Model):
    """
    作者信息模型
    """
    author_id = models.IntegerField(primary_key=True)  # 作者ID
    author_name = models.CharField(max_length=100)  # 作者名
    nationality = models.CharField(max_length=100, null=True)  # 国籍
    author_summary = models.TextField(null=True)  # 作者简介

    def __str__(self):
        return self.author_name


class CollectionBook(models.Model):
    """
    图书收藏表
    """
    op_id = models.AutoField(primary_key=True)  # 流水号
    user_id = models.IntegerField()  # 用户ID
    book_id = models.IntegerField()  # 图书ID
    create_date = models.DateField()  # 收藏日期

    def __str__(self):
        return self.op_id


class CollectionAuthor(models.Model):
    """
    作者收藏表
    """
    op_id = models.AutoField(primary_key=True)  # 流水号
    user_id = models.IntegerField()  # 用户ID
    author_id = models.IntegerField()  # 作者ID
    create_date = models.DateField()  # 收藏日期

    def __str__(self):
        return self.op_id


class BookNote(models.Model):
    """
    读书笔记
    """
    note_id = models.AutoField(primary_key=True)  # 流水号
    book_id = models.IntegerField()  # 图书ID
    user_id = models.IntegerField()  # 用户ID
    user_name = models.CharField(max_length=100)  # 用户名
    title = models.CharField(max_length=100, null=True)  # 标题
    content = models.TextField(null=True)  # 内容
    create_date = models.DateField()  # 收藏日期

    def __str__(self):
        return self.title


class BookEvaluate(models.Model):
    """
    图书评论表
    """
    op_id = models.AutoField(primary_key=True)  # 流水号
    book_id = models.IntegerField()  # 图书ID
    user_name = models.CharField(max_length=100)  # 用户名
    content = models.TextField(null=True)  # 内容
    create_date = models.DateField()  # 评价日期

    def __str__(self):
        return self.op_id


class BookScore(models.Model):
    """
    图书评分表
    """
    op_id = models.AutoField(primary_key=True)  # 流水号
    book_id = models.IntegerField()  # 图书ID
    user_id = models.IntegerField()  # 用户ID
    score = models.IntegerField(null=True)  # 内容
    create_date = models.DateField()  # 评价日期

    def __str__(self):
        return self.op_id
