# -*- coding:utf-8 -*-

import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserAsk, UserFavorite
from courses.models import Course


#课程机构筛选页
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        all_citys = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get('category', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'fav_nums':
            all_orgs = all_orgs.order_by('-fav_nums')

        org_nums = all_orgs.count()

        try:
            page = request.GET.get('page', '1')
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)

        return render(request, 'oragnization/org-list.html',  {
                        'all_orgs': orgs,
                        'all_citys': all_citys,
                        'org_nums': org_nums,
                        'city_id': city_id,
                        'sort': sort,
                        'category': category,
                        'hot_orgs': hot_orgs,
                      })


#添加用户咨询
class AddUserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        res = dict()
        if user_ask_form.valid():
            user_ask_form.save(commit=True)
            res['status'] = 'success'
        else:
            res['status'] = 'fail'
            res['message'] = '添加出错'
        return ResponseHttp(json.dumps(res), content_type='application/json')


#课程机构详情首页
class OrgHomeView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]

        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        current_page = 'home'

        return render(request, 'oragnization/org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'has_fav': has_fav,
            'current_page': current_page,
            'org_id': org_id,
        })


#课程机构课程页
class OrgCourseView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'course'
        all_courses = course_org.course_set.all()

        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 2, request=request)

        courses = p.page(page)

        return render(request, 'oragnization/org-detail-course.html', {
            'all_courses': all_courses,
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav,
        })


#课程机构介绍页面
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'oragnization/org-detail-desc.html', {
            'course_org': course_org,
            'has_fav': has_fav,
            'current_page': current_page,
        })


#课程机构讲师页
class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        current_page = 'teacher'

        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'oragnization/org-detial-teacher.html', {
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,
            'course_org': course_org,
        })


#用户收藏、取消
class AddFavView(View):
    def set_fav_nums(self, fav_type, fav_id, num=1):
        if fav_type == 1:
            course = course.objects.get(id=int(fav_id))
            course.fav_nums += num
            course.save()
        elif fav_type == 2:
            course_org = courseOrg.objects.get(id=int(fav_id))
            course_org.fav_nums += num
            course_org.save()
        elif fav_type == 3:
            teacher = Teacher.objects.get(id=int(fav_id))
            teacher.fav_nums += num
            teacher.save()

    def post(self, request):
        fav_type = int(request.POST.get('fav_type', 0))
        fav_id = int(request.POST.get('fav_id', 0))

        res = dict()
        if not request.user.is_authenticated():
            res['status'] = 'success'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_type=fav_type, fav_id=fav_id)
        if exist_records:
            exist_records.delete()
            self.set_fav_nums(fav_type, fav_id, -1)
            res['status'] = 'success'
            res['msg'] = '取消收藏'

        else:
            user_fav = UserFavorite()
            if fav_id and fav_type:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                self.set_fav_nums(fav_type, fav_id, 1)

                res['status'] = 'success'
                res['msg'] = '收藏成功'

            else:
                res['status'] = 'fail'
                res['msg'] = '收藏出错'

        return render(json.dumps(res), content_type='application/json')


#讲师列表页
class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.POST.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords)|
                Q(work_company__icontains=search_keywords)|
                Q(work_position__icontains=searchwords)
            )
        sort = request.POST.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)

        return render(request, 'oragnization/teachers-list.html', {
            'teachers': teachers,
            'sorted_teacher': sorted_teacher,
            'sort': sort,
        })


#讲师详情页
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()

        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
                has_teacher_fav = True

        has_org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_org_fav = True

        return render(request, 'oragnization/teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,
        })













