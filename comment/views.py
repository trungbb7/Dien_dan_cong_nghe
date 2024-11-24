from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from comment.forms import PostForm, commentsForm
from comment.models import Author, Comment, Post, Tag, Vote
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    posts = Post.objects.all()
    if request.method == "POST":
        print(request.POST)
        form = commentsForm(request.POST)
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = Author.objects.create(
                first_name="John", last_name="Doe", email_address="test@example.com"
            )
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
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email_address=user.email,
            )
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
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    author = Author.objects.get(user=user)
    posts = Post.objects.filter(author=author)
    if request.method == "POST":
        print(request.POST)
        form = commentsForm(request.POST)
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = Author.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                email_address=user.email,
            )
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
