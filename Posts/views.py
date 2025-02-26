from django.http import Http404
from django.shortcuts import render

from .models import Post, Notice


def post(request, input_id):
    try:
        _post = Post.objects.get(id=input_id)
    except Post.DoesNotExist:
        raise Http404("请求的文章不存在")
    else:
        context = {
            "input_id": _post.id,
            "post":
                {"title": _post.title,
                 "content": _post.content,
                 "author": _post.author,
                 "post_time": _post.post_time,
                 "update_time": _post.update_time, }
        }
        return render(request, "posts/post.html", context)


def notice(request, input_id):
    try:
        _post = Notice.objects.get(id=input_id)
    except Notice.DoesNotExist:
        raise Http404("请求的通知不存在")
    else:
        context = {
            "input_id": _post.id,
            "post":
                {"title": _post.title,
                 "content": _post.content,
                 "post_time": _post.post_time,
                 "update_time": _post.update_time, }
        }
        return render(request, "posts/notice.html", context)


def post_list(request):
    posts = Post.objects.all().order_by("-post_time")
    notices = Notice.objects.all().order_by("-post_time")
    context = {
        "posts": posts,
        "notices": notices,
    }
    return render(request, "posts/list.html", context)
