from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadNumExpandMethod, ReadDetail
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation


class BlogType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField('博客类型', max_length=15)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name_plural = verbose_name = '博客类型'


class Blog(models.Model, ReadNumExpandMethod):
    id = models.AutoField(primary_key=True)
    title = models.CharField('标题', max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='博客类型')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_updated_time = models.DateTimeField('修改时间', auto_now=True)
    content = RichTextUploadingField()

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        verbose_name = verbose_name_plural = '博客'
        ordering = ['-created_time']
