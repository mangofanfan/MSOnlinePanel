from django.shortcuts import render

def index(request):
    context = {
        "num_school": 6,
        "num_user": 26782,
        "sidebars":
            [

            ],
        "global_page_top": True,
    }
    return render(request, "MSOnlinePanel/index.html", context)

def about(request):
    return render(request, "MSOnlinePanel/about.html")