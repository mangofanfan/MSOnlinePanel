from django.shortcuts import render
from django.template.loader import render_to_string

from Users.models import SiteUser
from Users.views import get_user_sidebar_widget


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
    except SiteUser.DoesNotExist: _user = None
    context["sidebars"].append(get_user_sidebar_widget(request, _user))
    return render(request, "MSOnlinePanel/index.html", context)

def about(request):
    return render(request, "MSOnlinePanel/about.html")