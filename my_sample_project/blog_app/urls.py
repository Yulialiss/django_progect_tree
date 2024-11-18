from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from . import views

app_name = "blog_app"

urlpatterns = [
    path('posts/<int:pk>/',BlogDetailView.as_view(), name="posts"),

    path('posts/', BlogListView.as_view(), name="posts"),
    path('posts/<int:pk>/', BlogDetailView.as_view(), name="detail_posts"),
    path('delete_posts/<int:pk>/', BlogDeleteView.as_view(), name="delete_posts"),
    path('update_posts/<int:pk>/', BlogUpdateView.as_view(), name='update_posts'),
    path('create_posts/', BlogCreateView.as_view(), name='create_posts'),
    path('author/<str:username>/', AuthorPostListView.as_view(), name='author_posts'),
    path('my-posts/', views.MyPostsListView.as_view(), name='my_posts'),
    path('post_comment/<int:post_id>/', post_comment, name="post_comment"),

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)