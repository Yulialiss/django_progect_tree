from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.urls import reverse
from taggit.managers import TaggableManager

from taggit.models import Tag

class BlogPostManager(models.Manager):
    def posts_by_author(self, author):
        return self.filter(owner=author)

    def published(self):
        return self.filter(status=self.model.PostStatus.PUBLISHED)

    def draft(self):
        return self.filter(status=self.model.PostStatus.DRAFT)

class BlogPost(models.Model):
    class PostStatus(models.TextChoices):
        DRAFT = 'draft', 'Чернетка'
        PUBLISHED = 'published', 'Опубліковано'

    title = models.CharField(max_length=200)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    published_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT)
    tags = TaggableManager()  # Поле для тегів

    objects = BlogPostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:detail_posts', kwargs={'pk': self.pk})

    def is_published(self):
        return self.status == self.PostStatus.PUBLISHED

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    blogpost = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blogpost.title}"

class TagSearchForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label="Фільтрувати за тегом")