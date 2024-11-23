from django.shortcuts import redirect
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from .models import BlogPost
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import EmailForm

def send_email_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            recipient = form.cleaned_data["recipient"]

            send_mail(
                subject,
                message,
                "yuliahuralgit@gmail.com",
                [recipient],
                fail_silently=False,
            )
            return render(request, "blog_app/email_success.html")
    else:
        form = EmailForm()

    return render(request, "blog_app/send_email.html", {"form": form})
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

        search_query = self.request.GET.get('search')
        if search_query:
            search_tag = search_query.strip('#')
            queryset = queryset.filter(tags__name__icontains=search_tag)

        tag_filter = self.request.GET.get('tag')
        if tag_filter:
            queryset = queryset.filter(tags__name=tag_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
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
    fields = ['title', 'text', 'image', 'status', 'tags']

    def get_queryset(self):
        return BlogPost.objects.filter(owner=self.request.user)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog_app/blogpost_create.html'
    success_url = reverse_lazy('blog_app:posts')
    fields = ['title', 'text', 'image', 'status', 'tags']

    def form_valid(self, form):
        blogpost = form.save(commit=False)
        blogpost.owner = self.request.user
        blogpost.save()

        tags = self.request.POST.get('tags')
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                blogpost.tags.add(tag.strip())

        return redirect('blog_app:detail_posts', blogpost.id)

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'blog_app/user_profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['posts'] = BlogPost.objects.filter(owner=user)
        return context

@login_required
def my_drafts(request):
    drafts = BlogPost.objects.filter(owner=request.user, status='draft')
    return render(request, 'blog_app/my_drafts.html', {'drafts': drafts})


