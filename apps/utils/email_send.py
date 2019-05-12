# -*- coding:utf-8 -*- 
__author__ = 'll'
__date__ = '19-4-28 下午4:19'

from random import Random
import string

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    emial_record.save()

    if send_type == 'register':
        email_title = '慕学在线注册激活'
        email_body = '请点击下面链接激活账户：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('发送成功')

    elif send_type == 'forget':
        email_title = '慕学在线重置密码'
        email_body = '请点击下面链接重置账户：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('发送成功')

    elif send_type == 'update_email':
        email_title = '慕学在线修改邮箱'
        email_body = '请点击下面链接修改邮箱：http://127.0.0.1:8000/update/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FORM, [email])
        if send_status:
            print('发送成功')


def random_str(random_length=16):
    code = ''
    chars = string.ascii_letters + str(string.digits)
    length = len(chars) - 1
    for i in range(random_length):
        code += chars[Random.randint(0, length)]
    return code

