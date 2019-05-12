from datetime import datetime
from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='机构')
    name = models.CharField(max_length=52, verbose_name='课程名字')
    teacher = models.ForeignKey(Teacher, verbose_name='老师')
    desc = models.CharField(max_length=300, verbose_name='课程描绘')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=(('cj', '初级课程'), ('zj', '中级课程'), ('gj', '高级课程')), max_length=2, verbose_name='课程等级')
    learn_times = models.IntegerField(default=0, verbose_name='学习时常(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', max_length=100, verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播图')
    category = models.CharField(default='后端', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=100, verbose_name='课程标签')
    youneed_know = models.CharField(default='', max_length=300, verbose_name='课程须知')
    teacher_tell = models.CharField(default='', max_length=200, verbose_name='老师告诉你能学什么')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta():
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=20, verbose_name='视频名')
    url = models.URLField(default='www.baidu.com', max_length=100, verbose_name='视频地址')
    learn_times = models.IntegerField(default=0, verbose_name='视频时长')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=20, verbose_name='资源名')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name='资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



