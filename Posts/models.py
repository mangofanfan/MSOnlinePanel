from django.db import models

from Users.models import SiteUser


class Post(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name="ID")
    title = models.CharField(max_length=100, verbose_name="文章标题")
    content = models.TextField(verbose_name="文章内容")
    author = models.ForeignKey(SiteUser, on_delete=models.CASCADE, verbose_name="文章作者")
    post_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def __str__(self):
        return f"[ {self.id} {self.author.__str__()} 的文章 {self.title} ]"

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class Notice(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name="ID")
    title = models.CharField(max_length=100, verbose_name="通知标题")
    content = models.TextField(verbose_name="通知内容")
    post_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def __str__(self):
        return f"[ 通知 {self.id} {self.title} ]"

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = verbose_name


