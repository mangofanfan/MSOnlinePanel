import json

from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from Upload.models import File
from Users.models import SiteUser
from Users.views import get_user_link
from .models import Post, Notice


def post(request, input_id):
    try:
        _post = Post.objects.get(id=input_id)
    except Post.DoesNotExist:
        raise Http404("请求的文章不存在")
    else:
        context = {
            "input_id": _post.id,
            "post": _post,
            "is_markdown_content": _post.is_markdown,
            "sidebars": [
                get_user_link(request, _post.author),
            ]
        }
        return render(request, "Posts/post.html", context)


def notice(request, input_id):
    try:
        _post = Notice.objects.get(id=input_id)
    except Notice.DoesNotExist:
        raise Http404("请求的通知不存在")
    else:
        context = {
            "input_id": _post.id,
            "post": _post,
            "is_markdown_content": _post.is_markdown,
        }
        return render(request, "Posts/notice.html", context)


def post_list(request):
    posts = Post.objects.all().order_by("-post_time")[:12]
    files = File.objects.all().order_by("-uploaded_at")[:18]
    notices = Notice.objects.all().order_by("-post_time")[:6]
    context = {
        "posts": posts,
        "files": files,
        "notices": notices,
    }
    return render(request, "Posts/list.html", context)


def post_edit(request):
    # 只允许登录的用户使用编辑器
    if (_id:=request.session.get("login_user_id")) is None:
        return redirect("/user/login/")

    context = {
        "global_page_top": True,
    }
    _user = SiteUser.objects.get(id=_id)
    if request.method == "POST":
        data = json.loads(request.body)
        if Post.objects.filter(title=data["title"], author=_user):
            return JsonResponse({"status": "warning", "msg": "您似乎已经发布过同名的文章，请更换一个标题再尝试，或检查是否重复发布。"})
        try:
            _image = File.objects.get(md5=data["image"])
        except File.DoesNotExist:
            _image = None
        _post = Post.objects.create(
            title=data["title"],
            content=data["md_content"],
            author=_user,
            is_markdown=True,
            image=_image,
        )
        return JsonResponse({"status": "success", "post_id": _post.id})
    else:
        return render(request, "Posts/post_edit.html", context)
