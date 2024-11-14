from django.shortcuts import get_object_or_404, redirect, render

from comment.forms import QuestionForm
from comment.models import Author, Post, Tags

# Create your views here.


def index(request):
    return render(request, "comment/index.html")


def askquestion(request):
    return render(request, "comment/askquestion.html")


def posts(request):
    posts = Post.objects.all()
    return render(request, "comment/index.html", {"posts": posts})


def ask_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Xử lý dữ liệu hợp lệ
            question_title = form.cleaned_data["question_title"]
            question_description = form.cleaned_data["question_description"]
            related_tags = form.cleaned_data["related_tags"]

            # Lưu dữ liệu vào database
            tags = Tags.objects.create(tag=related_tags)
            author = Author.objects.get(user=request.user)
            post = Post.objects.create(
                title=question_title, content=question_description, author=author
            )
            post.tags.add(tags)
            post.save()
            return redirect("home")
    else:
        form = QuestionForm()

    return render(request, "comment/askquestion.html", {"form": form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(
        request,
        "comment/post_detail.html",
        {"post": post, "post_tags": post.tags.all()},
    )
