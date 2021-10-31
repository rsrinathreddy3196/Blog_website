from django.db import models
from django.db.models.fields import DateField, EmailField
from django.db.models.fields.files import ImageField

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address =models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=100)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True ,related_name="posts")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class comment(models.Model):
    user_name = models.CharField(max_length=50)
    user_mail = models.EmailField()
    text = models.TextField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")


