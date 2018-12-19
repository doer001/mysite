from django import template
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm

register = template.Library()
# 注册我们自定义的标签，只有注册过的标签，系统才能认识你，这是固定写法


# @register.simple_tag(name='get_comment_count') 不指定名字默认使用函数名
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)  # 通过model或者model的实例来寻找ContentType类型
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_form = CommentForm(initial={
        'content_type': content_type.model,
        'object_id': obj.pk,
        'reply_comment_id': 0, })
    return comment_form


@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')
