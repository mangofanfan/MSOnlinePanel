from datetime import datetime

from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import loader

from MSOnlinePanel.settings import SITE_URL
from .forms import SignUpForm, LoginForm
from .models import SiteUser
from Posts.models import Post


def user(request, input_id):
    try:
        _user = SiteUser.objects.get(id=input_id)
    except SiteUser.DoesNotExist:
        raise Http404("请求的用户不存在")
    else:
        context = {
            "user": {
                "id": _user.id,
                "student_number": _user.student_number,
                "nick_name": _user.nick_name,
                "phone_number": _user.phone_number,
                "register_time": _user.register_time,
                "login_time": _user.login_time,
                "sign": _user.sign,
            },
            "sidebars":
                [get_post_list(request, _user)],
            "global_page_top": True if _user.sign else False,

        }
        return render(request, "Users/user.html", context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            nick_name = request.POST.get('nick_name')
            rel_name = request.POST.get('rel_name')
            phone_number = request.POST.get('phone_number')
            student_number = request.POST.get('student_number')
            password = request.POST.get('password')
            try:
                SiteUser.objects.create(nick_name=nick_name,
                                        rel_name=rel_name,
                                        phone_number=phone_number,
                                        student_number=student_number,
                                        password=password)
                return render(request, "Users/user_signup.html", {"form": form, "signup_success": True, "global_page_top": True})
            except IntegrityError:
                return render(request, "Users/user_signup.html", {"form": form, "msg": "学号已经被占用，请尝试与平台管理员联系。", "global_page_top": True})
        else:
            return render(request, 'Users/user_signup.html', {'form': form, "msg": "表单数据格式验证失败，请重新填写再提交！", "global_page_top": True})
    else:
        form = SignUpForm()
        return render(request, 'Users/user_signup.html', {'form': form, "global_page_top": True})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            student_number = request.POST.get('student_number')
            password = request.POST.get('password')
            try:
                _user = SiteUser.objects.get(student_number=student_number)
            except SiteUser.DoesNotExist:
                return render(request, "Users/user_login.html", {"form": form, "msg": "输入的学号尚未注册。", "global_page_top": True})
            if _user.password == password:
                # 登录成功，跳转到用户中心
                request.session["login_user_id"] = _user.id
                request.session["login_user_name"] = _user.nick_name
                _user.save()
                return redirect("/user/me/")
            else:
                return render(request, "Users/user_login.html", {"form": form, "msg": "输入的密码错误。", "global_page_top": True})
        else:
            return render(request, "Users/user_login.html", {"form": form, "msg": "表单数据格式验证失败，请重新填写再提交！", "global_page_top": True})
    else:
        try: SiteUser.objects.get(id=request.session.get("login_user_id"))
        except SiteUser.DoesNotExist:
            form = LoginForm()
            return render(request, 'Users/user_login.html', {'form': form, "global_page_top": True})
        else:
            return redirect("/user/me/")


def logout(request):
    if request.method == 'POST':
        for _name in ["login_user_id", "login_user_name"]:
            try: del request.session[_name]
            except KeyError: pass
        return redirect(SITE_URL)
    else:
        return render(request, "Users/user_logout.html", {"global_page_top": True})


def me(request):
    # 先获取用户信息
    try: _user = SiteUser.objects.get(id=request.session.get("login_user_id"))
    except KeyError: return redirect("/users/me/")
    context = {
        "user":
            {
                "id": _user.id,
                "student_number": _user.student_number,
                "nick_name": _user.nick_name,
                "rel_name": _user.rel_name,
                "phone_number": _user.phone_number,
                "register_time": _user.register_time,
                "login_time": _user.login_time,
                "value_P": _user.value_P,
                "sign": _user.sign,
            },
        "sidebars":
            [
                get_post_list(request, _user),
                get_user_link(request, _user),
            ],
        "global_page_top": True,
    }

    if request.method == "POST":
        _dict = {}
        try: _dict["nick_name"] = request.POST.get("nick_name")
        except KeyError: pass
        try: _dict["sign"] = request.POST.get("sign")
        except KeyError: pass
        if not _dict:
            context["success"] = False
            context["msg"] = "未获取到需要更新的用户资料或签名。"
            return render(request, "Users/user_me.html", context)
        for key, value in _dict.items():
            if not value: continue
            setattr(_user, key, value)
            _user.save()
        context["success"] = True
        return render(request, "Users/user_me.html", context)

    else:
        return render(request, "Users/user_me.html", context)


def get_post_list(request, _user: SiteUser):
    post_list = []
    for _post in Post.objects.filter(author=_user):
        post_list.append({"id": _post.id, "title": _post.title})
    return loader.render_to_string("Posts/post_list_widget.html", {"prefix": _user.nick_name, "post_list": post_list}, request)


def get_user_link(request, _user: SiteUser):
    return loader.render_to_string("Users/user_link_widget.html", {"prefix": _user.nick_name, "id": _user.id}, request)
