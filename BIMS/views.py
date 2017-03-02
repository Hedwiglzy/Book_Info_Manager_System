#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视图层
"""

import datetime
from math import ceil

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

from BIMS.models import User, Book, Author, CollectionBook, CollectionAuthor
from BIMS.tools.forms import LoginForm, RegisterForm, SreachForm


# Create your views here.

def search(keyword):
    """
    搜索信息
    :param keyword:关键字
    """
    search_result = []
    for book in Book.objects.filter(book_name__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(author_name__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(press_house__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(isbn__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(isbn__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(title__contains=keyword):
        search_result.append(book)
    return search_result


def get_book_collection(user_id):
    """
    获取用户收藏的图书
    :param user_id:用户ID
    """
    book_collections = []
    collections = CollectionBook.objects.filter(user_id=user_id)
    for collection in collections:
        book_collections.append(Book.objects.get(book_id=collection.book_id))
    return book_collections


def get_author_collection(user_id):
    """
    获取用户收藏的作者
    :param user_id:用户ID
    """
    autuor_collections = []
    collections = CollectionAuthor.objects.filter(user_id=user_id)
    for collection in collections:
        autuor_collections.append(Author.objects.get(author_id=collection.author_id))
    return autuor_collections


def get_note_collection(user_id):
    """
    获取用户收藏的图书
    """


def get_author_book(author_id):
    """
    获取作者所有作品
    :param author_id:作者ID
    """
    return Book.objects.filter(author_id=author_id)


def get_user_info(request):
    """
    用户信息
    :param request:请求
    :return:用户个人信息
    """
    user_id = request.session.get('user_id', 'user_not_exist')
    if user_id == 'user_not_exist':
        return render_to_response('user_not_exist.html', )
    else:
        if request.method == 'POST':
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                results = search(keyword)
                return render_to_response('result.html', {'results': results})
        else:
            sreach_form = SreachForm()
            user = User.objects.get(user_id=user_id)
            sex = {1: '男', 2: '女', 0: '其他'}
            avatar = {0: 10000, 1: user_id}
            book_collections = get_book_collection(user_id)
            author_collections = get_author_collection(user_id)
            authors_and_books = []
            for author in author_collections:
                author_books = get_author_book(author.author_id)
                if len(author_books) > 4:
                    author_books = author_books[0:4]
                else:
                    pass
                author_and_book = {
                    'author': author,
                    'book': author_books
                }
                authors_and_books.append(author_and_book)
            # quotient = divmod(len(book_collections), 6)
            # height = (quotient[0] + ceil(quotient[1] / 6)) * 260 + 50
            return render_to_response('user.html', {'sreach_form': sreach_form, 'user': user, 'sex': sex[user.sex], 'avatar': avatar[user.image], 'book_collections': book_collections, 'authors_and_books': authors_and_books},)


def get_book_info(request, book_id):
    """
    图书信息
    :param request:请求
    :param book_id:图书id
    :return:图书信息
    """
    user_id = request.session.get('user_id', 'user_not_exist')
    if user_id == 'user_not_exist':
        return render_to_response('user_not_exist.html', )
    else:
        if request.method == 'POST':
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                results = search(keyword)
                return render_to_response('result.html', {'results': results})
        else:
            sreach_form = SreachForm()
            user = User.objects.get(user_id=user_id)
            avatar = {0: 10000, 1: user_id}
            book_id = int(book_id)
            book = Book.objects.get(book_id=book_id)
            author = Author.objects.get(author_id=book.author_id)
            if int(book.score) == 0:
                score = ''
            else:
                score = book.score
            return render_to_response('book.html', {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image], 'book': book, 'score': score, 'author': author}, )


def get_author_info(request, author_id):
    """
    图书信息
    :param request:请求
    :param author_id:作者id
    :return:作者信息
    """
    user_id = request.session.get('user_id', 'user_not_exist')
    if user_id == 'user_not_exist':
        return render_to_response('user_not_exist.html', )
    else:
        if request.method == 'POST':
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                results = search(keyword)
                return render_to_response('result.html', {'results': results})
        else:
            sreach_form = SreachForm()
            user = User.objects.get(user_id=user_id)
            avatar = {0: 10000, 1: user_id}
            author_id = int(author_id)
            author = Author.objects.get(author_id=author_id)
            author_books = Book.objects.filter(author_id=author_id)
            return render_to_response('author.html', {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image], 'author': author, 'author_books': author_books}, )


def register(request):
    """
    注册
    :param request:请求
    :return: 注册成功
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
            user = User(user_name=username, password=password, tel=int(tel), email=email,
                        birthday=birthday, age=age, sex=sex, locate=province + city, remark=remark,
                        create_date=create_date, image=0)
            user.save()

            return render_to_response('register_successed.html', )
    else:
        register_form = RegisterForm()
        return render_to_response('register.html', {'register_form': register_form})


def login(request):
    """
    登录
    :param request:请求
    :return: 登录成功或失败
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
                # return HttpResponseRedirect(reverse(get_user_info, args=[user_id]))
                request.session['user_id'] = user_id
                return HttpResponseRedirect('/index/')
            else:
                return render_to_response('wrong_password.html', )
    else:
        login_form = LoginForm()
        return render_to_response('login.html', {'LoginForm': login_form})


def logout(request):
    """
    登出
    :param request:请求
    :return:登录界面
    """
    del request.session['user_id']
    return HttpResponseRedirect('/login/')


# @cache_page(60 * 30)
def index(request):
    """
    主页
    登录后跳转
    :param request:请求
    """
    user_id = request.session.get('user_id', 'user_not_exist')
    if user_id == 'user_not_exist':
        return render_to_response('user_not_exist.html', )
    else:
        if request.method == 'POST':
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                request.session['user_id'] = user_id
                request.session['keyword'] = keyword
                return HttpResponseRedirect('/result/')
        else:
            sreach_form = SreachForm()
            user = User.objects.get(user_id=user_id)
            avatar = {0: 10000, 1: user_id}
            hot_books = Book.objects.order_by('-evaluate_num')[0:6]
            new_books = Book.objects.order_by('-create_date')[0:6]
            return render_to_response('index.html', {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image], 'hot_books': hot_books, 'new_books': new_books})


def result(request):
    """
    搜索结果界面
    :param request:请求
    """
    user_id = request.session.get('user_id', 'user_not_exist')
    if user_id == 'user_not_exist':
        return render_to_response('user_not_exist.html', )
    else:
        if request.method == 'POST':
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                request.session['keyword'] = keyword
                return HttpResponseRedirect('/result/')
        else:
            sreach_form = SreachForm()
            user = User.objects.get(user_id=user_id)
            avatar = {0: 10000, 1: user_id}
            keyword = request.session.get('keyword', ' ')
            print(keyword)
            search_results = search(keyword)
            return render_to_response('result.html', {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image], 'results': search_results})
