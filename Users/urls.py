from django.urls import path

from . import views

urlpatterns = [
    path("<int:input_id>/", views.user, name="user"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("me/", views.me, name="me"),
]