from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path("post/<int:input_id>/", views.post, name="post"),
    path("notice/<int:input_id>/", views.notice, name="notice"),
    path("edit/<int:input_id>/", views.post_edit, name="post_edit"),
    path("edit/", views.post_publish, name="post_edit"),
]