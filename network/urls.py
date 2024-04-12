
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("create-post", views.create_post, name="create_post"),
    path("pg/<str:user>", views.profile, name="profile"),

    # API paths
    path("pg/<str:username>/is-following", views.is_following, name="is_following"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
