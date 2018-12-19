from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


def update_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

    # 返回数据,(使用ajax)
        data = dict()
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text

        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data = dict()
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)


    ''' 不使用ajax
        return redirect(referer)
    else:
        context = {'message': comment_form.errors, 'redirect_to': referer}
        return render(request, 'blog/error.html', context)
    '''




'''
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    # 数据检查

    if not request.user.is_authenticated:
        context = {'message': '用户未登陆', 'redirect_to': referer}
        return render(request, 'blog/error.html', context)

    text = request.POST.get('text', '').strip()
    if text == '':
        context = {'message': '评论内容为空', 'redirect_to': referer}
        return render(request, 'blog/error.html', context)

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        context = {'message': '评论对象不存在', 'redirect_to': referer}
        return render(request, 'blog/error.html', context)
    # 检查通过，保存数据
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    referer = request.META.get('HTTP_REFERER', reverse('home'))
    return redirect(referer)

'''