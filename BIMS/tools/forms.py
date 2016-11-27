#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" forms"""

__pyname__ = 'forms.py'
__author__ = 'Hedwig'
__date__ = '2016/11/27'

from django import forms

class User(forms.Form):
    user_name = forms.CharField()
    email = forms.EmailField()