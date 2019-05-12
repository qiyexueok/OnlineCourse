# -*- coding:utf-8 -*-

import json

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UserInfoForm, UploadImageForm
from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


#用户登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponsePermanentRedirect(reverse('index'))
                return render(request, 'login.html', {'message': '用户未激活'})
            return render(request, 'login.html', {'message': '用户或者密码错误'})

        return render(request, 'login.html', {'form_errors': login_form.errors})


#用户登出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponsePermanentRedirect(reverse('index'))


#用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid:
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form}, {'message': '邮箱已注册'})
            password = request.POST.get('password', '')

            user_profiel = UserProfie()
            user_profile.username = email
            user_profiel.email = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕学在线'
            user_message.save()

            send_register_email(email, 'register')
            return render(request, 'send-success.html')

        return render(request, 'register.html', {'register_form': register_form})


#用户注册后，邮箱激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')

        return render(request, 'active-fail.html')


#忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.get(email=email):
                send_register_email(email, 'forget')
                return render(request, 'send-success.html')
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})

        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


#重置密码页面
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecird.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = reocrd.email
                return render(request, 'password-reset.html', {'email': email})
        return render(request, 'active-fail.html')


#重置密码提交新密码页面
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get('eamil', '')
        if modify_form.is_valid:
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password-reset.html', {'email': email, 'message': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        return render(request, 'password-reset.html', {'email': email, 'modify_form': modify_form})


#个人用户信息展示、修改
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoForm(requests.POST, instance=request.user)
        res = dict()

        if user_info_form.is_valid():
            user_info_form.save()
            res['status'] = 'success'
        else:
            res = user_info_form.errors

        return HttpResponse(json.dumps(res), content_type='application/json')


#用户修改头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        res = dict()
        if image_form.is_valid():
            image_form.save()
            res['status'] = 'success'
            res['msg'] = '头像修改成功'
        else:
            res['status'] = 'fail'
            res['msg'] = '头像修改失败'

        return HttpResponse(json.dumps(res), content_type='application/json')


#用户在个人中心修改密码
class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        res = dict()

        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')

            if pwd1 != pwd2:
                res['status'] = 'fail'
                res['msg'] = '密码不一致'
                return HttpResponse(json.dumps(res), content_type='application/json')

            user = request.user
            user.password = make_password(password2)
            user.save()
            res['status'] = 'success'
            res['msg'] = '密码修改成功'

        else:
            res = modify_form.errors

        return HttpResponse(json.dumps(res), content_type='application/json')


#修改邮箱发送验证码
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        res = dict()
        if UserProfile.objects.filter(email=email):
            res['status'] = 'fail'
            res['msg'] = '邮箱已经注册'
            return HttpResponse(json.dumps(res), content_type='application/json')
        send_register_email(email, 'update_email')
        res['status'] = 'success'
        res['msg'] = '发送成功'

        return HttpResponse(json.dumps(res), content_type='application/json')


#修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        code = request.POST.get('code', '')
        email = request.POST.get('email', '')

        exist_records = EmailVerifyRecord.objects.filter(email=email, code=code)
        res = []
        if exist_records:
            user= request.user
            user.email = email
            user.save()
            res['status'] = 'success'
            res['msg'] = '修改成功'
        else:
            res['status'] = 'fail'
            res['msg'] = '修改失败'

        return HttpResponse(json.dumps(res), content_type='application/json')


#我学习的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.object(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


#收藏的机构
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


#收藏的讲师
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


#收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.get(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course = Course.objects.get(id=fav_course.fav_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
                      'course_list': course_list,
        })


#我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user)

        all_unread_message = UserMessage.objects.filter(user=request.user, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 3, request=request)
        message = p.page(p)

        return render(request, 'usercenter-message.html', {
            'message': message,
        })


#慕学在线首页
class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all()
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses':courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


#全局404处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', '')
    response.status_code = 404
    return response

#全局500处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', '')
    response.status_code = 500
    return response



















