from django.db import models

from Users.models import SiteUser


class Chat(models.Model):
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE, verbose_name="打开此聊天上下文的用户")
    messages = models.TextField(verbose_name="JSON化聊天内容")
