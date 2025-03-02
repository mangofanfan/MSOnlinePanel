from django.db import models

from Users.models import SiteUser


class File(models.Model):
    filename = models.CharField(max_length=255)
    md5 = models.CharField(max_length=32, unique=True)
    uploader = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = verbose_name
