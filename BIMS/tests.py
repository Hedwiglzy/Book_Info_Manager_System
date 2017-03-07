#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用
"""
import re
import urllib.request

import requests
from bs4 import BeautifulSoup

# loginUrl = 'http://accounts.douban.com/login'
# formData = {
#     "redir": "http://movie.douban.com/mine?status=collect",
#     "form_email": '1432659378@qq.com',
#     "form_password": '6073651428kk',
#     "login": u'登录'
# }
# headers = {
#     "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# r = requests.post(loginUrl, data=formData, headers=headers)
# page = r.text
# # print r.url
#
# '''''获取验证码图片'''
# # 利用bs4获取captcha地址
# soup = BeautifulSoup(page, "html.parser")
# captchaAddr = soup.find('img', id='captcha_image')['src']
# # 利用正则表达式获取captcha的ID
# reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
# captchaID = re.findall(reCaptchaID, page)
# # print captchaID
# # 保存到本地
# urllib.request.urlretrieve(captchaAddr, "captcha.jpg")
# captcha = input('please input the captcha:')
#
# formData['captcha-solution'] = captcha
# formData['captcha-id'] = captchaID
#
# r = requests.post(loginUrl, data=formData, headers=headers)
# page = r.text
# if r.url != 'http://movie.douban.com/mine?status=collect':
#     if r.url == 'http://movie.douban.com/mine?status=collect':
#         print('Login successfully!!!')
#         print('我看过的电影', '-' * 60)
#         # 获取看过的电影
#         soup = BeautifulSoup(page, "html.parser")
#         result = soup.findAll('li', attrs={"class": "title"})
#         # print result
#         for item in result:
#             print(item.find('a').get_text())
#     else:
#         print("failed!")

import re

