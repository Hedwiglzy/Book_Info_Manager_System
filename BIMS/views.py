#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Template,Context
import datetime

# Create your views here.

def hello(request):
    now = datetime.datetime.now()
    html = '''<html>
	            <title>welcome</title>
	            <style>
	                #text{
	                    position: absolute;
	                    top: 0;
                        bottom: 0;
                        left: 0;
                        right: 0;
                        margin: auto;
                        height: 240px;
                        width:70%%;
                        color:#2693FF}
	            </style>
              <body>
                    <div id = "text">
                        <h1><font face = "Monaco" size = 30 ><center> Welcome Django! <center></font></h1>
                            <font face = "Monaco"><center> 当前时间为:%s <center></font>
                    </div>
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
