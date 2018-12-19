from django.shortcuts import render,  get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.cache import cache
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read,\
    get_seven_days_read_data, get_today_read_data, get_yesterday_read_data


import datetime


each_page_blogs_number = 2


def get_blog_list_from_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, each_page_blogs_number)  # 将博客列表分成指定篇数一页
    page_num = request.GET.get('page', 1)           # 获取url页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)    # 每页的博客

    current_page_num = page_of_blogs.number         # 获取当前页码数
    page_range = list(range(max(current_page_num-2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num+2, paginator.num_pages)+1))  # 页码数列表
    # 加上省略号
    if page_range[0]-1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上第一页和最后一页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类对应博客数量
    blog_types_list = []
    blog_types = BlogType.objects.all()
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count  # 给blog_type绑定属性并赋值
        blog_types_list.append(blog_type)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = dict()
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = dict()    # 事实上，{}和dict()是一样的
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = blog_types_list
    context['blog_dates'] = blog_dates_dict
    return context


def get_7_days_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
        .filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:5]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)

    # 获取7天热门博客缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blog()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 60*60)
        print('calc')
    else:
        print('use cache')
    context = dict()
    context['dates'], context['read_nums'] = get_seven_days_read_data(blog_content_type)
    context['today_hot_data'] = get_today_read_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_read_data(blog_content_type)
    context['week_hot_data'] = hot_blogs_for_7_days
    return render(request, 'blog/home.html', context)


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_from_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_from_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_from_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_with_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    context = dict()
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['user'] = request.user
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response
