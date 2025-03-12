import json

from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

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
                get_toc(request),
            ]
        }
        if request.session.get("login_user_id") == _post.author.id:
            context["sidebars"].append(get_post_panel(request, _post))
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


def post_publish(request):
    # 只允许登录的用户使用编辑器
    if (_id:=request.session.get("login_user_id")) is None:
        return redirect("/user/login/")

    _user = SiteUser.objects.get(id=_id)
    context = {
        "global_page_top": True,
        "user": _user,
    }
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


def post_edit(request, input_id: int):
    # 只允许登录的用户使用编辑器
    if (_id:=request.session.get("login_user_id")) is None:
        return redirect("/user/login/")
    _user = SiteUser.objects.get(id=_id)

    # 检查文章是否存在，与是否是作者正在编辑
    if (_post:=Post.objects.get(id=input_id)) is None:
        return Http404("请求编辑的文章不存在")
    if _post.author != _user:
        return redirect("/post/")

    context = {
        "global_page_top": True,
        "user": _user,
        "post": _post,
    }
    if request.method == "POST":
        data = json.loads(request.body)
        if len(Post.objects.filter(title=data["title"], author=_user)) > 1:
            return JsonResponse({"status": "warning", "msg": "您似乎已经发布过同名的文章，请更换一个标题再尝试，或检查是否重复发布。"})
        try:
            _image = File.objects.get(md5=data["image"])
        except File.DoesNotExist:
            _image = None
        _post = Post.objects.get(id=input_id)
        _post.title = data["title"]
        _post.content = data["md_content"]
        _post.image = _image
        _post.is_markdown = True
        _post.save()
        return JsonResponse({"status": "success", "post_id": _post.id})
    else:
        return render(request, "Posts/post_edit.html", context)


def get_toc(request):
    return render_to_string("Posts/post_toc_widget.html", {}, request)

def get_post_panel(request, post: Post):
    return render_to_string("Posts/post_panel_widget.html", {"post": post}, request)
