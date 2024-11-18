from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.urls import reverse

class BlogPostManager(models.Manager):
    def posts_by_author(self, author):
        return self.filter(owner=author)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    published_at = models.DateTimeField(default=timezone.now)

    objects = BlogPostManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:detail_posts', kwargs={'pk': self.pk})

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    blogpost = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

