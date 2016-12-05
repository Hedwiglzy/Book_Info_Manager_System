#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse,Http404
from django.template import Template,Context
from django.shortcuts import render_to_response
from BIMS.models import User as mUser
from .tools.forms import User as fUser
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
            </html>''' % (now,request.path)
    return HttpResponse(html)

def test_template(request,name,age):
    raw_template = '''
              <html>
                <title>template</title>
                <body>
                    <center> 我的名字是{{ name }} </center>
                    <p></p>
                    <center> 我的年龄是{{ age }} </center>
                    <p></p>
                    <center> 当前时间为{{ date|date:"Y-m-d H:i:s" }} </center>
                </body>
              </html>
              '''
    age = int(age)
    tl_object = Template(raw_template)
    ct_object = Context({'name':name,'age':age,'date': datetime.datetime.now()})
    last_html = tl_object.render(ct_object)
    return HttpResponse(last_html)

def test_login(request):
    return render_to_response('login.html')

def get_user_info(request,user_id):
    user_id = int(user_id)
    user = mUser.objects.get(user_id=user_id)
    sex = {1:'男',2:'女',0:'其他'}
    return render_to_response('user_info.html',{'user_name':user.user_name,'tel':user.tel,'email':user.email,'sex':sex[user.sex],'birthday':user.birthday,'locate':user.locate})

def display_meta(request):
    values = request.META.items()
    values = sorted(values)
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    a = '<table>%s</table>' % '\n'.join(html)
    print(a)
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def register(request):
    if request.method =='POST':
        form = fUser(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password  = form.cleaned_data['password']
            tel       = form.cleaned_data['tel']
            email     = form.cleaned_data['email']
            sex       = form.cleaned_data['sex']
            birthday  = form.cleaned_data['birthday']
            age       = form.cleaned_data['tel']
            locate    = form.cleaned_data['locate']
            remark    = form.cleaned_data['remark']
            user = mUser(user_name = user_name,password = password,tel= tel,email = email,
                         sex = sex,birthday = birthday,age = age,locate = locate,remark = remark)
            user.save()
            return HttpResponse('注册成功!')
    else:
        form = fUser()
        print(form)
        return render_to_response('register.html',{'form':form})