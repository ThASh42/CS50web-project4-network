import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .models import User, Post, Follow, PostLike


@require_GET
def index(request):

    # Get all posts
    posts = Post.objects.all().order_by("-datetime")

    # Use paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    like_post_dict = {}
    current_user = request.user
    for post in page_obj:
        is_liked = PostLike.objects.filter(post = post, user = current_user).exists()
        like_post_dict[post.id] = is_liked
    return render(request, f"network/index.html", {
        "page_obj": page_obj,
        "range_pages": range(1, 1 + paginator.num_pages),
        "like_post_json": json.dumps(like_post_dict),
    })


@require_GET
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

    # Create boolean dictionary of liked post
    like_post_dict = {}
    for post in page_obj:
        is_liked = PostLike.objects.filter(post = post, user = current_user).exists()
        like_post_dict[post.id] = is_liked

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "range_pages": range(1, 1 + paginator.num_pages),
        "like_post_json": json.dumps(like_post_dict),
    })


@require_GET
def profile(request, user):

    # Get user from database
    profile_user = User.objects.get(username = user)

    # Get user's posts
    posts = Post.objects.filter(user = profile_user).order_by("-datetime")

    # Get user's followers and following number
    followers_count = Follow.objects.filter(followed_user = profile_user).count()
    following_count = Follow.objects.filter(follower = profile_user).count()

    # * Check following of user
    # Get all user's followings
    all_followings = Follow.objects.filter(follower = request.user.id)
    # Get user that must be followed
    followed_user = User.objects.get(username = user)
    # Check if the user already following
    is_following = all_followings.filter(followed_user = followed_user.id).exists()

    # Render profile page
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })


@require_POST
def create_post(request):
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
@require_http_methods("PUT")
def edit_post(request, post_id):
    data = json.loads(request.body)
    post = Post.objects.get(pk=post_id)
    
    post.content = data["post_content"]
    post.save()

    return HttpResponse(status=204)


@csrf_exempt
@login_required
@require_http_methods(["POST", "DELETE"])
def follow_unfollow(request, username):
    data = json.loads(request.body)
    follower = User.objects.get(username = data["follower"])
    followed_user = User.objects.get(username = data["followed_user"])
    
    if request.method == "POST":
        follow_model = Follow(
            follower = follower,
            followed_user = followed_user,
        ).save()
        return HttpResponse(status=201)

    elif request.method == "DELETE":
        follow_model = Follow.objects.filter(follower = follower, 
        followed_user = followed_user).delete()
        return HttpResponse(status=204)


@csrf_exempt
@login_required
@require_http_methods(["GET", "POST", "DELETE"])
def post_like(request, post_id):
    
    liked_post = get_object_or_404(Post, pk = post_id)
    if request.method == "GET":
        # Check user liked the post
        is_liked = liked_post.likes.filter(pk=request.user.id).exists()
        return JsonResponse({"is_liked": is_liked})

    elif request.method == "POST":
        current_user = request.user
        # Add user to post's ManyToManyField
        liked_post.likes.add(current_user)
        # Create PostLike object
        PostLike(
            user = current_user,
            post = liked_post,
        ).save()
        return HttpResponse(status=201)

    elif request.method == "DELETE":
        # Remove user from post's ManyToManyField
        liked_post.likes.remove(request.user)
        # Delete PostLike object
        post_like = get_object_or_404(PostLike, user = request.user, post = liked_post)
        post_like.delete()
        return HttpResponse(status=204)


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
