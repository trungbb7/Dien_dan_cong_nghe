from django.shortcuts import get_object_or_404, redirect, render

from comment.forms import PostForm
from comment.models import Author, Post, Tag

# Create your views here.


def index(request):
    posts = Post.objects.all()
    for post in posts:
        print(post)
    return render(request, "comment/index.html", {"posts": posts})


def askquestion(request):
    return render(request, "comment/askquestion.html")


def posts(request):
    posts = Post.objects.all()
    return render(request, "comment/index.html", {"posts": posts})


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


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(
        request,
        "comment/post_detail.html",
        {"post": post, "post_tags": post.tags.all()},
    )
