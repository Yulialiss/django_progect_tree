from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from .models import BlogPost
from .forms import ContactForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import BlogPost
from .forms import CommentForm

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
    return render(
        request,
        'blog_app/comment.html',
        {
            'blogpost': post,
            'comment_form': form,
            'comment': None
        }
    )



def contact(request):
    return render(request, 'blog_app/contacts.html')



class AuthorPostListView(ListView):
    model = BlogPost
    template_name = 'blog_app/author_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        author_username = self.kwargs.get('username')
        author = User.objects.get(username=author_username)
        return BlogPost.objects.posts_by_author(author)


class MyPostsListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog_app/my_posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(owner=self.request.user)

class BlogListView(ListView):
    model = BlogPost
    paginate_by = 5
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
        form.instance.published_at = timezone.now()
        return super().form_valid(form)
