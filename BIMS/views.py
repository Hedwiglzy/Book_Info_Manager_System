#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视图层
"""

import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from BIMS.models import User
from BIMS.tools.forms import LoginForm, RegisterForm


# Create your views here.

def get_user_info(request, user_id):
    """
    用户信息
    """
    user_id = int(user_id)
    user = User.objects.get(user_id=user_id)
    sex = {1: '男', 2: '女', 0: '其他'}
    avatar = {0: 'original', 1: user_id}
    return render_to_response('people.html', {'user': user, 'sex': sex[user.sex], 'avatar': avatar[user.image]}, )


def register(request):
    """
    注册
    """
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            tel = register_form.cleaned_data['tel']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            birthday = register_form.cleaned_data['birthday']
            province = register_form.cleaned_data['province']
            city = register_form.cleaned_data['city']
            remark = register_form.cleaned_data['remark']
            age = int(str(datetime.date.today())[0:4]) - int(str(birthday)[0:4])
            create_date = datetime.date.today()
            user = User(user_name=username, password=password, tel=tel, email=email,
                        birthday=birthday, age=age, sex=sex, locate=province + city, remark=remark,
                        create_date=create_date)
            user.save()

            return render_to_response('register_successed.html', )
    else:
        register_form = RegisterForm()
        return render_to_response('register.html', {'register_form': register_form})


def login(request):
    """
    登录
    """
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                User.objects.get(user_name=username)
            except User.DoesNotExist:
                return render_to_response('user_not_exist.html', )
            real_pswd = User.objects.get(user_name=username).password
            user_id = User.objects.get(user_name=username).user_id
            if password == real_pswd:
                return HttpResponseRedirect(reverse(get_user_info, args=[user_id]))
            else:
                return render_to_response('wrong_password.html', )
    else:
        login_form = LoginForm()
        return render_to_response('login.html', {'LoginForm': login_form})
