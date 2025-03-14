from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload, name="upload"),
    path("vditor/", views.upload_vditor, name="vditor"),
    path("<str:md5>/", views.page, name="page"),
    path("file/<str:md5>/", views.file, name="file"),
]