"""GraduationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

import BIMS.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/image/favicon.ico')),
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/$', views.get_user_info, name='user'),
    url(r'^book/(\d+)/$', views.get_book_info, name='book'),
    url(r'^author/(\d+)/$', views.get_author_info, name='author'),
    url(r'^index/$', views.index, name='index'),
    url(r'^result/(\d+)/$', views.result, name='result'),
    url(r'^hotbook/$', views.get_hot_book, name='hotbook'),
    url(r'^newbook/$', views.get_new_book, name='newbook'),
    url(r'^tag/(.+)/(\d+)/$', views.get_tag_book, name='tag'),
    url(r'^evaluate/$', views.add_evaluate, name='evaluate'),
    url(r'^addnote/$', views.add_note, name='addnote'),
    url(r'^savenote/$', views.save_note, name='savenote'),
    url(r'^note/(\d+)/$', views.get_note, name='note'),
    url(r'^explore/$', views.explore, name='explore'),
    url(r'^alltags/$', views.all_tags, name='alltags'),
    url(r'^addbookcollection/(\d+)/$', views.add_book_collection, name='addbookcollection'),
    url(r'^addauthorcollection/(\d+)/$', views.add_author_collection, name='addauthorcollection'),
    url(r'^delbookcollection/$', views.del_book_collection, name='delbookcollection'),
    url(r'^delauthorcollection/(\d+)/$', views.del_author_collection, name='delauthorcollection'),
    url(r'^setuserinfo/$', views.set_userinfo, name='setuserinfo'),
    url(r'^addbook/$', views.add_book, name='addbook'),
    url(r'^management/$', views.management, name='management'),
    url(r'^sysinfo/$', views.sys_info, name='sysinfo'),
    url(r'^score/(\d+)/$', views.add_book_score, name='score')
    ]
