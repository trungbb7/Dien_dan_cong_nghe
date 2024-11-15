from django.db import models
from django.utils.text import slugify

# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption


class Author(models.Model):
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
    votes = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, related_name="posts_related")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"title: {self.title} - author:{self.author} - tags {self.tags.all()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title+str(self.id)}")
        super().save(*args, **kwargs)
