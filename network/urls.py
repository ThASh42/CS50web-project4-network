
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("create-post", views.create_post, name="create_post"),
    path("edit-post/<int:post_id>", views.edit_post, name="edit_post"),
    path("pg/<str:user>", views.profile, name="profile"),

    # API paths
    path("pg/<str:username>/is-following", views.is_following, name="is_following"),
    path("post-like/<int:post_id>", views.post_like, name="post_like"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
