#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.shortcuts import render_to_response
from BIMS.models import User
from .tools.forms import RegisterForm,LoginForm
import datetime


# Create your views here.

def hello(request):
    now = datetime.datetime.now()
    html = '''<html>
	            <title>welcome</title>
                    <style>
                      #null{height:30px}
                      #text{font-size:80px;font-family:HYMiaoHunTiW;text-align: center;}
                      #time{font-size:16px;font-family:Monaco;text-align: center;}
                      #path{font-size:16px;font-family:Monaco;text-align: center;}
                    </style>
	          <body>
	            <div id = "null"></div>
	            <div id = "text">Django is running!</div>
                <p></p>
                <div id = "time">当前时间为:%s</div>
                <p></p>
                <div id = "path">访问地址为:%s</div>
              </body>
            </html>''' % (now, request.path)
    return HttpResponse(html)

def get_user_info(request, user_id):
    user_id = int(user_id)
    user = User.objects.get(user_id=user_id)
    sex = {1: '男', 2: '女', 0: '其他'}
    return render_to_response('user_info.html',
                              {'user_name': user.user_name, 'tel': user.tel, 'email': user.email, 'sex': sex[user.sex],
                               'birthday': user.birthday, 'locate': user.locate})

def register(request):
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
            remark = register_form.cleaned_data['introduce']
            age = int(str(datetime.date.today())[0:4]) - int(str(birthday)[0:4])
            user = User(user_name=username, password=password, tel=tel, email=email,
            birthday=birthday, age=age, sex=sex, locate=province+city, remark=remark)
            user.save()
            return render_to_response('register_successed.html', )
    else:
        register_form = RegisterForm()
        return render_to_response('register.html', {'register_form': register_form})

def login(request):
    if request.method == 'POST':
        Login_Form = LoginForm(request.POST)
        if Login_Form.is_valid():
            username = Login_Form.cleaned_data['username']
            password = Login_Form.cleaned_data['password']
            try:
                User.objects.get(user_name=username)
            except User.DoesNotExist:
                return render_to_response('user_not_exist.html',)
            real_pswd = User.objects.get(user_name=username).password
            user_id = User.objects.get(user_name=username).user_id
            if password ==real_pswd:
                return HttpResponseRedirect(reverse(get_user_info,args=[user_id]))
            else:
                return HttpResponse('密码错误!')
    else:
        Login_Form = LoginForm()
        return render_to_response('login.html', {'LoginForm': Login_Form})