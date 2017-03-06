#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视图层
"""
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
# from django.views.decorators.cache import cache_page

from BIMS.models import User, Book, Author, CollectionBook, CollectionAuthor, BookEvaluate, BookNote, BookScore
from BIMS.tools.forms import LoginForm, RegisterForm, SreachForm, EvaluateForm, NoteForm

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


def get_user_info(request):
    """
    用户信息
    :param request:请求
    :return:用户个人信息
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
                                                    'authors_and_books': authors_and_books, 'notes_and_books': notes_and_books},)
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


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
            sreach_form = SreachForm(request.POST)
            if sreach_form.is_valid():
                keyword = sreach_form.cleaned_data['sreach']
                results = search(keyword)
                return render_to_response('result.html', {'results': results})
        else:
            sreach_form = SreachForm()
            evaluate_form = EvaluateForm()
            note_form = NoteForm()
            user = User.objects.get(user_id=user_id)
            avatar = {0: 10000, 1: user_id}
            book_id = int(book_id)
            book = Book.objects.get(book_id=book_id)
            author = Author.objects.get(author_id=book.author_id)
            book_evaluates = BookEvaluate.objects.filter(book_id=book_id).order_by('-create_date')
            book_evaluates = book_evaluates[0:6] if len(book_evaluates) > 6 else book_evaluates
            book_notes = BookNote.objects.filter(book_id=book_id).order_by('-create_date')
            book_notes = book_notes[0:3] if len(book_notes) > 3 else book_notes
            if int(book.score) == 0:
                score = ''
            else:
                score = book.score
            return render_to_response('book.html', {'sreach_form': sreach_form, 'evaluate_form': evaluate_form, 'user': user, 'avatar': avatar[user.image],
                                                    'book': book, 'score': score, 'author': author, 'book_evaluates': book_evaluates, 'book_notes': book_notes, 'note_form': note_form}, )
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
            create_date = datetime.date.today()
            user = User(user_name=username, password=password, tel=int(tel), email=email,
                        birthday=birthday, age=age, sex=sex, locate=province + city, remark=remark,
                        create_date=create_date, image=0)
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
                # return HttpResponseRedirect(reverse(get_user_info, args=[user_id]))
                request.session['user_id'] = user_id
                return HttpResponseRedirect('/index/')
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


def index(request):
    """
    主页
    登录后跳转
    :param request:请求
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            hot_authors = Book.objects.raw('SELECT book_id,author_id FROM bims_book GROUP BY author_id ORDER BY count(author_id) DESC LIMIT 3')
            authors_and_books = []
            for author in hot_authors:
                author_books = get_author_book(author.author_id)[0:5]
                author_and_book = {
                    'author': author,
                    'books': author_books
                }
                authors_and_books.append(author_and_book)
            hot_tags = Book.objects.raw('SELECT book_id,title FROM bims_book GROUP BY title ORDER BY count(title) DESC LIMIT 3')
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
                                       'hot_books': hot_books, 'new_books': new_books, 'authors_and_books': authors_and_books,
                                       'tags_and_books': tags_and_books})
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def explore(request):
    """
    发型页面
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            book = list(Book.objects.order_by('?')[:2])
            note = list(BookNote.objects.order_by('?')[:2])
            author = list(Author.objects.order_by('?')[:2])
            return render_to_response('explore.html',
                                      {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                       'book1': book[0], 'book2': book[1], 'note1': note[0], 'note2': note[1],
                                       'author1': author[0], 'author2': author[1]})
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def all_tags(request):
    """
    所有分类
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            return render_to_response('alltags.html',
                                      {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image]})
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def result(request):
    """
    搜索结果界面
    :param request:请求
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            search_results = search(keyword)
            return render_to_response('result.html', {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                                      'results': search_results, 'title': '搜索结果'})
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def get_hot_book(request):
    """
    热门图书
    :param request: 请求
    :return: 热门图书结果界面
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            hot_books = Book.objects.order_by('-evaluate_num')[0:20]
            return render_to_response('result.html',
                                      {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                       'results': hot_books, 'title': '热门图书'})
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def get_new_book(request):
    """
    最新图书
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            new_books = Book.objects.order_by('-create_date')[0:20]
            return render_to_response('result.html',
                                      {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                       'results': new_books, 'title': '最新上架'})
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def get_tag_book(request, tag):
    """
    图书分类
    :param request: 请求
    :param tag: 图书的标签
    :return: 返回分类的图书
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            tag_books = Book.objects.filter(title=tag)
            return render_to_response('result.html',
                                      {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image],
                                       'results': tag_books, 'title': tag + '类所有图书'})
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def add_evaluate(request):
    """
    添加评价
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if user_id:
        if request.method == 'POST':
            evaluate_form = EvaluateForm(request.POST)
            if evaluate_form.is_valid():
                content = evaluate_form.cleaned_data['evaluate']
                book_id = evaluate_form.cleaned_data['book_id']
                user_name = User.objects.get(user_id=user_id).user_name
                evaluate = BookEvaluate(book_id=book_id, user_name=user_name, content=content, create_date=datetime.date.today())
                evaluate.save()
                return HttpResponseRedirect('/book/'+book_id)

        else:
            return render_to_response('index.html',)
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def add_note(request):
    """
    添加读书笔记
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def save_note(request):
    """
    保存读书笔记
    :param request: 请求
    :return:
    """
    user_id = request.session.get('user_id', )
    if user_id:
        if request.method == 'POST':
            note_form = NoteForm(request.POST)
            if note_form.is_valid():
                book_id = note_form.cleaned_data['book_id']
                user_name = User.objects.get(user_id=user_id)
                title = note_form.cleaned_data['title']
                content = note_form.cleaned_data['content']
                book_note = BookNote(book_id=book_id, user_id=user_id, user_name=user_name, title=title, content=content, create_date=datetime.date.today())
                book_note.save()
                return HttpResponseRedirect('/book/' + book_id)
        else:
            return render_to_response('index.html', )
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})


def get_note(request, note_id):
    """
    读书笔记主页
    :param request: 请求
    :param note_id:读书笔记ID
    :return:
    """
    user_id = request.session.get('user_id', )
    if user_id:
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
            note = BookNote.objects.get(note_id=int(note_id))
            return render_to_response('note.html', {'sreach_form': sreach_form, 'user': user, 'avatar': avatar[user.image], 'note': note}, )
    else:
        return render_to_response('skip.html', {'instruction': '请先登录'})
