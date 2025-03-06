import hashlib
import os

from django.http import FileResponse, JsonResponse, Http404
from django.shortcuts import render, redirect

from Users.models import SiteUser
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
    context = {
        "form": UploadForm(),
        "global_page_top": True,
    }
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            md5, filename = handle_upload_file(request, request.FILES.get('file'))
            context["status"] = "success"
            context["msg"] = f"文件 <a href='/upload/{md5}/'>{filename}</a> 上传成功，MD5：{md5}。<button class='btn btn-success' onClick='copyMd5(\"{md5}\")'>点击复制</button>"
            return render(request, "Upload/upload.html", context)
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
        }
    }
    return render(request, "Upload/file_page.html", context)


def file(request, md5: str):
    return FileResponse(open(os.path.join(UPLOAD_ROOT, md5), "rb"), content_type="image/jpeg")
