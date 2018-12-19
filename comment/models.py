from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 代表哪个app下的哪张表
    object_id = models.PositiveIntegerField()  # 代表哪张表中的对象id
    content_object = GenericForeignKey('content_type', 'object_id')  # 不会生成额外的列

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = verbose_name = '评论'
        ordering = ['-comment_time']
