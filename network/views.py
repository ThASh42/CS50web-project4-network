import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow


def index(request):

    # Get all posts
    posts = Post.objects.all().order_by("-datetime")

    # Use paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, f"network/index.html", {
        "page_obj": page_obj,
        "range_pages": range(1, 1 + paginator.num_pages),
    })


@login_required
def following(request):
    # Get current user
    current_user = request.user
    # Get all model objects of followed people by current user
    all_following = Follow.objects.filter(follower = current_user)
    # Receive all posts from your followers
    posts = Post.objects.filter(user__in = all_following.values("followed_user")).order_by("-datetime")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "range_pages": range(1, 1 + paginator.num_pages),
    })


def profile(request, user):

    # Get user from database
    profile_user = User.objects.get(username = user)

    # Get user's posts
    posts = Post.objects.filter(user = profile_user).order_by("-datetime")

    # Get user's followers and following number
    followers_count = Follow.objects.filter(followed_user = profile_user).count()
    following_count = Follow.objects.filter(follower = profile_user).count()

    # Render profile page
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
    })


def create_post(request):
    if request.method == "POST":

        content = request.POST["add-new-post-form-textarea"].strip()

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
def edit_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        
        post.content = data["post_content"]
        post.save()

        return HttpResponse(status=204)
    else:
        return HttpResponseBadRequest("Method must be PUT")


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
    else:
        data = json.loads(request.body)
        follower = User.objects.get(username = data["follower"])
        followed_user = User.objects.get(username = data["followed_user"])
        
        if request.method == "POST":
            follow_model = Follow(
                follower = follower,
                followed_user = followed_user,
            ).save()
            return HttpResponse(status=204)
        elif request.method == "DELETE":
            follow_model = Follow.objects.filter(follower = follower, 
            followed_user = followed_user).delete()
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest("GET, POST or DELETE requests required")


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
