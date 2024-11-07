from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost
    context_object_name = 'blogpost_list'
    template_name = 'blog_app/blogpost_list.html'


class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = 'blogpost'
    template_name = 'blog_app/blogpost_detail.html'


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog_app:posts')

    def get_queryset(self):
        return BlogPost.objects.filter(owner=self.request.user)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    success_url = reverse_lazy('blog_app:posts')
    fields = ['title', 'text', 'image']

    def get_queryset(self):
        return BlogPost.objects.filter(owner=self.request.user)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog_app/blogpost_create.html'
    success_url = reverse_lazy('blog_app:posts')
    fields = ['title', 'text', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
