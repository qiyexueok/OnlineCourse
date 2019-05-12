# -*- coding:utf-8 -*- 
__author__ = 'll'
__date__ = '19-5-12 上午9:53'

from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [

    url(r'^info/$', UserInfoView.as_view(), name='user_info'),


    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),


    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),


    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),


    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),


    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),


    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),


    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),


    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),


    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]