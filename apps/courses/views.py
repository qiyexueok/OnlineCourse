# -*- coding:utf-8 -*-

import json

from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import EmptyPage, Paginator, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, UserCourse, CourseComments
from utils.mixin_utils import LoginRequiredMixin


#课程列表首页
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                             Q(desc__icontains=search_keywords)|
                                             Q(detail__icontains=search_keywords)
                                             )

        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_course.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Pagonator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'courses/course-list.html',{
                      'courses': courses,
                      'hot_courses': hot_courses,
                      'sort': sort,
        })


#课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.click_nums += 1
        course.save()

        tag = course.tag
        relate_courses = []
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id,type=2):
                has_fav_org = True

        return render(request, 'courses/course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


#课程信息
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'courses/course-video.html', {
            'course': course,
            'relate_courses': relate_courses,
            'all_resources': all_resources,

        })


#课程评论
class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids =[user_course.course.id for user_course in all_user_courses]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'courses/course-comment.html', {
            'course': course,
            'all_comments': all_comments,
            'relate_courses': relate_courses,
            'all_resources': all_resources,
        })


#添加评论
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        res = dict()

        if request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg'] = '没有登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')

        if course_id and comments:
            course_comment = Coursecomment()
            course_comment.course = Course.objects.get(int(course_id))
            course_comment.user = request.user
            course_commment.comment = comments
            course_comment.save()
            res['status'] = 'success'
            res['msg'] = '评论成功'
        else:
            res['status'] = 'fail'
            res['msg'] = '评论失败'

        return HttpResponse(json.dumps(res), content_type='application/json')


#课程播放信息
class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = vidoe.lesson.course

        user_courses = UserCourse.object.filter(user=request.user, course=course)
        if not user_course:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'courses/course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video,
        })

















