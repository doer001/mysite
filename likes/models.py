from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 代表哪个app下的哪张表
    object_id = models.PositiveIntegerField()  # 代表哪张表中的对象id
    content_object = GenericForeignKey('content_type', 'object_id')  # 不会生成额外的列

    liked_num = models.IntegerField(default=0)


class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 代表哪个app下的哪张表
    object_id = models.PositiveIntegerField()  # 代表哪张表中的对象id
    content_object = GenericForeignKey('content_type', 'object_id')  # 不会生成额外的列

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)
