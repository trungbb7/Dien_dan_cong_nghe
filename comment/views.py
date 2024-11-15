from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from comment.forms import PostForm, commentsForm
from comment.models import Author, Comment, Post, Tag

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


def askquestion(request):
    return render(request, "comment/askquestion.html")


def ask_question(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.create(
                first_name="John", last_name="Doe", email_address="Diango@gasd.com "
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
