from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class SiteUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name="ID")
    student_number = models.CharField(unique=True, max_length=10, verbose_name="学号")
    password = models.CharField(max_length=20, verbose_name="密码")
    rel_name = models.CharField(max_length=20, verbose_name="真实姓名")
    nick_name = models.CharField(max_length=20, verbose_name="显示昵称")
    phone_number = models.CharField(max_length=11, verbose_name="电话号码")
    sign = models.TextField(null=True, blank=True, verbose_name="个性签名")
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    login_time = models.DateTimeField(auto_now=True, verbose_name="上次编辑时间")

    value_P = models.IntegerField(null=True, blank=True, validators=(MinValueValidator(0), MaxValueValidator(100)), verbose_name="最终指标P")
    value_Q1 = models.IntegerField(null=True, blank=True, validators=(MinValueValidator(0), MaxValueValidator(100)), verbose_name="生理指标Q1")
    value_Q2 = models.IntegerField(null=True, blank=True, validators=(MinValueValidator(0), MaxValueValidator(100)), verbose_name="网络指标Q2")
    value_Q3 = models.IntegerField(null=True, blank=True, validators=(MinValueValidator(0), MaxValueValidator(100)), verbose_name="行为指标Q3")

    def __str__(self):
        return f"[ 用户 {self.student_number} {self.rel_name} ]"

    class Meta:
        verbose_name = "心理健康用户"
        verbose_name_plural = verbose_name
