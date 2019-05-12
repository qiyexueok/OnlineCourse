# -*- coding:utf-8 -*- 
__author__ = 'll'
__date__ = '19-4-27 下午4:13'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner, UserProfile

class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '在线管理系统'
    site_footer = '在线系统'
    menu_style = 'accordion'


class UserProfileAdmin(object):
    list_display = ['username', 'nick_name', 'gender', 'birthday', 'address', 'mobile']
    search_fields = ['username', 'nick_name', 'gender', 'birthday', 'address', 'mobile']
    list_filter = ['username', 'nick_name', 'gender', 'birthday', 'address', 'mobile']


class BannerAdmin(object):
    list_display = ['title', 'url', 'image', 'index', 'add_time']
    search_fields = ['title', 'url', 'image', 'index']
    list_filter = ['title', 'url', 'image', 'index', 'add_time']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
