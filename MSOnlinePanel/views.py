from django.shortcuts import render

from Posts.models import Post
from Users.models import SiteUser
from Users.views import get_user_sidebar_widget


def index(request):
    context = {
        "num_school": 6,
        "num_user": 26782,
        "sidebars": [],
        "global_page_top": True,
        "posts": []
    }
    # 加载用户侧边栏，包括访客边栏
    try: _user = SiteUser.objects.get(id=request.session.get("login_user_id"))
    except SiteUser.DoesNotExist: _user = None
    context["sidebars"].append(get_user_sidebar_widget(request, _user))

    # 获取首页文章
    # 根据 https://blog.csdn.net/cugbabybear/article/details/17141103 ，在数据量一般的情况下，采用如下方法是可接受的
    for _post in Post.objects.order_by("-post_time")[:2]:
        context["posts"].append(_post)
    for _post in Post.objects.order_by("?")[:2]:
        context["posts"].append(_post)

    return render(request, "MSOnlinePanel/index.html", context)

def about(request):
    return render(request, "MSOnlinePanel/about.html")