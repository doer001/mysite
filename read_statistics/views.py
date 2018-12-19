from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums = get_seven_days_read_data(blog_content_type)
    context = dict()
    context['read_nums'] = read_nums
    return render(request, 'blog/home.html', context)
