#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视图层
"""
import datetime
import random

import plotly.graph_objs as go
import plotly.offline as py
from django.db.models import Avg, Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from BIMS.models import Author, Book, BookEvaluate, BookNote, BookScore, CollectionAuthor, CollectionBook, User
from BIMS.tools.decorator import login_required
from BIMS.tools.forms import BookForm, EvaluateForm, LoginForm, NoteForm, RegisterForm, SreachForm


# Create your views here.


def search(keyword):
    """
    搜索信息
    :param keyword:关键字
    """
    search_result = []
    for book in Book.objects.filter(book_id__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(book_name__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(author_name__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(press_house__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(isbn__contains=keyword):
        search_result.append(book)
    for book in Book.objects.filter(title__contains=keyword):
        search_result.append(book)
    search_result = set(search_result)
    search_result = sorted(search_result, key=lambda result_book: result_book.book_id)
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
        autuor_collections.append(
            Author.objects.get(author_id=collection.author_id))
    return autuor_collections


def get_user_note(user_id):
    """
    获取用户的读书笔记
    """
    notes = BookNote.objects.filter(user_id=user_id)
    return notes


def get_author_book(author_id):
    """
    获取作者所有作品
    :param author_id:作者ID
    """
    return Book.objects.filter(author_id=author_id)


def get_book_score(book_id):
    """
    求出图书综合评分
    :param book_id:图书ID
    计算公式如下：weighted rank (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
    其中：
    R = average for the movie (mean) = (Rating) （是用普通的方法计算出的平均分）
    v = number of votes for the movie = (votes) （投票人数）
    m = minimum votes required (currently 10) （需要的最小票数）
    C = the mean vote across the whole report (currently) （目前所有电影的平均得分）
    """
    rating = BookScore.objects.filter(book_id=book_id).aggregate(Avg('score'))['score__avg']
    votes = BookScore.objects.filter(book_id=book_id).count()
    minimum = 10
    currently = BookScore.objects.aggregate(Avg('score'))['score__avg']
    book_score = round((votes / (votes + minimum)) * rating + (minimum / (votes + minimum)) * currently, 1)
    return book_score


@login_required
def get_user_info(request):
    """
    用户信息
    :param request:请求
    :return:用户个人信息
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['user_id'] = user_id
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
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
        notes = get_user_note(user_id)
        notes_and_books = []
        for note in notes:
            book = Book.objects.get(book_id=note.book_id)
            note_and_book = {
                'note': note,
                'book': book
            }
            notes_and_books.append(note_and_book)
        return render_to_response('user.html', {'sreach_form': sreach_form, 'user': user, 'sex': sex[user.sex],
                                                'avatar': avatar[user.image], 'book_collections': book_collections,
                                                'authors_and_books': authors_and_books,
                                                'notes_and_books': notes_and_books}, )


def get_book_info(request, book_id):
    """
    图书信息
    :param request:请求
    :param book_id:图书id
    :return:图书信息
    """
    user_id = request.session.get('user_id', )
    if user_id:
        if request.method == 'POST':
            if request.method == 'POST':
                sreach_form = SreachForm(request.POST)
                if sreach_form.is_valid():
                    keyword = sreach_form.cleaned_data['sreach']
                    request.session['user_id'] = user_id
                    request.session['keyword'] = keyword
                    return HttpResponseRedirect('/result/1/')
        else:
            sreach_form = SreachForm()
            evaluate_form = EvaluateForm()
            note_form = NoteForm()
            user = User.objects.get(user_id=user_id)
            avatar = {0: 10000, 1: user_id}
            book_id = int(book_id)
            book = Book.objects.get(book_id=book_id)
            author = Author.objects.get(author_id=book.author_id)
            evaluates = BookEvaluate.objects.filter(
                book_id=book_id).order_by('-create_date')
            book_evaluates = evaluates[0:6] if len(
                evaluates) > 6 else evaluates
            notes = BookNote.objects.filter(
                book_id=book_id).order_by('-create_date')
            book_notes = notes[0:3] if len(notes) > 3 else notes
            is_collection = CollectionBook.objects.filter(
                user_id=user_id, book_id=book_id)
            if is_collection:
                collection = 1
            else:
                collection = 0
            collect_num = CollectionBook.objects.filter(book_id=book_id).count()
            is_score = BookScore.objects.filter(book_id=book_id)
            if is_score:
                book_score = get_book_score(book_id)
            else:
                book_score = '无人评价'
            evaluate_num = BookScore.objects.filter(book_id=book_id).count()
            my_score = BookScore.objects.filter(
                user_id=user_id, book_id=book_id)
            if my_score:
                my_score = my_score[0].score+1
            else:
                my_score = 0
            return render_to_response('book.html',
                                      {'sreach_form': sreach_form, 'evaluate_form': evaluate_form, 'user': user,
                                       'avatar': avatar[user.image], 'book': book, 'book_score': book_score,
                                       'collect_num': collect_num, 'evaluate_num': evaluate_num, 'author': author,
                                       'book_evaluates': book_evaluates, 'book_notes': book_notes,
                                       'note_form': note_form, 'collection': collection, 'my_score': my_score}, )
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def get_author_info(request, author_id):
    """
    图书信息
    :param request:请求
    :param author_id:作者id
    :return:作者信息
    """
    user_id = request.session.get('user_id', )
    if user_id:
        if request.method == 'POST':
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                request.session['user_id'] = user_id
                request.session['keyword'] = keyword
                return HttpResponseRedirect('/result/1/')
        else:
            sreach_form = SreachForm()
            user = User.objects.get(user_id=user_id)
            avatar = {0: 10000, 1: user_id}
            author_id = int(author_id)
            author = Author.objects.get(author_id=author_id)
            author_books = Book.objects.filter(author_id=author_id)
            return render_to_response('author.html',
                                      {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                       'author': author, 'author_books': author_books}, )
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


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
            user = User(user_name=username, password=password, tel=int(tel), email=email,
                        birthday=birthday, age=age, sex=sex, province=province, city=city, remark=remark,
                        create_date=datetime.date.today(), image=0)
            user.save()
            return render_to_response('skip.html', {'instruction': '注册成功'})
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
                return render_to_response('skip.html', {'instruction': '用户不存在'})
            real_pswd = User.objects.get(user_name=username).password
            user_id = User.objects.get(user_name=username).user_id
            if password == real_pswd:
                if user_id == 99999:
                    request.session['user_id'] = user_id
                    return HttpResponseRedirect('/management/')
                else:
                    request.session['user_id'] = user_id
                    return HttpResponseRedirect('/index/')
                    # return HttpResponseRedirect(reverse(get_user_info, args=[user_id]))
            else:
                return render_to_response('skip.html', {'instruction': '密码错误'})
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


@login_required
def index(request):
    """
    主页
    登录后跳转
    :param request:请求
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['user_id'] = user_id
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        hot_book_ids = Book.objects.raw(
            'SELECT book_id,count(book_id) FROM `bims_collectionbook` GROUP BY book_id ORDER BY count(book_id) DESC LIMIT 18')
        hot_books = []
        for hot_book_id in hot_book_ids:
            hot_book = Book.objects.get(book_id=hot_book_id.book_id)
            hot_books.append(hot_book)
        new_books = Book.objects.order_by('-create_date')[0:12]
        hot_authors = Book.objects.raw(
            'SELECT book_id,author_id FROM bims_book GROUP BY author_id ORDER BY count(author_id) DESC LIMIT 3')
        authors_and_books = []
        for author in hot_authors:
            author_books = get_author_book(author.author_id)[0:5]
            author_and_book = {
                'author': author,
                'books': author_books
            }
            authors_and_books.append(author_and_book)
        hot_tags = Book.objects.raw(
            'SELECT book_id,title FROM bims_book GROUP BY title ORDER BY count(title) DESC LIMIT 3')
        tags_and_books = []
        for hot_tag in hot_tags:
            books = Book.objects.filter(title=hot_tag.title)[0:5]
            tag_and_books = {
                'tag': hot_tag.title,
                'books': books
            }
            tags_and_books.append(tag_and_books)
        return render_to_response('index.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                   'hot_books': hot_books, 'new_books': new_books,
                                   'authors_and_books': authors_and_books,
                                   'tags_and_books': tags_and_books})


@login_required
def explore(request):
    """
    发型页面
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['user_id'] = user_id
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        book = Book.objects.get(book_id=random.randint(10001, Book.objects.all().count()+10000))
        note = BookNote.objects.get(note_id=random.randint(10001, BookNote.objects.all().count()+10000))
        author = Author.objects.get(author_id=random.randint(10001, Author.objects.all().count()+10000))
        return render_to_response('explore.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                   'book': book, 'note': note, 'author': author})


@login_required
def all_tags(request):
    """
    所有分类
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['user_id'] = user_id
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        return render_to_response('alltags.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image]})


@login_required
def result(request, page):
    """
    搜索结果界面
    :param request:请求
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        keyword = request.session.get('keyword', ' ')
        search_results = search(keyword)
        if len(search_results) % 10 == 0:
            result_pages = [i for i in range(int(len(search_results)/10)+1)]
        else:
            result_pages = [i for i in range(int(len(search_results)/10)+2)]
        search_results = search_results[0+(10*int(page))-10:10+(10*int(page))-10]
        return render_to_response('result.html',
                                  {
                                      'sreach_form': sreach_form,
                                      'user': user,
                                      'avatar': avatar[user.image],
                                      'results': search_results,
                                      'result_pages': {'result_pages': result_pages, 'len': len(result_pages)-1},
                                      'page': {'prev': int(page)-1, 'now': int(page), 'next': int(page)+1},
                                      'title': '搜索结果'
                                  })


@login_required
def get_hot_book(request):
    """
    热门图书
    :param request: 请求
    :return: 热门图书结果界面
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        hot_book_ids = Book.objects.raw(
            'SELECT book_id FROM bims_collectionbook GROUP BY book_id ORDER BY count(book_id) DESC LIMIT 20')
        hot_books = []
        for hot_book_id in hot_book_ids:
            hot_book = Book.objects.get(book_id=hot_book_id.book_id)
            hot_books.append(hot_book)
        return render_to_response('result.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                   'results': hot_books, 'title': '热门图书'})


@login_required
def get_new_book(request):
    """
    最新图书
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        new_books = Book.objects.order_by('-create_date')[0:20]
        return render_to_response('result.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                   'results': new_books, 'title': '最新上架'})


@login_required
def get_tag_book(request, tag, page):
    """
    图书分类
    :param request: 请求
    :param tag: 图书的标签
    :return: 返回分类的图书
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        tag_books = Book.objects.filter(title=tag)
        if len(tag_books)%10 == 0:
            result_pages = [i for i in range(int(len(tag_books)/10))]
        else:
            result_pages = [i for i in range(int(len(tag_books)/10)+1)]
        # result_pages = [i for i in range(len(tag_books)/10)]
        return render_to_response('result.html',
                                  {
                                      'sreach_form': sreach_form,
                                      'user': user,
                                      'avatar': avatar[user.image],
                                      'result_pages': {'result_pages': result_pages, 'len': len(result_pages) - 1},
                                      'page': {'prev': int(page) - 1, 'now': int(page), 'next': int(page) + 1},
                                      'results': tag_books,
                                      'title': tag + '类所有图书'
                                  })


def add_evaluate(request):
    """
    添加评价
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        evaluate_form = EvaluateForm(request.POST)
        if evaluate_form.is_valid():
            content = evaluate_form.cleaned_data['evaluate']
            book_id = evaluate_form.cleaned_data['book_id']
            user_name = User.objects.get(user_id=user_id).user_name
            evaluate = BookEvaluate(book_id=book_id, user_name=user_name, content=content,
                                    create_date=datetime.date.today())
            evaluate.save()
            return HttpResponseRedirect('/book/' + book_id)
    else:
        return render_to_response('index.html', )


@login_required
def add_note(request):
    """
    添加读书笔记
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            book_id = note_form.cleaned_data['book_id']
            user = User.objects.get(user_id=user_id)
            book = Book.objects.get(book_id=book_id)
            avatar = {0: 10000, 1: user_id}
            sreach_form = SreachForm()
            note_form = NoteForm()
            return render_to_response('addnote.html',
                                      {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                       'book': book, 'note_form': note_form})
    else:
        return render_to_response('index.html', )


@login_required
def save_note(request):
    """
    保存读书笔记
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            book_id = note_form.cleaned_data['book_id']
            user_name = User.objects.get(user_id=user_id)
            title = note_form.cleaned_data['title']
            content = note_form.cleaned_data['content']
            book_note = BookNote(book_id=book_id, user_id=user_id, user_name=user_name, title=title,
                                 content=content, create_date=datetime.date.today())
            book_note.save()
            return HttpResponseRedirect('/book/' + book_id)
    else:
        return render_to_response('index.html', )


def get_note(request, note_id):
    """
    读书笔记主页
    :param request: 请求
    :param note_id:读书笔记ID
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['user_id'] = user_id
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        note = BookNote.objects.get(note_id=int(note_id))
        return render_to_response('note.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                   'note': note}, )


@login_required
def add_book_collection(request, book_id):
    """
    添加图书收藏
    :param request:请求
    :param book_id:图书ID
    :return:
    """
    user_id = request.session.get('user_id', )
    evaluate = CollectionBook(user_id=user_id, book_id=int(book_id), create_date=datetime.date.today())
    evaluate.save()
    return HttpResponseRedirect('/book/' + book_id)


@login_required
def set_userinfo(request):
    """
    修改用户信息
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    user = User.objects.get(user_id=user_id)
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            tel = register_form.cleaned_data['tel']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            birthday = register_form.cleaned_data['birthday']
            age = int(str(datetime.date.today())[0:4]) - int(str(birthday)[0:4])
            province = register_form.cleaned_data['province']
            city = register_form.cleaned_data['city']
            remark = register_form.cleaned_data['remark']
            upload = register_form.cleaned_data['image']
            if upload:
                image = open('BIMS/static/image/avatar/hd/% s.jpg' %
                             str(user_id), 'wb')
                image.write(upload.read())
                image.close()
                image_state = 1
            else:
                image_state = 0
            user = User(user_id=user_id, user_name=username, password=user.password, tel=int(tel), email=email,
                        birthday=birthday, age=age, sex=sex, province=province, city=city, remark=remark,
                        image=image_state, create_date=user.create_date)
            user.save()
            return HttpResponseRedirect('/user/')
        else:
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                results = search(keyword)
                return render_to_response('result.html', {'results': results})
    else:
        sreach_form = SreachForm()
        userinfo = {
            'username': user.user_name,
            'password': user.password,
            'tel': user.tel,
            'email': user.email,
            'birthday': user.birthday,
            'province': user.province,
            'city': user.city,
            'remark': user.remark
        }
        register_form = RegisterForm(userinfo)
        avatar = {0: 10000, 1: user_id}
        return render_to_response('setuserinfo.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                   'register_form': register_form}, )


@login_required
def add_book(request):
    """
    添加书籍(管理员)
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_name = book_form.cleaned_data['book_name']
            author_name = book_form.cleaned_data['author_name']
            press_house = book_form.cleaned_data['press_house']
            translator = book_form.cleaned_data['translator']
            publication_date = book_form.cleaned_data['publication_date']
            pages = book_form.cleaned_data['pages']
            price = book_form.cleaned_data['price']
            package = book_form.cleaned_data['package']
            isbn = book_form.cleaned_data['isbn']
            content_summary = book_form.cleaned_data['content_summary']
            title = book_form.cleaned_data['title']
            try:
                author = Author.objects.get(
                    author_name__contains=author_name)
            except Author.DoesNotExist:
                author_max_id = Author.objects.all()
                author_id = int(author_max_id.aggregate(
                    Max('author_id'))['author_id__max']) + 1
            else:
                author_id = author.author_id
            book = Book(book_name=book_name, author_name=author_name, press_house=press_house,
                        translator=translator, publication_date=publication_date, pages=pages, price=price,
                        package=package, isbn=isbn, content_summary=content_summary, title=title,
                        author_id=author_id, create_date=datetime.date.today())
            book.save()
            try:
                Author.objects.get(author_id=author_id)
            except Author.DoesNotExist:
                author = Author(author_id=author_id,
                                author_name=author_name)
                author.save()
            else:
                pass
            upload = book_form.cleaned_data['image']
            if upload:
                image = open('BIMS/static/image/book/cover/% s.jpg' %
                             str(book.book_id), 'wb')
                image.write(upload.read())
                image.close()
            return HttpResponseRedirect('/index/')
        else:
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                results = search(keyword)
                return render_to_response('result.html', {'results': results})
    else:
        book_form = BookForm()
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        return render_to_response('addbook.html',
                                  {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                   'book_form': book_form}, )


@login_required
def management(request):
    """
    管理员界面
    :param request:请求
    return:管理员界面
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['user_id'] = user_id
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        sreach_form = SreachForm()
        user = User.objects.get(user_id=user_id)
        avatar = {0: 10000, 1: user_id}
        user_count = User.objects.all().count() - 1
        book_count = Book.objects.all().count()
        author_count = Author.objects.all().count()
        all_users = User.objects.all().exclude(user_id=99999)
        return render_to_response('management.html', {
            'sreach_form': sreach_form,
            'user': user,
            'avatar': avatar[user.image],
            'user_count': user_count,
            'book_count': book_count,
            'author_count': author_count,
            'all_users': all_users
        }, )


@login_required
def sys_info(request):
    """
    系统信息
    :param request:请求
    """
    user_id = request.session.get('user_id', )
    if request.method == 'POST':
        sreach_form = SreachForm(request.POST)
        if sreach_form.is_valid():
            keyword = sreach_form.cleaned_data['sreach']
            request.session['user_id'] = user_id
            request.session['keyword'] = keyword
            return HttpResponseRedirect('/result/1/')
    else:
        titles_and_counts = Book.objects.raw(
            'select book_id,title,count(1) as count from bims_book group by title'
        )
        titles = [title_and_count.title for title_and_count in titles_and_counts]
        counts = [title_and_count.count for title_and_count in titles_and_counts]
        trace = go.Pie(labels=titles, values=counts)
        py.plot([trace], filename='E:/GitHub/Book_Info_Manager_System/BIMS/templates/pie-for-dashboard', auto_open=False)
        # py.plot(book_data, filename='E:/GitHub/Book_Info_Manager_System/BIMS/templates/sysinfo', auto_open=False)
        return render_to_response('pie-for-dashboard.html')


@login_required
def add_book_score(request, book_id):
    """
    图书评分
    """
    user_id = request.session.get('user_id', )
    if request.is_ajax():
        score = request.POST.get('book_score')
        book_score = BookScore(user_id=user_id, book_id=book_id, score=score, create_date=datetime.date.today())
        book_score.save()
        response = HttpResponse('successed')
        response.status_code = 204
        return response
    else:
        return HttpResponseRedirect('/book/' + book_id)

@login_required
def test_deco(request, user_id):
    """
    装饰器测试
    """
    info = 'user id is %d' % int(user_id)
    return HttpResponse(info)
