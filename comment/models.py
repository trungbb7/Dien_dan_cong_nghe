from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.first_name

class Comment(models.Model):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="comments_related"
    )
    content = models.TextField(default=" ")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_votes(self):
        upvotes = self.votes_related.filter(is_upvote=True).count()
        downvotes = self.votes_related.filter(is_upvote=False).count()
        return upvotes - downvotes

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes_related")
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate votes
