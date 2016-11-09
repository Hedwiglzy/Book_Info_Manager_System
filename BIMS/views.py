#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

# Create your views here.

def hello(request):
    s = 'hello!'
    current_time = datetime.datetime.now()
    html = '<html><head></head><body><h1><center> %s <center></h1><center> %s <center></body></html>' %(s,current_time)
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
