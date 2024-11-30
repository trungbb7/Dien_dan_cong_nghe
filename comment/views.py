from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from comment.forms import PostForm, commentsForm
from comment.models import Author, Comment, Post, Tag, Vote
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q

# Create your views here.

from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import commentsForm
from .models import Post, Author, User


@login_required
def index(request):
    currentUser = request.user
    query = request.GET.get('q', '')
    
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()

    if request.method == "POST":
        form = commentsForm(request.POST)
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            print(f"Current user: {currentUser}")

            author, created = Author.objects.get_or_create(
                user=currentUser,
                defaults={
                    "first_name": currentUser.username,
                    "last_name": currentUser.last_name,
                    "email_address": currentUser.email,
                },
            )
            comment.author = author
            comment.save()
            post.comments.add(comment)
            return redirect("home")
        else:
            return JsonResponse({"error": form.errors})
    else:
        form = commentsForm()

    return render(
        request,
        "comment/index.html",
        {"posts": posts, "form": form},
    )


def ask_question(request):
    currentUser = request.user
    print(currentUser)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            author, created = Author.objects.get_or_create(
                user=currentUser,
                defaults={
                    "first_name": currentUser.username,
                    "last_name": currentUser.last_name,
                    "email_address": currentUser.email,
                },
            )
            post.author = author
            post.save()
            tags_list = form.cleaned_data["tags"].split(",")
            for tag in tags_list:
                tag = Tag.objects.get_or_create(caption=tag.strip())
                post.tags.add(tag[0])
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "comment/askquestion.html", {"form": form})


def my_QNA(request):
    currentUser = request.user
    author = Author.objects.get(user=currentUser)
    posts = Post.objects.filter(author=author)
    if request.method == "POST":
        form = commentsForm(request.POST)
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            author, created = Author.objects.get_or_create(
                user=currentUser,
                defaults={
                    "first_name": currentUser.username,
                    "last_name": currentUser.last_name,
                    "email_address": currentUser.email,
                },
            )
            comment.author = author
            comment.save()
            post.comments.add(comment)
            return redirect("home")
        else:
            return JsonResponse({"error": form.errors})
    else:
        form = commentsForm()
    return render(
        request,
        "comment/index.html",
        {"posts": posts, "form": form},
    )


def vote(request):
    if request.method == "POST" and request.user.is_authenticated:
        post_id = request.POST.get("post_id")
        is_upvote = request.POST.get("is_upvote") == "true"
        post = get_object_or_404(Post, id=post_id)

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={"is_upvote": is_upvote},
        )

        if not created:
            if vote.is_upvote != is_upvote:
                vote.is_upvote = is_upvote
                vote.save()
            else:
                vote.delete()

        else:
            vote.is_upvote = is_upvote
            vote.save()

        # Return the updated vote count
        return JsonResponse({"total_votes": post.total_votes()})
    return JsonResponse({"error": "Invalid request"}, status=400)
