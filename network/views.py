from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Posts


def index(request):
    posts = Posts.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


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
    
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Posts.objects.create(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")

def profile(request, username):
    curr_user = User.objects.get(username=username)
    posts = curr_user.user_posts.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "profile": curr_user,
        "page_obj": page_obj
    })

def follow(request, username):
    user = request.user
    followed_user = User.objects.get(username=username)
    user.following.add(followed_user)
    return HttpResponseRedirect(reverse("profile", args=[username]))

def unfollow(request, username):
    user = request.user
    followed_user = User.objects.get(username=username)
    user.following.remove(followed_user)
    return HttpResponseRedirect(reverse("profile", args=[username]))

def following(request):
    user = request.user
    following_users = user.following.all()
    posts = Posts.objects.filter(user__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

def post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    liked = False
    if request.user.is_authenticated:
        liked = post.likes.filter(id=request.user.id).exists()
    return render(request, "network/post.html", {
        "post": post,
        "liked": liked,
        "like_count": post.likes.count()
    })

@login_required
@csrf_exempt
def like_post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post", args=[post_id]))

def edit_post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    if request.method == "POST":
        post.content = request.POST["content"]
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/edit_post.html", {
            "post": post
        })