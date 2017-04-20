#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 装饰器 """

from django.shortcuts import render_to_response

__pyname__ = 'decorator'
__author__ = 'Hedwig'
__date__ = '2017/4/19'


def login_required(func):
    """
    登录认证
    :param func:函数
    """
    def wrapper(request, *args):
        """
        检查是否登录
        :param request:请求
        """
        user_id = request.session.get('user_id', )
        if user_id:
            return func(request, *args)
        else:
            return render_to_response('skip.html', {'instruction': '请先登录'})
    return wrapper
