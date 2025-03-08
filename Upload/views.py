import hashlib
import json
import os

from django.http import FileResponse, JsonResponse, Http404
from django.shortcuts import render, redirect

from Users.models import SiteUser
from Users.views import get_user_link
from .forms import UploadForm
from .models import File

UPLOAD_ROOT = os.path.dirname(os.path.dirname(__file__)) + "/MSOnlinePanel/upload/"

def handle_upload_file(request, _file):
    hc = hashlib.md5()
    for chuck in _file.chunks():
        hc.update(chuck)
    filename = hc.hexdigest()
    with open(os.path.join(UPLOAD_ROOT, filename), "wb+") as f:
        for chuck in _file.chunks():
            f.write(chuck)
    File.objects.create(md5=filename,
                        filename=_file.name,
                        uploader=SiteUser.objects.get(id=request.session.get("login_user_id")))
    return filename, _file.name



def upload(request):
    if request.session.get("login_user_id") is None:
        return redirect("/user/login/")
    context = {
        "form": UploadForm(),
        "global_page_top": True,
    }
    if request.method == "POST":
        try:
            md5, filename = handle_upload_file(request, request.FILES.get('file'))
            return JsonResponse({"status": "success", "md5": md5, "filename": filename})
        except Exception:
            return JsonResponse({"status": "error", "message": "出现了一些问题，文件上传失败。"})
    else:
        return render(request, "Upload/upload.html", context)


def upload_vditor(request):
    if request.method == "POST":
        md5, filename = handle_upload_file(request, request.FILES.get("file[]"))
        return JsonResponse({"filename": filename, "md5": md5})
    else:
        return redirect("/upload/")


def page(request, md5: str):
    try:
        _file = File.objects.get(md5=md5)
    except File.DoesNotExist:
        raise Http404("请求的图片未找到。")
    context = {
        "file": {
            "name": _file.filename,
            "md5": md5,
            "uploader": _file.uploader,
            "uploaded_at": _file.uploaded_at,
        },
        "sidebars": [
            get_user_link(request, _file.uploader),
        ]
    }
    return render(request, "Upload/file_page.html", context)


def file(request, md5: str):
    return FileResponse(open(os.path.join(UPLOAD_ROOT, md5), "rb"), content_type="image/jpeg")
