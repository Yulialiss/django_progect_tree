from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView
from django.utils import timezone
from django.contrib.auth.models import User
from .models import BlogPost
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CommentForm, EmailForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from taggit.models import Tag
from .models import BlogPost


# Пошук за тегами
def tag_search_view(request):
    tag = request.GET.get('tag', '').strip()
    posts = BlogPost.objects.filter(tags__name__icontains=tag) if tag else None
    return render(request, 'blog_app/tag_search.html', {'posts': posts, 'tag': tag})


# Автодоповнення тегів
def tag_search_autocomplete(request):
    query = request.GET.get('term', '').strip()
    if query:
        tags = Tag.objects.filter(name__icontains=query).values_list('name', flat=True)
        return JsonResponse(list(tags), safe=False)
    return JsonResponse([], safe=False)
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.blogpost = post
        comment.user = request.user
        comment.save()
        return redirect(post.get_absolute_url())
    return render(request, 'blog_app/comment.html', {'blogpost': post, 'comment_form': form, 'comment': None})
#
# class AuthorPostListView(ListView):
#     model = BlogPost
#     template_name = 'blog_app/author_post_list.html'
#     context_object_name = 'posts'
#
#     def get_queryset(self):
#         author_username = self.kwargs.get('username')
#         status_filter = self.request.GET.get('status')
#         try:
#             author = User.objects.get(username=author_username)
#         except User.DoesNotExist:
#             author = None
#
#         if author:
#             queryset = BlogPost.objects.filter(owner=author)
#             if status_filter:
#                 queryset = queryset.filter(status=status_filter)
#             return queryset
#         return BlogPost.objects.none()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['posts_count'] = self.get_queryset().count()
#         return context

class MyPostsListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog_app/my_posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        status_filter = self.request.GET.get('status')
        queryset = BlogPost.objects.filter(owner=self.request.user)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_count'] = BlogPost.objects.filter(owner=self.request.user).count()
        return context

class BlogListView(ListView):
    model = BlogPost
    paginate_by = 6
    context_object_name = 'blogpost_list'
    template_name = 'blog_app/blogpost_list.html'

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_count'] = BlogPost.objects.count()
        return context



class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = 'blogpost'
    template_name = 'blog_app/blogpost_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogpost = context['blogpost']
        if blogpost.status == BlogPost.PostStatus.DRAFT:
            context['is_draft'] = True
        return context

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog_app:posts')

    def get_queryset(self):
        return BlogPost.objects.filter(owner=self.request.user)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    success_url = reverse_lazy('blog_app:posts')
    fields = ['title', 'text', 'image', 'status']

    def get_queryset(self):
        return BlogPost.objects.filter(owner=self.request.user)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog_app/blogpost_create.html'
    success_url = reverse_lazy('blog_app:posts')
    fields = ['title', 'text', 'image', 'status']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.published_at = timezone.now()
        return super().form_valid(form)

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'blog_app/user_profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['posts'] = BlogPost.objects.filter(owner=user)
        return context

def share_by_email(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    form = EmailForm()
    ctx = {'form': form, 'post': post}
    return render(request, "blog_app/share_post_email.html", ctx)



@login_required
def my_drafts(request):
    drafts = BlogPost.objects.filter(owner=request.user, status='draft')
    return render(request, 'blog_app/my_drafts.html', {'drafts': drafts})

