from django import forms

from Users.models import SiteUser


class SignUpForm(forms.Form):
    nick_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label="昵称",
                                help_text="昵称会被用作标记并显示您的个人资料")
    rel_name = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label="真实姓名",
                               help_text="您的真实姓名不会被其他人知道")
    student_number = forms.CharField(required=True,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     label="学号",
                                     help_text="请填写您的校内学号")
    phone_number = forms.CharField(required=True,
                                   max_length=11,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   label="电话号码",
                                   help_text="我们需要您的联系方式，以备不时之需")
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label="密码",
                               help_text="为这个账户设置一个密码")

    """class Meta:
        model = SiteUser
        fields = ('nick_name', 'rel_name', 'student_number', 'phone_number', 'password')"""


class LoginForm(forms.Form):
    student_number = forms.CharField(required=True,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     label="学号",)
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label="密码")