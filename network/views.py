from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow


def index(request):

    posts = Post.objects.all().order_by("-datetime")

    return render(request, "network/index.html", {
        "posts": posts,
    })


def profile(request, user):

    # Get user from database
    profile_user = User.objects.get(username = user)

    # Get user's posts
    posts = Post.objects.filter(user = profile_user).order_by("-datetime")

    # Render profile page
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
    })


def create_post(request):
    if request.method == "POST":

        content = request.POST["new-post-content-textarea"].strip()

        if not content:
            # Create error message
            messages.error(request, "Post cannot be empty", extra_tags="danger")
            return HttpResponseRedirect(reverse("index"))

        post = Post(
            content = content,
            user = request.user,
        )
        post.save()

        messages.success(request, "Post was created successfully")
        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def is_following(request, username):
    if request.method == "GET":

        # Get all user's followings
        all_followings = Follow.objects.filter(follower = request.user.id)
        # Get user that must be followed
        followed_user = User.objects.get(username = username)
        
        # Check if the user already following
        is_following = all_followings.filter(followed_user = followed_user.id).exists()
        
        return JsonResponse({"is_following": is_following})
    
    elif request.method == "POST":
        return 0
    elif request.method == "DELETE":
        return 0



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
