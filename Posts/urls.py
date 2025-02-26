from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path("post/<int:input_id>/", views.post, name="post"),
    path("notice/<int:input_id>/", views.notice, name="notice"),
]