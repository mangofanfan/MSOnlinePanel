from django.shortcuts import render
from django.template.loader import render_to_string

from Users.models import SiteUser


def index(request):
    context = {
        "num_school": 6,
        "num_user": 26782,
        "sidebars":
            [

            ],
        "global_page_top": True,
    }
    context_user = {}
    try: _user = SiteUser.objects.get(id=request.session.get("login_user_id"))
    except SiteUser.DoesNotExist: pass
    else:
        context_user = {
            "id": _user.id,
            "nick_name": _user.nick_name,
            "sign": _user.sign,
            "cover_image": _user.cover_image,
        }
    context["sidebars"].append(render_to_string("Users/user_sidebar_widget.html", context_user, request))
    return render(request, "MSOnlinePanel/index.html", context)

def about(request):
    return render(request, "MSOnlinePanel/about.html")