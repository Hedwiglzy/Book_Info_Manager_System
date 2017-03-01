#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用
"""
import re
import urllib.request

import requests
from bs4 import BeautifulSoup

loginUrl = 'http://accounts.douban.com/login'
formData = {
    "redir": "http://movie.douban.com/mine?status=collect",
    "form_email": '1432659378@qq.com',
    "form_password": '6073651428kk',
    "login": u'登录'
}
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
r = requests.post(loginUrl, data=formData, headers=headers)
page = r.text
# print r.url

'''''获取验证码图片'''
# 利用bs4获取captcha地址
soup = BeautifulSoup(page, "html.parser")
captchaAddr = soup.find('img', id='captcha_image')['src']
# 利用正则表达式获取captcha的ID
reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
captchaID = re.findall(reCaptchaID, page)
# print captchaID
# 保存到本地
urllib.request.urlretrieve(captchaAddr, "captcha.jpg")
captcha = input('please input the captcha:')

formData['captcha-solution'] = captcha
formData['captcha-id'] = captchaID

r = requests.post(loginUrl, data=formData, headers=headers)
page = r.text
if r.url != 'http://movie.douban.com/mine?status=collect':
    if r.url == 'http://movie.douban.com/mine?status=collect':
        print('Login successfully!!!')
        print('我看过的电影', '-' * 60)
        # 获取看过的电影
        soup = BeautifulSoup(page, "html.parser")
        result = soup.findAll('li', attrs={"class": "title"})
        # print result
        for item in result:
            print(item.find('a').get_text())
    else:
        print("failed!")

"""
出版说明 在中国近现代美术史上，鲁迅与美术始终纠缠在一起，从童年对美术的热爱到编辑出版中外美术书籍；从鲁迅美术思想的提出到倡导新兴木刻，鲁迅一生始终贯串着美术活动。从这一角度看鲁迅，他是名符其实的“美术人”。 鲁迅作为二十世纪的伟大人物，其人格魅力和思想光焰几乎笼罩中国一个世纪。至今，仍然可以说鲁迅始终处于中国文坛的中心，鲁迅给世人留下了卷帙浩繁的著作，鲁迅之后的中国文坛难以出现如此伟大的人物。鲁迅去世后近八十年的鲁迅研究中，大多以鲁迅的小说、散文、杂文为研究主体，对鲁迅生命本体的研究诸如数十种鲁迅传记，是以他的生平、创作为主要对象，然而并没有一部完备的鲁迅美术年谱来纪传鲁迅的美术生活。这也是笔者著纂本书的起因。 通过对鲁迅一生美术活动的梳理，我们可以看到年仅五十六岁的鲁迅，生命付出最多的，除了创作和翻译之外便是在美术活动上。
"""
