#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Template,Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
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
                    </style>
	          <body>
	            <div id = "null"></div>
	            <div id = "text">Django is running!</div>
                <p></p>
                <div id = "time">当前时间为:%s</div>
              </body>
            </html>''' % now
    return HttpResponse(html)

def add(request):
    a = request.GET.get('a',0)
    b = request.GET.get('b',0)
    c = int(a) + int(b)
    return  HttpResponse(str(c))

def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))

def index(request):
    return render(request,'home.html')

def time_plus(request,i):
    try:
        i = int(i)
    except ValueError:
        raise Http404()
    now  = datetime.datetime.now()
    time = now + datetime.timedelta(hours = i)
    html = '''<html>
                <title>time plus</title>
                <body>
                    <h1><center> 当前时间为%s <center></h1>
                    <h1><center> %s小时之后为%s <center></h1>
                </body>
              </html>''' % (now,i,time)
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

def test_keke(request):
    now = datetime.datetime.now()
    tl_object = get_template('home.html')
    ct_object =Context({'time':now})
    last_html = tl_object.render(ct_object)
    return HttpResponse(last_html)

def test_haha(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'time':now})

def test_login(request):
    return render_to_response('login.html')